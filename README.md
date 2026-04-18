# Agent Skills

Canonical source for:
- `skills.sh` skill installation
- Claude Code Marketplace plugins

One repo is enough for both distribution methods. Splitting into a second marketplace-only repo would duplicate metadata and make drift more likely. The rule in this repo is simple:
- `skills/` contains standalone skills that should also be installable as standalone Claude plugins.
- `plugins/` contains multi-skill Claude plugins with shared commands, agents, hooks, or references; any nested `skills/*/SKILL.md` is intentionally `skills.sh` installable.
- `.agents/skills/` contains local authoring helpers for this repo and is not part of the published catalog.

## Layout

| Path | Purpose | Published through |
| --- | --- | --- |
| `skills/<name>/` | Standalone skill, dual-published | `skills.sh` and Claude Marketplace |
| `plugins/<name>/` | Claude plugin bundle | Claude Marketplace |
| `plugins/<name>/skills/<skill>/` | Specialized skill inside a shared plugin | `skills.sh` |
| `.agents/skills/<name>/` | Local helper skill for contributors | not published |

Repository rules:
- Every directory directly under `skills/` must contain `SKILL.md` and `.claude-plugin/plugin.json`.
- Every published Claude plugin root must be listed in [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json).
- Slash commands belong in `commands/`, not in `skills/`.
- Published plugin roots must be self-contained because Claude Marketplace installs from a cached copy of each plugin.

## Catalog

| Capability | `skills.sh` install | Claude Marketplace install |
| --- | --- | --- |
| agent-orchestrator | `agent-orchestrator` | `agent-orchestrator@mrclrchtr-skills` |
| agent-orchestrator-standalone | `agent-orchestrator-standalone` | `agent-orchestrator-standalone@mrclrchtr-skills` |
| commit | `commit` | `commit@mrclrchtr-skills` |
| review-changes | `review-changes` | `review-changes@mrclrchtr-skills` |
| skill-creator | `skill-creator` | `skill-creator@mrclrchtr-skills` |
| openspec-brainstorm | `openspec-brainstorm` | `openspec-brainstorm@mrclrchtr-skills` |
| stitch-downloader | `stitch-downloader` | `stitch-downloader@mrclrchtr-skills` |
| web-fetch-to-markdown | `web-fetch-to-markdown` | `web-fetch-to-markdown@mrclrchtr-skills` |
| web-design-guidelines | `web-design-guidelines-design`, `web-design-guidelines-apply`, `web-design-guidelines-review` | `web-design-guidelines@mrclrchtr-skills` |
| react-testing-techniques | `react-testing` | `react-testing-techniques@mrclrchtr-skills` |

## Install

### skills.sh

List the installable skills in this repo:

```bash
npx skills add mrclrchtr/skills --list
```

Install a standalone skill:

```bash
npx skills add mrclrchtr/skills --skill commit
npx skills add mrclrchtr/skills --skill review-changes
```

Install a specialized skill from a shared plugin:

```bash
npx skills add mrclrchtr/skills --skill web-design-guidelines-review
npx skills add mrclrchtr/skills --skill react-testing
```

Use `-g` to install globally instead of into the current project:

```bash
npx skills add mrclrchtr/skills --skill web-fetch-to-markdown -g
```

### Claude Code Marketplace

Add the marketplace once:

```bash
/plugin marketplace add mrclrchtr/skills
```

Then install plugins by name:

```bash
/plugin install commit@mrclrchtr-skills
/plugin install web-design-guidelines@mrclrchtr-skills
/plugin install react-testing-techniques@mrclrchtr-skills
```

Heads up: many skill bodies are still written in Codex-flavored language, so Claude Code users may still see `$skill-name` examples or Codex-specific phrasing.

## Use

Once installed, invoke skills by name in your prompt:
- `$agent-orchestrator` — “$agent-orchestrator implement milestone 1”
- `$agent-orchestrator-standalone` — “$agent-orchestrator-standalone implement milestone 1”
- `$commit` — “$commit”
- `$review-changes` — “$review-changes”
- `$skill-creator` — “$skill-creator”
- `$stitch-downloader` — “$stitch-downloader download this Stitch screenshot at 2560x2048”
- `$web-fetch-to-markdown` — “$web-fetch-to-markdown https://example.com/docs/page”
- `$web-design-guidelines-design` — “$web-design-guidelines-design propose a direction for this analytics dashboard before I build it”
- `$web-design-guidelines-apply` — “$web-design-guidelines-apply implement this settings page in our React app”
- `$web-design-guidelines-review` — “$web-design-guidelines-review audit this diff for accessibility and interaction issues”
- `$react-testing` — “$react-testing write tests for this modal”

## Development

Internal build or test sources for shipped runtimes live under `tools/`. For example, [`tools/web-fetch-md`](./tools/web-fetch-md) builds the bundled runtime shipped in [`skills/web-fetch-to-markdown/scripts/fetchmd.js`](./skills/web-fetch-to-markdown/scripts/fetchmd.js).

Validate the published catalog:

```bash
bash scripts/validate-skills.sh
```

Set up local git hooks with `hk` and `mise`:

```bash
mise install
hk install
```

Run hooks manually:

```bash
hk run pre-commit
```

Note: `hk install` manages `.git/hooks/pre-commit` for this clone and replaces previously generated hook scripts.

## References

- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Vercel skills docs](https://skills.sh/docs)
- [Agentskills specification](https://agentskills.io/specification.md)
