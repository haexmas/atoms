# Quickstart: adopting graphify-first-authoring

This walks through adopting the atom on a repo that already uses spaex's v4 manifest (`.spaex/manifest.json`, `spaex install`).

## 1. Prerequisite: the `graphify` CLI

```console
$ uv tool install graphifyy
$ graphify --help
```

If this is already installed, continue to step 2. Otherwise, `spaex install`
offers this package installation with a default-Yes prompt after the molecule
has been adopted. Declining the prompt leaves the repository unchanged and
prints the manual follow-up.

## 2. Adopt the atom in `.spaex/manifest.json`

Add the molecule id to a `compounds[].molecules[]` allowlist entry:

```json
{
  "molecules": ["com.github.haexmas.atoms.graphify-first-authoring"],
  "revision": "<pinned commit SHA>",
  "source": "https://github.com/haexmas/atoms"
}
```

## 3. Install

```console
$ spaex install
```

`spaex install` runs the molecule's declared `install.py` hook on the tracked
branch. If `graphify` is missing, the hook offers to install `graphifyy`; it
also installs the Git hooks and adds `graphify-out/` to `.gitignore`. Review the
generated `.spaex/constitution.md` before committing. The fragment is
materialized under `.spaex/constitution.d/` and composed with any other active
behavior fragments.

## 4. Verify

```console
$ spaex constitution show
```

The printed output should show the adopted behavior fragment. From this point,
any agent bound by this harness consults `graphify-out/` before authoring
new named code.

## 5. Confirm the hooks are live

```console
$ git commit --allow-empty -m "chore: test graphify-out refresh"
$ ls graphify-out/.meta.json   # should reflect the new HEAD
```

When creating a feature worktree from `main` or another tracked branch, the
hook finds the source automatically by matching the new checkout HEAD. A
feature-from-feature worktree can still pass the source explicitly:

```console
# Linux / macOS / WSL2
$ git worktree add -b feature/x ../hive-feature

# Feature from a linked worktree (optional explicit override)
$ GRAPHIFY_PARENT_WORKTREE="$PWD" git worktree add -b feature/x ../hive-feature

# PowerShell
PS> git worktree add -b feature/x ..\hive-feature

# Feature from a linked worktree (optional explicit override)
PS> $env:GRAPHIFY_PARENT_WORKTREE = (Get-Location).Path
PS> git worktree add -b feature/x ..\hive-feature
```

If no tracked source worktree matches, the hook leaves the destination
untouched; the agent-side rule handles the missing snapshot according to the
branch type.

## Suspending the rule for one session

Tell the agent explicitly: "skip graphify check" — this holds only for the current session and must be re-issued next time.
