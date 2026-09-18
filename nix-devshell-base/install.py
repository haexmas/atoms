"""Installer for the nix-devshell-base molecule.

Checks that `nix` is on PATH after `flake.nix`/`.envrc` are delivered, so
an operator adopting this molecule sees an actionable hint immediately
rather than discovering `nix develop`/`direnv allow` silently does
nothing. Never installs Nix itself — that needs interactive root access
spaex should not attempt unattended.
"""

from __future__ import annotations

import shutil
import sys


def install() -> int:
    if shutil.which("nix") is not None:
        return 0
    print(
        "nix-devshell-base: 'nix' is not on PATH. flake.nix and .envrc were "
        "delivered, but the devShell needs Nix with flakes enabled to do "
        "anything. Install it (e.g. https://install.determinate.systems/nix, "
        "or the official installer at https://nixos.org/download), then run "
        "'direnv allow' if you use direnv.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(install())
