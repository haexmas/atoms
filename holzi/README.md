# holzi devShell extras

A `nix_packages`-only molecule contributing the system libraries
[holzi](https://github.com/haexmas/holzi)'s Tauri v2 app needs to build on
Linux, beyond what the generic
[`com.github.haexmas.atoms.nix-rust`](../nix-rust/) and
[`com.github.haexmas.atoms.nix-nodejs`](../nix-nodejs/) molecules already
provide.

- Atom id: `com.github.haexmas.atoms.holzi`
- Version: `0.3.0`
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

`cudatoolkit` (v0.2.0) is the one exception not mirrored from CI: CI has
no GPU, so it never builds holzi's `llm-cuda` feature. It's here for the
manual `pnpm tauri:dev:cuda`/`tauri:build:cuda` smoke test on a
CUDA-capable dev machine (Etappe-0 finding #3 — `mistralrs/cuda`'s
`cudarc` build script needs `nvcc` on `PATH`). It's an unfree package
(CUDA EULA) — see
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)'s
README for why that molecule's `flake.nix` needs `allowUnfree`.

`lld` (v0.3.0) works around a linker-ordering bug that only shows up once
`cudatoolkit` is in play: enabling holzi's `llm-cuda` feature (`cudarc`)
reshapes the crate dependency graph enough to change the order Cargo
emits native-library link args in, and GNU `ld.bfd` (order-sensitive,
single-pass symbol resolution) then fails with spurious `undefined
reference` errors against `libgtk-3`/`libcairo`/`libwebkit2gtk` symbols
that resolve fine on a plain (non-CUDA) build. `lld` isn't
order-sensitive the same way and resolves cleanly — see holzi's
`src-tauri/.cargo/config.toml`, which sets `-fuse-ld=lld` for the Linux
target. Verified live: `cargo build --features llm-cuda` fails
reproducibly with `ld.bfd`, succeeds with `-fuse-ld=lld`.

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
