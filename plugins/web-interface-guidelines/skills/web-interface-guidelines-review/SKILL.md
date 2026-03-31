---
name: web-interface-guidelines-review
description: Use when reviewing existing frontend UI, UI code, or design changes for issues in interactions, accessibility, forms, motion, performance, responsive behavior, or copy.
---

# Web Interface Guidelines Review

## Overview

Review UI against the shared web interface guidelines and report concrete findings. Ground criticism in the imported guideline categories instead of generic frontend opinions.

## Review Workflow

1. Identify the relevant surface: interaction flow, form, layout, list, modal, settings page, navigation, or content-heavy page.
2. Read only the matching shared references under `../../references/core/`.
3. Produce findings first, ordered by severity.
4. For each finding, explain the user impact and name the violated guideline category.

## Reference Map

- `../../references/core/interactions.md`: keyboard access, focus, async states, hit targets, URL state, destructive flows
- `../../references/core/forms.md`: labels, validation, submission timing, placeholder usage, field-level errors
- `../../references/core/animation.md`: reduced motion, animation quality, compositor-safe motion, SVG motion
- `../../references/core/layout.md`: responsive layout, safe areas, overflow control, alignment, state-aware structure
- `../../references/core/content-accessibility.md`: semantics, headings, labels, locale handling, content resilience
- `../../references/core/performance.md`: render cost, large lists, layout work, image and font loading
- `../../references/core/theming-copy.md`: contrast, status cues, button labels, error messages, active voice
- `../../references/core/anti-patterns.md`: disabled zoom, `transition: all`, unlabeled controls, loading text regressions

## Findings Format

Each finding should include:

- affected surface or element
- what fails and why it matters
- the relevant guideline category
- whether it is a bug, regression risk, or lower-priority polish issue

If no findings are present, say so explicitly and note residual testing gaps.

## Guardrails

- Do not invent requirements that are not supported by the guideline corpus.
- Distinguish user-facing defects from subjective visual preference.
- Preserve review discipline: findings first, summary second.
- Call out missing states when the code or UI only covers the happy path.
