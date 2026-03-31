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

skill_manifests=()
if command -v fd >/dev/null 2>&1; then
  while IFS= read -r manifest; do
    skill_manifests+=("${manifest}")
  done < <(fd --type file --glob "SKILL.md" skills | sort)
else
  while IFS= read -r manifest; do
    skill_manifests+=("${manifest}")
  done < <(find skills -type f -name "SKILL.md" | sort)
fi

if [ "${#skill_manifests[@]}" -eq 0 ]; then
  echo "No SKILL.md files found under skills/."
  exit 0
fi

run_skills_ref_validate() {
  local skill_dir="$1"

  (
    # Git hooks export repository-local GIT_* variables. Clear them before uvx
    # fetches the remote skills-ref repo so nested git operations use a clean env.
    if command -v git >/dev/null 2>&1; then
      while IFS= read -r git_var; do
        [ -n "${git_var}" ] || continue
        unset "${git_var}"
      done < <(git rev-parse --local-env-vars 2>/dev/null || true)
    fi

    uvx --from "${SKILLS_REF_FROM}" skills-ref validate "${skill_dir}"
  )
}

failures=0

for manifest in "${skill_manifests[@]}"; do
  skill_dir="$(dirname "${manifest}")"
  echo "Validating ${skill_dir}"

  if run_skills_ref_validate "${skill_dir}"; then
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
