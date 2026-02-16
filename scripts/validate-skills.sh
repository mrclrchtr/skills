#!/usr/bin/env bash
set -euo pipefail

# Pinned for reproducible validation behavior. Update intentionally.
SKILLS_REF_SHA="b7442eb9acf4c05545ea9c26b139acbda15eb718"
SKILLS_REF_FROM="git+https://github.com/agentskills/agentskills.git@${SKILLS_REF_SHA}#subdirectory=skills-ref"

if ! command -v uvx >/dev/null 2>&1; then
  echo "Error: uvx is required but was not found on PATH." >&2
  echo "Install uv (https://docs.astral.sh/uv/) and retry." >&2
  exit 2
fi

if ! command -v fd >/dev/null 2>&1; then
  echo "Error: fd is required but was not found on PATH." >&2
  exit 2
fi

skill_manifests=()
while IFS= read -r manifest; do
  skill_manifests+=("${manifest}")
done < <(fd --type file --glob "SKILL.md" skills | sort)

if [ "${#skill_manifests[@]}" -eq 0 ]; then
  echo "No SKILL.md files found under skills/."
  exit 0
fi

failures=0

for manifest in "${skill_manifests[@]}"; do
  skill_dir="$(dirname "${manifest}")"
  echo "Validating ${skill_dir}"

  if uvx --from "${SKILLS_REF_FROM}" skills-ref validate "${skill_dir}"; then
    echo "PASS ${skill_dir}"
  else
    echo "FAIL ${skill_dir}" >&2
    failures=$((failures + 1))
  fi
done

if [ "${failures}" -gt 0 ]; then
  echo "Validation failed for ${failures} skill(s)." >&2
  exit 1
fi

echo "All skills validated successfully."
