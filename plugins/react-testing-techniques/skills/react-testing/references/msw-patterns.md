# MSW Patterns

Mock Service Worker v2 patterns for API mocking in tests.

## Setup

### Server Configuration

```typescript
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Test Setup Integration

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from '../mocks/server';

beforeAll(() => {
  server.listen({ onUnhandledRequest: 'error' });
});

afterEach(() => {
  cleanup();
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
```

## Handler Syntax (v2)

### GET Request

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' },
    ]);
  }),
];
```

### GET with Path Parameters

```typescript
http.get('/api/users/:id', ({ params }) => {
  const { id } = params;
  return HttpResponse.json({ id, name: 'John Doe' });
});
```

### GET with Query Parameters

```typescript
http.get('/api/search', ({ request }) => {
  const url = new URL(request.url);
  const query = url.searchParams.get('q');
  const limit = url.searchParams.get('limit') || '10';
  
  return HttpResponse.json({
    query,
    results: [],
    limit: parseInt(limit),
  });
});
```

### POST Request

```typescript
http.post('/api/users', async ({ request }) => {
  const body = await request.json();
  
  return HttpResponse.json(
    { id: Date.now(), ...body },
    { status: 201 }
  );
});
```

### PUT/PATCH Request

```typescript
http.put('/api/users/:id', async ({ params, request }) => {
  const { id } = params;
  const updates = await request.json();
  
  return HttpResponse.json({ id, ...updates });
});

http.patch('/api/users/:id', async ({ params, request }) => {
  const { id } = params;
  const updates = await request.json();
  
  return HttpResponse.json({ id, ...updates });
});
```

### DELETE Request

```typescript
http.delete('/api/users/:id', ({ params }) => {
  return new HttpResponse(null, { status: 204 });
});
```

## Response Helpers

### JSON Response

```typescript
// Basic JSON
HttpResponse.json({ data: 'value' });

// With status code
HttpResponse.json({ data: 'value' }, { status: 201 });

// With headers
HttpResponse.json(data, {
  headers: {
    'X-Custom-Header': 'value',
  },
});
```

### Text Response

```typescript
HttpResponse.text('Plain text response');
```

### Empty Response

```typescript
new HttpResponse(null, { status: 204 });
```

### Error Response

```typescript
HttpResponse.json(
  { error: 'Not found', message: 'User does not exist' },
  { status: 404 }
);
```

## Per-Test Handler Override

Override default handlers for specific test scenarios:

```typescript
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('handles API error gracefully', async () => {
  // Override handler for this test only
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    })
  );
  
  render(<UserList />);
  
  expect(await screen.findByText(/error/i)).toBeInTheDocument();
});

test('handles empty response', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json([]);
    })
  );
  
  render(<UserList />);
  
  expect(await screen.findByText(/no users/i)).toBeInTheDocument();
});
```

## Testing Different States

### Loading State

Test by delaying the response:

```typescript
import { delay, http, HttpResponse } from 'msw';

test('shows loading state', async () => {
  server.use(
    http.get('/api/users', async () => {
      await delay(100);
      return HttpResponse.json([]);
    })
  );
  
  render(<UserList />);
  
  expect(screen.getByText('Loading...')).toBeInTheDocument();
  
  await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));
});
```

### Error States

```typescript
test('shows 404 error', async () => {
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    })
  );
  
  render(<UserProfile userId="999" />);
  
  expect(await screen.findByText(/not found/i)).toBeInTheDocument();
});

test('shows network error', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.error();
    })
  );
  
  render(<UserList />);
  
  expect(await screen.findByText(/network error/i)).toBeInTheDocument();
});
```

### Validation Errors

```typescript
test('shows validation errors', async () => {
  server.use(
    http.post('/api/users', () => {
      return HttpResponse.json(
        {
          errors: {
            email: 'Invalid email format',
            password: 'Password too short',
          },
        },
        { status: 422 }
      );
    })
  );
  
  render(<RegistrationForm />);
  
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));
  
  expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
});
```

## Request Assertions

### Verify Request Was Made

```typescript
import { http, HttpResponse } from 'msw';

test('sends correct data', async () => {
  let capturedBody: unknown;
  
  server.use(
    http.post('/api/users', async ({ request }) => {
      capturedBody = await request.json();
      return HttpResponse.json({ id: 1 }, { status: 201 });
    })
  );
  
  render(<CreateUserForm />);
  
  await userEvent.type(screen.getByLabelText(/name/i), 'John');
  await userEvent.click(screen.getByRole('button', { name: /create/i }));
  
  await waitFor(() => {
    expect(capturedBody).toEqual({ name: 'John' });
  });
});
```

### Verify Headers

```typescript
test('sends auth header', async () => {
  let authHeader: string | null;
  
  server.use(
    http.get('/api/protected', ({ request }) => {
      authHeader = request.headers.get('Authorization');
      return HttpResponse.json({ data: 'secret' });
    })
  );
  
  render(<ProtectedComponent />);
  
  await waitFor(() => {
    expect(authHeader).toBe('Bearer test-token');
  });
});
```

## One-Time Handlers

Handler that responds once then removes itself:

```typescript
server.use(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1 }]);
  }, { once: true })
);
```

## Base URL Handling

For APIs with base URLs:

```typescript
const API_BASE = 'https://api.example.com';

export const handlers = [
  http.get(`${API_BASE}/users`, () => {
    return HttpResponse.json([]);
  }),
];
```

Or use path patterns:

```typescript
http.get('*/api/users', () => {
  return HttpResponse.json([]);
});
```
