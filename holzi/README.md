# holzi devShell extras

A `nix_packages`-only molecule contributing the system libraries
[holzi](https://github.com/haexmas/holzi)'s Tauri v2 app needs to build on
Linux, beyond what the generic
[`com.github.haexmas.atoms.nix-rust`](../nix-rust/) and
[`com.github.haexmas.atoms.nix-nodejs`](../nix-nodejs/) molecules already
provide.

- Atom id: `com.github.haexmas.atoms.holzi`
- Version: `0.5.0`
- Delivered atoms: a package fragment under `atoms.nix_packages` — no
  `flake.nix` of its own (adopt
  [`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)
  for that).

This molecule is deliberately scoped to holzi, not a generic "Tauri"
molecule: the package list (`libayatana-appindicator`,
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
GTK stack (`libgtk-3`, `libcairo`, `libglib-2.0`/`libgobject-2.0`/
`libgio-2.0`, `libgdk_pixbuf-2.0`, `libdbus-1`, `libsoup-3.0`), and none
of it was ever actually resolvable at *runtime* before this — nothing
wired up `LD_LIBRARY_PATH` (see
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)'s
README), so the app crashed on the first "shared object not found"
whether or not CUDA was involved; nobody had noticed yet because
`cudatoolkit`'s own libraries happened to be earlier in the binary's
needed-library list and masked it. `gcc.cc.lib` is the one CUDA-only
addition here (`libstdc++`/`libgcc_s`, needed transitively by `cudarc`'s
C++ CUDA libraries, not by holzi's own Rust code, nor by GTK).

Some of these packages split their shared library into a non-default
output (`dbus`'s default output has no `lib/`; plain `glib` resolves to
its `bin` output, not the one with `libglib-2.0.so`) — that's why the
list uses dotted names (`glib.out`, `dbus.lib`): see
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)'s
README for how `flake.nix` resolves those.

### `webkitgtk_4_1` was removed again (v0.5.0)

It briefly lived here (v0.4.0) alongside the GTK stack above, then got
pulled back out. WebKit's own helper-process binaries
(`WebKitWebProcess`/`WebKitNetworkProcess`, shipped prebuilt inside the
package) hardcode their own nix store path internally — there's no env
var to relocate them (checked: not present in this build), so making
them host-glibc-consistent (needed for the same reason below) means
either a full from-source WebKit rebuild just to relink two `patchelf`
calls, or accepting that they're always Nix-glibc-linked and will ABI-
clash with anything host-provided they end up needing. Neither is worth
it: `sudo pacman -S webkit2gtk-4.1` (or the consumer's own distro
equivalent) instead, and `scripts/with-nix-host-bridge.sh` in holzi
puts the host's `/usr/lib/pkgconfig` on `PKG_CONFIG_PATH` so the build
finds it. The rest of the GTK stack (gtk3, cairo, glib, ...) stays
Nix-provided — mixing was already proven fine in the direction
"Nix-provided libraries loaded into a host-glibc-primary process";
WebKit's helper processes specifically are the piece that can't be made
consistent either way without a full rebuild.

The proprietary GPU driver (`libcuda.so.1`) is the other piece that
deliberately still comes from the host (`nvidia-utils` via pacman, or
equivalent) — Nix can't reproducibly bundle a driver matching whatever
kernel module happens to be loaded. Since the binary now always links
the host's WebKit too, `src-tauri/build.rs` points its own ELF
interpreter at the host's dynamic linker (verified newer here, so
backward-compatible with Nix's) and adds `/usr/lib` as an rpath —
*unconditionally* whenever `rustc` itself is Nix-provided (detected via
`RUSTC` starting with `/nix/store/`), not just for `llm-cuda`, since
every build now needs this. Never on CI (ubuntu-24.04 via `apt-get`/
rustup, no Nix involved), where it would break things: wrong FHS
`/lib64` path, and CI's own `libwebkit2gtk-4.1-dev` apt package is
already fully host-native with no clash to begin with.

### `scripts/with-nix-host-bridge.sh` (holzi repo, not this molecule)

Beyond `PKG_CONFIG_PATH`, running the actual GUI app needs three more
host bridges Nix's dynamic linker doesn't provide by default: Mesa's
GBM/DRI loader defaults to the NixOS-only `/run/opengl-driver`
convention (`GBM_BACKENDS_PATH`) and so does GLVND's EGL vendor dispatch
(`__EGL_VENDOR_LIBRARY_DIRS`); and Nix's gdk-pixbuf doesn't register
png/jpeg (compiled in, but not listed for module-based format sniffing)
or svg (a separate package, librsvg, whose setup-hook points
`GDK_PIXBUF_MODULE_FILE` at an svg-only cache that shadows gdk-pixbuf's
own) in a way GTK's icon loading can see — the script generates a
combined `gdk-pixbuf-query-loaders` cache for both at devShell-shellHook
time. All Linux-host-specific (Arch/CachyOS-family paths); adjust for
other distros.

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
