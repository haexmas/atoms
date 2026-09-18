# Nix devShell skeleton

Delivers a reproducible `nix develop`/`direnv` devShell to the consumer
repo root: `flake.nix` and `.envrc`.

- Atom id: `com.github.haexmas.atoms.nix-devshell-base`
- Version: `0.5.0`
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
list to `pkgs.mkShell`. Adopt this molecule alongside whichever package
molecules a repo needs (e.g. [`com.github.haexmas.atoms.nix-rust`](../nix-rust/),
[`com.github.haexmas.atoms.nix-nodejs`](../nix-nodejs/)): each contributes
its own package names, and this molecule's `flake.nix` never needs to
change when contributors are added or removed.

The read is guarded (`builtins.pathExists`): no adopted molecule
declaring `nix_packages` is a valid "no extra packages" state, not an
error, since this molecule's own lifecycle is independent of any
particular package contributor's.

### Dotted package names (v0.5.0+)

A `nix_packages` entry is normally a plain top-level attribute name
(`"gtk3"` → `pkgs.gtk3`). It can also be a dotted path (`"gcc.cc.lib"`,
`"dbus.lib"`), resolved via `lib.getAttrFromPath` instead of `pkgs.${name}`.
This exists because some nixpkgs packages split their shared library out
of the *default* output: plain `glib` resolves to its `bin` output (not
the one with `libglib-2.0.so`), and `dbus`'s default output has no
`lib/` at all — the library is in `dbus.lib`. There's no flat top-level
alias for `libstdc++`/`libgcc_s` either; it's `gcc.cc.lib`. A consumer
needing one of these writes `"glib.out"`/`"dbus.lib"`/`"gcc.cc.lib"` in
its own `nix_packages` fragment instead of the plain name.

### Runtime library resolution (v0.5.0+)

`devShells.default` sets `LD_LIBRARY_PATH` to
`lib.makeLibraryPath packages` via a `shellHook` — every resolved
package's `lib/` directory, generically, driven entirely by whatever
`nix_packages` molecules contribute (no per-package or per-consumer
special-casing). This exists because Nix's own dynamic linker does
**not** consult the host's `/etc/ld.so.cache`: a package landing in
`packages` makes it resolvable at *build* time (via `pkg-config`/`-L`
flags) but not necessarily at *runtime*, and RPATH isn't a reliable
alternative here either — at least for
[`com.github.haexmas.atoms.holzi`](../holzi/)'s Tauri binary, Tauri's own
build process overwrites whatever RPATH the Nix cc-wrapper would have
auto-added with its own bundle-relative convention. Without this, a
GUI binary linking something like `webkitgtk_4_1` compiles fine and then
fails at first run with "shared object not found" — caught live: this
molecule's `flake.nix` had shipped since v0.3.0 without ever actually
being used to run a GUI app through it.

### Unfree packages

`flake.nix`'s `import nixpkgs { ... }` sets `config.allowUnfree = true`
(v0.4.0+). Some package-contributor molecules need a package nixpkgs
marks unfree — e.g.
[`com.github.haexmas.atoms.holzi`](../holzi/)'s `cudatoolkit`, gated
behind the CUDA EULA. Without this, `pkgs.${name}` throws `Refusing to
evaluate package ... because it has an unfree license` at flake
evaluation time, before `nix develop`/`direnv` even gets to build
anything.

This is a blanket allow, not a per-package predicate
(`config.allowUnfreePredicate`): `cudatoolkit` alone is a meta-package
bundling several separately unfree-licensed sub-derivations
(`cuda_nvcc`, `cuda_cuobjdump`, ...), and that set of names is not
stable across nixpkgs revisions — a predicate listing them would break
silently on a `nixpkgs` bump. Since this molecule's `flake.nix` is the
sole place any consumer's `import nixpkgs` happens, this is also the
only place such an allowance can live; a package-contributor molecule
has no flake of its own to set it in.

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

## First-time consumer setup

Three preconditions are easy to miss on a fresh machine; the
`install_hook` only checks the first one.

1. **Flakes must be enabled.** A default Nix install has `nix-command`
   and `flakes` behind the `experimental-features` flag — without it,
   `nix develop`/`direnv`'s `use flake` fail with `experimental Nix
   feature 'nix-command' is disabled`. Enable it per-user, no root
   needed:

   ```bash
   mkdir -p ~/.config/nix
   echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
   ```

2. **direnv itself must be installed.** Nix does not bring it in; install
   it via your distro/package manager (e.g. `sudo pacman -S direnv`,
   `sudo apt install direnv`, `brew install direnv`, or
   `nix profile install nixpkgs#direnv`).

3. **direnv must be hooked into your shell.** Add the hook line for your
   shell to its startup file, then open a new shell:

   ```bash
   # bash (~/.bashrc) / zsh (~/.zshrc)
   eval "$(direnv hook bash)"   # or: zsh

   # fish (~/.config/fish/config.fish)
   direnv hook fish | source
   ```

With all three in place, `cd` into the consumer repo and run
`direnv allow` once; direnv builds the devShell (first run can take a
while) and loads `nix`-provisioned tools (`node`, `pnpm`, `cargo`, ...)
into `PATH` automatically on every subsequent `cd`. Without direnv,
`nix develop` (with flakes enabled per step 1) drops into an equivalent
shell manually.
