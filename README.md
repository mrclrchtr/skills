# Agent Skills

Reusable agent skills for the open agent skills ecosystem.
This repo currently contains one skill (`agent-orchestrator`), and more may be added over time.

## Quick start

Install the skill via the `skills` CLI from `vercel-labs/skills`:

```bash
npx skills add mrclrchtr/skills --skill agent-orchestrator
```

> Note: Use skills selectively. Installing/loading everything tends to dilute context and reduce quality.

## Skill catalog

- `agent-orchestrator`: Coordinate complex work using a phase-gated, multi-agent engineering loop (audit → design → implement → review → validate → deliver).

## More install options

```bash
# List skills available in this repo (no install)
npx skills add mrclrchtr/skills --list

# Install directly from the skill directory path
npx skills add https://github.com/mrclrchtr/skills/tree/main/skills/agent-orchestrator

# Install from a local checkout
npx skills add . --skill agent-orchestrator
```

# References

- [OpenAi Skill Docs](https://developers.openai.com/codex/skills.md)
- [Vercel Labs Skills CLI](https://skills.sh/docs)
- [Agentskills Specification](https://agentskills.io/specification.md)
