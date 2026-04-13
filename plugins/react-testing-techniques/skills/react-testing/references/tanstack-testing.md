# TanStack Testing Patterns

Patterns for testing TanStack Query (v5) and TanStack Router (v1).

## TanStack Query

### QueryClient Setup

Create a fresh QueryClient for each test to ensure isolation. Disabling retries is essential to prevent test timeouts when testing error scenarios.

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render as testingLibraryRender } from '@testing-library/react';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,        // Essential: prevents test timeouts on errors
        gcTime: 0,           // No garbage collection delay
        staleTime: 0,        // Data always stale (fetch on mount)
      },
      mutations: {
        retry: false,
      },
    },
  });
}

// In test-utils.tsx
export function render(ui: React.ReactElement) {
  const queryClient = createTestQueryClient();
  
  return {
    ...testingLibraryRender(
      <QueryClientProvider client={queryClient}>
        {ui}
      </QueryClientProvider>
    ),
    queryClient,
  };
}
```

**Important**: Query-level retry settings override defaults. If a query specifies `retry: 3`, it will still retry despite the default configuration.

### Testing Components with useQuery

Use `findBy*` queries to wait for async data. MSW handles network mocking.

```typescript
import { render, screen } from '../test/test-utils';
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('displays user data', async () => {
  // MSW handles the API mock (set up in beforeEach/setupTests)
  render(<UserProfile userId="1" />);
  
  // findBy* waits for the element to appear
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});

test('displays error state', async () => {
  // Override handler for this specific test
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json({ error: 'Not found' }, { status: 404 });
    })
  );
  
  render(<UserProfile userId="999" />);
  
  expect(await screen.findByText(/error/i)).toBeInTheDocument();
});
```

### Testing Custom Hooks with renderHook

For React 18+, use `renderHook` from `@testing-library/react` directly. The separate `@testing-library/react-hooks` package is only needed for React 17 and earlier.

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUsers } from '../hooks/useUsers';

test('fetches users successfully', async () => {
  const queryClient = createTestQueryClient();
  
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
  
  const { result } = renderHook(() => useUsers(), { wrapper });
  
  // Initially loading
  expect(result.current.isLoading).toBe(true);
  
  // Wait for success
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  
  // Check data
  expect(result.current.data).toHaveLength(2);
});
```

### Testing Mutations

Test mutations through user interactions. For programmatic testing, `mutateAsync` returns a promise that can be awaited.

```typescript
import userEvent from '@testing-library/user-event';
import { render, screen } from '../test/test-utils';
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('creates user successfully', async () => {
  const user = userEvent.setup();
  
  render(<CreateUserForm />);
  
  await user.type(screen.getByLabelText(/name/i), 'Jane');
  await user.type(screen.getByLabelText(/email/i), 'jane@example.com');
  await user.click(screen.getByRole('button', { name: /create/i }));
  
  // Wait for success message
  expect(await screen.findByText(/user created/i)).toBeInTheDocument();
});

test('shows mutation error', async () => {
  server.use(
    http.post('/api/users', () => {
      return HttpResponse.json(
        { error: 'Email already exists' },
        { status: 409 }
      );
    })
  );
  
  const user = userEvent.setup();
  
  render(<CreateUserForm />);
  
  await user.type(screen.getByLabelText(/email/i), 'existing@email.com');
  await user.click(screen.getByRole('button', { name: /create/i }));
  
  expect(await screen.findByText(/email already exists/i)).toBeInTheDocument();
});
```

### Testing Mutations with mutateAsync

For hook-level testing, use `mutateAsync` which returns a promise:

```typescript
test('mutation hook handles error', async () => {
  server.use(
    http.post('/api/todos', () => {
      return HttpResponse.json({ error: 'Failed' }, { status: 500 });
    })
  );

  const { result } = renderHook(() => useCreateTodo(), { wrapper });

  await expect(result.current.mutateAsync({ title: 'Test' })).rejects.toThrow();
  expect(result.current.isError).toBe(true);
});
```

### Pre-populating Query Cache

Pre-populate the cache **before** rendering to skip loading states:

```typescript
test('renders with cached data', () => {
  const queryClient = createTestQueryClient();
  
  // Pre-populate cache BEFORE render
  queryClient.setQueryData(['users', '1'], {
    id: '1',
    name: 'Cached User',
  });
  
  render(<UserProfile userId="1" />, { queryClient });
  
  // Data shows immediately (no loading state)
  expect(screen.getByText('Cached User')).toBeInTheDocument();
});
```

### Testing Query Invalidation

```typescript
test('refreshes data after mutation', async () => {
  const user = userEvent.setup();
  
  render(<UserDashboard />);
  
  // Initial data
  expect(await screen.findByText('John')).toBeInTheDocument();
  
  // Update the mock to return new data
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json({ id: '1', name: 'John Updated' });
    })
  );
  
  await user.click(screen.getByRole('button', { name: /refresh/i }));
  
  // Updated data after invalidation triggers refetch
  expect(await screen.findByText('John Updated')).toBeInTheDocument();
});
```

### Testing Error Boundaries with throwOnError

Use `throwOnError: true` to propagate errors to React error boundaries:

```typescript
// In your query/mutation
const { data } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  throwOnError: true, // Errors thrown to nearest error boundary
});

// Test error boundary behavior
test('renders error boundary on query failure', async () => {
  server.use(
    http.get('/api/user', () => HttpResponse.error())
  );
  
  render(
    <ErrorBoundary fallback={<div>Error occurred</div>}>
      <UserProfile />
    </ErrorBoundary>
  );
  
  expect(await screen.findByText('Error occurred')).toBeInTheDocument();
});
```

## TanStack Router

### Router Test Setup (Code-Based Routes)

Use `createMemoryHistory` for controlled navigation in tests. Create reusable test utilities:

```typescript
// test/router-utils.tsx
import React from 'react';
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import {
  createMemoryHistory,
  createRootRoute,
  createRoute,
  createRouter,
  RouterProvider,
  Outlet,
  AnyRoute,
} from '@tanstack/react-router';

export const rootRoute = createRootRoute({
  component: () => <Outlet />,
});

// Factory function for creating test routers
export function createTestRouter(routes: AnyRoute[], initialLocation = '/') {
  const routeTree = rootRoute.addChildren(routes);
  
  return createRouter({
    routeTree,
    history: createMemoryHistory({ initialEntries: [initialLocation] }),
  });
}

interface RenderWithRouterOptions extends Omit<RenderOptions, 'wrapper'> {
  initialLocation?: string;
  routes?: AnyRoute[];
}

export function renderWithRouter(
  ui: React.ReactElement,
  { initialLocation = '/', routes = [], ...renderOptions }: RenderWithRouterOptions = {}
) {
  const testRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/',
    component: () => ui,
  });
  
  const router = createTestRouter([testRoute, ...routes], initialLocation);
  
  return {
    ...testingLibraryRender(<RouterProvider router={router} />, renderOptions),
    router,
  };
}

// Re-export for convenience
export { rootRoute as TestRootRoute };
```

### Router Test Setup (File-Based Routes)

For file-based routing, import the generated route tree:

```typescript
// test/file-route-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { createRouter, RouterProvider, createMemoryHistory } from '@tanstack/react-router';
import { routeTree } from '../routeTree.gen';

interface RenderWithFileRoutesOptions extends Omit<RenderOptions, 'wrapper'> {
  initialLocation?: string;
  routerContext?: Record<string, unknown>;
}

export function renderWithFileRoutes(
  ui: React.ReactElement,
  { initialLocation = '/', routerContext = {}, ...renderOptions }: RenderWithFileRoutesOptions = {}
) {
  const router = createRouter({
    routeTree,
    history: createMemoryHistory({ initialEntries: [initialLocation] }),
    context: routerContext,
  });

  function Wrapper({ children }: { children: React.ReactNode }) {
    return <RouterProvider router={router}>{children}</RouterProvider>;
  }

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    router,
  };
}
```

### Testing Link Navigation

```typescript
import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Link, createRoute } from '@tanstack/react-router';
import { renderWithRouter, rootRoute } from '../test/router-utils';

describe('Navigation', () => {
  it('navigates when link is clicked', async () => {
    const user = userEvent.setup();
    
    function HomePage() {
      return (
        <div>
          <h1>Home</h1>
          <Link to="/about">About</Link>
        </div>
      );
    }
    
    const homeRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/',
      component: HomePage,
    });
    
    const aboutRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/about',
      component: () => <h1>About Page</h1>,
    });
    
    const { router } = renderWithRouter(<div />, {
      routes: [homeRoute, aboutRoute],
      initialLocation: '/',
    });
    
    expect(router.state.location.pathname).toBe('/');
    expect(screen.getByText('Home')).toBeInTheDocument();
    
    await user.click(screen.getByRole('link', { name: /about/i }));
    
    expect(router.state.location.pathname).toBe('/about');
    expect(screen.getByText('About Page')).toBeInTheDocument();
  });
});
```

### Testing Dynamic Routes

```typescript
it('navigates to dynamic route with params', async () => {
  const user = userEvent.setup();
  
  const userRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/users/$userId',
    component: function UserDetail() {
      const { userId } = userRoute.useParams();
      return <h1>User {userId}</h1>;
    },
  });
  
  const { router } = renderWithRouter(<UserList />, {
    routes: [userRoute],
  });
  
  await user.click(screen.getByRole('link', { name: /view user 123/i }));
  
  expect(router.state.location.pathname).toBe('/users/123');
  expect(screen.getByText('User 123')).toBeInTheDocument();
});
```

### Testing Search Parameters

```typescript
it('navigates with search params', async () => {
  const user = userEvent.setup();
  
  const searchRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/search',
    component: SearchPage,
    validateSearch: (search) => ({
      q: (search.q as string) || '',
      page: Number(search.page) || 1,
    }),
  });
  
  const { router } = renderWithRouter(<div />, {
    initialLocation: '/search',
    routes: [searchRoute],
  });
  
  await user.type(screen.getByRole('textbox'), 'react');
  await user.click(screen.getByRole('button', { name: /search/i }));
  
  expect(router.state.location.search).toMatchObject({
    q: 'react',
  });
});

// Type-safe navigation test
it('provides type-safe navigation', async () => {
  const user = userEvent.setup();
  
  function TestComponent() {
    const navigate = useNavigate();
    
    return (
      <button onClick={() => navigate({
        to: '/posts/$postId',
        params: { postId: '123' },
        search: { tab: 'comments' }
      })}>
        Navigate
      </button>
    );
  }
  
  const { router } = renderWithRouter(<TestComponent />, {
    routes: [postRoute],
  });
  
  await user.click(screen.getByRole('button'));
  
  expect(router.state.location.pathname).toBe('/posts/123');
  expect(router.state.location.search).toEqual({ tab: 'comments' });
});
```

### Testing Programmatic Navigation

```typescript
import { waitFor } from '@testing-library/react';

it('redirects after form submit', async () => {
  const user = userEvent.setup();
  
  const successRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/success',
    component: () => <h1>Success!</h1>,
  });
  
  const { router } = renderWithRouter(<CheckoutForm />, {
    routes: [successRoute],
  });
  
  await user.click(screen.getByRole('button', { name: /complete order/i }));
  
  await waitFor(() => {
    expect(router.state.location.pathname).toBe('/success');
  });
  
  expect(screen.getByText('Success!')).toBeInTheDocument();
});
```

### Testing Protected Routes

```typescript
it('redirects unauthenticated user', async () => {
  const loginRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/login',
    component: () => <h1>Login</h1>,
  });
  
  const { router } = renderWithRouter(<ProtectedDashboard />, {
    initialLocation: '/dashboard',
    routes: [loginRoute],
  });
  
  await waitFor(() => {
    expect(router.state.location.pathname).toBe('/login');
  });
});
```

### Testing Route Loaders

```typescript
it('renders loader data', async () => {
  const userRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/users/$userId',
    loader: async ({ params }) => {
      // MSW intercepts this fetch
      const res = await fetch(`/api/users/${params.userId}`);
      return res.json();
    },
    component: function UserPage() {
      const data = userRoute.useLoaderData();
      return <h1>{data.name}</h1>;
    },
  });
  
  renderWithRouter(<div />, {
    initialLocation: '/users/1',
    routes: [userRoute],
  });
  
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});
```

### Testing Router Context

Use `createRootRouteWithContext` to provide typed context to routes:

```typescript
import { createRootRouteWithContext, createRoute, Outlet } from '@tanstack/react-router';

interface RouterContext {
  auth: {
    user: { id: string; name: string } | null;
    isAuthenticated: boolean;
  };
}

it('provides context to routes', () => {
  const rootRouteWithContext = createRootRouteWithContext<RouterContext>()({
    component: () => <Outlet />,
  });
  
  function UserDashboard() {
    const { auth } = Route.useRouteContext();
    return <div>Welcome, {auth.user?.name || 'Guest'}!</div>;
  }
  
  const dashboardRoute = createRoute({
    getParentRoute: () => rootRouteWithContext,
    path: '/dashboard',
    component: UserDashboard,
  });
  
  const mockContext = {
    auth: {
      user: { id: '1', name: 'John Doe' },
      isAuthenticated: true,
    },
  };
  
  const router = createRouter({
    routeTree: rootRouteWithContext.addChildren([dashboardRoute]),
    context: mockContext,
    history: createMemoryHistory({ initialEntries: ['/dashboard'] }),
  });
  
  render(<RouterProvider router={router} />);
  
  expect(screen.getByText('Welcome, John Doe!')).toBeInTheDocument();
});
```

### Testing Route Error Boundaries

```typescript
import { vi } from 'vitest';

it('handles component errors with error boundary', () => {
  // Suppress React error boundary console output
  const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
  
  const errorRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/error',
    component: () => {
      throw new Error('Test error');
    },
    errorComponent: () => <div>Something went wrong</div>,
  });
  
  renderWithRouter(<div />, {
    initialLocation: '/error',
    routes: [errorRoute],
  });
  
  expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  
  consoleSpy.mockRestore();
});

it('handles loader errors', async () => {
  const dataRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/data',
    loader: async () => {
      throw new Error('Load failed');
    },
    errorComponent: () => <div>Failed to load data</div>,
  });
  
  renderWithRouter(<div />, {
    initialLocation: '/data',
    routes: [dataRoute],
  });
  
  expect(await screen.findByText('Failed to load data')).toBeInTheDocument();
});
```

### Testing Deferred Data Loading

Use `defer` for non-critical data and `Await` with `Suspense` for rendering:

```typescript
import { Suspense } from 'react';
import { createFileRoute, defer, Await } from '@tanstack/react-router';

// In your route file
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId); // Critical - awaited
    const commentsPromise = fetchComments(params.postId); // Deferred
    
    return {
      post,
      comments: defer(commentsPromise),
    };
  },
  component: function PostPage() {
    const { post, comments } = Route.useLoaderData();
    
    return (
      <article>
        <h1>{post.title}</h1>
        <Suspense fallback={<div>Loading comments...</div>}>
          <Await promise={comments}>
            {(data) => (
              <ul>
                {data.map((c) => <li key={c.id}>{c.body}</li>)}
              </ul>
            )}
          </Await>
        </Suspense>
      </article>
    );
  },
});

// Test
it('renders deferred data', async () => {
  renderWithFileRoutes(<div />, {
    initialLocation: '/posts/1',
  });
  
  // Critical data renders immediately
  expect(await screen.findByText('Post Title')).toBeInTheDocument();
  
  // Deferred data shows loading state then resolves
  expect(screen.getByText('Loading comments...')).toBeInTheDocument();
  expect(await screen.findByText('First comment')).toBeInTheDocument();
});
```

**Important**: `Await` requires a `Suspense` boundary ancestor or it will error.

## Combined Query + Router Testing

When using both TanStack Query and Router, combine the providers in your test utilities:

```typescript
// test/combined-utils.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createRouter, RouterProvider, createMemoryHistory } from '@tanstack/react-router';
import { render as testingLibraryRender } from '@testing-library/react';

export function renderWithQueryAndRouter(
  ui: React.ReactElement,
  {
    initialLocation = '/',
    routes = [],
    queryClient = createTestQueryClient(),
  } = {}
) {
  const router = createTestRouter(routes, initialLocation);
  
  return {
    ...testingLibraryRender(
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    ),
    queryClient,
    router,
  };
}
```

```typescript
it('fetches data and navigates', async () => {
  const user = userEvent.setup();
  
  const { queryClient, router } = renderWithQueryAndRouter(<App />, {
    initialLocation: '/users',
    routes: [usersRoute, userDetailRoute],
  });
  
  // Data loads via TanStack Query
  expect(await screen.findByText('John')).toBeInTheDocument();
  
  // Navigate via TanStack Router
  await user.click(screen.getByRole('link', { name: /view john/i }));
  
  expect(router.state.location.pathname).toBe('/users/1');
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});
```

## Key Testing Principles

1. **Isolate each test**: Create fresh QueryClient and router instances per test
2. **Disable retries**: Prevents timeouts when testing error states
3. **Use MSW for network mocking**: Intercepts fetch calls at the network level
4. **Prefer `findBy*` queries**: Automatically wait for async operations
5. **Use `userEvent` over `fireEvent`**: More realistic user interaction simulation
6. **Test user-facing behavior**: Focus on what users see, not implementation details
7. **Mock at boundaries**: Use MSW for API calls, memory history for routing
