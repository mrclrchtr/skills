---
name: web-interface-guidelines-review
description: Use when reviewing existing frontend UI, UI code, or design changes for issues in interactions, accessibility, forms, motion, performance, responsive behavior, or copy.
---

# Web Interface Guidelines Review

## Overview

Audit UI code or diffs with findings first, high signal, and minimal subjectivity. Stay focused on concrete breakage, not broad aesthetic commentary.

## Review Workflow

1. Read only the files needed to understand the change and its surrounding context.
2. Prioritize `../../references/core/anti-patterns.md` and the core guidance that directly applies to the surface under review.
3. Output findings first, grouped by file and referenced with `file:line`.
4. Classify each issue as `bug`, `regression risk`, or `polish`.
5. If nothing is provably wrong, say so explicitly and note any residual testing gaps.

## Reference Map

- `../../references/core/anti-patterns.md`
- `../../references/core/interactions.md`
- `../../references/core/forms.md`
- `../../references/core/animation.md`
- `../../references/core/layout.md`
- `../../references/core/content-accessibility.md`
- `../../references/core/performance.md`
- `../../references/core/theming-copy.md`
- `../../references/design/anti-slop.md`

## Guardrails

- Prefer concrete violations and anti-patterns over broad aesthetic commentary.
- Use design guidance only when the UI is clearly generic or undirected.
- Keep findings terse and actionable.
- Avoid turning the review into a checklist recital.
