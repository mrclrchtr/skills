# React and Next.js

- Keep hydration-safe rendering in mind for inputs, date-time output, and any text that depends on locale or time zone.
- Use controlled inputs (`value` + `onChange`) when the UI needs source-of-truth state, validation, or derived behavior.
- Use uncontrolled inputs (`defaultValue`) when the field can manage itself and the framework does not need to mirror every keystroke.
- Treat controlled versus uncontrolled as a cost decision; unnecessary control adds rerenders, bookkeeping, and hydration risk.
- Prefer framework routing and URL state for filters, sort order, pagination, and other shareable UI state.
- Use built-in loading primitives, suspense boundaries, and route-level placeholders instead of hand-rolled loading shells when they fit the framework.
- Provide explicit image dimensions or use framework image helpers so layout stays stable.
- Preload fonts and other assets only when the gain is material enough to justify the extra complexity.
- Keep client-only behavior narrow when the initial server render can already express the interface safely.
