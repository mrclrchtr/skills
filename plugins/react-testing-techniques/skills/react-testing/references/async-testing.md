# Async Testing Patterns

Patterns for testing asynchronous behavior in React components.

## Core Async Utilities

### findBy Queries (Preferred for Elements)

Use `findBy*` when elements appear after async operations. These combine `getBy*` queries with `waitFor` internally:

```typescript
// Element appears after data fetch
const userName = await screen.findByText('John Doe');
expect(userName).toBeInTheDocument();

// With query options and waitFor options (separate arguments)
const slowElement = await screen.findByText(
  'Loaded',
  {},                    // query options
  { timeout: 3000 }      // waitFor options
);
```

`findBy*` automatically retries until the element appears or timeout (default: 1000ms).

### waitFor (For Assertions)

Use `waitFor` when you need to wait for non-element conditions. The callback must **throw an error** to trigger a retry; returning a falsy value is not sufficient:

```typescript
import { waitFor } from '@testing-library/react';

// Wait for mock to be called
await waitFor(() => {
  expect(mockSubmit).toHaveBeenCalledTimes(1);
});

// Wait for async operation that returns a promise
await waitFor(async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// Full options signature
await waitFor(
  () => expect(mockFn).toHaveBeenCalled(),
  {
    timeout: 2000,          // Max wait time (default: 1000ms)
    interval: 100,          // Retry interval (default: 50ms)
    onTimeout: (error) => { // Custom timeout handler
      error.message = `Timed out: ${error.message}`;
      return error;
    },
  }
);
```

**Best practice**: Use `findBy*` for elements, `waitFor` for non-element assertions like mock calls, state changes, or API responses.

### waitForElementToBeRemoved

Wait for elements to disappear from the DOM. This is a wrapper around `waitFor` optimized for element removal:

```typescript
import { waitForElementToBeRemoved } from '@testing-library/react';

// Preferred: Use a callback that returns the element
await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));

// Alternative: Pass the element directly (must exist when called)
const spinner = screen.getByRole('progressbar');
await waitForElementToBeRemoved(spinner);

// Then assert loaded content
expect(screen.getByText('Data loaded')).toBeInTheDocument();
```

**Important**: When using a callback, use `queryBy*` (returns null when not found). When passing an element directly, use `getBy*` to ensure the element exists initially.

## UserEvent with Async

### Always Setup and Await

All `userEvent` methods are async and must be awaited. The `setup()` call creates a shared session with keyboard and pointer state:

```typescript
import userEvent from '@testing-library/user-event';

test('form submission', async () => {
  const user = userEvent.setup();
  
  render(<LoginForm onSubmit={mockSubmit} />);
  
  // All actions share keyboard/pointer state within the session
  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.tab(); // Tab to next field
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /login/i }));
  
  await waitFor(() => {
    expect(mockSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});
```

### Common UserEvent Actions

```typescript
const user = userEvent.setup();

// Typing (clicks the element first by default)
await user.type(input, 'text');
await user.type(input, 'text', { skipClick: true }); // Don't click first
await user.clear(input);

// Clicking
await user.click(button);
await user.dblClick(element);
await user.tripleClick(textField); // Select all text

// Keyboard (requires element to be focused)
await user.keyboard('Hello World');     // Type text
await user.keyboard('{Enter}');         // Press Enter
await user.keyboard('{Shift>}A{/Shift}'); // Shift+A (types 'A')
await user.keyboard('{Control>}a{/Control}'); // Ctrl+A (select all)

// Selection
await user.selectOptions(select, ['option1', 'option2']);

// Pointer
await user.hover(element);
await user.unhover(element);

// Clipboard
await user.copy();
await user.paste();

// Tab navigation
await user.tab();
await user.tab({ shift: true }); // Shift+Tab
```

## Testing Loading States

```typescript
test('shows loading then content', async () => {
  render(<DataFetcher />);
  
  // Assert loading state appears
  expect(screen.getByText('Loading...')).toBeInTheDocument();
  
  // Wait for loading to complete
  await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));
  
  // Assert content appears
  expect(screen.getByText('Data loaded')).toBeInTheDocument();
});
```

## Testing with Fake Timers

### Setup Pattern

When using fake timers with `userEvent`, you **must** configure `advanceTimers` to prevent test timeouts. Do not use `delay: null` as it causes unexpected behavior:

```typescript
import { vi } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.runOnlyPendingTimers(); // Clean up pending timers
  vi.useRealTimers();
});
```

### Testing Debounced Input

```typescript
test('debounces search input', async () => {
  // REQUIRED: Connect userEvent to fake timers
  const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
  
  render(<SearchInput onSearch={mockSearch} debounceMs={300} />);
  
  await user.type(screen.getByRole('textbox'), 'test');
  
  // Not called immediately due to debounce
  expect(mockSearch).not.toHaveBeenCalled();
  
  // Advance past debounce delay
  vi.advanceTimersByTime(300);
  
  expect(mockSearch).toHaveBeenCalledWith('test');
});
```

### Jest Equivalent

```typescript
// In Jest, use jest.advanceTimersByTime
const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
```

## Testing Form Validation

```typescript
test('shows validation error on submit', async () => {
  const user = userEvent.setup();
  
  render(<RegistrationForm />);
  
  // Submit without filling required field
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  // Wait for validation error
  expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
});

test('clears error on valid input', async () => {
  const user = userEvent.setup();
  
  render(<RegistrationForm />);
  
  // Trigger error
  await user.click(screen.getByRole('button', { name: /submit/i }));
  expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
  
  // Fill valid input
  await user.type(screen.getByLabelText(/email/i), 'valid@email.com');
  
  // Wait for error to clear
  await waitFor(() => {
    expect(screen.queryByText(/email is required/i)).not.toBeInTheDocument();
  });
});
```

## Testing Toasts/Notifications

```typescript
test('shows success toast after action', async () => {
  const user = userEvent.setup();
  
  render(<ActionButton />);
  
  await user.click(screen.getByRole('button', { name: /save/i }));
  
  // Toast appears
  expect(await screen.findByRole('alert')).toHaveTextContent(/saved successfully/i);
  
  // Toast disappears (if auto-dismiss)
  await waitForElementToBeRemoved(() => screen.queryByRole('alert'), {
    timeout: 5000,
  });
});
```

## Handling act() Warnings

The "not wrapped in act()" warning indicates state updates happened after the test completed. This usually means an async operation was not properly awaited.

### Solution 1: Wait for the async result (Preferred)

```typescript
test('loads user data', async () => {
  render(<UserProfile userId="123" />);
  
  // Wait for the async operation to complete
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
});
```

### Solution 2: Mock the async operation

```typescript
test('displays placeholder before data loads', () => {
  // Mock the hook/API to return immediately
  vi.mocked(useUser).mockReturnValue({
    data: null,
    isLoading: true,
  });
  
  render(<UserProfile userId="123" />);
  
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

**Note**: React 18 logs `act()` warnings to `console.error`. React 19 logs them to `console.warn` and provides an `onCaughtError` option for error boundaries.

## Testing Error Boundaries

```typescript
test('error boundary catches error and shows fallback', () => {
  // Suppress expected error logging
  const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
  
  render(
    <ErrorBoundary fallback={<div>Something went wrong</div>}>
      <ComponentThatThrows />
    </ErrorBoundary>
  );
  
  expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  
  consoleSpy.mockRestore();
});

// React 19: Use onCaughtError to suppress error logging
render(
  <ErrorBoundary fallback={<div>Error</div>}>
    <ComponentThatThrows />
  </ErrorBoundary>,
  { onCaughtError: () => {} } // React 19 only
);
```

## Testing Infinite Scroll/Pagination

```typescript
test('loads more items on scroll', async () => {
  const user = userEvent.setup();
  
  render(<InfiniteList />);
  
  // Initial items
  expect(await screen.findAllByRole('listitem')).toHaveLength(10);
  
  // Scroll to bottom (trigger load more)
  const list = screen.getByRole('list');
  fireEvent.scroll(list, { target: { scrollTop: list.scrollHeight } });
  
  // Wait for more items
  await waitFor(() => {
    expect(screen.getAllByRole('listitem')).toHaveLength(20);
  });
});
```

## Anti-Patterns

### Don't Use waitFor for Element Queries

```typescript
// ❌ Wrong - unnecessary wrapper
await waitFor(() => {
  expect(screen.getByText('Hello')).toBeInTheDocument();
});

// ✅ Correct - findBy handles waiting
expect(await screen.findByText('Hello')).toBeInTheDocument();
```

### Don't Mix Sync and Async Unnecessarily

```typescript
// ❌ Wrong - sync element doesn't need await
const button = await screen.findByRole('button'); // Already rendered

// ✅ Correct - use getBy for sync elements
const button = screen.getByRole('button');
```

### Don't Forget to Await UserEvent

```typescript
// ❌ Wrong - missing await
user.click(button);
expect(mockFn).toHaveBeenCalled(); // May fail - click not complete

// ✅ Correct - await the action
await user.click(button);
await waitFor(() => expect(mockFn).toHaveBeenCalled());
```

### Don't Use Fixed Timeouts

```typescript
// ❌ Wrong - brittle, slow
await new Promise(r => setTimeout(r, 1000));
expect(screen.getByText('Done')).toBeInTheDocument();

// ✅ Correct - wait for actual condition
expect(await screen.findByText('Done')).toBeInTheDocument();
```

### Don't Return Falsy Values in waitFor

```typescript
// ❌ Wrong - returning false doesn't trigger retry
await waitFor(() => {
  return screen.queryByText('Hello') !== null; // Just returns false
});

// ✅ Correct - throw an error to trigger retry
await waitFor(() => {
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

### Don't Use delay: null with Fake Timers

```typescript
// ❌ Wrong - causes unexpected behavior
const user = userEvent.setup({ delay: null });

// ✅ Correct - use advanceTimers option
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
```

### Don't Perform Side Effects in waitFor Callbacks

```typescript
// ❌ Wrong - side effects run multiple times
await waitFor(() => {
  fireEvent.click(button); // Clicks multiple times during retries!
  expect(count).toBe(1);
});

// ✅ Correct - perform action before waitFor
await user.click(button);
await waitFor(() => {
  expect(count).toBe(1);
});
```
