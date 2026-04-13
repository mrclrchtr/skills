# Anti-Patterns

## Accessibility and Semantics

- NEVER disable browser zoom.
- NEVER remove focus outlines without providing a visible replacement.
- NEVER leave icon-only buttons or inputs unlabeled.
- NEVER use buttons for navigation when a link would be the correct control.

## Performance and Implementation

- NEVER use `transition: all`.
- NEVER omit width and height or equivalent dimensions for images and other media that affect layout.
- NEVER render large lists without virtualization or another containment strategy.
- NEVER hard-code locale-sensitive formatting for dates, times, numbers, or currencies.
- NEVER override component library internals with utility classes that bypass the library's own styling API.

## Loading States

- NEVER replace the action text with a loading label that removes what the button does.

## Visual Noise

- NEVER use `backdrop-blur` on content surfaces; it obscures text contrast and conflicts with opaque surface hierarchy.
- NEVER add decorative gradients, watermarks, or ornamental backgrounds to content areas when they carry no meaning.

## Competing Signals

- NEVER use multiple accent colors on the same row (colored border AND colored badge AND colored text).
- NEVER pair a status badge with status-colored text that says the same thing.
- NEVER make section headers louder than the content rows they introduce.
- NEVER use saturated badge colors for non-urgent categorical labels.
- NEVER scatter related metadata across disconnected positions in a row.
- NEVER give every element in a list equal visual weight; hierarchy requires differentiation.
