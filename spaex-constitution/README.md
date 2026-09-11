# `spaex-constitution`

The spaex project's own constitution, relocated here from the spaex repo
itself (see the spaex repo's ADR 0016, and this molecule's own history
before that: ADR 0014/0015 in the spaex repo cover the original split
into fragments while it was still self-published).

`constitution.md` is the authoritative, human-readable text. `manifest.json`
declares the same directives as Spec 023 behavior fragments under
`fragments/`, one file per directive. Any spaex-family consumer's
`spaex install` materializes those fragments and composes them into its
own `.spaex.md`.

Amending a principle in `constitution.md` MUST update its corresponding
fragment file in the same commit (see constitution.md's own Governance
section and its `self-modifying-instructions-review-gated` /
`amendment-procedure-requires-single-commit` / `amendment-mirrors-fragment-in-same-commit`
fragments).

The spaex repo itself now consumes this molecule the same way any other
consumer would, via its own `.spaex.json`, rather than self-publishing it.
