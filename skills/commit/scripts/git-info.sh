#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: git-info.sh

Print repository state for commit preparation:
  DATE    — current timestamp
  BRANCH  — active branch name
  STATUS  — porcelain v1 status (staged + unstaged)
  DIFF    — unstaged and staged diffs
  LOG     — last 20 commits (oneline graph)

Options:
  --help  Show this message and exit.

All data goes to stdout. Diagnostics go to stderr.
EOF
}

if [[ "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "${1:-}" != "" ]]; then
  echo "Error: unknown option '${1}'. Use --help for usage." >&2
  exit 2
fi

if ! git rev-parse --git-dir &>/dev/null; then
  echo "Error: not inside a git repository." >&2
  exit 1
fi

echo "## DATE"
date "+%Y-%m-%d %H:%M:%S"

echo "## BRANCH"
git branch --show-current

echo "## STATUS"
git status --porcelain=v1

echo "## DIFF (unstaged)"
git --no-pager diff

echo "## DIFF (staged)"
git --no-pager diff --staged

echo "## LOG (last 20)"
git --no-pager log --oneline -20 --graph
