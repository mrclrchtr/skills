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

### Unhandled Request Strategies

```typescript
// Throw error on unhandled requests (recommended for tests)
server.listen({ onUnhandledRequest: 'error' });

// Warn but don't fail
server.listen({ onUnhandledRequest: 'warn' });

// Silently bypass
server.listen({ onUnhandledRequest: 'bypass' });

// Custom handler for selective bypass
server.listen({
  onUnhandledRequest(request, print) {
    if (request.url.includes('cdn.com')) {
      return; // Ignore CDN requests
    }
    print.warning();
  },
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

## TypeScript Support

### Typed Request Handlers

```typescript
import { http, HttpResponse } from 'msw';

type UserParams = {
  userId: string;
};

type CreateUserBody = {
  name: string;
  email: string;
};

type UserResponse = {
  id: string;
  name: string;
  email: string;
};

// Fully typed handler with generics
http.post<UserParams, CreateUserBody, UserResponse, '/users/:userId'>(
  '/users/:userId',
  async ({ params, request }) => {
    const { userId } = params; // typed as string
    const body = await request.json(); // typed as CreateUserBody

    return HttpResponse.json({
      id: userId,
      name: body.name,
      email: body.email,
    });
  }
);
```

### Abstracting Handlers with HttpResponseResolver

```typescript
import { http, HttpResponseResolver, HttpResponse } from 'msw';

type ApiRequest = { transactionId: string };
type ApiResponse = { transactionId: string; success: boolean };

function createApiHandler(
  resolver: HttpResponseResolver<never, ApiRequest, ApiResponse>
) {
  return http.post('https://api.example.com/endpoint', resolver);
}

export const handlers = [
  createApiHandler(async ({ request }) => {
    const data = await request.json();
    return HttpResponse.json({
      transactionId: data.transactionId,
      success: true,
    });
  }),
];
```

## GraphQL Handlers

### Query Handler

```typescript
import { graphql, HttpResponse } from 'msw';

export const handlers = [
  graphql.query('GetUser', ({ variables }) => {
    const { userId } = variables;

    return HttpResponse.json({
      data: {
        user: {
          id: userId,
          name: 'John Doe',
        },
      },
    });
  }),
];
```

### Mutation Handler

```typescript
graphql.mutation('UpdateUser', ({ variables, cookies, operationName }) => {
  console.log('Operation:', operationName);
  console.log('Cookies:', cookies);

  return HttpResponse.json({
    data: {
      updateUser: {
        success: true,
        user: variables.input,
      },
    },
  });
});
```

### GraphQL Error Response

```typescript
graphql.query('GetUser', () => {
  return HttpResponse.json({
    errors: [
      {
        message: 'User not found',
        extensions: { code: 'NOT_FOUND' },
      },
    ],
  });
});
```

## Passthrough and Bypass

### Passthrough Requests

Use `passthrough()` to let specific requests proceed to the actual server:

```typescript
import { http, passthrough, HttpResponse } from 'msw';

http.get('/resource', ({ request }) => {
  // Conditionally pass through based on headers
  if (request.headers.has('x-bypass-mock')) {
    return passthrough();
  }

  return HttpResponse.json({ mocked: true });
});
```

### Bypass for Response Patching

Use `bypass()` to fetch real data and modify it:

```typescript
import { http, HttpResponse, bypass } from 'msw';

http.get('/user', async ({ request }) => {
  // Fetch the real response
  const response = await fetch(bypass(request));
  const realUser = await response.json();

  // Patch with mocked data
  return HttpResponse.json({
    ...realUser,
    lastName: 'Mocked',
  });
});
```

## Advanced Response Types

### FormData Response

```typescript
http.post('/upload', () => {
  const form = new FormData();
  form.append('id', 'abc-123');
  form.append('status', 'uploaded');

  return HttpResponse.formData(form);
});
```

### Binary/ArrayBuffer Response

```typescript
http.get('/file', () => {
  const buffer = new ArrayBuffer(8);

  return HttpResponse.arrayBuffer(buffer, {
    headers: {
      'Content-Type': 'application/octet-stream',
    },
  });
});
```

### Streaming Response

```typescript
http.get('/stream', () => {
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(new TextEncoder().encode('chunk1'));
      controller.enqueue(new TextEncoder().encode('chunk2'));
      controller.close();
    },
  });

  return new HttpResponse(stream, {
    headers: { 'Content-Type': 'text/plain' },
  });
});
```

### Streaming with Delays

```typescript
import { http, HttpResponse, delay } from 'msw';

http.get('/video', () => {
  const stream = new ReadableStream({
    async start(controller) {
      controller.enqueue(new Uint8Array([1, 2, 3]));
      await delay(1000);
      controller.enqueue(new Uint8Array([4, 5, 6]));
      await delay(200);
      controller.close();
    },
  });

  return new HttpResponse(stream, {
    headers: { 'Content-Type': 'video/mp4' },
  });
});
```

### Server-Sent Events (SSE)

```typescript
import { sse } from 'msw';

export const handlers = [
  sse('/events', ({ client }) => {
    client.send({
      data: 'hello world',
      event: 'message',
      id: '1',
    });

    // Close the connection after sending
    queueMicrotask(() => client.close());
  }),
];
```

## Cookies

### Setting Response Cookies

```typescript
http.post('/login', () => {
  return new HttpResponse(null, {
    headers: {
      'Set-Cookie': 'authToken=abc-123; HttpOnly; Secure',
    },
  });
});
```

### Reading Request Cookies

```typescript
http.get('/protected', ({ cookies }) => {
  if (!cookies.authToken) {
    return HttpResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return HttpResponse.json({ data: 'secret' });
});
```

## Lifecycle Events

### Monitoring Requests

```typescript
server.events.on('request:start', ({ request, requestId }) => {
  console.log('Outgoing:', request.method, request.url);
});

server.events.on('response:mocked', ({ request, response }) => {
  console.log(`${request.method} ${request.url} -> ${response.status}`);
});
```

### Handling Errors in Resolvers

```typescript
server.events.on('unhandledException', ({ request, error }) => {
  console.error(`Handler error for ${request.url}:`, error);
});
```

### Reading Request Body in Events

```typescript
server.events.on('request:start', async ({ request }) => {
  // Clone before reading to avoid consuming the body
  const payload = await request.clone().text();
  console.log('Request body:', payload);
});
```

## Global Response Delay

Apply delay to all handlers:

```typescript
import { http, delay, HttpResponse } from 'msw';

export const handlers = [
  // Catch-all handler runs first, delays, then falls through
  http.all('*', async () => {
    await delay(500);
    // No return = falls through to next matching handler
  }),

  http.get('/users', () => {
    return HttpResponse.json([]);
  }),
];
```

## Best Practices

### Validate Request Data in Handlers (Not Tests)

Instead of asserting request data in tests, validate in handlers:

```typescript
// Good: Handler validates and returns appropriate response
http.post('/login', async ({ request }) => {
  const data = await request.formData();
  const email = data.get('email');

  if (!email) {
    return new HttpResponse('Missing email', { status: 400 });
  }

  return HttpResponse.json({ token: 'abc-123' });
});

// Test: Verify UI behavior based on response
test('shows error when email missing', async () => {
  render(<LoginForm />);
  await userEvent.click(screen.getByRole('button', { name: /login/i }));

  // UI assertion - the handler returns 400, component shows error
  expect(await screen.findByText(/missing email/i)).toBeInTheDocument();
});
```

### Use onUnhandledRequest: 'error' in Tests

This ensures all API calls have explicit handlers:

```typescript
beforeAll(() => {
  server.listen({ onUnhandledRequest: 'error' });
});
```

### Reading FormData from Requests

```typescript
http.post('/upload', async ({ request }) => {
  const formData = await request.clone().formData();
  const file = formData.get('file') as File;

  console.log('Uploaded file:', file.name);

  return HttpResponse.json({ filename: file.name, size: file.size });
});
```
