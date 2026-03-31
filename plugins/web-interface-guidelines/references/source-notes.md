# Source Notes

## Vercel Source

- Source URL: `https://github.com/vercel-labs/web-interface-guidelines`
- Pinned revision: `3f6b1449dee158479deb8019f6372ff85e663406`
- Role: concrete interface rules, anti-patterns, and review discipline

The `references/core/` files stay close to this source by topic and intent, but they are rewritten into shorter local rules that are easier to apply during implementation and review.

## Anthropic Source

- Source URL: `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`
- Pinned revision: `2d5c1bab92971bbdaecdb1767481973215ee7f2d`
- Role: design direction, anti-generic stance, and generation posture

The `references/design/` files preserve that aesthetic-direction guidance in local wording, keeping the opinionated tone without mirroring the upstream plugin structure.

## Local Adaptation Rules

- `references/core/` remains the closest local match to the Vercel source by topic and severity.
- `references/design/` holds the local design-point-of-view guidance and keeps the Anthropic influence focused on art direction rather than implementation mechanics.
- `references/frameworks/react-next.md` holds framework-specific guidance so React and Next.js constraints do not get buried inside the broader core rules.
- Skill files point into these shared references instead of duplicating the corpus in multiple places.

## Intentional Omissions

- No Claude-specific wrapper files were added.
- No marketplace integration is included in this iteration.
- No exact mirror of the upstream repository layout is attempted.
