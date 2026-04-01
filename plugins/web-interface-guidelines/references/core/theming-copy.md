# Theming and Copy

- SHOULD edit component library source files when their defaults conflict with the design system's token scale or conventions, rather than layering theme overrides or wrapper hacks on top.
- MUST set `color-scheme` so form controls and scrollbars match the intended theme.
- SHOULD set `theme-color` metadata to match the current surface.
- MUST check contrast with APCA or other perceptual methods when available, and keep contrast higher on hover, active, and focus states.
- SHOULD keep chart and status colors usable for color-blind users.
- SHOULD use layered shadows, borders, and radii to create depth without muddy edges.
- SHOULD use active voice and specific labels.
- SHOULD keep terminology consistent across a flow.
- SHOULD keep copy concise and remove words that do not help the user act or understand.
- MUST make error copy explain what went wrong and what the user can do next.
- SHOULD use numerals for counts and keep number-unit formatting consistent.
- SHOULD use `and` in prose and labels unless `&` is part of a proper name or a space-constrained design choice.
