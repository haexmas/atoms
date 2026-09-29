# Node.js/Corepack/pnpm Nix devShell packages

A `nix_packages`-only molecule contributing Node.js, Corepack and pnpm to a
consumer's composed Nix devShell.

- Atom id: `com.github.haexmas.atoms.nix-nodejs`
- Version: `0.2.0`
- Delivered atoms: a package fragment under `atoms.nix_packages` — no
  `flake.nix` of its own (adopt
  [`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)
  for that).

Deliberately separate from
[`com.github.haexmas.atoms.coding-guideline-javascript-typescript`](../coding-guideline-javascript-typescript/)
(behavior/coding-guidance only): adopting JS/TS coding guidance and
adopting a Node/Corepack/pnpm Nix devShell are independent decisions, and bundling
them would force every adopter of one to also take the other. Pinned to
Node 22 (nixpkgs' current LTS attributes for Node.js and Corepack); a project needing a different
major should add its own override rather than expect this fragment to
track it.

## Adopting

Add the molecule to a consumer's `.spaex/manifest.json` and pin the full
commit SHA of this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.nix-nodejs"]
}
```

Then run `spaex install`.
