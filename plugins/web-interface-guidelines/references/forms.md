# Forms

- Give every control an associated label, even when the visual design hides it.
- Let Enter submit the obvious single-input case. In multi-line textareas, keep Enter for new lines and use modified Enter for submit.
- Keep submit controls enabled until submission starts. During the request, disable repeated submits and show in-flight feedback.
- Do not pre-disable submit just because the form is incomplete. Let the user submit and show actionable validation feedback.
- Do not block typing to enforce strict formats. Accept user input, then validate and explain corrections.
- Place field errors next to the relevant input and move focus to the first error on submit when the form fails.
- Use meaningful `name`, `autocomplete`, `type`, and `inputmode` attributes so browsers and password managers can help instead of fight the form.
- Use placeholders as examples or patterns, not as the only label. Placeholder examples should suggest the expected format.
- Preserve compatibility with password managers and one-time-code flows. Allow pasting OTP values.
- Warn before navigation when unsaved work would be lost.
- Avoid dead zones around radios and checkboxes by making label and control part of one generous target.
- Trim or normalize inconsequential whitespace when input methods add it automatically and would otherwise trigger confusing validation failures.
