# Performance

- MUST test on constrained devices and browsers, not just a fast local desktop browser.
- SHOULD profile with CPU and network throttling when interactions depend on rendering or network speed.
- MUST keep input handling cheap and minimize rerenders.
- SHOULD batch layout reads and writes to avoid forced reflow and repaint churn.
- MUST keep mutation round trips such as `POST`, `PATCH`, and `DELETE` feeling fast enough for interactive use.
- MUST virtualize or otherwise contain very large lists.
- MUST reserve layout space for images and media to avoid layout shift.
- SHOULD preload only what is genuinely critical above the fold and lazy-load the rest.
- SHOULD use preconnect or preload for fonts and external origins only when they materially improve first render.
- SHOULD move long-running computation off the main thread when it would block interaction.
