# Interactions

## Keyboard and Focus

- MUST support the full core flow with keyboard alone and follow native control patterns or WAI-ARIA patterns where native ones do not exist.
- MUST keep focus visible. Use `:focus-visible` or an equivalent approach; set `:focus-within` for grouped controls.
- MUST manage focus with traps for dialogs and modals; move and return focus according to WAI-ARIA patterns.
- SHOULD autofocus the primary input on desktop when there is a single obvious target. Rarely autofocus on mobile because the keyboard opening causes layout shift.
- SHOULD localize keyboard shortcuts for non-QWERTY layouts and show platform-specific modifier symbols.

## Targets and Touch

- SHOULD make visible targets match hit targets. If a control is visually small, expand the interactive area instead of shrinking usability.
- MUST eliminate dead zones: if part of a control looks interactive, it must be interactive.
- SHOULD design forgiving interactions with generous hit targets, clear affordances, and predictable behavior. Use techniques like prediction cones for dropdown menus so diagonal mouse movement toward submenu items does not accidentally close the menu.
- SHOULD set `touch-action: manipulation` on interactive controls to prevent double-tap zoom.
- MAY customize `-webkit-tap-highlight-color` to match the design system.

## Navigation and State

- MUST use links (`<a>` or `<Link>`) for navigation so open-in-new-tab, copy-link, and browser history behavior work naturally.
- SHOULD deep-link everything: filters, tabs, pagination, expanded panels, and any `useState` that affects the view.
- SHOULD restore expected scroll positions on Back and Forward navigation.

## Loading and Feedback

- MUST preserve the original action label while loading; add a spinner or progress cue without removing the text.
- SHOULD avoid loading-state flicker by delaying spinners 150–300ms and showing them for at least 300–500ms once visible.
- SHOULD use an ellipsis for actions or statuses that imply more input or an in-progress state, such as `Rename…` or `Saving…`.
- SHOULD use optimistic updates when success is likely and reconcile on failure with rollback, error handling, or undo.
- SHOULD announce important async updates through `aria-live` regions when toasts or inline feedback need to be heard.

## Destructive and Modal Actions

- MUST confirm destructive actions or provide a safe undo path.
- SHOULD set `overscroll-behavior: contain` on modals and drawers to prevent background scroll.
- SHOULD apply `inert` to background content and disable text selection while dragging to prevent unintended interactions.

## Input Integrity

- NEVER disable browser zoom.
- NEVER block paste into text inputs or textareas.
- MUST keep input focus, value, and selection stable through hydration and other state transitions.

## Tooltips

- SHOULD delay the first tooltip in a group; subsequent peer tooltips appear without delay.
