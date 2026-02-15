# Agent Skills

Reusable skills for agent workflows (Codex / agent-skill loaders).

This repo currently contains:
- `agent-orchestrator`: Coordinate complex work using a phase-gated, multi-agent engineering loop (audit → design → implement → review → validate → deliver).
- `git-commit`: Create safe, repo-convention commits by inspecting diffs, staging intentionally, and writing high-quality commit messages (prefer Conventional Commits when the repo uses them).

## Install

Install one skill at a time via the `skills` CLI from `vercel-labs/skills`:

```bash
# Install from this repo (recommended)
npx skills add mrclrchtr/skills --skill agent-orchestrator
npx skills add mrclrchtr/skills --skill git-commit
```

Use `-g, --global` to install to your user directory instead of the current project:

```bash
# Install globally (available across projects; not meant to be committed)
npx skills add mrclrchtr/skills --skill agent-orchestrator -g
npx skills add mrclrchtr/skills --skill git-commit -g
```

Tip: install only what you need. Loading everything can dilute context and reduce quality.

## Use

Once installed, invoke skills by name in your prompt:

- `$agent-orchestrator` — “$agent-orchestrator implement milestone 1”
- `$git-commit` — Simply “$git-commit”

## More install options

```bash
# List skills available in this repo (no install)
npx skills add mrclrchtr/skills --list

# Install directly from a skill directory path
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/agent-orchestrator
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/git-commit

# Install from a local checkout
npx skills add . --skill agent-orchestrator
npx skills add . --skill git-commit
```

## References

- [OpenAI Skill Docs](https://developers.openai.com/codex/skills.md)
- [Vercel Labs Skills CLI](https://skills.sh/docs)
- [Agentskills Specification](https://agentskills.io/specification.md)
