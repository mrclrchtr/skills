# Layout

- MUST align elements intentionally; optical alignment can matter more than strict geometry.
- SHOULD keep icon/text lockups balanced so the visual center and text baseline feel deliberate.
- SHOULD check narrow mobile widths, standard laptop widths, and ultra-wide displays.
- MUST respect safe areas and viewport insets for notches, system bars, and other cutouts.
- MUST avoid accidental overflow and unnecessary scrollbars.
- SHOULD test with always-visible scrollbars when possible to catch platform-specific overflow issues.
- SHOULD prefer CSS layout primitives such as grid, flexbox, intrinsic sizing, and wrapping before using JavaScript measurement.
- SHOULD make layout state-aware so empty, dense, collapsed, and error states still read cleanly and do not jump unexpectedly.
- SHOULD plan for scrollable regions explicitly instead of letting overflow happen by accident.
