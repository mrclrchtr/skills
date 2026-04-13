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

// Chain once values with default fallback
const mockWithSequence = vi.fn()
  .mockReturnValue('default')
  .mockReturnValueOnce('first')
  .mockReturnValueOnce('second');

// First call returns 'first', second returns 'second', rest return 'default'
```

### Assert Mock Calls

```typescript
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('final');
expect(mockFn).toHaveBeenNthCalledWith(1, 'first');
expect(mockFn).toHaveBeenCalledOnce(); // Exactly once

// Assert return values
expect(mockFn).toHaveReturnedWith(42);
expect(mockFn).toHaveLastReturnedWith('result');

// Access call history directly
expect(mockFn.mock.calls).toEqual([['arg1'], ['arg2']]);
expect(mockFn.mock.lastCall).toEqual(['arg2']);
expect(mockFn.mock.results[0].value).toBe(42);
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

### Mock with Spy Option (Vitest 2.0+)

```typescript
// Keep original implementation but wrap in spies for assertions
vi.mock('./src/calculator.ts', { spy: true });

import { calculator } from './src/calculator.ts';

// Calls the REAL implementation but allows assertions
const result = calculator(1, 2);

expect(result).toBe(3); // Real result
expect(calculator).toHaveBeenCalledWith(1, 2);
expect(calculator).toHaveReturnedWith(3);
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

### Mock with Module Promise (Better Type Inference)

```typescript
// Module promise provides automatic type inference
vi.mock(import('./path/to/module.js'), async (importOriginal) => {
  const mod = await importOriginal();
  return {
    ...mod,
    total: vi.fn(),
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

### Using vi.hoisted for Mock Variables

```typescript
// Variables in vi.hoisted are available in vi.mock factories
// (vi.mock is hoisted, so normal variables are not accessible)
const { mockFetch, mockData } = vi.hoisted(() => {
  return {
    mockFetch: vi.fn(),
    mockData: { id: 1, name: 'Test' },
  };
});

vi.mock('./api', () => ({
  fetchData: mockFetch.mockResolvedValue(mockData),
}));

import { fetchData } from './api';

test('using hoisted mocks', async () => {
  const result = await fetchData();
  expect(result).toEqual(mockData);
  expect(mockFetch).toHaveBeenCalled();

  // Can change mock behavior in tests
  mockFetch.mockResolvedValueOnce({ id: 2, name: 'Updated' });
});
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

### Spy on Getters and Setters

```typescript
const cart = {
  get total() {
    return this._total;
  },
  set total(value) {
    this._total = value;
  },
  _total: 0,
};

// Spy on getter
const getSpy = vi.spyOn(cart, 'total', 'get').mockReturnValue(100);
expect(cart.total).toBe(100);

// Spy on setter
const setSpy = vi.spyOn(cart, 'total', 'set');
cart.total = 50;
expect(setSpy).toHaveBeenCalledWith(50);
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
  
  // Must re-import after stubbing for modules that read env at import time
  const { apiClient } = await import('../api');
  
  expect(apiClient.key).toBe('test-key-123');
});

test('throws when API key missing', async () => {
  vi.stubEnv('VITE_API_KEY', '');
  
  const { getConfig } = await import('../config');
  
  expect(() => getConfig()).toThrow('Missing API key');
});

// Works with both process.env AND import.meta.env
test('stub works on both env objects', () => {
  vi.stubEnv('NODE_ENV', 'production');

  expect(process.env.NODE_ENV).toBe('production');
  expect(import.meta.env.NODE_ENV).toBe('production');
});

// Use undefined to unset
test('unset env variable', () => {
  vi.stubEnv('API_KEY', undefined);
  expect(process.env.API_KEY).toBe(undefined);
});
```

## Global Stubbing

### Stub Global Values

```typescript
import { vi, afterEach, test } from 'vitest';

afterEach(() => {
  vi.unstubAllGlobals();
});

test('stub window dimensions', () => {
  vi.stubGlobal('innerWidth', 1024);
  vi.stubGlobal('innerHeight', 768);

  expect(innerWidth).toBe(1024);
  expect(globalThis.innerWidth).toBe(1024);
});

test('stub fetch', async () => {
  vi.stubGlobal('fetch', vi.fn(() =>
    Promise.resolve(new Response('{"data": "mock"}'))
  ));

  const response = await fetch('/api');
  expect(fetch).toHaveBeenCalledWith('/api');
});

test('stub IntersectionObserver', () => {
  const MockIntersectionObserver = vi.fn(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  }));

  vi.stubGlobal('IntersectionObserver', MockIntersectionObserver);

  const observer = new IntersectionObserver(() => {});
  expect(MockIntersectionObserver).toHaveBeenCalled();
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

test('setInterval execution', () => {
  let count = 0;
  setInterval(() => count++, 100);

  vi.advanceTimersByTime(350);

  expect(count).toBe(3); // 100ms, 200ms, 300ms
});
```

### Timer Control Methods

```typescript
vi.runAllTimers();           // Run all pending timers (including intervals)
vi.runOnlyPendingTimers();   // Run only currently pending (not new timers created)
vi.advanceTimersByTime(1000); // Advance by milliseconds
vi.advanceTimersToNextTimer(); // Advance to next scheduled timer

// Step through timers one at a time
test('step through timers', () => {
  const callback = vi.fn();
  setTimeout(callback, 100);
  setTimeout(callback, 200);

  vi.advanceTimersToNextTimer(); // First timer fires
  expect(callback).toHaveBeenCalledTimes(1);

  vi.advanceTimersToNextTimer(); // Second timer fires
  expect(callback).toHaveBeenCalledTimes(2);
});
```

### Mock System Time

```typescript
test('mock current date', () => {
  const date = new Date(2024, 0, 15, 12, 0, 0);
  vi.useFakeTimers();
  vi.setSystemTime(date);

  expect(new Date()).toEqual(date);
  expect(Date.now()).toBe(date.getTime());

  vi.useRealTimers();
});

test('business hours validation', () => {
  vi.useFakeTimers();

  // Test during business hours
  vi.setSystemTime(new Date(2024, 0, 15, 10, 0)); // 10 AM
  expect(isBusinessHours()).toBe(true);

  // Test outside business hours
  vi.setSystemTime(new Date(2024, 0, 15, 22, 0)); // 10 PM
  expect(isBusinessHours()).toBe(false);

  vi.useRealTimers();
});
```

## Module Reset

### Reset Between Tests

```typescript
import { vi, afterEach } from 'vitest';

afterEach(() => {
  vi.clearAllMocks();    // Clear call history, keep implementations
  vi.resetAllMocks();    // Reset call history AND implementations
  vi.restoreAllMocks();  // Restore spies to original implementations
  vi.resetModules();     // Clear module cache (for dynamic imports)
  vi.unstubAllEnvs();    // Remove env stubs
  vi.unstubAllGlobals(); // Remove global stubs
});
```

### Clear vs Reset vs Restore

```typescript
const mockFn = vi.fn().mockReturnValue(42);

mockFn();
mockFn();

// clearAllMocks - clears call history, KEEPS implementation
vi.clearAllMocks();
expect(mockFn).not.toHaveBeenCalled(); // true
expect(mockFn()).toBe(42); // still returns 42

// resetAllMocks - clears history AND resets implementation
vi.resetAllMocks();
expect(mockFn()).toBe(undefined); // no longer returns 42

// For vi.fn(impl), resetAllMocks restores to original impl:
const mockWithImpl = vi.fn(() => 'original');
mockWithImpl.mockReturnValue('mocked');
vi.resetAllMocks();
expect(mockWithImpl()).toBe('original'); // Back to original impl

// restoreAllMocks - restores spies to original (removes spy)
const spy = vi.spyOn(console, 'log').mockImplementation(() => {});
vi.restoreAllMocks();
// console.log is now the real function again
```

### Vitest Config for Auto-Reset

```typescript
// vitest.config.ts - enable automatic reset between tests
export default defineConfig({
  test: {
    clearMocks: true,    // vi.clearAllMocks() before each test
    mockReset: true,     // vi.resetAllMocks() before each test
    restoreMocks: true,  // vi.restoreAllMocks() before each test
    unstubEnvs: true,    // vi.unstubAllEnvs() before each test
    unstubGlobals: true, // vi.unstubAllGlobals() before each test
  },
});
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

// Only for trivial components - prefer explicit assertions
test('renders address', () => {
  const { container } = render(
    <AddressView address={{ street: '123 Main', city: 'NYC' }} />
  );
  
  // Saves to __snapshots__/file.test.ts.snap
  expect(container).toMatchSnapshot();

  // Named snapshots for multiple in one test
  expect(container.querySelector('.street')).toMatchSnapshot('street');
  expect(container.querySelector('.city')).toMatchSnapshot('city');
});

// Inline snapshot (better for small output - auto-updated by Vitest)
test('formats date', () => {
  expect(formatDate(new Date('2024-01-15'))).toMatchInlineSnapshot(`"January 15, 2024"`);
});

// File snapshot - compare against specific file
test('generated HTML matches template', async () => {
  const html = renderComponent();
  await expect(html).toMatchFileSnapshot('./snapshots/component.html');
});

// Error snapshots
test('error snapshot', () => {
  expect(() => {
    throw new Error('Something went wrong');
  }).toThrowErrorMatchingSnapshot();

  expect(() => {
    throw new Error('Inline error');
  }).toThrowErrorMatchingInlineSnapshot(`[Error: Inline error]`);
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

### Using vi.mocked (Recommended)

```typescript
import { vi, expect, test } from 'vitest';
import * as api from '../api';

vi.mock('../api');

test('handles user fetch', async () => {
  // vi.mocked is a type helper - returns same object with mock types
  vi.mocked(api.fetchUser).mockResolvedValue({ id: 1, name: 'John' });
  
  const result = await api.fetchUser(1);
  
  expect(result.name).toBe('John');
  expect(api.fetchUser).toHaveBeenCalledWith(1);
});
```

### Partial Mocking with vi.mocked

```typescript
// When mock doesn't return complete type
vi.mocked(api.fetchSomething, { partial: true }).mockResolvedValue({ 
  ok: false, 
  // Don't need to provide all Response properties
});

// Deep partial for nested objects
vi.mocked(api.getUser, { partial: true, deep: true }).mockReturnValue({
  address: { city: 'Los Angeles' },
  // Don't need to provide all User or Address properties
});
```

### Legacy: MockedFunction Type

```typescript
import { vi, type Mock } from 'vitest';
import { fetchUser } from '../api';

vi.mock('../api');

// For explicit type annotation (vi.mocked is usually cleaner)
const mockedFetchUser = fetchUser as Mock<typeof fetchUser>;

test('handles user fetch', async () => {
  mockedFetchUser.mockResolvedValue({ id: 1, name: 'John' });
  
  const result = await mockedFetchUser(1);
  
  expect(result.name).toBe('John');
});
```

### Type-Safe Class Instance Mocking

```typescript
import { vi } from 'vitest';

class Dog {
  speak() {
    return 'bark';
  }
}

vi.mock('./Dog');

test('mock class instance method', () => {
  const dog = new Dog();

  // vi.mocked wraps method in Mock<T> type
  vi.mocked(dog.speak).mockReturnValue('woof woof');

  expect(dog.speak()).toBe('woof woof');
});
```
