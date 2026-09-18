# Rust best practices

Behavior atom for Rust projects.

- Atom id: `com.github.haexmas.atoms.rust`
- Version: `0.4.0`
- Delivered atoms: `rust.md` and `testing.md` under `atoms.behavior`

The atoms give coding agents a compact baseline for ownership, types, error
handling, async code, unsafe code, and Rust's unit, integration, and
documentation testing workflow.
Project-specific conventions and tool commands take precedence where they are
more specific.

This molecule is behavior-only — it does not provision the Rust toolchain
itself. For a Nix devShell with `rustc`/`cargo`/`clippy`/`rustfmt`, adopt
[`com.github.haexmas.atoms.nix-rust`](../nix-rust/) alongside
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/). Kept
separate deliberately: adopting Rust coding guidance and adopting a Rust
Nix devShell are independent decisions (v0.3.0 briefly coupled them via a
`nix_packages` fragment on this molecule — reverted).

## Adopting

Add the molecule to a consumer's `.spaex.json` and pin the full commit SHA of
this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.rust"]
}
```

Then run `spaex install`.

## Research basis

The guidance is based on the official
[Rust Book](https://doc.rust-lang.org/book/),
[Rust API Guidelines](https://rust-lang.github.io/api-guidelines/),
[Clippy documentation](https://doc.rust-lang.org/clippy/), and the
[Async Rust Book](https://rust-lang.github.io/async-book/). These sources
describe recommendations and project-configurable tooling; they do not
replace a consuming project's own supported toolchain or conventions.

The testing guidance additionally follows the [Rust testing chapter](https://doc.rust-lang.org/book/ch11-01-writing-tests.html)
and [Cargo's test documentation](https://doc.rust-lang.org/cargo/commands/cargo-test.html).
