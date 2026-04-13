# Vitest Patterns

Vitest-specific mocking, spying, and testing patterns. Use these instead of Jest equivalents.

## Function Mocking

### Create Mock Function

```typescript
import { vi, expect, test } from 'vitest';

const mockFn = vi.fn();

// With implementation
const mockAdd = vi.fn((a: number, b: number) => a + b);

// With return value
const mockGetUser = vi.fn().mockReturnValue({ id: 1, name: 'John' });

// With resolved value (async)
const mockFetchUser = vi.fn().mockResolvedValue({ id: 1, name: 'John' });

// With rejected value
const mockFailingFetch = vi.fn().mockRejectedValue(new Error('Network error'));
```

### Assert Mock Calls

```typescript
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('final');
expect(mockFn).toHaveBeenNthCalledWith(1, 'first');
```

## Module Mocking

### Mock Entire Module

```typescript
import { vi } from 'vitest';

// Auto-mock all exports
vi.mock('../services/api');

// With implementation
vi.mock('../services/api', () => ({
  fetchUsers: vi.fn().mockResolvedValue([]),
  createUser: vi.fn().mockResolvedValue({ id: 1 }),
}));
```

### Mock Partial Module

```typescript
vi.mock('../utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../utils')>();
  return {
    ...actual,
    formatDate: vi.fn().mockReturnValue('2024-01-01'),
  };
});
```

### Mock with Factory

```typescript
vi.mock('../config', () => ({
  default: {
    apiUrl: 'http://test-api.com',
    timeout: 1000,
  },
}));
```

## Spying

### Spy on Object Method

```typescript
import { vi } from 'vitest';
import { userService } from '../services/user';

const spy = vi.spyOn(userService, 'getUser');

// With mock implementation
vi.spyOn(userService, 'getUser').mockResolvedValue({ id: 1 });

// Restore original
spy.mockRestore();
```

### Spy on Console

```typescript
// Suppress console.error in test
const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

// After test
consoleSpy.mockRestore();
// Or use vi.restoreAllMocks() in afterEach
```

## Environment Variables

### Stub Environment Variables

```typescript
import { vi, afterEach, test } from 'vitest';

afterEach(() => {
  vi.unstubAllEnvs();
  vi.resetModules();
});

test('uses API key from env', async () => {
  vi.stubEnv('VITE_API_KEY', 'test-key-123');
  
  // Must re-import after stubbing
  const { apiClient } = await import('../api');
  
  expect(apiClient.key).toBe('test-key-123');
});

test('throws when API key missing', async () => {
  vi.stubEnv('VITE_API_KEY', '');
  
  const { getConfig } = await import('../config');
  
  expect(() => getConfig()).toThrow('Missing API key');
});
```

## Timers

### Fake Timers

```typescript
import { vi, beforeEach, afterEach, test } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

test('debounces input', async () => {
  const callback = vi.fn();
  const debouncedFn = debounce(callback, 300);
  
  debouncedFn('first');
  debouncedFn('second');
  
  expect(callback).not.toHaveBeenCalled();
  
  vi.advanceTimersByTime(300);
  
  expect(callback).toHaveBeenCalledOnce();
  expect(callback).toHaveBeenCalledWith('second');
});
```

### Run All Timers

```typescript
vi.runAllTimers();      // Run all pending timers
vi.runOnlyPendingTimers(); // Run only currently pending
vi.advanceTimersByTime(1000); // Advance by milliseconds
```

## Module Reset

### Reset Between Tests

```typescript
import { vi, afterEach } from 'vitest';

afterEach(() => {
  vi.resetAllMocks();    // Reset mock call history
  vi.restoreAllMocks();  // Restore original implementations
  vi.resetModules();     // Clear module cache
  vi.unstubAllEnvs();    // Remove env stubs
});
```

### Clear vs Reset vs Restore

```typescript
const mockFn = vi.fn().mockReturnValue(42);

mockFn();
mockFn();

// clearAllMocks - clears call history, keeps implementation
vi.clearAllMocks();
expect(mockFn).not.toHaveBeenCalled(); // true
expect(mockFn()).toBe(42); // still returns 42

// resetAllMocks - clears history AND implementation
vi.resetAllMocks();
expect(mockFn()).toBe(undefined); // no longer returns 42

// restoreAllMocks - restores spies to original
vi.restoreAllMocks();
```

## Dynamic Imports

### Test Dynamic Imports

```typescript
test('loads module dynamically', async () => {
  vi.stubEnv('FEATURE_FLAG', 'true');
  vi.resetModules();
  
  // Import fresh copy with new env
  const { featureEnabled } = await import('../features');
  
  expect(featureEnabled).toBe(true);
});
```

## Snapshot Testing (Use Sparingly)

```typescript
import { expect, test } from 'vitest';
import { render } from '../test/test-utils';

// Only for trivial components
test('renders address', () => {
  const { container } = render(
    <AddressView address={{ street: '123 Main', city: 'NYC' }} />
  );
  
  expect(container).toMatchSnapshot();
});

// Inline snapshot (better for small output)
test('formats date', () => {
  expect(formatDate(new Date('2024-01-15'))).toMatchInlineSnapshot(`"January 15, 2024"`);
});
```

## Testing Thrown Errors

```typescript
test('throws on invalid input', () => {
  expect(() => validateInput(null)).toThrow('Input required');
  expect(() => validateInput(null)).toThrowError(/required/i);
});

// Async errors
test('rejects with error', async () => {
  await expect(fetchInvalidUser()).rejects.toThrow('User not found');
});
```

## Type-Safe Mocking

```typescript
import { vi, type MockedFunction } from 'vitest';
import { fetchUser } from '../api';

vi.mock('../api');

const mockedFetchUser = fetchUser as MockedFunction<typeof fetchUser>;

test('handles user fetch', async () => {
  mockedFetchUser.mockResolvedValue({ id: 1, name: 'John' });
  
  const result = await mockedFetchUser(1);
  
  expect(result.name).toBe('John');
});
```
