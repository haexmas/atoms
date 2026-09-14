# `ast-grep` molecule

Optional behavior molecule for syntax-aware search and rewrites with
[`ast-grep`](https://github.com/ast-grep/ast-grep), also available as the
`sg` executable.

- **Molecule id**: `com.github.haexmas.atoms.ast-grep`
- **Version**: `0.1.0`
- **Delivers**: `atoms.behavior: ["constitution.md"]`

The behavior is intentionally complementary to Graphify: use Graphify to
locate the relevant domain artifacts and relationships, then use ast-grep to
find or validate syntax-shaped matches. It does not install the external
binary. If ast-grep is unavailable, the behavior requires a scoped `rg`
fallback rather than an automatic package installation.

## Adoption

Add the molecule to a consumer's `.spaex/manifest.json`, pinning the full
publisher revision, and run `spaex install`:

```json
{
  "spaex_version": "4",
  "compounds": [
    {
      "source": "https://github.com/haexmas/atoms",
      "revision": "<full-40-char-sha>",
      "molecules": ["com.github.haexmas.atoms.ast-grep"]
    }
  ]
}
```

Install ast-grep separately through the package manager appropriate for the
consumer environment. The molecule only contributes the workflow contract.
