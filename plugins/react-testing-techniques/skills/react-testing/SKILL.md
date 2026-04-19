---
name: react-testing
description: This skill should be used when the user asks to "write React tests", "test a component", "set up test utils", "mock an API", "use React Testing Library", "configure MSW", "test async behavior", "choose query type", "test Mantine components", "test a modal", or when writing tests for React components using Vitest, RTL, MSW, or Mantine. Provides best practices for component and integration testing.
---

# React Testing Techniques

Best practices for testing React components with Vitest, React Testing Library (RTL), and Mock Service Worker (MSW).

## Core Principles

### Test Like a User

Write tests that interact with components the way users do. Avoid testing implementation details.

- Query elements by accessible roles, labels, and text - not by test IDs or class names
- Simulate real user interactions with `userEvent`, not `fireEvent`
- Test behavior and outcomes, not internal state or method calls
- Prefer integration tests over isolated unit tests

### Prefer Integration Over Mocking

Combine multiple components and use MSW for API mocking at the network level. Avoid mocking component internals, hooks, or services unless absolutely necessary.

## Query Selection Decision

Choose the right query based on the scenario:

| Scenario | Query | Why |
|----------|-------|-----|
| Element exists synchronously | `getBy*` | Throws if not found - fails fast |
| Element appears after async operation | `findBy*` | Waits with retry, use with `await` |
| Assert element does NOT exist | `queryBy*` | Returns null instead of throwing |
| Multiple elements expected | `*AllBy*` variants | Returns array of matches |

**Priority order for queries:**
1. `getByRole` - most accessible, preferred
2. `getByLabelText` - for form fields
3. `getByPlaceholderText` - for inputs
4. `getByText` - for non-interactive content
5. `getByTestId` - last resort only

## UserEvent Setup (Required Pattern)

Always use `userEvent.setup()` before interactions:

```typescript
import { render, screen } from '../test/test-utils';
import userEvent from '@testing-library/user-event';

test('submits form correctly', async () => {
  const user = userEvent.setup();
  render(<MyForm />);
  
  await user.type(screen.getByRole('textbox', { name: /email/i }), 'test@example.com');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  expect(await screen.findByText(/success/i)).toBeInTheDocument();
});
```

**Never use `fireEvent`** - it dispatches raw DOM events without realistic user interaction simulation.

## Async Testing Patterns

### Use `findBy*` for Elements That Appear Async

```typescript
// Element appears after data loads
expect(await screen.findByText('John Doe')).toBeInTheDocument();
```

### Use `waitFor` for Assertions Only

```typescript
// Wait for a side effect or state change
await waitFor(() => expect(handleSubmit).toHaveBeenCalledTimes(1));
```

### Use `waitForElementToBeRemoved` for Disappearing Elements

```typescript
// Wait for loading spinner to disappear
await waitForElementToBeRemoved(() => screen.getByText('Loading...'));
```

## MSW v2 Patterns

Use Mock Service Worker for API mocking. Always use v2 syntax:

```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'John' }]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Override handlers per test:**

```typescript
test('handles error state', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ error: 'Not found' }, { status: 404 });
    })
  );
  // Test error handling...
});
```

## Vitest-Specific Patterns

Use Vitest APIs, not Jest:

| Operation | Vitest | Not Jest |
|-----------|--------|----------|
| Mock function | `vi.fn()` | ~~jest.fn()~~ |
| Mock module | `vi.mock()` | ~~jest.mock()~~ |
| Spy on method | `vi.spyOn()` | ~~jest.spyOn()~~ |
| Stub env var | `vi.stubEnv()` | ~~process.env~~ |
| Reset modules | `vi.resetModules()` | ~~jest.resetModules()~~ |
| Restore mocks | `vi.restoreAllMocks()` | ~~jest.restoreAllMocks()~~ |

**Environment variable testing:**

```typescript
import { afterEach, vi } from 'vitest';

afterEach(() => {
  vi.unstubAllEnvs();
  vi.resetModules();
});

test('handles missing env var', async () => {
  vi.stubEnv('API_KEY', '');
  const { config } = await import('./config');
  expect(() => config.apiKey).toThrow();
});
```

## Test Utils Setup

Create a custom render with all providers. Read `references/test-utils-setup.md` for complete setup with:
- MantineProvider (with `env="test"`)
- QueryClientProvider (fresh client per test)
- RouterProvider (TanStack Router)

## What to Avoid

### Never Test Implementation Details
- Internal state
- Private methods
- Component lifecycle
- Hook internals

### Never Use Snapshot Tests
Except for trivial components (<30 lines of output). Snapshots encode structure, not intent.

### Never Mock What You Don't Own
Use MSW for APIs instead of mocking fetch/axios. Mock only at system boundaries.

## Additional Resources

### Reference Files

Consult these for detailed patterns:
- **`references/test-utils-setup.md`** - Complete custom render setup with providers
- **`references/query-selection.md`** - Detailed query type decision guide
- **`references/vitest-patterns.md`** - Vitest mocking, spying, and stubbing
- **`references/msw-patterns.md`** - MSW v2 handlers, overrides, error simulation
- **`references/async-testing.md`** - waitFor, findBy, timing patterns
- **`references/tanstack-testing.md`** - TanStack Query and Router testing
- **`references/user-interactions.md`** - userEvent patterns and edge cases
- **`references/mantine-testing.md`** - Mantine component testing (modals, forms, select)
