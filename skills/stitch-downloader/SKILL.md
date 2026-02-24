---
name: stitch-downloader
description: "Download Stitch (stitch.withgoogle.com) screen screenshots at best quality from `screenshot.downloadUrl` (often `lh3.googleusercontent.com`). Use to normalize googleusercontent size parameters from canvas dimensions, download with curl, optionally verify pixel dimensions, and avoid committing signed URLs."
---

# Stitch Downloader

## Quick start (googleusercontent)

Use `scripts/download-googleusercontent.sh` to force full-resolution downloads from `lh3.googleusercontent.com` by appending `=w{width}-h{height}`.

```bash
./skills/stitch-downloader/scripts/download-googleusercontent.sh \
  "$SCREENSHOT_URL" \
  2560 \
  2048 \
  "docs/stitch/exports/2026-02-23--p123/wt-01--p123--sabc123--2560x2048.png"
```

- Pass the **canvas** size (not the viewport size). If you don’t know it, fetch screen metadata first.
- The script prints a short SHA256 fingerprint of the URL so you can correlate downloads without saving the signed URL.

## MCP-assisted flow (from ids)

If you have MCP tools for Stitch available, fetch the `screenshot.downloadUrl` and canvas dimensions first, then download.

1) List screens and pick a `screenId`:
- `mcp__stitch__list_screens({ projectId: "<project_id>" })`

2) Fetch metadata for that screen:
- `mcp__stitch__get_screen({ projectId: "<project_id>", screenId: "<screen_id>", name: "projects/<project_id>/screens/<screen_id>" })`

3) Use the returned canvas `width`/`height` with the downloader script.

## Guardrails

- Do not commit signed URLs (including `screenshot.downloadUrl`) to git.
- Commit only the downloaded image file(s) if the user wants them checked in.
