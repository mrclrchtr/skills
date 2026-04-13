---
name: review
description: Delegate UI code reviews to a subagent. Reviews components, pages, git changes, or specification files using web design guidelines.
argument-hint: "[target] - optional file path, directory, commit hash, or 'changes' for git diff"
allowed-tools:
  - Agent
  - Glob
  - AskUserQuestion
---

# Web Design Guidelines Review (Subagent)

## Step 1: Determine Target

**With argument:** Use it directly.

**Without argument:** Determine from session context:
- Clear single target (one commit, one file) → use it
- Ambiguous (multiple commits, unclear scope) → ask user via `AskUserQuestion`

**Ask when unclear.** Example options:
- "All session changes" — all commits made in this conversation
- "Whole feature" — all commits on this branch vs main
- "Last commit only (abc123)"
- "Uncommitted changes"
- "Specific file..."

## Step 2: Find Design System Path

Quick glob (don't read):
```
glob: "docs/**/design-system.md"  
glob: "**/DESIGN_SYSTEM.md"
```

## Step 3: Spawn Agent

**Do NOT gather content yourself.** Just pass identifiers — the agent gets the content.

```yaml
tool: Agent
parameters:
  description: "UI review: [target]"
  subagent_type: "web-design-guidelines:ui-reviewer"
  prompt: |
    Review: [TARGET IDENTIFIER - e.g. "commit abc123", "src/Button.tsx", "uncommitted changes"]
    Design system: [PATH or "none"]
    Context: [BRIEF SESSION CONTEXT - what feature, what spec, focus areas]
```

**Don't:**
- Run `git diff` or `git show`
- Read file contents
- Write diffs to temp files

**Do:**
- Pass commit hash, file path, or "uncommitted changes"
- Pass design system path
- Pass brief context (feature name, spec reference, focus areas)

## Step 4: Return findings to user
