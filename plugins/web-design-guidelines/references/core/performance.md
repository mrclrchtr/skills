# Performance

## Testing Environment

- MUST test on constrained devices and browsers, not just a fast local desktop browser.
- SHOULD test on iOS Low Power Mode and macOS Safari specifically.
- SHOULD disable browser extensions when profiling to avoid measurement noise.
- SHOULD profile with CPU and network throttling when interactions depend on rendering or network speed.

## Rendering

- MUST keep input handling cheap and minimize rerenders.
- SHOULD track and minimize re-renders using React DevTools or React Scan.
- SHOULD prefer uncontrolled inputs; make controlled input loops cheap when they are necessary.
- SHOULD batch layout reads and writes to avoid forced reflow and repaint churn.

## Network

- MUST keep mutation round trips such as `POST`, `PATCH`, and `DELETE` under 500ms for interactive use.
- SHOULD use `<link rel="preconnect">` for asset and CDN domains (with `crossorigin` when needed) to reduce DNS/TLS latency.

## Large Content

- MUST virtualize or otherwise contain very large lists (e.g., with `virtua` or `content-visibility: auto`).
- MUST reserve layout space for images and media to avoid layout shift.
- SHOULD preload only what is genuinely critical above the fold and lazy-load the rest.

## Fonts

- SHOULD preload critical fonts to avoid flash of unstyled text and layout shift.
- SHOULD subset fonts using `unicode-range` and limit variable axes to what you actually use.

## Main Thread

- SHOULD move long-running computation to Web Workers when it would block interaction with the page.
