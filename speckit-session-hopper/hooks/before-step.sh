#!/usr/bin/env sh
set -eu

STEP="${1:-<step>}"
BRANCH="$(git branch --show-current 2>/dev/null || echo '<unknown>')"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

cat <<EOF
======================================================
Next step: /speckit-${STEP}
Recommendation: run this in a NEW session (isolated context).

Open a new session in the same worktree:
    cd ${ROOT}
Expected branch: ${BRANCH}
Then run:
    /speckit-${STEP}

Or reply "inline" to keep this agent running the step here.
======================================================
EOF
