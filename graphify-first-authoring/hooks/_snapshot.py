"""Fork-point snapshot of ``graphify-out/`` for the post-checkout hook.

Per contracts/git-hooks.md §post-checkout and FR-008: when a new worktree is
created from a tracked branch, copy that branch worktree's complete
``graphify-out/`` (including ``graph.json``) into the new one so the feature
branch sees a correct fork-point graph immediately. An explicit
``GRAPHIFY_PARENT_WORKTREE`` override supports worktrees created from another
linked worktree. Never overwrite an existing complete ``graphify-out/`` in the
new worktree. An incomplete destination is treated as absent and replaced
once a complete parent graph is available.
Never raise — warn to stderr on any failure, so the calling hook can always
exit 0 and the underlying ``git worktree add``/``git checkout`` cannot be
affected.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import _tracked_branches

_PARENT_WORKTREE_ENV = "GRAPHIFY_PARENT_WORKTREE"


def _registered_worktrees(current: Path) -> list[tuple[Path, str, str | None]]:
    """Return registered worktrees as ``(path, head, branch)`` records."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(current), "worktree", "list", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    records: list[tuple[Path, str, str | None]] = []
    path: Path | None = None
    head = ""
    branch: str | None = None
    for line in proc.stdout.splitlines() + [""]:
        if line.startswith("worktree "):
            if path is not None:
                records.append((path, head, branch))
            path = Path(line[len("worktree "):].strip()).resolve()
            head = ""
            branch = None
        elif line.startswith("HEAD "):
            head = line[len("HEAD "):].strip()
        elif line.startswith("branch "):
            branch = line[len("branch "):].strip()
        elif not line and path is not None:
            records.append((path, head, branch))
            path = None

    return records


def _branch_name(ref: str | None) -> str | None:
    """Convert a worktree branch ref to the short local branch name."""
    prefix = "refs/heads/"
    if ref is None or not ref.startswith(prefix):
        return None
    return ref[len(prefix):]


def _is_ancestor(current: Path, ancestor: str, descendant: str) -> bool:
    """Return whether ``ancestor`` is reachable from ``descendant``."""
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(current),
                "merge-base",
                "--is-ancestor",
                ancestor,
                descendant,
            ],
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return proc.returncode == 0


def _has_complete_graph(worktree: Path) -> bool:
    """Return whether a worktree has a usable graphify snapshot."""
    return (worktree / "graphify-out" / "graph.json").is_file()


def _parent_worktree(current: Path, new_head: str | None = None) -> Path | None:
    """Return the source worktree selected for this checkout.

    An explicit ``GRAPHIFY_PARENT_WORKTREE`` is authoritative and is validated
    against Git's registered worktrees. Otherwise, select the tracked-branch
    worktree whose HEAD equals the new checkout HEAD. A complete snapshot from
    any exact-HEAD source is accepted for feature-from-feature worktrees. If
    that source has no complete snapshot, fall back to a tracked-branch
    worktree whose HEAD is an ancestor of the new checkout HEAD, and finally to
    any tracked-branch worktree with a complete graph (default branch first).
    Git supplies that HEAD to ``post-checkout`` for ``git worktree add``; the
    tracked exact match keeps ``main``/``develop`` snapshots distinct, while the
    other paths avoid requiring an environment variable.
    """
    records = _registered_worktrees(current)
    current_resolved = current.resolve()
    source_value = os.environ.get(_PARENT_WORKTREE_ENV)
    if source_value:
        source = Path(source_value).expanduser().resolve()
        if source == current_resolved:
            return None
        for registered, _, _ in records:
            if registered == source:
                return source
        return None

    if not new_head:
        return None
    tracked = _tracked_branches.tracked_branches(current)
    for registered, head, branch_ref in records:
        branch = _branch_name(branch_ref)
        if (
            registered != current_resolved
            and head == new_head
            and branch in tracked
        ):
            return registered

    for registered, head, _ in records:
        if (
            registered != current_resolved
            and head == new_head
            and _has_complete_graph(registered)
        ):
            return registered

    for registered, head, branch_ref in records:
        branch = _branch_name(branch_ref)
        if (
            registered != current_resolved
            and head
            and branch in tracked
            and _has_complete_graph(registered)
            and _is_ancestor(current, head, new_head)
        ):
            return registered

    # A tracked branch that moved on after this checkout forked is no ancestor
    # of it any more, yet its graph is still a far better fork-point snapshot
    # than none. Prefer the repository's default branch among the candidates.
    default = _tracked_branches._default_branch(current)
    candidates = [
        (branch != default, registered)
        for registered, head, branch_ref in records
        if (branch := _branch_name(branch_ref)) in tracked
        and registered != current_resolved
        and head
        and _has_complete_graph(registered)
    ]
    if candidates:
        return min(candidates, key=lambda candidate: candidate[0])[1]
    return None


def snapshot(current_worktree: Path, new_head: str | None = None) -> bool:
    """Copy the selected parent graph into ``current_worktree``.

    Returns ``True`` if a copy was performed, ``False`` on any no-op or
    failure. A ``False`` return is silent when the destination already has a
    complete graph, and warns to stderr when no source graph is available or a
    partial copy had to be rolled back. An incomplete destination directory is removed only after a
    complete parent graph has been found. Never raises.
    """
    dest = current_worktree / "graphify-out"
    if dest.exists() and (
        not dest.is_dir() or (dest / "graph.json").is_file()
    ):
        return False

    parent = _parent_worktree(current_worktree, new_head)
    if parent is None:
        print(
            "graphify-first-authoring post-checkout: no tracked-branch worktree "
            "has a complete graphify-out/ to snapshot — graph stays absent "
            "(run `graphify update` on a tracked branch, or set "
            f"{_PARENT_WORKTREE_ENV})",
            file=sys.stderr,
        )
        return False

    source = parent / "graphify-out"
    if not source.is_dir() or not (source / "graph.json").is_file():
        return False

    try:
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source, dest, symlinks=False)
    except OSError as exc:
        print(
            f"graphify-first-authoring post-checkout: snapshot failed ({exc}) — "
            "leaving graphify-out/ absent (agent bootstrap will handle it)",
            file=sys.stderr,
        )
        if dest.exists():
            with contextlib.suppress(OSError):
                shutil.rmtree(dest)
        return False

    return True
