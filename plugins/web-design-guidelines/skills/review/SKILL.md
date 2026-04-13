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

## Step 1: Find Design System Path (quick glob)

```
glob: "docs/**/design-system.md"
glob: "**/DESIGN_SYSTEM.md"
```

Just get the **path** — don't read it. Pass path to agent.

## Step 2: Spawn Agent Immediately

```yaml
tool: Agent
parameters:
  description: "UI review: [target]"
  subagent_type: "web-design-guidelines:ui-reviewer"
  prompt: |
    Review: [TARGET]
    Design system: [PATH if found, or "none"]
    Context: [ANY ADDITIONAL CONTEXT from conversation, or "none"]
```

**Target examples:**
- No argument or `changes` → `"uncommitted changes (git diff)"`
- `src/Button.tsx` → `"src/Button.tsx"`
- `src/components/` → `"src/components/ directory"`
- `471051c7` → `"commit 471051c7"`
- `docs/spec.md` → `"docs/spec.md (specification)"`

**Context examples:**
- User mentioned focus area → `"focus on form validation"`
- Prior conversation about feature → `"this implements haulage event editing per the spec at openspec/changes/haulage-event-edit/"`
- No extra context → `"none"`

## Step 3: Return findings to user
