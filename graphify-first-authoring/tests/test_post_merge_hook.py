"""Integration tests for the installed post-merge and post-checkout refresh.

``git merge`` and ``git pull`` never run ``post-commit``, so pull requests that
land on a tracked branch need ``post-merge`` to keep ``graphify-out/`` current.
Switching onto a tracked branch needs ``post-checkout`` for the same reason.
Uses a scratch git repo and a ``graphify`` stub, like the post-commit tests.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
from pathlib import Path

import pytest

from .test_post_commit_hook import _git, _init_repo, _make_graphify_stub

_MOLECULE_HOOKS = Path(__file__).resolve().parent.parent / "hooks"


def _install_hooks(repo: Path, *names: str) -> None:
    hooks_dir = repo / ".git" / "hooks"
    for name in names:
        target = hooks_dir / name
        body = (_MOLECULE_HOOKS / name).read_text(encoding="utf-8")
        target.write_text(f"#!{sys.executable}\n{body}", encoding="utf-8")
        target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    for helper in ("_tracked_branches.py", "_refresh.py", "_snapshot.py"):
        shutil.copy2(_MOLECULE_HOOKS / helper, hooks_dir / helper)


@pytest.fixture
def env_with_stub(tmp_path: Path) -> dict[str, str]:
    bin_dir = tmp_path / "bin"
    _make_graphify_stub(bin_dir, tmp_path)
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    return env


@pytest.fixture
def scratch_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    _init_repo(repo)
    return repo


def _indexed_sha(repo: Path) -> str:
    meta = repo / "graphify-out" / ".meta.json"
    assert meta.is_file(), "graphify-out/.meta.json was not written by the hook"
    return json.loads(meta.read_text())["indexed_at_sha"]


def _commit_on_branch(repo: Path, branch: str, env: dict[str, str]) -> None:
    _git(repo, "checkout", "-q", "-b", branch, env=env)
    (repo / f"{branch.replace('/', '-')}.txt").write_text("change\n")
    _git(repo, "add", ".", env=env)
    _git(repo, "commit", "-q", "-m", f"work on {branch}", env=env)
    _git(repo, "checkout", "-q", "main", env=env)


def test_merge_commit_on_tracked_branch_refreshes_graph(
    scratch_repo: Path, env_with_stub: dict[str, str]
) -> None:
    _commit_on_branch(scratch_repo, "feature/x", env_with_stub)
    (scratch_repo / "main.txt").write_text("diverge\n")
    _git(scratch_repo, "add", ".", env=env_with_stub)
    _git(scratch_repo, "commit", "-q", "-m", "main diverges", env=env_with_stub)
    _install_hooks(scratch_repo, "post-merge")

    _git(scratch_repo, "merge", "-q", "--no-ff", "-m", "merge", "feature/x", env=env_with_stub)

    assert _indexed_sha(scratch_repo) == _git(scratch_repo, "rev-parse", "HEAD")


def test_fast_forward_pull_on_tracked_branch_refreshes_graph(
    scratch_repo: Path, env_with_stub: dict[str, str]
) -> None:
    _commit_on_branch(scratch_repo, "feature/x", env_with_stub)
    _install_hooks(scratch_repo, "post-merge")

    _git(scratch_repo, "merge", "-q", "--ff-only", "feature/x", env=env_with_stub)

    assert _indexed_sha(scratch_repo) == _git(scratch_repo, "rev-parse", "HEAD")


def test_merge_on_untracked_branch_leaves_graph_alone(
    scratch_repo: Path, env_with_stub: dict[str, str]
) -> None:
    _commit_on_branch(scratch_repo, "feature/x", env_with_stub)
    _git(scratch_repo, "checkout", "-q", "-b", "feature/y", env=env_with_stub)
    _install_hooks(scratch_repo, "post-merge")

    _git(scratch_repo, "merge", "-q", "--ff-only", "feature/x", env=env_with_stub)

    assert not (scratch_repo / "graphify-out").exists()


def test_merge_never_fails_when_refresh_fails(
    scratch_repo: Path, tmp_path: Path
) -> None:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    failing = bin_dir / "graphify"
    failing.write_text("#!/bin/sh\nexit 1\n")
    failing.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    _commit_on_branch(scratch_repo, "feature/x", env)
    _install_hooks(scratch_repo, "post-merge")

    _git(scratch_repo, "merge", "-q", "--ff-only", "feature/x", env=env)


def test_switching_onto_tracked_branch_builds_a_missing_graph(
    scratch_repo: Path, env_with_stub: dict[str, str]
) -> None:
    _commit_on_branch(scratch_repo, "feature/x", env_with_stub)
    _git(scratch_repo, "checkout", "-q", "feature/x", env=env_with_stub)
    _install_hooks(scratch_repo, "post-checkout")
    assert not (scratch_repo / "graphify-out").exists()

    _git(scratch_repo, "checkout", "-q", "main", env=env_with_stub)

    assert _indexed_sha(scratch_repo) == _git(scratch_repo, "rev-parse", "HEAD")


def test_switching_onto_tracked_branch_leaves_a_fresh_graph_alone(
    scratch_repo: Path, env_with_stub: dict[str, str]
) -> None:
    _commit_on_branch(scratch_repo, "feature/x", env_with_stub)
    graph = scratch_repo / "graphify-out"
    graph.mkdir()
    (graph / "graph.json").write_text("sentinel\n")
    (graph / ".meta.json").write_text(
        json.dumps({"indexed_at_sha": _git(scratch_repo, "rev-parse", "main")})
    )
    _git(scratch_repo, "checkout", "-q", "feature/x", env=env_with_stub)
    _install_hooks(scratch_repo, "post-checkout")

    _git(scratch_repo, "checkout", "-q", "main", env=env_with_stub)

    assert (graph / "graph.json").read_text() == "sentinel\n", (
        "a graph indexed at the current HEAD must not be rebuilt"
    )


def test_switching_onto_feature_branch_does_not_refresh(
    scratch_repo: Path, env_with_stub: dict[str, str]
) -> None:
    _commit_on_branch(scratch_repo, "feature/x", env_with_stub)
    _install_hooks(scratch_repo, "post-checkout")

    _git(scratch_repo, "checkout", "-q", "feature/x", env=env_with_stub)

    assert not (scratch_repo / "graphify-out").exists()
