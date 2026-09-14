# haexmas/atoms

A collection of [spaex](https://github.com/haexmas/spaex) atoms
published from a single repository. Every atom lives in its own top-level
directory and is registered in the publisher manifest at
[`manifest.json`](manifest.json).

## Atoms

### `graphify-first-authoring`

A constitution-contributing atom that enforces a graphify-first authoring
workflow: after every commit and every checkout onto a tracked branch, a
per-repo hook regenerates the graphify snapshot so the constitution's
"read graphify before authoring" clause stays enforceable.

- Atom id: `com.github.haexmas.atoms.graphify-first-authoring`
- Kind: `constitution` + git hooks (v4 `atoms.constitution`, plus repo-side
  `install.py` that materializes hooks into `.git/hooks/`).
- Path: [`graphify-first-authoring/`](graphify-first-authoring/)

**Adopting**

Add the atom to the consumer's `.spaex.json` and run `spaex install`.
See [`graphify-first-authoring/README.md`](graphify-first-authoring/README.md)
and [`graphify-first-authoring/specs/quickstart.md`](graphify-first-authoring/specs/quickstart.md)
for the full adoption walkthrough. Publisher-side history and design
context are preserved verbatim under `graphify-first-authoring/specs/` and
`graphify-first-authoring/design.md`; those documents retain historical
source references.

### `speckit`

A Spec Kit integration molecule that provisions the pinned official
`specify-cli` and delegates project-local agent integration installation to
the official CLI. It includes Codex, Claude, Gemini, and the other integration
keys supported by `specify-cli 1.0.6`; it does not copy agent skill files into
the molecule.

- Atom id: `com.github.haexmas.atoms.speckit`
- Kind: Spec Kit integration declaration (`speckit`)
- Path: [`speckit/`](speckit/)

Adopt it with `spaex add` without a `--speckit-agents` flag. `spaex` will show
the declared integrations and ask the operator which ones to install. For
automation, pass an explicit comma-separated subset such as
`--speckit-agents claude,codex`; never use `--speckit-agents all` as an
unattended shortcut. See [`speckit/README.md`](speckit/README.md).

### `spaex-constitution`

The spaex project's own constitution: the authoritative `constitution.md`
text plus a Spec 023 behavior fragment per directive, relocated here from
the spaex repo's former self-published molecule.

- Atom id: `com.github.haexmas.atoms.spaex-constitution`
- Kind: constitution fragments (v4 `atoms.behavior`, one file per directive)
- Path: [`spaex-constitution/`](spaex-constitution/)

**Adopting**

Add the atom to the consumer's `.spaex.json` and run `spaex install`.
See [`spaex-constitution/README.md`](spaex-constitution/README.md) for
this molecule's history and governance notes.

### `ponytail`

The portable behavior part of
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): prefer
YAGNI, existing code, standard-library and native platform features, and the
smallest correct implementation. It is published as one `atoms.behavior`
fragment so it can be composed with other spaex behavior atoms.

- Atom id: `com.github.haexmas.atoms.ponytail`
- Kind: behavior fragment (`atoms.behavior`)
- Path: [`ponytail/`](ponytail/)

The upstream repository's host-specific plugin files, hooks, and skills are
not mirrored; use Ponytail's native plugin or skill installation for those
surfaces. See [`ponytail/README.md`](ponytail/README.md) for provenance and
adoption details.

### Language best practices

The publisher also contains language-specific behavior molecules. Each one is
deliberately small and can be adopted independently:

- `com.github.haexmas.atoms.rust` — ownership, types, error handling, async
  code, unsafe code, and Cargo verification; includes Rust testing guidance.
- `com.github.haexmas.atoms.javascript-typescript` — strict typing, trust
  boundaries, async control flow, module design, and verification; includes
  JavaScript/TypeScript testing guidance.
- `com.github.haexmas.atoms.python` — typing, explicit data models, validation,
  exceptions, resource management, async code, and verification; includes
  Python testing guidance.

All three are behavior molecules delivered through `atoms.behavior`. They are
baseline guidance: a consuming project's explicit conventions and supported
runtime versions remain authoritative.

### `general-coding`

Language-agnostic coding guidance covering practical LoC heuristics, function
and file boundaries, module structure, dependency direction, abstractions,
tests, and reviewable change size.

- Atom id: `com.github.haexmas.atoms.general-coding`
- Kind: behavior fragment (`atoms.behavior`)
- Path: [`general-coding/`](general-coding/)

## License

TBD.
