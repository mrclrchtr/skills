# Test Utils Setup

Create a custom render function that wraps components with all required providers. This ensures tests run in an environment similar to the real app.

## Directory Structure

```
src/test/
├── setup.ts          # Vitest setup file
├── test-utils.tsx    # Custom render and exports
└── helpers.ts        # Test helper functions
```

## Setup File (setup.ts)

Configure in `vite.config.ts`:

```typescript
// vite.config.ts
export default defineConfig({
  test: {
    environment: 'happy-dom',
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

The setup file:

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

## Custom Render (test-utils.tsx)

### Basic Setup with MantineProvider

```typescript
// src/test/test-utils.tsx
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

export function render(ui: React.ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return testingLibraryRender(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { render };
export { default as userEvent } from '@testing-library/user-event';
```

### With TanStack Query

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import { theme } from '../theme';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
        staleTime: 0,
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

export function render(ui: React.ReactElement, options: CustomRenderOptions = {}) {
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
    queryClient,
  };
}
```

### With TanStack Router

```typescript
import { createMemoryHistory, createRootRoute, createRoute, createRouter, RouterProvider } from '@tanstack/react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MantineProvider } from '@mantine/core';
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import { theme } from '../theme';

// Create root route for testing
const rootRoute = createRootRoute({
  component: ({ children }) => <>{children}</>,
});

interface RouterRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  initialRoute?: string;
  routes?: typeof rootRoute[];
  queryClient?: QueryClient;
}

export function renderWithRouter(
  ui: React.ReactElement,
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
    getParentRoute: () => rootRoute,
    path: '/',
    component: () => ui,
  });

  const routeTree = rootRoute.addChildren([testRoute, ...routes]);

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

## Import Pattern

Replace React Testing Library imports with test-utils:

```typescript
// Before
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// After
import { render, screen, userEvent } from '../test/test-utils';
```

## Initial Route Testing

Pass an initial route to the custom render:

```typescript
render(<App />, { initialRoute: '/dashboard' });
```

## Query Client Access

Access the query client for cache manipulation:

```typescript
const { queryClient } = render(<MyComponent />);
queryClient.setQueryData(['users'], mockUsers);
```
