# React and Next.js

- MUST keep hydration-safe rendering in mind for inputs, date-time output, and any text that depends on locale or time zone.
- MUST provide explicit image dimensions or use framework image helpers so layout stays stable.
- SHOULD use controlled inputs (`value` + `onChange`) when the UI needs source-of-truth state, validation, or derived behavior.
- SHOULD use uncontrolled inputs (`defaultValue`) when the field can manage itself and the framework does not need to mirror every keystroke.
- SHOULD treat controlled versus uncontrolled as a cost decision; unnecessary control adds rerenders, bookkeeping, and hydration risk.
- SHOULD prefer framework routing and URL state for filters, sort order, pagination, and other shareable UI state.
- SHOULD use built-in loading primitives, suspense boundaries, and route-level placeholders instead of hand-rolled loading shells when they fit the framework.
- SHOULD keep client-only behavior narrow when the initial server render can already express the interface safely.
- SHOULD preload fonts and other assets only when the gain is material enough to justify the extra complexity.
