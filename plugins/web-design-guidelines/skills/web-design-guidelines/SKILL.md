---
name: web-design-guidelines
description: Design, implement, and review web interfaces with shared UI guidance. Use whenever creating, redesigning, restyling, building, modifying, or reviewing frontend UI, components, pages, or UI diffs, including requests about design direction, interactions, accessibility, forms, motion, performance, responsive behavior, or interface copy—even when the user does not explicitly ask for web design guidelines.
---

# Web Design Guidelines

Use one shared set of guidelines across design, implementation, and review. Follow only the workflow the request needs; do not turn a focused fix into a redesign or a review into an unsolicited implementation.

## Choose the Mode

- **Design** — Establish or change the visual direction. Return a design proposal; do not change code when the user asks only for a concept or plan.
- **Apply** — Build or modify UI. Use an approved direction or the existing product language. If neither exists, briefly establish a direction before implementation.
- **Review** — Audit existing UI, code, diffs, or specifications. Return findings without editing files unless fixes are also requested.

Infer the mode from the request rather than asking the user to choose a label. For mixed requests, combine only the needed workflows: design then apply for a new interface, or review then apply for an audit with requested fixes. Ask a focused question only when the scope or permission to change files is genuinely unclear.

## Shared Setup

1. Identify the surface, audience, task constraints, and host product conventions. Inspect only the files needed for the task.
2. Check for a project-local design system or style guide before reading the shared references. Look for `DESIGN_SYSTEM.md`, `docs/**/design-system.md`, `docs/**/style-guide.md`, theme files such as `theme.ts` or `theme/index.ts`, and files linked from project instructions such as `CLAUDE.md` or `AGENTS.md`.
3. Read any applicable local guidance first. Explicit project-local design system decisions take precedence on specifics; shared guidance fills gaps. Preserve established product language unless a redesign is requested, and flag accessibility conflicts rather than silently reproducing them.
4. Load only the references that materially affect this task using the map below. Read framework guidance only for the stack in use.

## Design Mode

1. Define the purpose, audience, tone, constraints, and conventions that must remain recognizable.
2. Read `references/design/direction.md` and the relevant design guidance, plus core accessibility and layout constraints that shape the proposal.
3. When choosing a new direction, present two or three viable directions with trade-offs. Do not reopen an already approved direction for a routine implementation task.
4. Recommend one direction, explain why it fits the product goals, and name one memorable differentiator that should survive implementation.
5. Specify enough hierarchy, typography, color, spacing, and interaction intent to guide the build. Keep keyboard support, contrast, reduced motion, and narrow-width behavior viable.

**Output:** A concise design proposal with alternatives, a recommendation, its differentiator, and implementation constraints. Distinctive minimalism is valid; decorative novelty is not a substitute for a coherent direction.

## Apply Mode

1. Start from the approved design direction or existing product conventions. If neither exists, state a reasonable direction from the product context before changing code; use Design mode when a substantial design decision is needed.
2. Read the applicable core, design, and framework references. Treat direction exploration as a design decision, not a prerequisite for every code change.
3. Implement semantics, keyboard interaction, loading and error states, responsive behavior, and performance together rather than as separate cleanup passes.
4. Prefer native elements before ARIA-heavy custom controls. Reuse existing components and tokens. Keep motion purposeful and respect `prefers-reduced-motion`.
5. Check applicable empty, loading, dense, error, destructive, and narrow-width behavior. Run relevant tests and browser checks when available; distinguish verified behavior from checks that could not be run.
6. Confirm the implementation still matches the chosen direction and host product language.

**Output:** The requested code changes, a short summary, verification results, and any remaining gaps. Avoid reciting the guidelines instead of implementing and checking the UI.

## Review Mode

1. Establish the review target and read only the necessary files, diff, or specification and surrounding context.
2. Prioritize `references/core/anti-patterns.md` and the core guidance directly relevant to the surface. Use framework guidance for stack-specific issues and design guidance only when the UI is clearly generic or undirected.
3. Report concrete violations and their user impact, not subjective preferences or hypothetical problems without evidence.
4. Output findings first, grouped by file with `file:line` references. Classify each issue as `bug`, `regression risk`, or `polish`, and give an actionable correction. For specifications, cite the document and distinguish missing requirements from observed implementation defects.
5. If nothing is provably wrong, say so explicitly. Note residual testing gaps, including interactions or visual behavior that source inspection alone cannot verify.

**Output:** Terse, actionable findings followed by testing gaps. Keep review-only requests read-only; do not turn the report into a checklist recital.

## Reference Map

> Resolve all paths below relative to this `SKILL.md` file's directory, not the working directory. Read only the topics needed for the selected mode and surface.

### Core interface behavior

- `references/core/interactions.md` — Keyboard, focus, hover, and press behavior.
- `references/core/forms.md` — Inputs, validation, errors, and submission states.
- `references/core/animation.md` — Transitions and reduced-motion support.
- `references/core/layout.md` — Responsive layout, spacing, and overflow.
- `references/core/mobile.md` — Touch targets, mobile inputs, and viewport behavior.
- `references/core/content-accessibility.md` — Semantics, accessible names, and screen readers.
- `references/core/performance.md` — Loading, rendering, and asset performance.
- `references/core/theming-copy.md` — Themes, tokens, and interface copy conventions.
- `references/core/copywriting.md` — Labels, messages, and actionable errors.
- `references/core/anti-patterns.md` — Concrete mistakes to prioritize during review.

### Visual direction

- `references/design/direction.md` — Direction, alternatives, and trade-offs.
- `references/design/typography-color.md` — Type hierarchy and color systems.
- `references/design/component-hierarchy.md` — Component emphasis and hierarchy.
- `references/design/visual-restraint.md` — Restrained visual treatment.
- `references/design/shadows-depth.md` — Elevation and depth.
- `references/design/motion-composition.md` — Motion as part of the composition.
- `references/design/anti-slop.md` — Avoiding generic, undirected UI.

### Frameworks and provenance

- `references/frameworks/react-next.md` — React and Next.js constraints.
- `references/frameworks/mantine.md` — Mantine components, theming, and Styles API.
- `references/frameworks/tailwind-integration.md` — Component-library and Tailwind integration.
- `references/source-notes.md` — Sources and local adaptation rationale; read when provenance matters.
