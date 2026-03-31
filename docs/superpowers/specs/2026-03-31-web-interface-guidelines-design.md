# Web Interface Guidelines Design

## Summary

Build a repo-local Codex plugin named `web-interface-guidelines` that packages two focused skills derived from Vercel's web interface guidelines:

- `web-interface-guidelines-apply`
- `web-interface-guidelines-review`

The plugin should help Codex apply the guidelines while building UI and audit existing UI against the same guideline set. The design should borrow packaging discipline from Anthropic's `frontend-design` plugin: keep the plugin wrapper thin and put the real behavior in concise, opinionated skills.

## Goals

- Create one repo-local plugin at `plugins/web-interface-guidelines/`.
- Split the behavior into two skills with distinct trigger conditions.
- Store the Vercel guideline content as reusable reference material instead of bloating each skill.
- Support both generation-time use and review-time use.
- Keep the plugin thin: metadata plus bundled skills and references.

## Non-Goals

- Reproducing the full Vercel repository structure locally.
- Adding a marketplace entry unless explicitly requested later.
- Building a Claude-specific plugin wrapper in this iteration.
- Turning the skill into a generic frontend-design system unrelated to the Vercel guideline corpus.

## Source Inputs

The implementation should learn from two sources:

1. Vercel source of truth
   - `https://github.com/vercel-labs/web-interface-guidelines`
   - Use as the substantive guideline corpus.
2. Anthropic structural reference
   - `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`
   - Use as a packaging reference only.

The Anthropic plugin demonstrates a good pattern:

- lightweight plugin manifest
- concentrated value in skill content
- opinionated, high-signal instructions

The implementation should not copy Claude-specific structures such as `.claude-plugin/` or collapse both use cases into one broad skill.

## User Model

The plugin supports two primary requests:

1. Apply mode
   - User asks Codex to build or modify UI.
   - Codex should use the `apply` skill to make implementation decisions that align with the guideline set.
2. Review mode
   - User asks Codex to review existing UI work.
   - Codex should use the `review` skill to find issues, risks, missing states, and regressions against the same guideline set.

These are different enough that combining them into one skill would reduce trigger precision and produce a larger, less focused `SKILL.md`.

## Plugin Architecture

Create:

- `plugins/web-interface-guidelines/.codex-plugin/plugin.json`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/`

Do not create a marketplace entry by default.

The plugin manifest should remain mostly placeholder-driven except for the normalized plugin name and a sensible minimal description. The skills should contain the actual logic and guidance.

## Skill Boundaries

### `web-interface-guidelines-apply`

Purpose:

- Guide implementation-time UI decisions for new or modified frontend work.

It should cover:

- interaction design choices
- accessibility and semantic HTML defaults
- form behavior
- loading and error states
- motion and layout decisions
- copy and labeling expectations
- responsive and performance-aware implementation choices

It should instruct Codex to:

- read only the relevant reference files for the task
- preserve existing design systems when working in established products
- apply the guidelines pragmatically rather than cargo-culting every item
- explicitly check core states such as empty, loading, dense, error, and destructive flows

### `web-interface-guidelines-review`

Purpose:

- Audit existing UI code or designs against the guideline corpus.

It should cover:

- accessibility findings
- interaction and keyboard gaps
- loading-state mistakes
- form usability defects
- layout and responsiveness risks
- performance hazards
- copy issues and unclear labels

It should instruct Codex to:

- produce findings first, ordered by severity
- cite the violated guideline category
- distinguish bugs and regressions from lower-priority polish issues
- avoid inventing requirements not supported by the guideline set

## Shared References

Both skills should share a compact set of topic-based reference files under the plugin so the skills stay short.

Recommended references:

- `references/interactions.md`
- `references/forms.md`
- `references/content-accessibility.md`
- `references/layout-motion.md`
- `references/performance.md`
- `references/design-copywriting.md`
- `references/source-notes.md`

`source-notes.md` should briefly document:

- the Vercel repository as the substantive source
- the Anthropic plugin as a structural example
- any normalization choices made while adapting the source into local references

The references should paraphrase and organize the guidelines rather than dumping a large raw copy into one file.

## Content Strategy

Use progressive disclosure:

- Keep each `SKILL.md` concise and trigger-focused.
- Move detailed guideline bullets into topic references.
- Link all references directly from each skill so they are discoverable without deep nesting.

The resulting skills should be opinionated but not verbose. The goal is a reusable operating guide, not an archive.

## Validation

Validation should cover:

- skill folder structure
- frontmatter correctness
- generated `agents/openai.yaml` files for both skills
- plugin manifest presence and validity
- `quick_validate.py` for each skill

If helper scripts are introduced, run them directly. No helper scripts are required for v1 unless a deterministic fetch or transformation step becomes necessary during implementation.

## Risks and Mitigations

- Skills become too broad
  - Mitigation: keep apply and review separate.
- References become a raw source dump
  - Mitigation: paraphrase and organize by topic.
- Plugin wrapper adds little value
  - Mitigation: keep it thin and use it only as a package boundary around the skills.
- Review skill turns into generic code review guidance
  - Mitigation: anchor findings to the imported guideline categories.

## Open Decisions Resolved

- Placement: repo-local
- Packaging: one Codex plugin
- Skill count: two skills
- Source strategy: Vercel for substance, Anthropic for structural reference
- Marketplace: not included by default

## Implementation Boundary for the Next Plan

The next implementation plan should cover:

- scaffolding the repo-local plugin
- initializing both skills with `init_skill.py`
- writing the two `SKILL.md` files
- generating `agents/openai.yaml` for both skills
- creating shared topic references
- validating the finished skills and plugin structure
