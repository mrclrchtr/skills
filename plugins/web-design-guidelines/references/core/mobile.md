# Mobile

## Touch Targets

- MUST make touch targets at least 44px on mobile devices.
- SHOULD expand targets under 24px to at least 24px on all devices.
- MAY keep visual targets smaller than interactive targets; use padding or pseudo-elements to expand the hit area.
- MUST ensure visual and interactive targets align so users tap what they see.

## Input Sizing

- MUST set input font size to at least 16px on mobile to prevent iOS Safari auto-zoom on focus.
- SHOULD test forms on actual mobile devices; desktop simulation misses zoom and keyboard behavior.

## Focus and Keyboard

- SHOULD avoid autofocus on mobile; the virtual keyboard causes layout shift and can obscure content.
- MUST account for the software keyboard when positioning fixed elements, modals, and action sheets.
- SHOULD test with both iOS and Android keyboards; behavior and sizing differ.

## Safe Areas

- MUST respect device safe areas using CSS `env(safe-area-inset-*)` for notches, home indicators, and rounded corners.
- SHOULD test on devices with notches and dynamic islands, not just rectangular viewports.

## Performance

- SHOULD test on iOS Low Power Mode and mid-range Android devices; flagship performance is not representative.
- SHOULD minimize main-thread work during scroll and touch interactions to avoid jank.
