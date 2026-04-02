# Content and Accessibility

- SHOULD prefer inline help over tooltips. Use tooltips only when inline explanation would be excessive.
- MUST keep page titles accurate to the current view and task.
- MUST make next steps explicit in empty, sparse, dense, success, warning, and error states.
- MUST use redundant status cues. Color alone is not enough.
- MUST give icon-only buttons descriptive accessible names.
- MUST use semantic HTML before ARIA: real buttons, links, labels, headings, tables, and lists whenever possible.
- MUST keep heading levels ordered and provide a skip link for main content on full pages.
- MUST hide decorative elements from assistive tech with `aria-hidden="true"` and give meaningful content accessible names.
- MUST make layouts resilient to short, average, and very long user-generated content.
- MUST format dates, times, numbers, currencies, and delimiters according to the user's locale.
- SHOULD prefer explicit language settings over location inference when deciding locale and language behavior.
- SHOULD use non-breaking spaces or other glue characters when units, shortcuts, or product names should stay together.
