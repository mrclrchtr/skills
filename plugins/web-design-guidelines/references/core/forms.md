# Forms

- MUST associate every control with a label, even when the label is visually hidden.
- MUST let Enter submit the obvious single-input case. In textareas, Enter inserts a newline and modified Enter submits.
- MUST keep submit controls enabled until submission starts. Once submitting, prevent repeat submits and show in-flight feedback.
- SHOULD allow submission even when validation will fail; do not pre-disable the action just because the form is incomplete.
- SHOULD validate after input rather than blocking typing to enforce strict formats.
- SHOULD surface field errors next to the relevant input and move focus to the first error on submit.
- SHOULD use `name`, `autocomplete`, `type`, and `inputmode` so browsers and password managers can help.
- SHOULD use placeholders as examples or patterns, not as the only label.
- MUST preserve password manager and one-time-code flows, including paste into OTP fields.
- MUST warn before navigation when unsaved work would be lost.
- SHOULD make checkbox and radio hit targets generous by combining label and control into one large interactive area.
- SHOULD trim or normalize inconsequential whitespace when input methods add it automatically.
