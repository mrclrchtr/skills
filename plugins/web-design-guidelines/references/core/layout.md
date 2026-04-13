# Layout

## Alignment

- MUST align elements intentionally; optical alignment can matter more than strict geometry.
- SHOULD keep icon/text lockups balanced so the visual center and text baseline feel deliberate.

## Responsive

- SHOULD check narrow mobile widths, standard laptop widths, and ultra-wide displays. For ultra-wide, zoom out to 50% to simulate.
- MUST respect safe areas and viewport insets for notches, system bars, and other cutouts.

## Overflow

- MUST avoid accidental overflow and unnecessary scrollbars.
- SHOULD test with always-visible scrollbars when possible to catch platform-specific overflow issues. On macOS, set "Show scroll bars" to "Always" to test what Windows users would see.
- SHOULD plan for scrollable regions explicitly instead of letting overflow happen by accident.

## Implementation

- SHOULD prefer CSS layout primitives such as grid, flexbox, intrinsic sizing, and wrapping before using JavaScript measurement.
- SHOULD make layout state-aware so empty, dense, collapsed, and error states still read cleanly and do not jump unexpectedly.

## Spacing Rhythm

- SHOULD establish a consistent spacing scale and use it everywhere; ad-hoc values create visual noise.
- SHOULD group related elements tightly and separate unrelated groups with more space.
- SHOULD use vertical padding within rows and vertical margin between rows, not the reverse.
- SHOULD leave more whitespace than feels necessary; cramped layouts read as unfinished.
- SHOULD let content breathe rather than filling every available pixel.
- SHOULD test spacing at different content densities; a layout that works with 3 items should also work with 30.

## Whitespace as Structure

- Whitespace is not empty space; it is a structural element that guides the eye.
- Uneven distribution of whitespace creates hierarchy without adding visual elements.
- When a layout feels cluttered, adding space often works better than removing elements.
