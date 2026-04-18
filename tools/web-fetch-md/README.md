# web-fetch-md (internal build source)

Internal TypeScript source for the shipped `skills/web-fetch-to-markdown`
install artifact. This directory is for local development and testing; users
should install and run the skill from `skills/web-fetch-to-markdown`.

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

Requires Node `>=20.19.0`.

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

`pnpm build` does two things:

1. builds `dist/fetchmd.js` for local package usage
2. refreshes the shipped, installable skill runtime at
   `skills/web-fetch-to-markdown/scripts/fetchmd.js` and the matching
   `.agents/skills/web-fetch-to-markdown/scripts/fetchmd.js` launcher

Step 2 writes files outside this directory — expect unstaged changes under
`skills/` and `.agents/` after a successful build.

That bundled `skills/web-fetch-to-markdown/scripts/fetchmd.js` file is the
self-contained artifact used by marketplace / skill installs. It must not
import `tools/web-fetch-md/dist/*` or any other repo-external path.

The bundle is committed and ships with `jsdom` inlined, so it weighs several
megabytes. We accept that cost in exchange for a single-file install that
needs no `node_modules` and no extra build step on the user's machine.

To refresh only the shipped skill runtime and the internal `.agents` launcher:

```bash
pnpm build:skill
```

## Typecheck

```bash
pnpm typecheck
```
