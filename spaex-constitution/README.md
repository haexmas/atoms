# `spaex-constitution`

The distributable form of spaex's own constitution. This directory
carries ONLY the Spec 023 behavior fragments (`fragments/*.md`, declared
in `manifest.json`'s `atoms.behavior`), one file per directive.

The authoritative, human-readable text lives in the spaex repo itself, at
`.specify/memory/constitution.md` — that is where spaex's own speckit
tooling (`/speckit-plan`, `/speckit-constitution`, etc.) reads it from
directly, independent of the atom/molecule system. This molecule does not
keep a second copy of that document: a standalone `constitution.md` here
would duplicate it with no reader (nothing in the delivery pipeline
references it; `manifest.json` only declares `fragments/`), and every
duplicate is a place content can drift out of sync.

Any spaex-family consumer's `spaex install` materializes these fragments
and composes them into its own `.spaex.md` — that composed file, not a
static document in this repo, is the fragment-derived human-readable view.

Amending a principle in the spaex repo's `constitution.md` MUST update the
corresponding fragment file here in the same logical change (see that
document's own Governance section and this repo's
`amendment-mirrors-fragment-in-same-commit` fragment). See ADR 0014/0015/0016
in the spaex repo for this molecule's full history: the original split
into fragments while still self-published, post-merge fidelity fixes, and
the relocation here.
