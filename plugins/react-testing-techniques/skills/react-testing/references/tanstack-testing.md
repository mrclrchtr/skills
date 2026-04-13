# TanStack Testing Patterns

Patterns for testing TanStack Query and TanStack Router.

## TanStack Query

### QueryClient Setup

Create a fresh QueryClient for each test to ensure isolation:

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,        // Don't retry failed queries in tests
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

### Testing Components with useQuery

```typescript
import { render, screen, waitFor } from '../test/test-utils';

test('displays user data', async () => {
  // MSW handles the API mock
  render(<UserProfile userId="1" />);
  
  // Wait for loading to finish
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});

test('displays error state', async () => {
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

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUsers } from '../hooks/useUsers';

test('fetches users successfully', async () => {
  const queryClient = createTestQueryClient();
  
  const wrapper = ({ children }) => (
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

```typescript
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

### Pre-populating Query Cache

```typescript
test('renders with cached data', async () => {
  const { queryClient } = render(<UserProfile userId="1" />);
  
  // Pre-populate cache
  queryClient.setQueryData(['users', '1'], {
    id: '1',
    name: 'Cached User',
  });
  
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
  
  // Update user
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json({ id: '1', name: 'John Updated' });
    })
  );
  
  await user.click(screen.getByRole('button', { name: /refresh/i }));
  
  // Updated data
  expect(await screen.findByText('John Updated')).toBeInTheDocument();
});
```

## TanStack Router

### Router Test Setup

```typescript
import {
  createMemoryHistory,
  createRootRoute,
  createRoute,
  createRouter,
  RouterProvider,
} from '@tanstack/react-router';

export const rootRoute = createRootRoute({
  component: () => <Outlet />,
});

export function renderWithRouter(
  ui: React.ReactElement,
  options: {
    initialRoute?: string;
    routes?: AnyRoute[];
  } = {}
) {
  const { initialRoute = '/', routes = [] } = options;
  
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
  
  return {
    ...testingLibraryRender(<RouterProvider router={router} />),
    router,
  };
}
```

### Testing Navigation

```typescript
test('navigates to about page', async () => {
  const user = userEvent.setup();
  
  const aboutRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/about',
    component: () => <h1>About Page</h1>,
  });
  
  const { router } = renderWithRouter(<HomePage />, {
    routes: [aboutRoute],
  });
  
  expect(router.state.location.pathname).toBe('/');
  
  await user.click(screen.getByRole('link', { name: /about/i }));
  
  expect(router.state.location.pathname).toBe('/about');
  expect(screen.getByText('About Page')).toBeInTheDocument();
});
```

### Testing Dynamic Routes

```typescript
test('navigates to user detail', async () => {
  const user = userEvent.setup();
  
  const userRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/users/$userId',
    component: () => {
      const { userId } = userRoute.useParams();
      return <h1>User {userId}</h1>;
    },
  });
  
  const { router } = renderWithRouter(<UserList />, {
    routes: [userRoute],
  });
  
  await user.click(screen.getByRole('link', { name: /view user 123/i }));
  
  expect(router.state.location.pathname).toBe('/users/123');
});
```

### Testing Search Parameters

```typescript
test('applies search filter', async () => {
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
    initialRoute: '/search',
    routes: [searchRoute],
  });
  
  await user.type(screen.getByRole('textbox'), 'react');
  await user.click(screen.getByRole('button', { name: /search/i }));
  
  expect(router.state.location.search).toEqual({
    q: 'react',
    page: 1,
  });
});
```

### Testing Programmatic Navigation

```typescript
test('redirects after form submit', async () => {
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
test('redirects unauthenticated user', async () => {
  const loginRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/login',
    component: () => <h1>Login</h1>,
  });
  
  const { router } = renderWithRouter(<ProtectedDashboard />, {
    initialRoute: '/dashboard',
    routes: [loginRoute],
  });
  
  await waitFor(() => {
    expect(router.state.location.pathname).toBe('/login');
  });
});
```

### Testing Route Loaders

```typescript
test('renders loader data', async () => {
  const userRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: '/users/$userId',
    loader: async ({ params }) => {
      // MSW intercepts this
      const res = await fetch(`/api/users/${params.userId}`);
      return res.json();
    },
    component: () => {
      const data = userRoute.useLoaderData();
      return <h1>{data.name}</h1>;
    },
  });
  
  renderWithRouter(<div />, {
    initialRoute: '/users/1',
    routes: [userRoute],
  });
  
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});
```

## Combined Query + Router Testing

```typescript
test('full page with query and navigation', async () => {
  const user = userEvent.setup();
  
  const { queryClient, router } = render(<App />, {
    initialRoute: '/users',
  });
  
  // Data loads
  expect(await screen.findByText('John')).toBeInTheDocument();
  
  // Navigate to detail
  await user.click(screen.getByRole('link', { name: /view john/i }));
  
  expect(router.state.location.pathname).toBe('/users/1');
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});
```
