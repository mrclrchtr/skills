---
name: web-interface-guidelines-apply
description: Use when building or modifying frontend UI and implementation choices should follow shared web interface guidelines for interactions, accessibility, forms, motion, performance, responsive behavior, or copy.
---

# Web Interface Guidelines Apply

## Overview

Apply a shared set of web interface standards while implementing or updating UI. Use this skill to guide decisions, not to cargo-cult every bullet.

## Workflow

1. Identify the UI surface you are changing: navigation, form, dialog, list, settings screen, marketing page, dashboard.
2. Read only the relevant shared references under `../../references/`.
3. Implement the change with semantics, keyboard support, loading behavior, error handling, and responsive behavior considered together.
4. Before finishing, check the core states the UI should support: empty, loading, dense, error, destructive, and mobile.

## Reference Map

- `../../references/interactions.md`: focus handling, hit targets, async feedback, URL state, forgiving interactions
- `../../references/forms.md`: labels, submission behavior, validation, autocomplete, placeholders, unsaved changes
- `../../references/content-accessibility.md`: semantics, naming, headings, skip links, resilient content, locale behavior
- `../../references/layout-motion.md`: responsive layout, safe areas, reduced motion, animation constraints, visual polish
- `../../references/performance.md`: render cost, lists, media loading, layout work, latency budgets
- `../../references/design-copywriting.md`: contrast, visual detail, active voice, labels, button text, error copy

## Guardrails

- Prefer native elements before ARIA-heavy custom controls.
- Preserve established design systems and product language when working in an existing product.
- Do not add decorative motion that obscures cause and effect or ignores `prefers-reduced-motion`.
- Keep loading indicators, destructive actions, and form validation explicit.
- If the task conflicts with the host product's existing patterns, follow the product unless the user asks for a redesign.

## Completion Check

Before claiming the work is ready, verify:

- keyboard access and visible focus for any interactive change
- loading and error behavior for async actions
- mobile and narrow-width behavior
- accessible names for icon-only controls and custom UI
- copy labels that tell the user what happens next
