# Go best practices

Behavior atom for Go projects.

- Atom id: `com.github.haexmas.atoms.coding-guideline-go`
- Version: `0.1.0`
- Delivered atoms: `go.md` and `testing.md` under `atoms.behavior`

The atoms give coding agents a compact baseline for error handling, contexts,
interfaces, concurrency, package layout, safe process execution, and Go's
table-driven, race-detector, and fuzz testing workflow.
Project-specific conventions and tool commands take precedence where they are
more specific.

This molecule is behavior-only — it does not provision the Go toolchain
itself. Adopting Go coding guidance and adopting a Go Nix devShell are
independent decisions, matching
[`coding-guideline-rust`](../coding-guideline-rust/) and
[`nix-rust`](../nix-rust/).

## Adopting

Adopt the molecule in a consumer repository with `spaex add`; it pins the
commit SHA of this publisher repository in `.spaex/manifest.json` and installs
the molecule:

```sh
spaex add https://github.com/haexmas/atoms com.github.haexmas.atoms.coding-guideline-go
```

## Research basis

The guidance is based on the official
[Effective Go](https://go.dev/doc/effective_go),
[Go Code Review Comments](https://go.dev/wiki/CodeReviewComments),
[Working with errors in Go 1.13](https://go.dev/blog/go1.13-errors), and the
[module layout guide](https://go.dev/doc/modules/layout). These sources
describe recommendations and project-configurable tooling; they do not
replace a consuming project's own supported toolchain or conventions.

The testing guidance additionally follows the
[`testing` package documentation](https://pkg.go.dev/testing) and the
[table-driven tests wiki page](https://go.dev/wiki/TableDrivenTests).
