# React Testing Techniques

A shared source for:
- the `react-testing` skill on `skills.sh`
- the `react-testing-techniques` Claude Code marketplace plugin

## Features

- **Query Selection Guide** - Choose the right RTL query (getBy, queryBy, findBy)
- **Async Testing Patterns** - waitFor, findBy, waitForElementToBeRemoved
- **MSW v2 Patterns** - API mocking with handler overrides
- **Vitest-Specific Patterns** - vi.mock, vi.fn, vi.spyOn, vi.stubEnv
- **TanStack Integration** - Testing Query and Router
- **UserEvent Best Practices** - Realistic user interaction simulation

## Installation

### skills.sh

```bash
npx skills add mrclrchtr/skills --skill react-testing
```

### Claude Code Marketplace

```bash
/plugin marketplace add mrclrchtr/skills
/plugin install react-testing-techniques@mrclrchtr-skills
```

## Usage

The skill automatically activates when:
- Writing React component tests
- Using React Testing Library
- Setting up MSW handlers
- Testing async behavior

Example triggers:
- "Write a test for this component"
- "Set up test utils"
- "Mock this API call"
- "Which query should I use?"

## Stack Support

Optimized for:
- **Test Runner**: Vitest
- **DOM Environment**: happy-dom
- **Testing Library**: @testing-library/react, @testing-library/user-event
- **API Mocking**: MSW v2
- **State Management**: TanStack Query
- **Routing**: TanStack Router
- **UI Library**: Mantine v9

## Skill Structure

```
plugins/react-testing-techniques/skills/react-testing/
├── SKILL.md                    # Core principles and quick reference
└── references/
    ├── test-utils-setup.md     # Custom render with providers
    ├── query-selection.md      # Query type decision guide
    ├── vitest-patterns.md      # Vitest mocking and spying
    ├── msw-patterns.md         # MSW v2 handlers
    ├── async-testing.md        # Async testing patterns
    ├── tanstack-testing.md     # Query and Router testing
    ├── user-interactions.md    # UserEvent patterns
    └── mantine-testing.md      # Mantine component testing
```

## Key Principles

1. **Test like a user** - Query by role, text, label - not test IDs
2. **Prefer integration** - Use MSW for APIs, avoid mocking internals
3. **Use userEvent.setup()** - Never fireEvent
4. **Choose the right query** - getBy (sync), findBy (async), queryBy (absence)
5. **Avoid snapshot tests** - Test behavior, not structure
