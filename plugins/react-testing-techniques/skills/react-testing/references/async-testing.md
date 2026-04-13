# Async Testing Patterns

Patterns for testing asynchronous behavior in React components.

## Core Async Utilities

### findBy Queries (Preferred for Elements)

Use `findBy*` when elements appear after async operations:

```typescript
// Element appears after data fetch
const userName = await screen.findByText('John Doe');
expect(userName).toBeInTheDocument();

// With custom timeout (default: 1000ms)
const slowElement = await screen.findByText('Loaded', {}, { timeout: 3000 });
```

`findBy*` automatically retries until the element appears or timeout.

### waitFor (For Assertions)

Use `waitFor` for assertions that need to wait:

```typescript
import { waitFor } from '@testing-library/react';

// Wait for mock to be called
await waitFor(() => {
  expect(mockSubmit).toHaveBeenCalledTimes(1);
});

// Wait for state change
await waitFor(() => {
  expect(screen.getByText('Success')).toBeInTheDocument();
});

// With options
await waitFor(
  () => expect(mockFn).toHaveBeenCalled(),
  { timeout: 2000, interval: 100 }
);
```

**Best practice**: Use `findBy*` for elements, `waitFor` for non-element assertions.

### waitForElementToBeRemoved

Wait for elements to disappear:

```typescript
import { waitForElementToBeRemoved } from '@testing-library/react';

// Wait for loading to finish
await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));

// Then assert loaded content
expect(screen.getByText('Data loaded')).toBeInTheDocument();
```

Must use `queryBy*` (returns null) not `getBy*` (throws).

## UserEvent with Async

### Always Setup and Await

```typescript
import userEvent from '@testing-library/user-event';

test('form submission', async () => {
  const user = userEvent.setup();
  
  render(<LoginForm onSubmit={mockSubmit} />);
  
  // All userEvent methods are async
  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
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

// Typing
await user.type(input, 'text');
await user.clear(input);

// Clicking
await user.click(button);
await user.dblClick(element);
await user.tripleClick(textField); // Select all text

// Keyboard
await user.keyboard('{Enter}');
await user.keyboard('{Shift>}A{/Shift}'); // Shift+A
await user.keyboard('[ControlLeft>][KeyA][/ControlLeft]'); // Ctrl+A

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

## Testing Debounced Input

```typescript
import { vi } from 'vitest';

test('debounces search input', async () => {
  vi.useFakeTimers();
  const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
  
  render(<SearchInput onSearch={mockSearch} />);
  
  await user.type(screen.getByRole('textbox'), 'test');
  
  // Not called immediately due to debounce
  expect(mockSearch).not.toHaveBeenCalled();
  
  // Advance past debounce delay
  vi.advanceTimersByTime(300);
  
  expect(mockSearch).toHaveBeenCalledWith('test');
  
  vi.useRealTimers();
});
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
