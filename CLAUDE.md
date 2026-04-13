# Skills & Plugins Monorepo

## Structure

- `plugins/` - Full plugins with multiple skills, references, agents
- `skills/` - Single-skill plugins (simpler structure)
- `.claude-plugin/marketplace.json` - Registry of all plugins

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
