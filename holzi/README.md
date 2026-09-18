# holzi devShell extras

A `nix_packages`-only molecule contributing the system libraries
[holzi](https://github.com/haexmas/holzi)'s Tauri v2 app needs to build on
Linux, beyond what the generic
[`com.github.haexmas.atoms.nix-rust`](../nix-rust/) and
[`com.github.haexmas.atoms.nix-nodejs`](../nix-nodejs/) molecules already
provide.

- Atom id: `com.github.haexmas.atoms.holzi`
- Version: `0.4.0`
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
`src-tauri/build.rs`, which sets `-fuse-ld=lld` (and two more linker
flags, below) only when `CARGO_FEATURE_LLM_CUDA` is set, never
unconditionally: CI (ubuntu-24.04, no GPU) never builds this feature and
uses a different FHS layout, so a blanket `.cargo/config.toml` rustflag
would have broken it. Verified live: `cargo build --features llm-cuda`
fails reproducibly with `ld.bfd`, succeeds with `-fuse-ld=lld`.

`gtk3` (v0.4.0) plus `cairo`, `glib.out`, `gdk-pixbuf`, `dbus.lib`,
`libsoup_3`, `gcc.cc.lib`: holzi's Tauri binary directly links a whole
GTK/WebKit stack (`libgtk-3`, `libcairo`, `libglib-2.0`/`libgobject-2.0`/
`libgio-2.0`, `libgdk_pixbuf-2.0`, `libdbus-1`, `libsoup-3.0`), not just
`webkitgtk_4_1`. None of that was ever actually resolvable at *runtime*
before this — nothing wired up `LD_LIBRARY_PATH` (see
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)'s
README), so the app crashed on the first "shared object not found"
whether or not CUDA was involved; nobody had noticed yet because
`cudartoolkit`'s own libraries happened to be earlier in the binary's
needed-library list and masked it. Consistently sourcing the *entire*
stack from Nix (not host + Nix mixed) matters: an earlier attempt at
"host provides GTK, Nix provides only WebKit" crashed with a glibc ABI
clash (`undefined symbol: __pointer_chk_guard, version GLIBC_PRIVATE`)
from loading two different glibc-linked copies of tightly-coupled
GTK/WebKit objects in one process. `gcc.cc.lib` is the one CUDA-only
addition here (`libstdc++`/`libgcc_s`, needed transitively by `cudarc`'s
C++ CUDA libraries, not by holzi's own Rust code).

Some of these packages split their shared library into a non-default
output (`dbus`'s default output has no `lib/`; plain `glib` resolves to
its `bin` output, not the one with `libglib-2.0.so`) — that's why the
list uses dotted names (`glib.out`, `dbus.lib`): see
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)'s
README for how `flake.nix` resolves those.

The proprietary GPU driver itself (`libcuda.so.1`) is the one piece that
deliberately still comes from the *host* (`nvidia-utils` via pacman, or
equivalent), not Nix — Nix can't reproducibly bundle a driver matching
whatever kernel module happens to be loaded. Because mixing a
Nix-glibc-linked binary with that host driver reintroduces the same
glibc ABI clash described above, `src-tauri/build.rs` also points the
`llm-cuda` binary's own ELF interpreter at the *host's* dynamic linker
(newer here, so backward-compatible with Nix's) and adds `/usr/lib` as
an rpath — again gated on `CARGO_FEATURE_LLM_CUDA`, and documented there
as FHS-layout-specific (Arch/CachyOS/Fedora's `/lib64`, not Debian's
`/lib/x86_64-linux-gnu`).

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
