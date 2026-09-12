## Per-step session isolation

Sessions in a repository that adopts
`com.github.haexmas.atoms.speckit-session-hopper` in `.spaex.json`
MUST, before every `command:` step of that workflow:

1. Execute the step's `hooks.before` script and capture its stdout.
2. Display the captured block to the operator verbatim.
3. Wait for the operator's answer.
4. Continue the step in the current session only if the operator's
   answer is exactly `inline` (case-insensitive). On any other
   answer, stop and defer the step to the new session the operator
   opens; the current session resumes at the next review gate once
   the new session's output is on disk.

Under the Spec 011 simplification amendment (2026-09-02), adoption of a
workflow atom in `.spaex.json` alone determines binding: there is
no `workflow-registry.json` and no `active_workflow` field.
