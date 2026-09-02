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
3. Edit `.specify/workflows/workflow-registry.json` and set
   `active_workflow` to
   `com.github.haexmas.atoms.speckit-session-hopper` to make the
   workflow binding. Unset (or set to `null`) to fall back to the
   bundled `speckit` workflow.

**Removing**

Remove the atom entry from `.haex-hive.json` and rerun `haex install`.
The published workflow directory, hook directory, and the constitution
fragment are removed by Spec 011 US3 delete-orphans; if
`active_workflow` still named this atom, it is reset to `null` in the
same generation.

## License

TBD.
