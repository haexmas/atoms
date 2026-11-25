# Playwright browsers for the Nix devShell

A `nix_packages`-only molecule contributing the browsers Playwright drives
(`playwright-driver.browsers`: Chromium, Chromium headless shell, Firefox, WebKit)
to a consumer's composed Nix devShell.

- Atom id: `com.github.haexmas.atoms.nix-playwright`
- Version: `0.1.0`
- Delivered atoms: a package fragment under `atoms.nix_packages` — no
  `flake.nix` of its own (adopt
  [`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/)
  for that, **version 0.10.0 or later**).

## What it does and what it does not

Playwright downloads its own browsers on first use into `~/.cache/ms-playwright`. Those
binaries are not reproducible and on NixOS-like hosts do not run at all. This molecule
puts the browsers of the pinned nixpkgs into the devShell instead.

`nix-devshell-base` (0.10.0+) notices this package by name and exports, like it already
does for `cudatoolkit` and `llvmPackages.libclang.lib`:

- `PLAYWRIGHT_BROWSERS_PATH` = the browsers of this nixpkgs, so Playwright uses them
  instead of downloading;
- `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true`, because the host check looks for
  system libraries that the Nix browsers bring themselves.

**The Playwright client must match the browsers.** The browsers are built for exactly one
Playwright release (the nixpkgs attribute `playwright-driver.version`). Install the
Python client (`pip install playwright==<version>`) or the npm client with that same
version, or Playwright reports "Executable doesn't exist". `nix eval nixpkgs#playwright-driver.version`
prints it for the pinned nixpkgs.

## Adopting

Add the molecule to a consumer's `.spaex/manifest.json` and pin the full
commit SHA of this publisher repository, as for the other `nix-*` molecules, then run
`spaex install`.

## Rendering WebGL pages

A Nix-built browser cannot reach the host's GPU drivers. For WebGL (three.js and the like),
`nix-devshell-base` 0.10.0+ additionally exports the paths of Mesa's software renderer
(llvmpipe) as inert variables: `PLAYWRIGHT_GL_LIBRARY_PATH`, `PLAYWRIGHT_GL_EGL_VENDOR`,
`PLAYWRIGHT_GL_DRIVERS`. Launch the browser with `--use-angle=gl` and give *that process*:

```python
env = {**os.environ,
       "LD_LIBRARY_PATH": os.environ["PLAYWRIGHT_GL_LIBRARY_PATH"],
       "__EGL_VENDOR_LIBRARY_FILENAMES": os.environ["PLAYWRIGHT_GL_EGL_VENDOR"],
       "LIBGL_DRIVERS_PATH": os.environ["PLAYWRIGHT_GL_DRIVERS"],
       "LIBGL_ALWAYS_SOFTWARE": "1"}
browser = p.chromium.launch(args=["--use-angle=gl", "--ignore-gpu-blocklist"], env=env)
```

Checked with the browsers of nixpkgs 2786a2a (Playwright 1.64.1): `WEBGL_debug_renderer_info`
reports `Mesa, llvmpipe`. SwiftShader (`--use-angle=swiftshader`) needs a Vulkan loader and
did not start on the test host.
