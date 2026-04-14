---
name: web-design-guidelines-design
description: Use when creating, redesigning, or restyling a UI and Codex should establish a clear design direction before implementation.
---

# Web Design Guidelines Design

## Overview

Use this skill to establish a strong design direction before implementation and prevent generic output. It is for moments when the interface needs a deliberate point of view, not a default UI blend.

## Workflow

1. Identify the UI surface, the intended audience, the constraints, and the host product conventions that must stay recognizable.
2. Check the project for a local design system or style guide. Look for files such as `docs/**/design-system.md`, `DESIGN_SYSTEM.md`, `docs/**/style-guide.md`, theme files (`theme.ts`, `theme/index.ts`), or any file referenced in the project's `CLAUDE.md` as the design system. If found, read it first — its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps.
3. Read the relevant files under `references/design/` and only the core constraints that materially shape the direction.
4. Present two or three viable directions with trade-offs so the options are explicit, not implicit.
5. Recommend one direction, commit to it, and explain why it best fits the product goals and constraints.
6. Name one memorable differentiator that should still be visible after implementation.

## Reference Map

- `references/design/direction.md`
- `references/design/typography-color.md`
- `references/design/motion-composition.md`
- `references/design/anti-slop.md`
- `references/core/layout.md`
- `references/core/content-accessibility.md`

## Guardrails

- Preserve established product systems unless the task explicitly asks for a stronger redesign.
- Distinctive minimalism is acceptable; generic output is not.
- Keep the chosen direction compatible with accessibility, responsiveness, and interactions.
- Do not trade away keyboard support, contrast, or narrow-width behavior for style.
- When a project-local design system is present, its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps.
