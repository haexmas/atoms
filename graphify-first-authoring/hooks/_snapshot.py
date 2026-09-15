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


def _parent_worktree(current: Path, new_head: str | None = None) -> Path | None:
    """Return the source worktree selected for this checkout.

    An explicit ``GRAPHIFY_PARENT_WORKTREE`` is authoritative and is validated
    against Git's registered worktrees. Otherwise, select the tracked-branch
    worktree whose HEAD equals the new checkout HEAD. Git supplies that HEAD to
    ``post-checkout`` for ``git worktree add``; matching it avoids guessing from
    worktree-list order and keeps ``main``/``develop`` snapshots distinct.
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
    return None


def snapshot(current_worktree: Path, new_head: str | None = None) -> bool:
    """Copy the selected parent graph into ``current_worktree``.

    Returns ``True`` if a copy was performed, ``False`` on any no-op or
    failure. A ``False`` return is silent when the situation is a legitimate
    no-op (destination exists, no parent, parent has no complete graph) and
    warns to stderr only on genuine failure (a partial copy that had to be
    rolled back). An incomplete destination directory is removed only after a
    complete parent graph has been found. Never raises.
    """
    dest = current_worktree / "graphify-out"
    if dest.exists() and (
        not dest.is_dir() or (dest / "graph.json").is_file()
    ):
        return False

    parent = _parent_worktree(current_worktree, new_head)
    if parent is None:
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
