#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo=$(mktemp -d)
trap 'rm -rf "$repo"' EXIT

git -C "$repo" init -q
git -C "$repo" config user.email test@example.com
git -C "$repo" config user.name Test
git -C "$repo" config commit.gpgsign false
mkdir "$repo/hooks"
git -C "$repo" config core.hooksPath hooks
printf 'tracked\n' >"$repo/tracked.txt"
git -C "$repo" add tracked.txt
git -C "$repo" commit -qm initial

printf 'one\ntwo\n' >"$repo/alpha.txt"
mkdir "$repo/nested"
printf 'three\n' >"$repo/nested/beta.txt"
printf '\0\1' >"$repo/data.bin"
printf 'four\n' >"$repo/-"
mkfifo "$repo/pipe"
ln -s pipe "$repo/pipe-link"

output=$(cd "$repo/nested" && "$script_dir/git-info.sh" </dev/null)
jq -e '
  .status.untrackedCount == 5
  and .stats.untracked.files == 5
  and .stats.untracked.insertions == 5
  and .stats.untracked.deletions == 0
  and ([.stats.untracked.byFile[].path] | sort == ["-", "alpha.txt", "data.bin", "nested/beta.txt", "pipe-link"])
' <<<"$output" >/dev/null

echo 'git-info.sh test passed'
