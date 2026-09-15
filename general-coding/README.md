# General coding best practices

Behavior atom for language-agnostic coding guidance.

- Atom id: `com.github.haexmas.atoms.general-coding`
- Version: `0.4.0`
- Delivered atom: `general-coding.md` under `atoms.behavior`

The atom covers repository-local worktrees, practical decisions about line
counts, function and file boundaries, module structure, dependencies,
abstractions, tests, and review size. Its thresholds are intentionally soft
prompts, not hard quality gates. It also prohibits LLM agents from leaving
self-references or agent attribution in project artifacts. Repository-specific
conventions remain authoritative.

## Adopting

Add the molecule to a consumer's `.spaex.json` and pin the full commit SHA of
this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.general-coding"]
}
```

Then run `spaex install`.

## Research basis

The guidance is informed by Google's
[code review standard](https://google.github.io/eng-practices/review/reviewer/standard.html),
[small change guidance](https://google.github.io/eng-practices/review/developer/small-cls.html),
and [review checklist](https://google.github.io/eng-practices/review/reviewer/looking-for.html).
Those documents explicitly favor maintainability, understandable design,
appropriate tests, and small self-contained changes while noting that there
are no hard universal size rules.
