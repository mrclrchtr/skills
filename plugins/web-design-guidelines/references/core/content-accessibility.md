# Content and Accessibility

## Help and Navigation

- SHOULD prefer inline help over tooltips. Use tooltips only when inline explanation would be excessive.
- MUST keep page titles accurate to the current view and task.
- MUST make next steps explicit in empty, sparse, dense, success, warning, and error states.
- MUST keep heading levels ordered and provide a skip link for main content on full pages.
- SHOULD set `scroll-margin-top` on section headings so anchor links land below sticky headers.

## Loading States

- MUST make skeleton screens mirror the final content layout exactly to avoid layout shift.

## Status and Feedback

- MUST use redundant status cues. Color alone is not enough.
- MUST give icon-only buttons descriptive accessible names and provide text labels that convey the same meaning.

## Semantic Structure

- MUST use semantic HTML before ARIA: real buttons, links, labels, headings, tables, and lists whenever possible.
- MUST hide decorative elements from assistive tech with `aria-hidden="true"` and give meaningful content accessible names.
- SHOULD separate visual presentation from accessibility: layouts may omit visible labels, but accessible names and labels must still exist for assistive tech. Do not ship the schema to the screen.

## Text and Layout

- MUST make layouts resilient to short, average, and very long user-generated content.
- SHOULD avoid widows and orphans; keep line breaks and rag tidy.
- SHOULD use curly quotes (" ") and the ellipsis character (…) rather than straight quotes and three periods.
- SHOULD apply `font-variant-numeric: tabular-nums` when numbers need to align in columns or comparisons.
- SHOULD use non-breaking spaces or other glue characters when units, shortcuts, or product names should stay together.

## Localization

- MUST format dates, times, numbers, currencies, and delimiters according to the user's locale.
- SHOULD prefer explicit language settings over location inference when deciding locale and language behavior.
- SHOULD wrap brand names, code tokens, and technical identifiers with `translate="no"` so browser auto-translate leaves them intact.
