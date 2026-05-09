#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: git-info.sh

Emit a JSON snapshot of repository state for commit preparation:
  - repo root and branch
  - staged / unstaged / untracked files
  - staged / unstaged diff stats
  - recent commit subjects

Options:
  --help  Show this message and exit.

Default behavior writes JSON to stdout. Diagnostics go to stderr.
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

repo_root=$(git rev-parse --show-toplevel)
branch=$(git branch --show-current)

parse_status_json() {
  git status --porcelain=v1 -z | jq -Rsc '
    def parse_entries:
      . as $raw
      | ($raw | split("\u0000") | map(select(length > 0))) as $entries
      | reduce range(0; $entries | length) as $i (
          {items: [], skipNext: false};
          if .skipNext then
            .skipNext = false
          else
            ($entries[$i]) as $entry
            | ($entry[0:2]) as $xy
            | ($entry[3:]) as $path
            | if ($xy | test("[RC]")) and ($i + 1 < ($entries | length)) then
                .items += [{
                  path: $path,
                  origPath: $entries[$i + 1],
                  indexStatus: $xy[0:1],
                  worktreeStatus: $xy[1:2]
                }]
                | .skipNext = true
              else
                .items += [{
                  path: $path,
                  indexStatus: $xy[0:1],
                  worktreeStatus: $xy[1:2]
                }]
              end
          end
        )
      | .items;

    parse_entries
  '
}

numstat_json() {
  local mode=${1:-unstaged}
  local cmd=(git diff --numstat)
  if [[ "$mode" == "staged" ]]; then
    cmd=(git diff --cached --numstat)
  fi

  "${cmd[@]}" | jq -Rsc '
    def toint:
      if . == "-" then 0 else tonumber end;

    split("\n")
    | map(select(length > 0) | split("\t")) as $rows
    | {
        files: ($rows | length),
        insertions: (($rows | map(.[0] | toint) | add) // 0),
        deletions: (($rows | map(.[1] | toint) | add) // 0),
        byFile: ($rows | map({
          path: (.[2:] | join("\t")),
          insertions: (.[0] | toint),
          deletions: (.[1] | toint)
        }))
      }
  '
}

recent_commits_json() {
  git log --format='%H%x09%s' --no-decorate -20 | jq -Rsc '
    split("\n")
    | map(select(length > 0) | capture("^(?<hash>[0-9a-f]+)\\t(?<subject>.*)$"))
  '
}

status_entries=$(parse_status_json)
staged_entries=$(jq -c '[.[] | select(.indexStatus != " " and .indexStatus != "?")]' <<<"$status_entries")
unstaged_entries=$(jq -c '[.[] | select(.worktreeStatus != " " and .worktreeStatus != "?")]' <<<"$status_entries")
untracked_entries=$(jq -c '[.[] | select(.indexStatus == "?" and .worktreeStatus == "?")]' <<<"$status_entries")
staged_stats=$(numstat_json staged)
unstaged_stats=$(numstat_json unstaged)
recent_commits=$(recent_commits_json)

jq -n \
  --arg repoRoot "$repo_root" \
  --arg branch "$branch" \
  --argjson staged "$staged_entries" \
  --argjson unstaged "$unstaged_entries" \
  --argjson untracked "$untracked_entries" \
  --argjson stagedStats "$staged_stats" \
  --argjson unstagedStats "$unstaged_stats" \
  --argjson recentCommits "$recent_commits" \
  '{
    repoRoot: $repoRoot,
    branch: $branch,
    status: {
      hasStaged: ($staged | length > 0),
      hasUnstaged: ($unstaged | length > 0),
      hasUntracked: ($untracked | length > 0),
      stagedCount: ($staged | length),
      unstagedCount: ($unstaged | length),
      untrackedCount: ($untracked | length)
    },
    files: {
      staged: $staged,
      unstaged: $unstaged,
      untracked: $untracked
    },
    stats: {
      staged: $stagedStats,
      unstaged: $unstagedStats
    },
    recentCommits: $recentCommits
  }'
