# web-fetch-md

Fetch a `http(s)` URL and output clean Markdown, preferring:

1. Content negotiation for Markdown (`Accept: text/markdown`)
2. Common sibling `*.md` endpoints
3. HTML extraction via Readability, then Markdown via Turndown

## Run (local)

From this directory:

```bash
npm install
npm run -s dev -- --help
npm run -s dev -- https://example.com > page.md
```

Flags are documented in `--help` (also accepts `-h`). Common ones:

- `--timeout-ms <ms>`
- `--no-abs-links`
- `--debug`

If `npm install` fails due to a broken global npm cache, run it with an isolated cache:

```bash
npm_config_cache="${TMPDIR:-/tmp}/npm-cache" npm install
```

## Build (local)

```bash
npm run -s build
node ./dist/fetchmd.js --help
```

`npm run build` also updates the skill entrypoint at `skills/web-fetch-md/scripts/fetchmd.js`.

## Typecheck

```bash
npm run -s typecheck
```
