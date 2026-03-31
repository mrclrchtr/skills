#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/bin" "$TMP_DIR/repo/skills/demo"

cat >"$TMP_DIR/repo/skills/demo/SKILL.md" <<'EOF'
---
name: demo
description: Demo skill for validate-skills hook env test
---
EOF

cat >"$TMP_DIR/bin/fd" <<'EOF'
#!/usr/bin/env bash
printf 'skills/demo/SKILL.md\n'
EOF

cat >"$TMP_DIR/bin/git" <<'EOF'
#!/usr/bin/env bash
if [[ "${1:-}" == "rev-parse" && "${2:-}" == "--local-env-vars" ]]; then
  printf 'GIT_DIR\nGIT_WORK_TREE\nGIT_INDEX_FILE\n'
  exit 0
fi

printf 'unexpected git invocation: %s\n' "$*" >&2
exit 1
EOF

cat >"$TMP_DIR/bin/uvx" <<'EOF'
#!/usr/bin/env bash
if [[ -n "${GIT_DIR:-}" || -n "${GIT_WORK_TREE:-}" || -n "${GIT_INDEX_FILE:-}" ]]; then
  printf 'git hook environment leaked into uvx\n' >&2
  exit 1
fi

printf '%s\n' "$*" >"$UVX_LOG"
exit 0
EOF

chmod +x "$TMP_DIR/bin/fd" "$TMP_DIR/bin/git" "$TMP_DIR/bin/uvx"

(
  cd "$TMP_DIR/repo"
  PATH="$TMP_DIR/bin:$PATH" \
  UVX_LOG="$TMP_DIR/uvx.log" \
  GIT_DIR=/fake/git-dir \
  GIT_WORK_TREE=/fake/worktree \
  GIT_INDEX_FILE=/fake/index \
  bash "$ROOT/scripts/validate-skills.sh"
)

grep -Fq 'skills-ref validate skills/demo' "$TMP_DIR/uvx.log"
