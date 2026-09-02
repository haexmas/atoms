# haexmas/atoms

A collection of [haex-hive](https://github.com/haexmas/haex-hive) atoms
published from a single repository. Every atom lives in its own top-level
directory and is registered in the publisher manifest at
[`manifest.json`](manifest.json).

## Atoms

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
