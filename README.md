# Agent Skills

Reusable skills for agent workflows (Codex / agent-skill loaders).

This repo currently contains:
- `agent-orchestrator`: Coordinate complex work using a phase-gated, multi-agent engineering loop (audit → design → implement → review → validate → deliver).
- `agent-orchestrator-standalone`: Run the same phase-gated workflow without relying on preconfigured agent roles (embeds role cards in the skill).
- `git-commit`: Create safe, repo-convention commits by inspecting diffs, staging intentionally, and writing high-quality commit messages (prefer Conventional Commits when the repo uses them).
- `skill-creator`: Create a new skill or update an existing skill (created by https://github.com/openai/skills/tree/main/skills/.system/skill-creator)
- `stitch-downloader`: Download Stitch (stitch.withgoogle.com) screenshots at full resolution (normalize `lh3.googleusercontent.com` size params; avoid committing signed URLs).
- `web-fetch-to-markdown`: Fetch http/https pages as clean Markdown by preferring content negotiation, then trying sibling `*.md` endpoints, then extracting HTML via Readability and converting to Markdown.

## How `agent-orchestrator` differs from `agent-orchestrator-standalone`

- `agent-orchestrator` assumes your environment already provides named agent roles (e.g. `architect`, `auditor`, `implementer`) and keeps role prompts/models in `./agents/*.toml`.
- `agent-orchestrator-standalone` does not rely on preconfigured roles; it embeds “role cards” in the skill so you can spawn generic sub-agents with consistent behavior.

## Install

Install one skill at a time via the `skills` CLI from `vercel-labs/skills`:

```bash
# Install from this repo (recommended)
npx skills add mrclrchtr/skills --skill agent-orchestrator
npx skills add mrclrchtr/skills --skill agent-orchestrator-standalone
npx skills add mrclrchtr/skills --skill git-commit
npx skills add mrclrchtr/skills --skill skill-creator
npx skills add mrclrchtr/skills --skill stitch-downloader
npx skills add mrclrchtr/skills --skill web-fetch-to-markdown
```

Use `-g, --global` to install to your user directory instead of the current project:

```bash
# Install globally (available across projects; not meant to be committed)
npx skills add mrclrchtr/skills --skill agent-orchestrator -g
npx skills add mrclrchtr/skills --skill agent-orchestrator-standalone -g
npx skills add mrclrchtr/skills --skill git-commit -g
npx skills add mrclrchtr/skills --skill skill-creator -g
npx skills add mrclrchtr/skills --skill stitch-downloader -g
npx skills add mrclrchtr/skills --skill web-fetch-to-markdown -g
```

Tip: install only what you need. Loading everything can dilute context and reduce quality.

## Use

Once installed, invoke skills by name in your prompt:

- `$agent-orchestrator` — “$agent-orchestrator implement milestone 1”
- `$agent-orchestrator-standalone` — “$agent-orchestrator-standalone implement milestone 1”
- `$git-commit` — Simply “$git-commit”
- `$skill-creator` — “$skill-creator”
- `$stitch-downloader` — “$stitch-downloader download this Stitch screenshot at 2560x2048”
- `$web-fetch-to-markdown` — “$web-fetch-to-markdown https://example.com/docs/page”

## More install options

```bash
# List skills available in this repo (no install)
npx skills add mrclrchtr/skills --list

# Install directly from a skill directory path
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/agent-orchestrator
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/git-commit
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/skill-creator

# Install from a local checkout
npx skills add . --skill agent-orchestrator
npx skills add . --skill git-commit
```

## Development

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
