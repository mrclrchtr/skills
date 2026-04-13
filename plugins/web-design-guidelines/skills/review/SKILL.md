---
name: review
description: Delegate UI code reviews to a subagent. Reviews components, pages, git changes, or specification files using web design guidelines.
argument-hint: "[target] - optional file path, directory, commit hash, or 'changes' for git diff"
allowed-tools:
  - Agent
  - Glob
---

# Web Design Guidelines Review (Subagent)

Spawn the `ui-reviewer` agent with minimal context. The agent does the work.

## Step 1: Determine Target + Find Design System

**Target:** Use argument if provided, otherwise determine from session context (what was just implemented, discussed, committed).

**Design system:** Quick glob for path (don't read):
```
glob: "docs/**/design-system.md"
glob: "**/DESIGN_SYSTEM.md"
```

## Step 2: Spawn Agent

```yaml
tool: Agent
parameters:
  description: "UI review: [target]"
  subagent_type: "web-design-guidelines:ui-reviewer"
  prompt: |
    Review: [TARGET]
    Design system: [PATH or "none"]
    Context: [RELEVANT SESSION CONTEXT or "none"]
```

Pass what you know — the agent handles the rest.

## Step 3: Return findings to user
