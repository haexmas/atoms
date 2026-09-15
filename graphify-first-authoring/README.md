# graphify-first-authoring molecule

Opt-in molecule that changes agent authoring behavior: **consult the graphify knowledge graph before authoring any new named code, and prefer extending an existing artifact over duplicating it.**

- **Molecule id**: `com.github.haexmas.atoms.graphify-first-authoring`
- **Delivers**: `atoms.behavior: ["constitution.md", "context-map.md"]` (composed into the adopting repo's `.spaex/constitution.md` via `spaex install`)
- **Also ships**: a `post-commit` hook (auto-refresh `graphify-out/` on tracked branches), a `post-checkout` hook (fork-point snapshot into new worktrees), and an installer for both

The `context-map` fragment defines a bounded, task-specific context operation
using the existing `graphify query --budget` interface. It is deliberately
agent-facing and does not add a second repository index or claim a separate
CLI command.

Nothing here is part of spaex's core constitution. Adopt it explicitly in your repo's `.spaex/manifest.json` if you want it.

## What the rule does

Before authoring **any new named function, class, component, store, module, or CLI command**, an agent bound by the assembled constitution:

1. On tracked branches, ensures a usable `graphify-out/graph.json` is present and fresh — bootstrapping or refreshing (`graphify update <repo-root>`) if the directory or graph file is absent, or the marker is missing/invalid or stale. Feature-branch/worktree snapshots stay frozen at their fork point and are not refreshed against feature `HEAD`; an incomplete snapshot is reported and handled as a failed consultation.
2. Queries the graph for candidates via plain `graphify` CLI (`graphify query "..."`, `graphify path`, `graphify explain`), evaluating unexported/incomplete artifacts too.
3. When a candidate matches: names the candidate location, proposes extending it, cites lines saved, rewrites **one** call-site as proof of concept — and waits for operator approval before touching anything else.
4. When similarity is borderline or scope-creep risk exists: **asks the operator** rather than deciding autonomously.
5. When the graph consult itself fails: warns, proceeds with authoring, and flags the skipped consult for a manual check later.

Full text lives in [`constitution.md`](constitution.md).

## Adoption (quick path)

For a repo that already runs spaex manifest v4 (`.spaex/manifest.json`, `spaex install`), see the [quickstart](specs/quickstart.md) for the complete adoption flow:

1. Add a `compounds[]` entry with this molecule id, pinned to a full SHA of this repo:

   ```json
   {"spaex_version": "4", "compounds": [{"source": "https://github.com/haexmas/atoms", "revision": "<full 40-char SHA>", "molecules": ["com.github.haexmas.atoms.graphify-first-authoring"]}]}
   ```
2. `spaex install` — materializes the behavior and runs the declared installer hook. If `graphify` is absent, the installer offers to install `graphifyy`.
3. `spaex constitution show` — verifies the installed constitution
4. `git commit --allow-empty -m "chore: test refresh"` — verifies the hook is live

## Files

| Path | Purpose |
|---|---|
| `manifest.json` | Molecule manifest v4, behavior files plus the `install.py` hook declaration |
| `constitution.md` | The contributed behavior fragment |
| `context-map.md` | Token-bounded context-map protocol backed by `graphify query` |
| `hooks/post-commit` | Refresh entrypoint (shebang set at install time) |
| `hooks/post-checkout` | Snapshot entrypoint (shebang set at install time) |
| `hooks/_refresh.py` | Refresh helper — `graphify update <root>`, warn-on-failure |
| `hooks/_snapshot.py` | Snapshot helper — copy the tracked source branch's `graphify-out/` into a new worktree |
| `hooks/_tracked_branches.py` | Tracked-branch set: detected default + `.spaex/manifest.json`'s `tracked_branches[]` |
| `install.py` | Installer — precondition-checked, refuses cleanly on any failure |

## What it does not do

- It does **not** rewrite existing duplicates already committed to the codebase (scope is new authoring).
- It does **not** replace human review — borderline calls escalate to the operator.
- It does **not** silently install anything into your Python environment (the installer prompts before `sys.executable -m pip install graphifyy`). It also prompts before `graphify install` when the local registration marker is absent, records successful registration in local git config, and skips that step only when the marker is present. `graphify-out/` presence alone is not a registration signal.
- If graph bootstrap or refresh fails, the agent warns and continues; the failed refresh is flagged for a later manual check.
- It does **not** cause git operations to fail — both hooks always exit 0 regardless of whether their work succeeded.
- Worktree snapshots automatically select the tracked source branch whose HEAD matches the new worktree's checkout HEAD. Set `GRAPHIFY_PARENT_WORKTREE` when creating a worktree from another linked worktree.

## Suspending for one session

Tell the agent: *"skip graphify check"* (or any equivalent). The suspension holds only for the current session and does not persist.

## Uninstall

Git's effective hooks directory is per-machine and never committed. To remove:

```bash
hooks_dir="$(git rev-parse --git-path hooks)"
rm "$hooks_dir"/post-commit "$hooks_dir"/post-checkout
rm "$hooks_dir"/_refresh.py "$hooks_dir"/_snapshot.py "$hooks_dir"/_tracked_branches.py
```

`graphify uninstall` handles the graphify side (harness registration) separately.
Clear the installer’s local registration marker as part of uninstall so a later
install performs registration again:

```bash
git config --local --unset graphify-first-authoring.registration || true
```
