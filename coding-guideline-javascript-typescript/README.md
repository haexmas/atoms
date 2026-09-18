# JavaScript and TypeScript best practices

Behavior atom for JavaScript and TypeScript projects.

- Atom id: `com.github.haexmas.atoms.coding-guideline-javascript-typescript`
- Version: `0.4.0`
- Delivered atoms: `javascript-typescript.md` and `testing.md` under
  `atoms.behavior`

The atoms give coding agents a compact baseline for type safety, trust-boundary
validation, asynchronous code, module design, and JavaScript/TypeScript test
strategy. Runtime- and repository-specific conventions take precedence.

This molecule is behavior-only — it does not provision a JS runtime itself.
For a Nix devShell with Node.js and pnpm, adopt
[`com.github.haexmas.atoms.nix-nodejs`](../nix-nodejs/) alongside
[`com.github.haexmas.atoms.nix-devshell-base`](../nix-devshell-base/). Kept
separate deliberately: adopting JS/TS coding guidance and adopting a
Node/pnpm Nix devShell are independent decisions (v0.2.0 briefly coupled
them via a `nix_packages` fragment on this molecule — reverted). Prefixed
`coding-guideline-` (renamed from plain `javascript-typescript` in
v0.4.0) so its scope is unambiguous alongside `nix-nodejs`.

## Adopting

Add the molecule to a consumer's `.spaex.json` and pin the full commit SHA of
this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.coding-guideline-javascript-typescript"]
}
```

Then run `spaex install`.

## Research basis

The guidance is based on the official
[TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/),
[TypeScript `strict` option](https://www.typescriptlang.org/tsconfig/strict),
[TypeScript modules documentation](https://www.typescriptlang.org/docs/handbook/2/modules.html),
and MDN's guides for
[modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
and [promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises).
Runtime and framework conventions remain project-specific.

The testing atom is intentionally framework-neutral; JavaScript and
TypeScript do not prescribe one universal test runner. Node projects may use
the built-in [`node:test`](https://nodejs.org/api/test.html) runner, while
browser and framework projects should follow their configured runner.
