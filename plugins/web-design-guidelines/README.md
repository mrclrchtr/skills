# web-design-guidelines

Design, implement, and review web interfaces with one skill and shared UI guidance.

## Install

### As a normal skill

```bash
npx skills add mrclrchtr/skills --skill web-design-guidelines
```

### As a Claude Code plugin

```bash
/plugin install web-design-guidelines@mrclrchtr-skills
```

Use the plugin when you want the same skill plus the `/web-design-guidelines:review` subagent shortcut.

## Unified Skill

`web-design-guidelines` loads for frontend design, implementation, and review tasks. It infers the appropriate mode from the request; you do not need to select a separate skill.

| Mode | Behavior |
|------|----------|
| **Design** | Establish a visual direction with alternatives, trade-offs, a recommendation, and a memorable differentiator |
| **Apply** | Build or modify UI using the approved direction, local conventions, and shared interface guidance |
| **Review** | Audit UI code, diffs, or specifications with actionable `file:line` findings; leave files unchanged unless fixes are requested |

For combined requests, the skill uses only the needed workflows. A routine implementation does not reopen an approved design direction, and a design-only request does not change code.

**Examples:**

```text
$web-design-guidelines propose a direction for this analytics dashboard before I build it
$web-design-guidelines implement this settings page in our React app
$web-design-guidelines audit this diff for accessibility and interaction issues
$web-design-guidelines review this form and fix the accessibility issues
```

### Review shortcut

The existing `review` delegation helper and command remain available in the plugin. They spawn `web-design-guidelines:ui-reviewer`, which uses the unified skill's Review mode with fresh context.

| Command | Description |
|---------|-------------|
| `/web-design-guidelines:review [target]` | Spawn a subagent to review UI code with fresh context |

```text
/web-design-guidelines:review                  # Infer target from context; ask if ambiguous
/web-design-guidelines:review src/Button.tsx   # Review a specific file
/web-design-guidelines:review src/pages/       # Review a directory
/web-design-guidelines:review docs/spec.md     # Review a specification before implementing
```

## Reference Library

The plugin keeps one shared reference corpus at `references/`, exposed through the unified skill's `references` symlink. The skill loads only topics relevant to the current task.

- **Core (`references/core/`)** — Interactions, forms, animation, layout, mobile behavior, accessibility, performance, theming, copywriting, and anti-patterns.
- **Design (`references/design/`)** — Direction, typography and color, component hierarchy, visual restraint, shadows and depth, motion composition, and avoiding generic UI.
- **Frameworks (`references/frameworks/`)** — React/Next.js, Mantine, and Tailwind integration.
- **Provenance (`references/source-notes.md`)** — Sources and adaptation rationale.

## Project-Local Design Systems

Every mode checks for a local design system first:
- `DESIGN_SYSTEM.md`
- `docs/**/design-system.md`
- `docs/**/style-guide.md`
- Theme files (`theme.ts`, `theme/index.ts`)
- Files referenced in project instructions such as `CLAUDE.md` or `AGENTS.md`

Explicit local design decisions take precedence; shared guidance fills gaps. Accessibility conflicts are flagged rather than silently reproduced.

## Migration from 0.5.x

The former `web-design-guidelines-design`, `web-design-guidelines-apply`, and `web-design-guidelines-review` skills are replaced by `web-design-guidelines`. Update installed skills and saved prompts to use the unified name. The plugin name and `/web-design-guidelines:review` shortcut are unchanged.

## Validation

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/web-design-guidelines/tests -p 'test_*.py' -v
```

Behavioral regression prompts live in `skills/web-design-guidelines/evals/evals.json` and cover design-only, implementation, and review-only requests.

## Version

0.6.0
