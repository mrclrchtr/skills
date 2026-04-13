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

Delegate UI review work to a subagent with fresh context. The subagent uses the `web-design-guidelines-review` skill internally, keeping the main conversation clean.

## Workflow

1. Determine the review target from arguments:
   - No argument or `changes`: review uncommitted git changes (`git diff` + `git diff --staged`)
   - File path (e.g., `src/components/Button.tsx`): review that specific file
   - Directory path (e.g., `src/components/`): review files in that directory
   - Specification file (e.g., `spec.md`, `design.md`): review the specification before implementation

2. Spawn an Explore agent with this prompt structure:

```
Review [TARGET] for UI/UX issues using web design guidelines.

Instructions:
1. Check for a project-local design system first (DESIGN_SYSTEM.md, theme files, CLAUDE.md references)
2. Use the web-design-guidelines-review skill - it provides the full review methodology
3. Prioritize anti-patterns and concrete violations over aesthetic opinions
4. Classify issues as: bug, regression risk, or polish
5. For specifications: flag potential implementation pitfalls before code is written

Report findings grouped by file with file:line references.
If nothing is provably wrong, say so explicitly.
```

3. Return the agent's findings to the user.

## Agent Tool Call

```yaml
tool: Agent
parameters:
  description: "UI review with design guidelines"
  subagent_type: "Explore"
  prompt: [constructed prompt with target substituted]
```

## Examples

### Review git changes (default)
```
/web-design-guidelines:review
```
Spawns agent to review uncommitted changes.

### Review specific file
```
/web-design-guidelines:review src/components/Modal.tsx
```
Spawns agent to review that component.

### Review specification
```
/web-design-guidelines:review docs/feature-spec.md
```
Spawns agent to review the spec for potential UI issues before implementation.

### Review directory
```
/web-design-guidelines:review src/pages/
```
Spawns agent to review all UI files in that directory.
