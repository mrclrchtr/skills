---
name: web-fetch-md
description: Fetch http/https pages as clean Markdown suitable for LLM ingestion. Prefer negotiated Markdown via Accept headers, then try common sibling *.md endpoints, and finally fall back to HTML → Readability → Markdown (Turndown). Use when a prompt includes a URL and you need the page content in Markdown to summarize, quote, diff, or store.
---

# Web Fetch Markdown

## Default workflow

Fetch a URL and print Markdown to stdout:

```bash
bash skills/web-fetch-md/scripts/fetchmd "<url>" > page.md
```

Write directly to a file:

```bash
bash skills/web-fetch-md/scripts/fetchmd "<url>" page.md
```

## Notes

- Fetch order: negotiated Markdown → sibling `*.md` → HTML extraction.
- Source lives in `src/web-fetch-md/`; `npm --prefix src/web-fetch-md run -s build` regenerates `skills/web-fetch-md/scripts/fetchmd.js`.
- For JS-rendered pages (HTML contains mostly placeholders), use a browser-based tool to capture rendered HTML first, then convert.
