# Anti-Patterns

- NEVER disable browser zoom.
- NEVER use `transition: all`.
- NEVER remove focus outlines without providing a visible replacement.
- NEVER leave icon-only buttons or inputs unlabeled.
- NEVER use buttons for navigation when a link would be the correct control.
- NEVER omit width and height or equivalent dimensions for images and other media that affect layout.
- NEVER render large lists without virtualization or another containment strategy.
- NEVER hard-code locale-sensitive formatting for dates, times, numbers, or currencies.
- NEVER replace the action text with a loading label that removes what the button does.
- NEVER override component library internals with utility classes that bypass the library's own styling API.
- NEVER use `backdrop-blur` on content surfaces; it obscures text contrast and conflicts with opaque surface hierarchy.
- NEVER add decorative gradients, watermarks, or ornamental backgrounds to content areas when they carry no meaning.
