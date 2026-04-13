---
name: review
description: Review UI code, diffs, or specifications against the web design guidelines.
---

# Web Design Guidelines Review Command

Use this command to delegate a UI review to the `ui-reviewer` agent with fresh context.

## Step 1: Determine target

**With an argument:** use it directly.

**Without an argument:** determine the most sensible target from session context.

- Clear single target (one file, one directory, one commit) → use it.
- Ambiguous scope → ask the user which target to review.

When asking, prefer options like:
- all session changes
- whole feature branch
- last commit
- uncommitted changes
- a specific file or directory discussed in the session

## Step 2: Find local design system path

Check whether the project has a local design system or style guide. Look for identifiers such as:
- `docs/**/design-system.md`
- `**/DESIGN_SYSTEM.md`
- `docs/**/style-guide.md`

Pass the path if found; otherwise pass `none`.

## Step 3: Spawn the reviewer agent

Do not gather the diff or file contents yourself unless the command environment requires it. Pass identifiers so the reviewer agent can fetch only what it needs.

Spawn `ui-reviewer` with:
- review target
- design system path
- brief task context

Example prompt payload:

```text
Review: src/components/Button.tsx
Design system: docs/design-system.md
Context: settings page refresh; focus on keyboard interaction and responsive layout
```

## Step 4: Return findings

Return the agent's findings directly to the user. Preserve `file:line` references and issue classification.
