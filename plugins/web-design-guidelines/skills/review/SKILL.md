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
- "Review all 3 commits on this branch"
- "Review only the last commit (abc123)"
- "Review uncommitted changes"
- "Review specific files..."

## Step 2: Find Design System Path

Quick glob (don't read):
```
glob: "docs/**/design-system.md"  
glob: "**/DESIGN_SYSTEM.md"
```

## Step 3: Spawn Agent

```yaml
tool: Agent
parameters:
  description: "UI review: [target]"
  subagent_type: "web-design-guidelines:ui-reviewer"
  prompt: |
    Review: [TARGET]
    Design system: [PATH or "none"]
    Context: [RELEVANT SESSION CONTEXT]
```

## Step 4: Return findings to user
