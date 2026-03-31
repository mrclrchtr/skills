# Performance

- Test on constrained devices and browsers, not only a fast local desktop browser.
- Profile with CPU and network throttling when interactions depend on rendering or network speed.
- Minimize rerenders and keep input handling cheap. Controlled inputs are fine only when their update path stays inexpensive.
- Batch layout reads and writes to avoid forced reflow and repaint churn.
- Keep mutation round trips such as `POST`, `PATCH`, and `DELETE` feeling fast enough for interactive use.
- Virtualize or otherwise contain very large lists.
- Reserve layout space for images and media to avoid layout shift.
- Preload only what is genuinely critical above the fold. Lazy-load the rest.
- Preconnect or preload fonts and external origins only when they materially improve first render.
- Move long-running computation off the main thread when it would block interaction.
