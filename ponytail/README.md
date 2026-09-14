# Ponytail

Portable spaex behavior atom derived from
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail).

- Atom id: `com.github.haexmas.atoms.ponytail`
- Version: `4.9.1`
- Upstream revision: `356918eba965ee1eac64bd3a7f0dd02108350de5`
- Delivered atom: `ponytail.md` under `atoms.behavior`

The fragment carries Ponytail's agent-neutral lazy-senior-dev rules. The
upstream repository's host-specific plugin manifests, lifecycle hooks, and
skills are intentionally not mirrored here; those belong to the respective
agent plugin or skill distribution mechanism.

## Adopting

Add the molecule to a consumer's `.spaex/manifest.json` and pin the full
commit SHA of this publisher repository:

```json
{
  "spaex_version": "4",
  "identity": "com.example.my-project",
  "compounds": [
    {
      "source": "https://github.com/haexmas/atoms",
      "revision": "<full-40-char-sha>",
      "molecules": ["com.github.haexmas.atoms.ponytail"]
    }
  ]
}
```

Then run `spaex install`.

## Upstream provenance

The behavior text is adapted from the upstream `AGENTS.md` at the revision
listed above. Ponytail is MIT-licensed upstream.
