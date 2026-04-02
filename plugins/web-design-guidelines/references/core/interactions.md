# Interactions

- MUST support the full core flow with keyboard alone and follow native control patterns or WAI-ARIA patterns where native ones do not exist.
- MUST keep focus visible. Use `:focus-visible` or an equivalent approach, and manage focus explicitly for dialogs, popovers, and similar contained flows.
- SHOULD make visible targets match hit targets. If a control is visually small, expand the interactive area instead of shrinking usability.
- MUST use links for navigation so open-in-new-tab, copy-link, and browser history behavior work naturally.
- NEVER disable browser zoom.
- MUST keep input focus, value, and selection stable through hydration and other state transitions.
- SHOULD keep navigation state in the URL when the state changes tabs, filters, pagination, or any shareable view.
- MUST preserve the original action label while loading; add a spinner or progress cue without removing the text.
- SHOULD avoid loading-state flicker by using a small delay before showing spinners or skeletons and a short minimum display duration once shown.
- SHOULD use an ellipsis for actions or statuses that imply more input or an in-progress state, such as `Rename…` or `Saving…`.
- MUST confirm destructive actions or provide a safe undo path.
- SHOULD announce important async updates through `aria-live` regions when toasts or inline feedback need to be heard.
- SHOULD restore expected scroll positions on Back and Forward navigation.
- SHOULD use optimistic updates when success is likely and reconcile on failure with rollback, error handling, or undo.
- NEVER block paste into text inputs or textareas.
