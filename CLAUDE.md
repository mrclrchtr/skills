# Skills & Plugins Monorepo

## Structure

- `plugins/` - Full plugins with multiple skills, references, agents
- `skills/` - Single-skill plugins (simpler structure)
- `.claude-plugin/marketplace.json` - Registry of all plugins

## Adding a Plugin

1. Create plugin in `plugins/` or `skills/`
2. Register in `.claude-plugin/marketplace.json` (add to `plugins` array)
3. Bump `metadata.version` (minor for new plugin, patch for fixes)

## Creating User-Invokable Skills (Slash Commands)

For skills that should be invokable via `/plugin:skill-name`:

```yaml
---
name: skill-name
description: What this skill does
argument-hint: "[arg] - description of arguments"
allowed-tools:
  - Agent
  - Read
  - Glob
---
```

Auto-triggered skills only need `name` and `description`.

## Plugin Validation

Use `/plugin-dev:create-plugin` workflow for guided plugin creation with validation.

## Fetching External Documentation

- `gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d` - Fetch file from GitHub
- `npx ctx7@latest library "<name>" "<question>"` then `npx ctx7@latest docs "<id>" "<question>"` - Fetch library docs

## Agent Naming

Use full agent names with prefix: `plugin-dev:plugin-validator`, `plugin-dev:skill-reviewer` (not just `plugin-validator`)
