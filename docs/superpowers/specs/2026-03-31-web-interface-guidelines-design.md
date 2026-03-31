# Web Interface Guidelines Design

## Summary

Redesign the repo-local `web-interface-guidelines` plugin so it combines the best parts of Anthropic's `frontend-design` plugin and Vercel's `web-interface-guidelines` repository without collapsing them into one vague skill.

The resulting plugin should expose three distinct skills backed by one shared reference corpus:

- `web-interface-guidelines-design`
- `web-interface-guidelines-apply`
- `web-interface-guidelines-review`

This is a deliberate shift away from the current two-skill, condensed-guidance model. The new design keeps the plugin balanced across design direction, implementation guidance, and review rigor.

## Goals

- Preserve a thin repo-local plugin wrapper at `plugins/web-interface-guidelines/`.
- Split design, implementation, and review into separate skills with explicit contracts.
- Keep a shared reference corpus that is close to source and only lightly adapted.
- Maintain a framework-agnostic core with optional React/Next.js add-ons.
- Use Anthropic-derived guidance for design direction and anti-generic frontend quality.
- Use Vercel-derived guidance for concrete interface rules and review discipline.
- Make the review skill operationally strict enough for real code review, not just general frontend commentary.

## Non-Goals

- Reproducing the upstream repositories exactly.
- Adding marketplace metadata unless requested later.
- Building Claude-specific wrapper files such as `.claude-plugin/`.
- Turning the plugin into a general-purpose design system unrelated to the two source inputs.
- Baking React/Next.js assumptions into the framework-agnostic core references.

## Source Inputs

The plugin should synthesize two upstream sources with different roles:

1. Vercel source of truth
   - `https://github.com/vercel-labs/web-interface-guidelines`
   - Primary source for concrete interface rules, anti-patterns, and review criteria.
2. Anthropic source of truth
   - `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`
   - Primary source for design-direction behavior, anti-generic aesthetic guidance, and skill-level generation posture.

The design should no longer treat Anthropic as structure-only. That was the main gap in the current plugin. Instead:

- Anthropic contributes creative direction and taste for `design` and `apply`.
- Vercel contributes operational UI rules and strict review guidance for `apply` and `review`.

## User Model

The plugin supports three distinct user intents:

1. Design mode
   - User wants to create, redesign, restyle, or meaningfully evolve a UI.
   - Codex should establish a clear design direction before code is written.
2. Apply mode
   - User wants to build or modify UI code.
   - Codex should implement against the shared standards while preserving the chosen direction.
3. Review mode
   - User wants an audit of existing UI code or a diff.
   - Codex should report concrete findings with minimal subjectivity.

These intents are close enough to share references but different enough to justify separate skills.

## Plugin Architecture

The plugin should remain thin and repo-local:

- `plugins/web-interface-guidelines/.codex-plugin/plugin.json`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/`
- `plugins/web-interface-guidelines/references/`

The manifest should advertise design, implementation, and review explicitly. The logic should remain concentrated in the skills and shared references.

## Skill Contracts

### `web-interface-guidelines-design`

Purpose:

- Establish a strong, explicit design direction for UI work before implementation.

Required behavior:

- Identify purpose, audience, constraints, and desired tone.
- Present two or three viable design directions with trade-offs.
- Recommend one direction and commit to it.
- Name one memorable differentiator that prevents the interface from feeling generic.
- Reject generic defaults such as interchangeable SaaS layouts, timid palettes, and overused font choices unless the host product already uses them intentionally.
- Preserve established product conventions when the task is inside an existing design system unless the user asks for a stronger redesign.

Primary source emphasis:

- Anthropic-derived design guidance
- Selected Vercel-derived constraints where accessibility, responsiveness, or interaction rules materially shape the design

### `web-interface-guidelines-apply`

Purpose:

- Implement or modify UI code in a way that preserves the chosen direction while meeting the shared interface standards.

Required behavior:

- Start from an approved direction when one exists; otherwise infer a clear direction and proceed explicitly.
- Read only the relevant shared references for the current surface.
- Enforce semantics, keyboard support, loading states, error behavior, responsive behavior, and performance-sensitive choices together rather than as isolated checks.
- Handle core states such as empty, loading, dense, error, destructive, and mobile/narrow-width behavior.
- Avoid generic UI output and avoid turning the response into a checklist recital.

Primary source emphasis:

- Anthropic-derived design direction
- Vercel-derived implementation rules

### `web-interface-guidelines-review`

Purpose:

- Audit UI code or diffs against the shared guideline corpus with high signal and low subjectivity.

Required behavior:

- Output findings first, grouped by file, using `file:line` formatting.
- Prefer concrete violations and anti-patterns over broad aesthetic commentary.
- Classify issues as bug, regression risk, or polish.
- Use design-direction guidance only when there is a clear generic or undirected-design problem, not as permission for arbitrary stylistic critique.
- If no issues are provable, say so explicitly and then note residual testing gaps or unverified states.

Primary source emphasis:

- Vercel-derived review command style and anti-patterns
- Limited Anthropic-derived design critique where clearly applicable

## Shared Reference Corpus

Replace the current flattened, condensed reference set with a closer-to-source hierarchy:

- `references/core/`
- `references/design/`
- `references/frameworks/`
- `references/source-notes.md`

### `references/core/`

Framework-agnostic rules, lightly adapted from Vercel and kept detailed enough to be operational.

Recommended files:

- `interactions.md`
- `forms.md`
- `animation.md`
- `layout.md`
- `content-accessibility.md`
- `performance.md`
- `theming-copy.md`
- `anti-patterns.md`

These files should preserve concrete rule granularity where it affects behavior, for example:

- keyboard and focus handling
- hit targets and touch behavior
- loading and destructive action rules
- URL-backed state
- reduced motion
- explicit animation anti-patterns
- safe areas and overflow handling
- headings, labels, and locale-sensitive formatting
- content resilience and empty states
- image, font, and list performance rules
- reviewable anti-patterns such as `transition: all`, disabled zoom, unlabeled controls, and non-semantic click targets

### `references/design/`

Anthropic-derived design-direction and anti-generic guidance.

Recommended files:

- `direction.md`
- `typography-color.md`
- `motion-composition.md`
- `anti-slop.md`

These files should preserve the strong design stance that is currently missing:

- commit to a clear aesthetic direction
- make typography a first-class choice
- use color and motion intentionally
- avoid generic AI-generated frontend patterns
- scale implementation complexity to the design vision

### `references/frameworks/react-next.md`

Optional framework-specific add-on guidance for React and Next.js only.

This file should cover framework-specific concerns that do not belong in the core, such as:

- hydration-safe inputs
- `value` and `onChange` expectations
- controlled vs uncontrolled input cost
- URL state in React/Next patterns
- Suspense or loading-state considerations where relevant
- image and font behavior that differs meaningfully in React/Next stacks

## Source Notes

`references/source-notes.md` should be rewritten to document provenance and adaptation discipline explicitly:

- which files are primarily Vercel-derived
- which files are primarily Anthropic-derived
- what was copied closely
- what was lightly adapted
- what was intentionally omitted and why

The purpose is auditability. A future maintainer should be able to tell whether the plugin is still aligned with upstream intent.

## Content Strategy

Use progressive disclosure without over-condensing:

- Keep each `SKILL.md` short and trigger-focused.
- Keep the detailed rules in shared references.
- Keep the references close enough to source that concrete guidance is not lost.
- Reorganize material only when it improves retrieval and skill ergonomics.

The plugin should not flatten strong rules into generic advice. "Lightly adapted" means rearranged and trimmed for local use, not reduced to broad summaries.

## Validation

Validation should cover:

- skill folder structure for all three skills
- frontmatter correctness
- generated `agents/openai.yaml` for each skill
- plugin manifest presence and metadata correctness
- `quick_validate.py` or equivalent local validation for all skills
- spot-checking that the skills point to the new reference layout

No automated fetch pipeline is required for v1 unless the implementation introduces one deliberately.

## Risks and Mitigations

- Three skills drift apart
  - Mitigation: shared references remain the single source of truth.
- Review becomes too stylistic
  - Mitigation: require concrete `file:line` findings and anti-pattern checks.
- Design becomes disconnected from implementation reality
  - Mitigation: `apply` must read both design and core references.
- Core references become too condensed again
  - Mitigation: preserve close-to-source rule granularity and document adaptation choices.
- React/Next guidance leaks into generic guidance
  - Mitigation: keep framework specifics in `references/frameworks/react-next.md` only.

## Success Criteria

The redesign is successful when:

- `web-interface-guidelines-design` reliably produces a distinct, non-generic design direction before UI implementation.
- `web-interface-guidelines-apply` can use that direction while still enforcing accessibility, interaction, performance, and responsive standards.
- `web-interface-guidelines-review` produces terse, actionable, `file:line` findings rather than general frontend opinions.
- The framework-agnostic core remains usable outside React/Next codebases.
- The React/Next add-on is clearly optional and additive.
- `source-notes.md` makes provenance and adaptation choices auditable.

## Open Decisions Resolved

- Placement: repo-local plugin
- Skill count: three skills
- Balance: equal emphasis on design, apply, and review
- Source strategy: close to source, lightly adapted
- Core strategy: framework-agnostic with React/Next add-ons
- Marketplace entry: not included by default

## Implementation Boundary for the Next Plan

The next implementation plan should cover:

- restructuring the plugin around three skills
- rewriting `plugin.json` and skill metadata for the new model
- replacing the current condensed references with the new `core/`, `design/`, and `frameworks/` hierarchy
- rewriting the three `SKILL.md` files to match the approved contracts
- validating the finished plugin structure and skill metadata
