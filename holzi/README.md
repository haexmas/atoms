# holzi devShell extras

A `nix_packages`-only molecule contributing the system libraries
[holzi](https://github.com/haexmas/holzi)'s Tauri v2 app needs to build on
Linux, beyond what the generic
[`com.github.haexmas.atoms.nix-rust`](../nix-rust/) and
[`com.github.haexmas.atoms.nix-nodejs`](../nix-nodejs/) molecules already
provide.

- Atom id: `com.github.haexmas.atoms.holzi`
- Version: `0.1.0`
- Delivered atoms: a package fragment under `atoms.nix_packages` — no
  `flake.nix` of its own (adopt
  [`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)
  for that).

This molecule is deliberately scoped to holzi, not a generic "Tauri"
molecule: the package list (`webkitgtk_4_1`, `libayatana-appindicator`,
`librsvg`, `alsa-lib`, `xdotool`, `openssl`, plus the usual `curl`/`wget`/
`file`/`pkg-config`) mirrors holzi's own
[`.github/workflows/ci.yml`](https://github.com/haexmas/holzi/blob/main/.github/workflows/ci.yml)
Linux build-dependency list, not a researched general Tauri baseline. If a
second Tauri app wants the same set, generalize then — not speculatively
now.

## Adopting

Add the molecule to a consumer's `.spaex/manifest.json` and pin the full
commit SHA of this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.holzi"]
}
```

Then run `spaex install`.
