# Query Selection Guide

Choose the right React Testing Library query based on the scenario.

## Query Type Matrix

| Query Type | No Match | 1 Match | Multiple Matches | Async? |
|------------|----------|---------|------------------|--------|
| `getBy*` | Throws | Returns element | Throws | No |
| `queryBy*` | Returns null | Returns element | Throws | No |
| `findBy*` | Throws | Returns element | Throws | Yes |
| `getAllBy*` | Throws | Returns array | Returns array | No |
| `queryAllBy*` | Returns [] | Returns array | Returns array | No |
| `findAllBy*` | Throws | Returns array | Returns array | Yes |

## Decision Guide

### Element Exists Now → Use `getBy*`

For elements that should be immediately present:

```typescript
// Element is rendered synchronously
const button = screen.getByRole('button', { name: /submit/i });
expect(button).toBeInTheDocument();
```

Fails immediately if element not found - good for fast feedback.

### Element Appears Later → Use `findBy*`

For elements that appear after async operations (data fetching, animations):

```typescript
// Wait for element to appear (default timeout: 1000ms)
const message = await screen.findByText('Success!');
expect(message).toBeInTheDocument();
```

Always use with `await`. Retries until element appears or timeout.

### Assert Element Does NOT Exist → Use `queryBy*`

For asserting absence:

```typescript
// Element should not be present
expect(screen.queryByText('Error')).not.toBeInTheDocument();

// Alternative: toBeNull()
expect(screen.queryByRole('alert')).toBeNull();
```

Never use `getBy*` to assert absence - it throws before the assertion.

### Multiple Elements Expected → Use `*AllBy*`

When expecting an array of elements:

```typescript
// Multiple items rendered
const items = screen.getAllByRole('listitem');
expect(items).toHaveLength(5);

// Async version
const rows = await screen.findAllByRole('row');
expect(rows).toHaveLength(10);
```

## Query Priority (Accessibility First)

Use queries in this order for best accessibility:

### 1. `getByRole` (Preferred)

Queries by ARIA role - most accessible, tests what assistive tech sees:

```typescript
// Buttons
screen.getByRole('button', { name: /submit/i });

// Links
screen.getByRole('link', { name: /home/i });

// Headings
screen.getByRole('heading', { level: 1 });

// Form elements
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('checkbox', { name: /agree/i });
screen.getByRole('combobox', { name: /country/i });

// Navigation
screen.getByRole('navigation');
screen.getByRole('main');
```

### 2. `getByLabelText`

For form fields with labels:

```typescript
screen.getByLabelText(/email address/i);
screen.getByLabelText(/password/i);
```

### 3. `getByPlaceholderText`

When placeholder is the only identifier:

```typescript
screen.getByPlaceholderText(/search/i);
```

### 4. `getByText`

For non-interactive text content:

```typescript
screen.getByText(/welcome back/i);
screen.getByText(/no results found/i);
```

### 5. `getByDisplayValue`

For current input values:

```typescript
screen.getByDisplayValue('current@email.com');
```

### 6. `getByAltText`

For images:

```typescript
screen.getByAltText(/company logo/i);
```

### 7. `getByTitle`

For elements with title attribute:

```typescript
screen.getByTitle(/close modal/i);
```

### 8. `getByTestId` (Last Resort)

Only when no semantic query works:

```typescript
// Avoid if possible
screen.getByTestId('custom-component');
```

## Common Patterns

### Check Element Visibility

```typescript
// Present in DOM
expect(screen.getByText('Hello')).toBeInTheDocument();

// Visible (not hidden)
expect(screen.getByText('Hello')).toBeVisible();
```

### Wait for Element to Disappear

```typescript
import { waitForElementToBeRemoved } from '@testing-library/react';

// Wait for loading to finish
await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));
```

### Within a Container

```typescript
import { within } from '@testing-library/react';

const dialog = screen.getByRole('dialog');
const submitButton = within(dialog).getByRole('button', { name: /submit/i });
```

### Case-Insensitive Matching

Use regex with `i` flag:

```typescript
screen.getByText(/submit/i);
screen.getByRole('button', { name: /submit/i });
```

### Partial Text Matching

```typescript
// Matches "Welcome, John!" or "Welcome, Jane!"
screen.getByText(/welcome/i);

// Exact match
screen.getByText('Welcome, John!');
```

## Anti-Patterns

### Don't Use getBy* for Absence Assertions

```typescript
// ❌ Wrong - throws before assertion
expect(screen.getByText('Error')).not.toBeInTheDocument();

// ✅ Correct - returns null if not found
expect(screen.queryByText('Error')).not.toBeInTheDocument();
```

### Don't Use queryBy* When Element Should Exist

```typescript
// ❌ Wrong - doesn't fail if element missing
const button = screen.queryByRole('button');
userEvent.click(button!);

// ✅ Correct - fails immediately if missing
const button = screen.getByRole('button');
await userEvent.click(button);
```

### Don't Use findBy* Unnecessarily

```typescript
// ❌ Wrong - adds unnecessary wait for sync element
const header = await screen.findByRole('heading');

// ✅ Correct - immediate for sync elements
const header = screen.getByRole('heading');
```

### Don't Use getByTestId as Default

```typescript
// ❌ Wrong - skips accessibility
screen.getByTestId('submit-btn');

// ✅ Correct - tests accessibility
screen.getByRole('button', { name: /submit/i });
```

## Debugging Queries

When queries fail, use `screen.debug()`:

```typescript
test('shows user name', () => {
  render(<UserProfile />);
  
  // Print the DOM to console
  screen.debug();
  
  // Or specific element
  screen.debug(screen.getByRole('main'));
});
```

Use `logRoles` to see available roles:

```typescript
import { logRoles } from '@testing-library/react';

test('find available roles', () => {
  const { container } = render(<MyComponent />);
  logRoles(container);
});
```
