---
name: git-commit
description: "Create safe, repo-convention git commits by inspecting `git status` and diffs, staging logical changes, and generating high-quality Conventional Commit messages. Use when the user asks to commit changes, stage and commit, write/improve a commit message, create a Conventional Commit (`type(scope): summary`), or mentions `/commit`."
---

# Git Commit

## Overview

Commit changes safely and consistently: check what changed, stage the right files, craft a Conventional Commit message that explains the user-facing why, and run the repo’s normal checks/hooks.

## When to Commit

- Commit after completing one logical, reviewable change (avoid mixing unrelated refactors, formatting, and behavior changes).
- Commit once the repo’s normal checks/hooks pass (or after you’ve fixed failures).
- Avoid “WIP” commits unless the user explicitly wants a checkpoint commit (and label it clearly).

## Workflow

### 1) Inspect repo state

Run these first (do not assume anything is staged):

```bash
git branch --show-current
git status --porcelain=v1
git --no-pager diff
git --no-pager diff --staged
git --no-pager log --oneline -20 --graph
```

### 2) Do quick safety checks

Before committing, scan for obvious problems:

```bash
# Obvious credential/private key patterns (best-effort; hooks/scanners still apply)
rg -n "(AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key\\s*=|secret\\s*=|password\\s*=)" -S .
```

If anything looks like a secret, stop and ask the user what to do (usually: remove from git history + rotate).

### 3) Stage changes intentionally

Goal: one logical change per commit.

Prefer:

```bash
# Stage specific paths (safe default)
git add path/to/file1 path/to/file2

# Interactive staging when changes are mixed
git add -p
```

Avoid `git add -A` unless you’ve confirmed everything in the working tree belongs in the commit.

### 4) Choose the commit message format

Default to Conventional Commits if the repo already uses them (check `git log --oneline`).
If the repo instead uses a simple `prefix: summary` convention (for example `tui: ...`, `core: ...`, `wip: ...`), match the repo’s existing style rather than forcing Conventional Commits.

Format:

```text
<type>(<scope>): <summary>
```

Types (common): `feat`, `fix`, `docs`, `refactor`, `test`, `perf`, `build`, `ci`, `chore`, `style`, `revert`.

Pick a `scope` that matches the main area changed (package/module/directory). Omit scope if it would be guessy.

Summary rules:
- Imperative, present tense (“add”, “fix”, “remove”)
- Describe user impact and intent (the “why”), not vague internalities
- Keep it short (aim <72 chars)

### 5) Commit (and report what happened)

Commit staged changes:

```bash
git commit -m "type(scope): summary"
```

After committing:

```bash
git --no-pager show --stat
```

## Guardrails

- Never bypass hooks with `--no-verify` unless the user explicitly asks.
- Never run destructive history edits (`--amend`, interactive rebase, force push) unless explicitly requested.
- If checks fail, fix the issue and re-run the normal workflow; ask if you’re unsure whether to amend vs make a follow-up commit.
