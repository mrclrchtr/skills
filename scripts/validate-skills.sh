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

search_roots=()
[ -d skills ] && search_roots+=("skills")
# Discover plugin-packaged skill roots so adding a new plugins/<name>/skills/<skill>
# does not require editing this script.
if [ -d plugins ]; then
  while IFS= read -r plugin_skill_root; do
    [ -n "${plugin_skill_root}" ] || continue
    search_roots+=("${plugin_skill_root}")
  done < <(
    if command -v fd >/dev/null 2>&1; then
      fd --type directory --max-depth 3 --glob "skills" plugins | while IFS= read -r skills_dir; do
        # Each immediate subdir of plugins/<plugin>/skills/ is a skill root.
        find "${skills_dir}" -mindepth 1 -maxdepth 1 -type d
      done | sort
    else
      find plugins -mindepth 3 -maxdepth 3 -type d -path "*/skills/*" | sort
    fi
  )
fi

skill_manifests=()
if [ "${#search_roots[@]}" -gt 0 ]; then
  if command -v fd >/dev/null 2>&1; then
    while IFS= read -r manifest; do
      skill_manifests+=("${manifest}")
    done < <(fd --type file --glob "SKILL.md" "${search_roots[@]}" | sort)
  else
    while IFS= read -r manifest; do
      skill_manifests+=("${manifest}")
    done < <(
      for root in "${search_roots[@]}"; do
        find "${root}" -type f -name "SKILL.md"
      done | sort
    )
  fi
fi

if [ "${#skill_manifests[@]}" -eq 0 ]; then
  echo "No SKILL.md files found under configured skill roots."
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

if [ ! -f .claude-plugin/marketplace.json ]; then
  echo "Missing root marketplace manifest: .claude-plugin/marketplace.json" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq is required but was not found on PATH." >&2
  exit 2
fi

published_plugin_dirs=()
if [ -d skills ]; then
  while IFS= read -r plugin_dir; do
    [ -n "${plugin_dir}" ] || continue
    plugin_dir="${plugin_dir%/}"
    published_plugin_dirs+=("${plugin_dir}")
  done < <(
    if command -v fd >/dev/null 2>&1; then
      fd --type directory --max-depth 1 . skills | sort
    else
      find skills -mindepth 1 -maxdepth 1 -type d | sort
    fi
  )
fi

if [ -d plugins ]; then
  while IFS= read -r plugin_dir; do
    [ -n "${plugin_dir}" ] || continue
    plugin_dir="${plugin_dir%/}"
    published_plugin_dirs+=("${plugin_dir}")
  done < <(
    if command -v fd >/dev/null 2>&1; then
      fd --type file --glob "plugin.json" plugins | sed 's#/.claude-plugin/plugin\.json$##' | sort
    else
      find plugins -type f -path "*/.claude-plugin/plugin.json" | sed 's#/.claude-plugin/plugin\.json$##' | sort
    fi
  )
fi

repo_failures=0

for plugin_dir in "${published_plugin_dirs[@]}"; do
  manifest_path="${plugin_dir}/.claude-plugin/plugin.json"
  expected_source="./${plugin_dir}"

  if [ ! -f "${manifest_path}" ]; then
    echo "Missing plugin manifest: ${manifest_path}" >&2
    repo_failures=$((repo_failures + 1))
    continue
  fi

  plugin_name="$(jq -r '.name // empty' "${manifest_path}")"
  if [ -z "${plugin_name}" ]; then
    echo "Plugin manifest missing name: ${manifest_path}" >&2
    repo_failures=$((repo_failures + 1))
    continue
  fi

  if ! jq -e --arg source "${expected_source}" '.plugins[] | select(.source == $source)' .claude-plugin/marketplace.json >/dev/null; then
    echo "Marketplace missing plugin source ${expected_source}" >&2
    repo_failures=$((repo_failures + 1))
    continue
  fi

  entry_name="$(
    jq -r --arg source "${expected_source}" '.plugins[] | select(.source == $source) | .name' .claude-plugin/marketplace.json
  )"
  if [ "${entry_name}" != "${plugin_name}" ]; then
    echo "Marketplace name mismatch for ${expected_source}: manifest=${plugin_name} marketplace=${entry_name}" >&2
    repo_failures=$((repo_failures + 1))
  fi
done

while IFS= read -r marketplace_source; do
  [ -n "${marketplace_source}" ] || continue
  source_dir="${marketplace_source#./}"
  if [ ! -d "${source_dir}" ]; then
    echo "Marketplace source does not exist: ${marketplace_source}" >&2
    repo_failures=$((repo_failures + 1))
  fi
done < <(jq -r '.plugins[].source' .claude-plugin/marketplace.json | sort)

if [ "${repo_failures}" -gt 0 ]; then
  echo "Repository distribution validation failed for ${repo_failures} item(s)." >&2
  exit 1
fi

echo "Repository distribution metadata validated successfully."
