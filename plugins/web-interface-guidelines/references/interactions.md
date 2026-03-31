# Interactions

- Ensure every core flow works with a keyboard and follows native or WAI-ARIA interaction patterns.
- Keep focus visible. Prefer `:focus-visible`, use `:focus-within` for grouped controls, and manage focus explicitly for dialogs, popovers, and other contained flows.
- Match visible targets to hit targets. If a control is visually small, expand the clickable area. Treat mobile targets as larger than desktop targets.
- Keep input behavior stable through hydration. Focus and value should not reset after the page becomes interactive.
- Never block paste into text inputs or textareas.
- Keep the original button label visible while loading. Add a spinner or progress cue without removing the action text.
- Avoid loading-state flicker by using a small delay before showing spinners or skeletons and a short minimum display duration once shown.
- Persist shareable UI state in the URL when the state affects navigation, tabs, filters, pagination, or other user-visible views.
- Use optimistic updates when success is likely. Reconcile on response and provide rollback, error handling, or undo when the action can fail.
- Add an ellipsis character to actions or statuses that imply more input or an in-progress state, such as `Rename…` or `Saving…`.
- Confirm destructive actions or provide a safe undo window.
- Use links for navigation so open-in-new-tab, copy-link, and browser navigation work naturally.
- Announce async updates through accessible live regions when toasts or inline validation are important.
- Restore expected scroll positions on Back and Forward navigation.
- Avoid dead zones. If part of a control looks interactive, it should behave that way.
