# Nix devShell skeleton

Delivers a reproducible `nix develop`/`direnv` devShell to the consumer
repo root: `flake.nix`, `.envrc`, and a `.direnv/` `.gitignore` entry.

- Atom id: `com.github.haexmas.atoms.nix-devshell-base`
- Version: `0.1.0`
- Delivered atoms: `flake.nix`, `.envrc`, `.gitignore` under
  `atoms.dev_environment` — an *exclusive* generic atom category (spaex
  Spec 027): materialized verbatim at the consumer repo root, owned by
  this one molecule, and removed again by `spaex remove`.

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
