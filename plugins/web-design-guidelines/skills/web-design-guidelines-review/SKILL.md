---
name: web-design-guidelines-review
description: Use when reviewing existing frontend UI, UI code, or design changes for issues in interactions, accessibility, forms, motion, performance, responsive behavior, or copy.
---

# Web Design Guidelines Review

## Overview

Audit UI code or diffs with findings first, high signal, and minimal subjectivity. Stay focused on concrete breakage, not broad aesthetic commentary.

## Review Workflow

1. Read only the files needed to understand the change and its surrounding context.
2. Check the project for a local design system or style guide. Look for files such as `docs/**/design-system.md`, `DESIGN_SYSTEM.md`, `docs/**/style-guide.md`, theme files (`theme.ts`, `theme/index.ts`), or any file referenced in the project's `CLAUDE.md` as the design system. If found, read it first — its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps.
3. Prioritize `references/core/anti-patterns.md` and the core guidance that directly apply to the surface under review.
4. Output findings first, grouped by file and referenced with `file:line`.
5. Classify each issue as `bug`, `regression risk`, or `polish`.
6. If nothing is provably wrong, say so explicitly and note any residual testing gaps.

## Reference Map

- `references/core/anti-patterns.md`
- `references/core/interactions.md`
- `references/core/forms.md`
- `references/core/animation.md`
- `references/core/layout.md`
- `references/core/content-accessibility.md`
- `references/core/performance.md`
- `references/core/theming-copy.md`
- `references/design/anti-slop.md`
- `references/frameworks/react-next.md`
- `references/frameworks/mantine.md`
- `references/frameworks/tailwind-integration.md`

## Guardrails

- Prefer concrete violations and anti-patterns over broad aesthetic commentary.
- Use design guidance only when the UI is clearly generic or undirected.
- Keep findings terse and actionable.
- Avoid turning the review into a checklist recital.
- When a project-local design system is present, its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps.
