# Nix devShell skeleton

Delivers a reproducible `nix develop`/`direnv` devShell to the consumer
repo root: `flake.nix` and `.envrc`.

- Atom id: `com.github.haexmas.atoms.nix-devshell-base`
- Version: `0.3.0`
- Delivered atoms: `flake.nix`, `.envrc` under `atoms.dev_environment` —
  an *exclusive* generic atom category (spaex Spec 027): materialized
  verbatim at the consumer repo root, owned by this one molecule, and
  removed again by `spaex remove`.
- `install_hook` (warn-only): checks `nix` is on `PATH` after install and
  prints an actionable hint if not. Never installs Nix itself — that
  needs interactive root access spaex should not attempt unattended.

**Does not deliver `.gitignore`.** An exclusive atom is rewritten
verbatim on *every* `spaex install`, not just the first — for `flake.nix`
that is correct (this molecule is its sole, authoritative source), but a
`.gitignore` typically already carries a consumer's own project-specific
rules (build output, env files, editor/OS cruft, ...) that this molecule
has no way to know about. Shipping `.gitignore` here would silently
overwrite those rules on every install, repeatedly, even after an
operator manually restores them. (Caught live adopting this molecule
into `holzi`, whose existing `.gitignore` — including its `.env` and
`.claude/` credential-safety rules — was clobbered down to one line on
first install; v0.1.0 shipped this bug.) Add `.direnv/` to your own
`.gitignore` once, by hand, instead.

## How it composes with other molecules

`flake.nix` ships no packages of its own. It reads
`.spaex/generated/nix-packages.json` — the file spaex regenerates from
every currently-adopted molecule's `atoms.nix_packages` fragment (the
*composable* generic atom category) — and passes the resulting package
list to `pkgs.mkShell`. Adopt this molecule alongside whichever
language/tool molecules a repo needs (e.g.
[`com.github.haexmas.atoms.rust`](../rust/),
[`com.github.haexmas.atoms.javascript-typescript`](../javascript-typescript/)):
each contributes its own package names, and this molecule's `flake.nix`
never needs to change when contributors are added or removed.

The read is guarded (`builtins.pathExists`): no adopted molecule
declaring `nix_packages` is a valid "no extra packages" state, not an
error, since this molecule's own lifecycle is independent of any
particular package contributor's.

## Adopting

Add the molecule to a consumer's `.spaex/manifest.json` and pin the full
commit SHA of this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.nix-devshell-base"]
}
```

Then run `spaex install`. Requires [Nix](https://nixos.org/download) with
flakes enabled, and [direnv](https://direnv.net/) for automatic shell
activation (`direnv allow` once after cloning).
