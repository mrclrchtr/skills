# web-design-guidelines

Design, implement, and review web interfaces with shared UI guidance.

## Skills

### Auto-triggered (contextual)

These skills load automatically when Claude detects relevant context:

| Skill | Triggers when... |
|-------|------------------|
| **web-design-guidelines-design** | Creating or redesigning UI; establishing design direction before implementation |
| **web-design-guidelines-apply** | Building or modifying frontend UI; implementation should follow shared guidelines |
| **web-design-guidelines-review** | Reviewing existing UI code, diffs, or design changes for issues |

### User-invokable (slash command)

| Command | Description |
|---------|-------------|
| `/web-design-guidelines:review [target]` | Spawn a subagent to review UI code with fresh context |

**Examples:**
```
/web-design-guidelines:review                    # Review git diff (uncommitted changes)
/web-design-guidelines:review src/Button.tsx    # Review specific file
/web-design-guidelines:review src/pages/        # Review directory
/web-design-guidelines:review docs/spec.md      # Review specification before implementing
```

## Reference Library

The plugin includes comprehensive guidance organized by category:

### Core (`references/core/`)
- `interactions.md` - Keyboard, focus, hover, press states
- `forms.md` - Input validation, error handling, field patterns
- `animation.md` - Motion, transitions, reduced-motion support
- `layout.md` - Responsive design, spacing, grid patterns
- `content-accessibility.md` - ARIA, semantic HTML, screen readers
- `performance.md` - Loading states, lazy loading, optimization
- `theming-copy.md` - Dark mode, tokens, microcopy
- `anti-patterns.md` - Common mistakes to avoid

### Design (`references/design/`)
- `direction.md` - Establishing design direction
- `typography-color.md` - Type scale, color systems
- `motion-composition.md` - Animation principles
- `anti-slop.md` - Avoiding generic AI-generated UI

### Frameworks (`references/frameworks/`)
- `react-next.md` - React and Next.js patterns
- `mantine.md` - Mantine component library
- `tailwind-integration.md` - Tailwind CSS usage

## Project-Local Design Systems

All skills check for a local design system first:
- `DESIGN_SYSTEM.md`
- `docs/**/design-system.md`
- `docs/**/style-guide.md`
- Theme files (`theme.ts`, `theme/index.ts`)
- Files referenced in `CLAUDE.md`

Local design system decisions take precedence; plugin guidance fills gaps.

## Version

0.2.1
