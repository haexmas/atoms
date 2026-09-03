# haexmas/atoms

A collection of [haex-hive](https://github.com/haexmas/haex-hive) atoms
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
- Kind: `constitution` + git hooks (v3 `atoms.constitution`, plus repo-side
  `install.py` that materializes hooks into `.git/hooks/`).
- Path: [`graphify-first-authoring/`](graphify-first-authoring/)

**Adopting**

Add the atom to the consumer's `.haex-hive.json` and run `haex install`.
See [`graphify-first-authoring/README.md`](graphify-first-authoring/README.md)
and [`graphify-first-authoring/specs/quickstart.md`](graphify-first-authoring/specs/quickstart.md)
for the full adoption walkthrough. Publisher-side history and design
context are preserved verbatim under `graphify-first-authoring/specs/` and
`graphify-first-authoring/design.md`; those documents were authored while
the atom lived in the haex-hive repository and still reference the old
identifiers.

### `speckit-session-hopper`

A `speckit-workflow` atom (Spec 011 atom kind) that mirrors the bundled
speckit "Full SDD Cycle" but prompts the operator, before every `command:`
step, to run that step in a NEW agent session instead of inline in the
current one. The prompt is advisory: the operator answers `inline` to
keep the current agent running the step, or opens a new session (in the
same worktree, on the same branch) and answers the prompt there.

- Atom id: `com.github.haexmas.atoms.speckit-session-hopper`
- Kind: `speckit-workflow` (via `contributes.speckit_workflow`)
- Path: [`speckit-session-hopper/`](speckit-session-hopper/)

**Adopting**

Under the Spec 011 simplification amendment (2026-09-02), adopting a
workflow atom in `.haex-hive.json` alone binds it. At most one
workflow atom may be adopted per repository; the reader falls back to
the bundled `speckit` workflow when none is adopted.

1. Add this atom to the consumer's `.haex-hive.json`:
   ```json
   {
     "includes": ["com.github.haexmas.atoms.speckit-session-hopper"],
     "revision": "<full-40-char-sha>",
     "source": "https://github.com/haexmas/atoms"
   }
   ```
2. Run `haex install --llm=file`. Review the pending constitution
   candidate. Rerun `haex install --accept-merged <candidate>`.

No third step is needed; the adoption itself is the binding signal.

**Removing**

Remove the atom entry from `.haex-hive.json` and rerun `haex install`.
The published workflow directory, hook directory, and the constitution
fragment are removed by Spec 011 US3 delete-orphans. After removal the
reader falls back to the bundled `speckit` workflow.

## License

TBD.
