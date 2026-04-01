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
- The shared references are organized for consumption by the skill files: `apply` and `review` already point into `references/core/`, while the design and framework docs are prepared for the next skill rewrites.

## Packaging

- The plugin is packaged for both Codex and Claude.
- `plugins/web-interface-guidelines/.codex-plugin/plugin.json` carries the Codex-facing interface metadata and default prompt list.
- `plugins/web-interface-guidelines/.claude-plugin/plugin.json` carries the minimal Claude plugin metadata needed for marketplace discovery.
- The shared `skills/` and `references/` trees remain the single source of truth.

## Intentional Omissions

- No exact mirror of the upstream repository layout is attempted.
