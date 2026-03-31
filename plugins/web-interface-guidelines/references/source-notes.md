# Source Notes

## Primary Source

These references are adapted from Vercel's public web interface guidelines:

- `https://github.com/vercel-labs/web-interface-guidelines`
- Pinned revision: `3f6b1449dee158479deb8019f6372ff85e663406`
- Accessed: `2026-03-31`

The local reference files reorganize the source material into topic groupings for Codex skill use. They paraphrase and condense the original guidance instead of mirroring the repository verbatim.

## Structural Reference

Packaging choices were informed by Anthropic's `frontend-design` plugin:

- `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`
- Pinned revision: `2d5c1bab92971bbdaecdb1767481973215ee7f2d`
- Accessed: `2026-03-31`

The useful pattern from that plugin is structural, not substantive:

- thin plugin wrapper
- value concentrated in skill content
- opinionated, triggerable skill descriptions

## Adaptation Notes

- The Vercel guideline set was split into interaction, form, content/accessibility, layout/motion, performance, and design/copywriting references.
- The plugin intentionally uses two skills instead of one: `apply` for implementation-time guidance and `review` for findings-first audits.
- No Claude-specific plugin wrapper was added in this iteration.
