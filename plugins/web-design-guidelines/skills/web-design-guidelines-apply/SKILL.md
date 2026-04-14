---
name: web-design-guidelines-apply
description: Use when building or modifying frontend UI and implementation choices should follow shared web interface guidelines for interactions, accessibility, forms, motion, performance, responsive behavior, or copy.
---

# Web Design Guidelines Apply

## Overview

Implement or update UI while preserving the intended design direction and shared standards. Use this skill to keep the build aligned with the chosen interface instead of drifting toward generic defaults.

## Workflow

1. Start from an approved design direction; if none exists, infer one explicitly from the product context before changing code.
2. Check the project for a local design system or style guide. Look for files such as `docs/**/design-system.md`, `DESIGN_SYSTEM.md`, `docs/**/style-guide.md`, theme files (`theme.ts`, `theme/index.ts`), or any file referenced in the project's `CLAUDE.md` as the design system. If found, read it first — its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps.
3. Read the relevant files under `references/core/`, `references/design/`, and `references/frameworks/` that materially affect the surface you are building.
4. Implement semantics, keyboard interaction, loading states, error states, responsive behavior, and performance together rather than as separate cleanup passes.
5. Before finishing, check empty, loading, dense, error, destructive, and narrow-width behavior.
6. Confirm the implementation still matches the chosen design direction and the host product language.

## Reference Map

- `references/core/interactions.md`
- `references/core/forms.md`
- `references/core/animation.md`
- `references/core/layout.md`
- `references/core/content-accessibility.md`
- `references/core/performance.md`
- `references/core/theming-copy.md`
- `references/core/anti-patterns.md`
- `references/design/direction.md`
- `references/design/typography-color.md`
- `references/design/motion-composition.md`
- `references/design/anti-slop.md`
- `references/frameworks/react-next.md`
- `references/frameworks/mantine.md`
- `references/frameworks/tailwind-integration.md`

## Guardrails

- Prefer native elements before ARIA-heavy custom controls.
- Preserve product language and system conventions when working in an existing interface.
- Do not add decorative motion that fights the interaction model or ignores `prefers-reduced-motion`.
- Avoid checklist recital; implement the states, then verify them in context.
- When a project-local design system is present, its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps.
