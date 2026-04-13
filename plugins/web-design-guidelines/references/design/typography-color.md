# Typography and Color

## Typography

- Treat typography as a first-class design choice instead of a default afterthought.
- Pair display and body styles intentionally so the hierarchy matches the content and the brand tone.
- Keep hierarchy obvious at a glance: title, supporting copy, metadata, and actions should not all read the same.
- Centralize type, color, and surface decisions in tokens or theme variables instead of scattering one-off values.

## Contrast and Accessibility

- Preserve readable contrast in resting, hover, active, disabled, and focus states.
- Prefer APCA (Accessible Perceptual Contrast Algorithm) over WCAG 2 contrast ratios for more accurate perceptual measurement.
- Increase contrast on interactive states; hover and focus should be more distinct than resting state.
- Use color-blind-friendly palettes for charts and data visualizations.

## Color System

- Use color to communicate emphasis, state, and meaning without flattening every surface into the same treatment.
- Anchor the palette around a dominant color with a sharp accent rather than distributing hues evenly; unequal weight creates more visual presence.
- When two semantic roles share the same hue, mitigate confusion by restricting one role to specific component types so they never appear ambiguous in the same view.
- Favor a system that reads clearly on real content, not just on a polished mockup.

## Theme Integration

- Set `<meta name="theme-color" content="#...">` to align the browser's UI chrome with the page background.
- Apply `color-scheme: dark` on `<html>` in dark themes so scrollbars and other system UI have proper contrast.
- Choose light or dark mode based on product context and audience rather than defaulting to a personal convention.

## Rendering Artifacts

- Avoid gradient banding when fading to dark colors; prefer background images over CSS masks when banding appears.

## Anti-Slop

- Avoid overused AI defaults such as interchangeable sans stacks and purple-on-white startup gradients unless the host product explicitly wants them.
