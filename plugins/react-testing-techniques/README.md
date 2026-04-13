# React Testing Techniques

A Claude Code plugin providing best practices for testing React components with Vitest, React Testing Library, and Mock Service Worker.

## Features

- **Query Selection Guide** - Choose the right RTL query (getBy, queryBy, findBy)
- **Async Testing Patterns** - waitFor, findBy, waitForElementToBeRemoved
- **MSW v2 Patterns** - API mocking with handler overrides
- **Vitest-Specific Patterns** - vi.mock, vi.fn, vi.spyOn, vi.stubEnv
- **TanStack Integration** - Testing Query and Router
- **UserEvent Best Practices** - Realistic user interaction simulation

## Installation

```bash
# Via --plugin-dir
claude --plugin-dir /path/to/react-testing-techniques

# Or copy to your project
cp -r react-testing-techniques .claude-plugin/
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
skills/react-testing/
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

