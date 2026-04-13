---
name: review
description: Delegate UI code reviews to a subagent. Reviews components, pages, git changes, or specification files using web design guidelines.
argument-hint: "[target] - optional file path, directory, or 'changes' for git diff"
allowed-tools:
  - Agent
  - Bash
  - Glob
  - Grep
  - Read
---

# Web Design Guidelines Review (Subagent)

Pre-gather all context, then spawn a minimal agent that only applies the review methodology.

## Step 1: Gather Everything (YOU do this)

### 1a. Determine target
- No argument or `changes`: git diff
- File path: that file
- Directory: files in that directory  
- Spec file: the specification

### 1b. Find and READ design system
```bash
# Search (parallel)
glob: "docs/**/design-system.md"
glob: "**/DESIGN_SYSTEM.md"
glob: "docs/**/style-guide.md"
grep -i "design.system\|style.guide" CLAUDE.md
```
**Read the first match found** — pass its content to the agent.

### 1c. Get content to review
- **Git changes**: `git diff && git diff --staged` — capture full output
- **File**: Read the file
- **Directory**: Glob for UI files, read them
- **Spec**: Read the spec file

## Step 2: Spawn Agent (minimal work)

Pass ALL content inline. The `ui-reviewer` agent auto-loads the review skill.

```yaml
tool: Agent
parameters:
  description: "UI review: [target]"
  subagent_type: "web-design-guidelines:ui-reviewer"
  prompt: |
    ## Project Design System
    [PASTE DESIGN SYSTEM CONTENT HERE, or "None found — use universal guidelines"]
    
    ## Content to Review
    [PASTE DIFF / FILE CONTENT / SPEC CONTENT HERE]
```

## Step 3: Return findings to user
