---
name: commit
description: "Creates a commit: detects conventions, stages intentionally, writes a clear subject, add a concise body when useful, and commits."
---

# Git Commit

## Goal

Make a logical, reviewable concise commit using the commit style of the repository.

## Available scripts

- **`scripts/git-info.sh`** — Emits a JSON snapshot of repository state for commit preparation.

## Guardrails

- If potential secrets are found: **STOP and ask** what to do.
- No `--no-verify`, no `--amend`/rebase/force-push, no pushing unless asked.
- Ask the user **only** if one of these is true:
  - Changes appear to span multiple logical commits
  - Potential secrets are present
  - Recent commit subjects do not make the repo's commit style clear
  - The staged diff does not match the intended commit
- Do **not** run `bash scripts/git-info.sh --help` during normal flow. Use `--help` only if the script fails or you are editing the script itself.

## Fast workflow

1) Gather information

    ```bash
    bash scripts/git-info.sh
    ```

   Read the JSON snapshot first. Use it to inspect:
   - `repoRoot`, `branch`
   - `status.hasStaged`, `status.hasUnstaged`, `status.hasUntracked`
   - `files.staged`, `files.unstaged`, `files.untracked`
   - `stats.staged`, `stats.unstaged`
   - `recentCommits`

   If ambiguity remains after the JSON snapshot, inspect only the needed files with normal git commands:

   ```bash
   git diff -- path/to/file
   git diff --cached -- path/to/file
   git diff --stat
   git diff --cached --stat
   git status --short
   git log --oneline -20
   ```

2) Stage changes intentionally

   ```bash
   git add path/to/file1 path/to/file2
   # or:
   git add -A # when all changes belong to the commit to create
   ```

   Verify the staged set before committing:

   ```bash
   git diff --cached --stat
   git diff --cached
   ```

   If the staged diff contains unrelated changes, **STOP and ask** what to do.

3) Write a concise commit message

   Infer commit style from recent subjects:
    - If they look like `type(scope): msg` → use Conventional Commits.
    - Otherwise, match the common pattern (caps, prefixes, ticket IDs, etc.).

   Subject rules:
    - Imperative mood, no trailing period
    - Prefer ≤ 72 chars (or match repo norm)
    - Include scope only if the repo typically does

   Body rules:
    - Add a body **only** if it answers "why" or prevents confusion:
        - Why this change is needed
        - Key tradeoffs or constraints
        - Notable side effects/follow-ups

4) Commit and verify
   Use multiple `-m` flags for multi-line messages (no \n).

   ```bash
   git commit -m "type(scope): concise summary"
   # or with body:
   git commit -m "type(scope): concise summary" -m "Why this change was needed (brief)."
   ```
