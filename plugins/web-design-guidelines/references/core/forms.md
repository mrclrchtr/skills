# Forms

## Labels and Structure

- MUST associate every control with a label, even when the label is visually hidden.
- MUST ensure clicking a `<label>` focuses its associated control.
- SHOULD make checkbox and radio hit targets generous by combining label and control into one large interactive area.

## Submission

- MUST let Enter submit the obvious single-input case. In textareas, Enter inserts a newline and modified Enter (Cmd/Ctrl+Enter) submits.
- MUST keep submit controls enabled until submission starts. Once submitting, disable the control, show in-flight feedback, and include an idempotency key to prevent duplicate submissions.
- SHOULD allow submission even when validation will fail; do not pre-disable the action just because the form is incomplete.

## Validation and Errors

- SHOULD validate after input rather than blocking typing to enforce strict formats.
- SHOULD surface field errors next to the relevant input and move focus to the first error on submit.

## Input Attributes

- SHOULD use `name`, `autocomplete`, `type`, and `inputmode` so browsers and password managers can help.
- SHOULD disable spellcheck for emails, codes, usernames, and similar non-prose fields.
- SHOULD use placeholders as example values or patterns (e.g., `+1 (123) 456-7890`) and end with an ellipsis to signal emptiness.

## Password Managers and Autofill

- MUST preserve password manager and one-time-code flows, including paste into OTP fields.
- SHOULD avoid triggering password managers on non-authentication fields by using `autocomplete="off"` or specific tokens like `autocomplete="one-time-code"` for OTP fields, and avoiding reserved names like `password`.

## Platform Quirks

- MUST use font size ≥16px for inputs on mobile to prevent iOS Safari from auto-zooming and panning on focus. Alternatively, set `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />`.
- SHOULD explicitly set `background-color` and `color` on native `<select>` elements to avoid dark-mode contrast bugs on Windows.
- SHOULD trim or normalize inconsequential whitespace when input methods add it automatically.

## Data Safety

- MUST warn before navigation when unsaved work would be lost.
