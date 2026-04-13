# Source Notes

## Vercel Source

- Source URL: `https://github.com/vercel-labs/web-interface-guidelines`
- Pinned revision: `3f6b1449dee158479deb8019f6372ff85e663406`
- Role: concrete interface rules, anti-patterns, and review discipline

The `references/core/` files stay close to this source by topic and intent, but they are rewritten into shorter local rules that are easier to apply during implementation and review.

## Vercel Design Website

- Source URL: `https://vercel.com/design/guidelines`
- Date accessed: 2026-04-13
- Role: comprehensive interface guidelines across interactions, animations, layout, content, forms, performance, and design

The public Vercel design guidelines website informed extensive updates across all `references/core/` files:
- `interactions.md`: focus management, touch-action, overscroll-behavior, deep-linking, inert during drag, tooltip timing, locale-aware shortcuts, forgiving interactions with prediction cones
- `animation.md`: input-driven motion, SVG transform wrappers, text anti-aliasing
- `content-accessibility.md`: stable skeletons, scroll-margin-top, translate="no", visual/accessibility separation ("don't ship the schema")
- `forms.md`: spellcheck control, password manager avoidance, Windows select styling, mobile input font size ≥16px, label activation, idempotency keys
- `performance.md`: iOS Low Power Mode testing, React DevTools, 500ms mutation targets, font subsetting
- `copywriting.md`: error message guidance, placeholder formats
- `layout.md`: ultra-wide testing, macOS scrollbar settings
- `typography-color.md`: theme-color meta, color-scheme, accessible charts, gradient banding

## Anthropic Source

- Source URL: `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`
- Pinned revision: `2d5c1bab92971bbdaecdb1767481973215ee7f2d`
- Role: design direction, anti-generic stance, and generation posture

The `references/design/` files preserve that aesthetic-direction guidance in local wording, keeping the opinionated tone without mirroring the upstream plugin structure.

## Local Adaptation Rules

- `references/core/` remains the closest local match to the Vercel source by topic and severity.
- `references/design/` holds the local design-point-of-view guidance and keeps the Anthropic influence focused on art direction rather than implementation mechanics.
- `references/frameworks/react-next.md` holds framework-specific guidance so React and Next.js constraints do not get buried inside the broader core rules.
- `references/frameworks/mantine.md` covers Mantine-specific theming, Styles API, and component conventions.
- `references/frameworks/tailwind-integration.md` covers the mechanics of bridging a component library with Tailwind (CSS variable mapping, dark mode sync, role boundaries).
- The shared references are organized for consumption by the skill files: all three skills point into the relevant reference trees (`core/`, `design/`, `frameworks/`).

## Project-Local Discovery

All three skills include a workflow step that checks the project for a local design system or style guide before reading plugin references. When a project-local document is found, its explicit decisions take precedence over universal plugin guidance on specifics; the plugin guidance fills gaps the project document does not address. This keeps the plugin technology-agnostic at its core while supporting project-specific overrides without forking.

## Packaging

- The plugin is packaged for both Codex and Claude.
- `plugins/web-design-guidelines/.codex-plugin/plugin.json` carries the Codex-facing interface metadata and default prompt list.
- `plugins/web-design-guidelines/.claude-plugin/plugin.json` carries the minimal Claude plugin metadata needed for marketplace discovery.
- The shared `skills/` and `references/` trees remain the single source of truth.

## Intentional Omissions

- No exact mirror of the upstream repository layout is attempted.
