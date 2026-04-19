# Agent Skills

Reusable skills for agent workflows (Codex / agent-skill loaders).

This repo currently contains:
- `agent-orchestrator`: Coordinate complex work using a phase-gated, multi-agent engineering loop (audit → design → implement → review → validate → deliver).
- `agent-orchestrator-standalone`: Run the same phase-gated workflow without relying on preconfigured agent roles (embeds role cards in the skill).
- `review-changes`: Review code, audit changes, check a PR/commit, or review a design/architecture document; emits findings grouped by severity.
- `skill-creator`: Create a new skill or update an existing skill (created by https://github.com/openai/skills/tree/main/skills/.system/skill-creator)
- `stitch-downloader`: Download Stitch (stitch.withgoogle.com) screenshots at full resolution (normalize `lh3.googleusercontent.com` size params; avoid committing signed URLs).
- `web-fetch-to-markdown`: Fetch http/https pages as clean Markdown by preferring content negotiation, then trying sibling `*.md` endpoints, then extracting HTML via Readability and converting to Markdown.
- `web-design-guidelines` plugin: Specialized design/apply/review UI skills with a shared reference corpus, plus a `/web-design-guidelines:review` command for Claude Code.
- `react-testing-techniques` plugin: Best practices for testing React components with Vitest, React Testing Library, MSW, TanStack Query/Router, and Mantine.

## How `agent-orchestrator` differs from `agent-orchestrator-standalone`

- `agent-orchestrator` assumes your environment already provides named agent roles (e.g. `architect`, `auditor`, `implementer`) and keeps role prompts/models in `./agents/*.toml`.
- `agent-orchestrator-standalone` does not rely on preconfigured roles; it embeds “role cards” in the skill so you can spawn generic sub-agents with consistent behavior.

## Install

### Claude Code Plugin Marketplace

This repository is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces). Install the marketplace and individual plugins:

```bash
# Add the marketplace
/plugin marketplace add mrclrchtr/skills

# Install individual plugins
/plugin install agent-orchestrator@mrclrchtr-skills
/plugin install agent-orchestrator-standalone@mrclrchtr-skills
/plugin install review-changes@mrclrchtr-skills
/plugin install skill-creator@mrclrchtr-skills
/plugin install stitch-downloader@mrclrchtr-skills
/plugin install web-fetch-to-markdown@mrclrchtr-skills
/plugin install web-design-guidelines@mrclrchtr-skills
/plugin install react-testing-techniques@mrclrchtr-skills
```

Heads up: skill bodies and agent-orchestrator role configs are written for OpenAI Codex (e.g. `$skill-name` invocation, TOML role cards). Most skills work in Claude Code, but expect Codex-flavored phrasing and references.

### Codex Local Marketplace

For Codex, the reliable local install pattern is a marketplace entry that points at a local plugin directory.

For a user-global install, add the plugin under `~/.codex/plugins/` and reference it from `~/.agents/plugins/marketplace.json`.

For a repo-local install without committing machine-specific paths:

1. Commit a repo-local marketplace file such as `.agents/plugins/marketplace.json`.
2. Point the plugin source at a relative path like `./.codex/plugins/web-design-guidelines`.
3. Ignore `.codex/plugins/` in the repo's `.gitignore`.
4. On each machine, create a local symlink from `.codex/plugins/web-design-guidelines` to your checkout of this plugin.

Example repo-local marketplace entry:

```json
{
  "name": "my-repo-local",
  "plugins": [
    {
      "name": "web-design-guidelines",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/web-design-guidelines"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Example local symlink:

```bash
mkdir -p .codex/plugins
ln -s /absolute/path/to/skills/plugins/web-design-guidelines \
  .codex/plugins/web-design-guidelines
```

### Vercel Skills CLI

Install one skill at a time via the `skills` CLI from `vercel-labs/skills`:

```bash
# Install from this repo (recommended)
npx skills add mrclrchtr/skills --skill agent-orchestrator
npx skills add mrclrchtr/skills --skill agent-orchestrator-standalone
npx skills add mrclrchtr/skills --skill review-changes
npx skills add mrclrchtr/skills --skill skill-creator
npx skills add mrclrchtr/skills --skill stitch-downloader
npx skills add mrclrchtr/skills --skill web-fetch-to-markdown
npx skills add mrclrchtr/skills --skill web-design-guidelines-design
npx skills add mrclrchtr/skills --skill web-design-guidelines-apply
npx skills add mrclrchtr/skills --skill web-design-guidelines-review
```

Use `-g, --global` to install to your user directory instead of the current project:

```bash
# Install globally (available across projects; not meant to be committed)
npx skills add mrclrchtr/skills --skill agent-orchestrator -g
npx skills add mrclrchtr/skills --skill agent-orchestrator-standalone -g
npx skills add mrclrchtr/skills --skill review-changes -g
npx skills add mrclrchtr/skills --skill skill-creator -g
npx skills add mrclrchtr/skills --skill stitch-downloader -g
npx skills add mrclrchtr/skills --skill web-fetch-to-markdown -g
npx skills add mrclrchtr/skills --skill web-design-guidelines-design -g
npx skills add mrclrchtr/skills --skill web-design-guidelines-apply -g
npx skills add mrclrchtr/skills --skill web-design-guidelines-review -g
```

Tip: install only what you need. Loading everything can dilute context and reduce quality.

## Use

Once installed, invoke skills by name in your prompt:

- `$agent-orchestrator` — “$agent-orchestrator implement milestone 1”
- `$agent-orchestrator-standalone` — “$agent-orchestrator-standalone implement milestone 1”
- `$review-changes` — “$review-changes” (or pass a path / PR number)
- `$skill-creator` — “$skill-creator”
- `$stitch-downloader` — “$stitch-downloader download this Stitch screenshot at 2560x2048”
- `$web-fetch-to-markdown` — “$web-fetch-to-markdown https://example.com/docs/page”
- `$web-design-guidelines-design` — “$web-design-guidelines-design propose a direction for this analytics dashboard before I build it”
- `$web-design-guidelines-apply` — “$web-design-guidelines-apply implement this settings page in our React app”
- `$web-design-guidelines-review` — “$web-design-guidelines-review audit this diff for accessibility and interaction issues”

## More install options

```bash
# List skills available in this repo (no install)
npx skills add mrclrchtr/skills --list

# Install directly from a skill directory path
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/agent-orchestrator
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/review-changes
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/skill-creator
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/web-fetch-to-markdown
npx skills add https://github.com/mrclrchtr/skills/tree/main/plugins/web-design-guidelines/skills/web-design-guidelines-design
npx skills add https://github.com/mrclrchtr/skills/tree/main/plugins/web-design-guidelines/skills/web-design-guidelines-apply
npx skills add https://github.com/mrclrchtr/skills/tree/main/plugins/web-design-guidelines/skills/web-design-guidelines-review

# Install from a local checkout (from this repo root)
npx skills add . --skill agent-orchestrator
npx skills add . --skill review-changes
npx skills add . --skill web-fetch-to-markdown
npx skills add . --skill web-design-guidelines-design
npx skills add . --skill web-design-guidelines-apply
npx skills add . --skill web-design-guidelines-review

# Install from a local checkout globally
npx skills add . --skill web-fetch-to-markdown -g
```

## Development

Installable artifacts live under `skills/`, `plugins/`, and `agents/`.
Internal build/test source for shipped runtimes lives under `tools/` (for example,
`tools/web-fetch-md` builds the bundled runtime shipped in
`skills/web-fetch-to-markdown/scripts/fetchmd.js`).

This repo validates skill metadata with [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref)

Run validation directly:

```bash
bash scripts/validate-skills.sh
```

Set up local git hooks with `hk` + `mise`:

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

- [OpenAI Skill Docs](https://developers.openai.com/codex/skills)
- [OpenAI Codex Multi-Agent](https://developers.openai.com/codex/multi-agent)
- [Claude Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Vercel Labs Skills CLI](https://skills.sh/docs)
- [Agentskills Specification](https://agentskills.io/specification.md)
