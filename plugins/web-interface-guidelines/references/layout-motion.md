# Layout and Motion

- Align elements intentionally. Optical alignment sometimes matters more than strict geometry, so small visual adjustments are acceptable when they improve perception.
- Check responsive behavior on narrow mobile widths, standard laptop widths, and very wide displays.
- Respect safe areas and viewport insets for devices with notches or system overlays.
- Avoid accidental overflow and unnecessary scrollbars. Test with always-visible scrollbars when possible to catch Windows-style overflow issues.
- Let CSS handle layout with grid, flexbox, intrinsic sizing, and wrapping before reaching for JavaScript measurement.
- Honor `prefers-reduced-motion` with a reduced or simplified motion path.
- Prefer CSS transitions and animations before JavaScript-driven motion, and keep motion on compositor-friendly properties such as `transform` and `opacity`.
- Animate only when it clarifies cause and effect or adds deliberate polish. Avoid autoplay theatrics.
- Keep motion interruptible by user input.
- Never use `transition: all`; animate only the properties you intend to change.
- Use layered shadows, crisp borders, nested radii, and hue-consistent accents to improve interface depth without muddying edges.
- Increase contrast on hover, active, and focus states rather than decreasing it.
