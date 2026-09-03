"""Test package conftest for the graphify-first-authoring atom.

Exposes the atom's ``install.py``, ``_refresh.py``, ``_snapshot.py`` and
``_tracked_branches.py`` on ``sys.path`` so tests can ``import`` them as plain
modules. In this publisher repo layout the atom lives directly under the
repository root (as ``graphify-first-authoring/``), one level shallower than
in the consumer ``.specify/molecules/graphify-first-authoring/`` layout it
was originally authored against.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ATOM_DIR = Path(__file__).resolve().parent.parent
_HOOKS_DIR = _ATOM_DIR / "hooks"

for path in (_ATOM_DIR, _HOOKS_DIR):
    sys_path_entry = str(path)
    if sys_path_entry not in sys.path:
        sys.path.insert(0, sys_path_entry)
