# web-fetch-md

Fetch a `http(s)` URL and output clean Markdown, preferring:

1. Content negotiation for Markdown (`Accept: text/markdown`)
2. Common sibling `*.md` endpoints
3. HTML extraction via Readability, then Markdown via Turndown

## Run (local)

From this directory:

```bash
pnpm install
pnpm dev -- --help
pnpm dev -- https://example.com > page.md
```

Flags are documented in `--help` (also accepts `-h`). Common ones:

- `--timeout-ms <ms>`
- `--no-abs-links`
- `--debug`

If you don't have `pnpm` installed yet, enable it via Corepack:

```bash
corepack enable
corepack prepare pnpm@latest --activate
```

## Build (local)

```bash
pnpm build
node ./dist/fetchmd.js --help
```

To update the skill entrypoint at `skills/web-fetch-to-markdown/scripts/fetchmd.js`:

```bash
pnpm bundle:skill
```

## Typecheck

```bash
pnpm typecheck
```
