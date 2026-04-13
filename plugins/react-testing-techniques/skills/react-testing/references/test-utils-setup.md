# Test Utils Setup

Create a custom render function that wraps components with all required providers. This ensures tests run in an environment similar to the real app.

## Directory Structure

```
src/test/
├── setup.ts          # Vitest setup file
├── test-utils.tsx    # Custom render and exports
└── helpers.ts        # Test helper functions
```

## Vitest Configuration

Configure in `vite.config.ts`:

```typescript
// vite.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true, // Enable global test APIs (describe, it, expect)
    environment: 'happy-dom', // or 'jsdom'
    setupFiles: ['./src/test/setup.ts'],
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    clearMocks: true,
    restoreMocks: true,
  },
});
```

Add TypeScript support for globals in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

## Setup File (setup.ts)

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test (required when globals: true)
afterEach(() => {
  cleanup();
});
```

Note: When using `globals: true`, some libraries like `@testing-library/react` rely on globals to perform auto cleanup. The explicit cleanup ensures consistent behavior.

## Custom Render (test-utils.tsx)

### Basic Setup with Providers

```typescript
// src/test/test-utils.tsx
import React, { ReactElement } from 'react';
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { theme } from '../theme';

function AllProviders({ children }: { children: React.ReactNode }) {
  return (
    <MantineProvider theme={theme} env="test">
      {children}
    </MantineProvider>
  );
}

export function render(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return testingLibraryRender(ui, { wrapper: AllProviders, ...options });
}

// Re-export everything from testing-library
export * from '@testing-library/react';
// Override render with custom version
export { render };
// Export userEvent for convenience
export { default as userEvent } from '@testing-library/user-event';
```

### With TanStack Query

Disable retries in tests to prevent timeouts when testing error scenarios. The library defaults to three retries with exponential backoff, which would cause tests to timeout.

```typescript
import React, { ReactElement } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import { theme } from '../theme';

// Create isolated QueryClient for each test
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Disable retries for faster test failures
        gcTime: 0, // Garbage collect immediately
        staleTime: 0, // Always consider data stale
      },
      mutations: {
        retry: false,
      },
    },
  });
}

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  queryClient?: QueryClient;
}

export function render(ui: ReactElement, options: CustomRenderOptions = {}) {
  const { queryClient = createTestQueryClient(), ...renderOptions } = options;

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <MantineProvider theme={theme} env="test">
          {children}
        </MantineProvider>
      </QueryClientProvider>
    );
  }

  return {
    ...testingLibraryRender(ui, { wrapper: Wrapper, ...renderOptions }),
    queryClient, // Return for cache manipulation in tests
  };
}
```

Important: If a specific query has explicit retry settings, those will override the defaults. Ensure test isolation by creating a new QueryClient per test.

### With TanStack Router

Use `createMemoryHistory` for testing - it keeps routing history in memory without interacting with the browser URL.

```typescript
import React, { ReactElement } from 'react';
import {
  createMemoryHistory,
  createRootRoute,
  createRoute,
  createRouter,
  RouterProvider,
  Outlet,
} from '@tanstack/react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import { theme } from '../theme';

// Reusable root route for testing
export const testRootRoute = createRootRoute({
  component: () => <Outlet />,
});

interface RouterRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  initialRoute?: string;
  routes?: ReturnType<typeof createRoute>[];
  queryClient?: QueryClient;
}

export function renderWithRouter(
  ui: ReactElement,
  options: RouterRenderOptions = {}
) {
  const {
    initialRoute = '/',
    routes = [],
    queryClient = createTestQueryClient(),
    ...renderOptions
  } = options;

  // Create test route that renders the component
  const testRoute = createRoute({
    getParentRoute: () => testRootRoute,
    path: '/',
    component: () => ui,
  });

  const routeTree = testRootRoute.addChildren([testRoute, ...routes]);

  const router = createRouter({
    routeTree,
    history: createMemoryHistory({ initialEntries: [initialRoute] }),
  });

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <MantineProvider theme={theme} env="test">
          <RouterProvider router={router} />
        </MantineProvider>
      </QueryClientProvider>
    );
  }

  return {
    ...testingLibraryRender(<></>, { wrapper: Wrapper, ...renderOptions }),
    router,
    queryClient,
  };
}
```

For browser history testing (when needed), add cleanup in afterEach:

```typescript
import { createBrowserHistory, RouterHistory } from '@tanstack/react-router';

let history: RouterHistory;

beforeEach(() => {
  history = createBrowserHistory();
});

afterEach(() => {
  history.destroy();
  window.history.replaceState(null, 'root', '/');
});
```

## Mantine-Specific: Disable Transitions

For testing Modals, Drawers, and other portal-based components:

```typescript
import { createTheme, mergeThemeOverrides, Modal, Drawer, Popover } from '@mantine/core';
import { theme } from '../theme';

const testTheme = mergeThemeOverrides(
  theme,
  createTheme({
    components: {
      Modal: Modal.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
      Drawer: Drawer.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
      Popover: Popover.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
    },
  })
);
```

## userEvent Setup

Use `userEvent.setup()` to create a session with shared keyboard/pointer state for realistic interactions:

```typescript
import { render, screen } from '../test/test-utils';
import userEvent from '@testing-library/user-event';

test('form interaction with shared state', async () => {
  const user = userEvent.setup();

  render(<LoginForm />);

  // All actions share keyboard/pointer state
  await user.type(screen.getByLabelText(/username/i), 'johndoe');
  await user.tab();
  await user.type(screen.getByLabelText(/password/i), 'secret123');
  await user.click(screen.getByRole('button', { name: /login/i }));

  expect(screen.getByText(/welcome/i)).toBeInTheDocument();
});
```

### With Fake Timers

```typescript
test('work with vitest fake timers', async () => {
  vi.useFakeTimers();

  const user = userEvent.setup({
    delay: 100,
    advanceTimers: (ms) => vi.advanceTimersByTime(ms),
  });

  render(<input />);
  await user.type(screen.getByRole('textbox'), 'test');

  expect(screen.getByRole('textbox')).toHaveValue('test');

  vi.useRealTimers();
});
```

## Import Pattern

Replace React Testing Library imports with test-utils:

```typescript
// Before
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// After
import { render, screen, userEvent } from '../test/test-utils';
```

## Usage Examples

### Initial Route Testing

```typescript
renderWithRouter(<App />, { initialRoute: '/dashboard' });
```

### Query Client Access

```typescript
const { queryClient } = render(<MyComponent />);
queryClient.setQueryData(['users'], mockUsers);
```

### Testing Custom Hooks

Use `renderHook` with a wrapper for testing custom hooks that use React Query:

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

test('useCustomHook returns data', async () => {
  const { result } = renderHook(() => useCustomHook(), {
    wrapper: createWrapper(),
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toEqual('Hello');
});
```

### Testing Route Loaders

```typescript
import { createRoute } from '@tanstack/react-router';
import { renderWithRouter, testRootRoute } from '../test/test-utils';

test('should load and display data from loader', async () => {
  const mockFetchUser = vi.fn().mockResolvedValue({
    id: 1,
    name: 'John Doe',
  });

  const userRoute = createRoute({
    getParentRoute: () => testRootRoute,
    path: '/users/$userId',
    component: function UserProfile() {
      const user = Route.useLoaderData();
      return <h1>{user.name}</h1>;
    },
    loader: ({ params }) => mockFetchUser(params.userId),
  });

  renderWithRouter(<div />, {
    routes: [userRoute],
    initialRoute: '/users/1',
  });

  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
```
