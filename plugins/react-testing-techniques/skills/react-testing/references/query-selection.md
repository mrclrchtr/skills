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

// Configure timeout for slow operations
const data = await screen.findByRole('table', {}, { timeout: 3000 });
```

Always use with `await`. `findBy*` combines `getBy*` with `waitFor` internally.

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

Use queries in this order for best accessibility. Prefer queries that reflect how users interact with your app.

### 1. `getByRole` (Preferred)

Queries by ARIA role - most accessible, tests what assistive tech sees. Should be your default choice.

```typescript
// Buttons
screen.getByRole('button', { name: /submit/i });

// Links
screen.getByRole('link', { name: /home/i });

// Headings
screen.getByRole('heading', { level: 1 });
screen.getByRole('heading', { name: /welcome/i });

// Form elements
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('checkbox', { name: /agree/i });
screen.getByRole('combobox', { name: /country/i });
screen.getByRole('spinbutton', { name: /quantity/i }); // number input

// Navigation & landmarks
screen.getByRole('navigation');
screen.getByRole('main');
screen.getByRole('banner'); // header
screen.getByRole('contentinfo'); // footer

// Lists and tables
screen.getByRole('list');
screen.getByRole('listitem');
screen.getByRole('table');
screen.getByRole('row');
screen.getByRole('cell');

// Dialogs and alerts
screen.getByRole('dialog');
screen.getByRole('alertdialog');
screen.getByRole('alert');
```

#### `getByRole` Options

Filter by accessibility state for precise queries:

```typescript
// By accessible name (aria-label, visible text, associated label)
screen.getByRole('button', { name: /submit/i });

// By accessible description (aria-describedby)
screen.getByRole('textbox', { description: /required field/i });

// By state attributes
screen.getByRole('checkbox', { checked: true });
screen.getByRole('button', { pressed: true });
screen.getByRole('tab', { selected: true });
screen.getByRole('combobox', { expanded: true });
screen.getByRole('region', { busy: true });
screen.getByRole('link', { current: 'page' });

// By heading level
screen.getByRole('heading', { level: 2 });

// Include hidden elements (for performance or testing hidden content)
screen.getByRole('button', { name: /open/i, hidden: true });
```

### 2. `getByLabelText`

For form fields with associated labels - mimics how users navigate forms:

```typescript
screen.getByLabelText(/email address/i);
screen.getByLabelText(/password/i);

// Works with aria-label too
screen.getByLabelText(/search/i);
```

### 3. `getByPlaceholderText`

When placeholder is the only identifier (prefer proper labels when possible):

```typescript
screen.getByPlaceholderText(/search/i);
```

### 4. `getByText`

For non-interactive text content:

```typescript
screen.getByText(/welcome back/i);
screen.getByText(/no results found/i);
```

Tip: For buttons and links, prefer `getByRole` with `name` option over `getByText`.

### 5. `getByDisplayValue`

For current input/select/textarea values:

```typescript
screen.getByDisplayValue('current@email.com');
screen.getByDisplayValue(/option 1/i);
```

### 6. `getByAltText`

For images:

```typescript
screen.getByAltText(/company logo/i);
```

### 7. `getByTitle`

For elements with title attribute (less common):

```typescript
screen.getByTitle(/close modal/i);
```

### 8. `getByTestId` (Last Resort)

Only when no semantic query works. Does not test accessibility:

```typescript
// Use sparingly - custom components, complex layouts
screen.getByTestId('data-grid');
screen.getByTestId('chart-canvas');
```

## Common Patterns

### Check Element Visibility

```typescript
// Present in DOM (may be hidden)
expect(screen.getByText('Hello')).toBeInTheDocument();

// Visible (not hidden by CSS or attributes)
expect(screen.getByText('Hello')).toBeVisible();

// toBeVisible checks: display, visibility, opacity, hidden attribute
// Use toBeInTheDocument when you only care about DOM presence
```

### Wait for Element to Disappear

```typescript
import { waitForElementToBeRemoved } from '@testing-library/react';

// Wait for loading spinner to finish
await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));

// Alternative: wait for element to be removed by reference
const spinner = screen.getByRole('status');
await waitForElementToBeRemoved(spinner);
```

### Wait for Arbitrary Conditions

```typescript
import { waitFor } from '@testing-library/react';

// Wait until callback doesn't throw (default timeout: 1000ms)
await waitFor(() => expect(mockFn).toHaveBeenCalled());

// Custom timeout and interval
await waitFor(() => expect(screen.getByText('Done')).toBeVisible(), {
  timeout: 3000,
  interval: 100,
});
```

### Within a Container

```typescript
import { within } from '@testing-library/react';

const dialog = screen.getByRole('dialog');
const submitButton = within(dialog).getByRole('button', { name: /submit/i });

// Chain within for nested containers
const form = within(dialog).getByRole('form');
const input = within(form).getByRole('textbox', { name: /email/i });
```

### Text Matching

```typescript
// Case-insensitive with regex
screen.getByText(/submit/i);
screen.getByRole('button', { name: /submit/i });

// Partial match with regex
screen.getByText(/welcome/i); // Matches "Welcome, John!"

// Exact match with string
screen.getByText('Welcome, John!');

// Substring match with exact: false
screen.getByText('llo Worl', { exact: false });

// Custom matcher function
screen.getByText((content, element) => {
  return content.startsWith('Price:') && element?.tagName === 'SPAN';
});
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
// ❌ Wrong - doesn't fail if element missing, may cause confusing errors
const button = screen.queryByRole('button');
userEvent.click(button!);

// ✅ Correct - fails immediately with clear message if missing
const button = screen.getByRole('button');
await userEvent.click(button);
```

### Don't Use findBy* Unnecessarily

```typescript
// ❌ Wrong - adds 1s timeout for sync element, slows tests
const header = await screen.findByRole('heading');

// ✅ Correct - immediate for sync elements
const header = screen.getByRole('heading');
```

### Don't Use getByTestId as Default

```typescript
// ❌ Wrong - skips accessibility, doesn't test what users see
screen.getByTestId('submit-btn');

// ✅ Correct - tests accessibility, more resilient to refactors
screen.getByRole('button', { name: /submit/i });
```

### Don't Query by Class or ID

```typescript
// ❌ Wrong - implementation detail, brittle
document.querySelector('.submit-button');
document.getElementById('submit');

// ✅ Correct - user-facing, stable
screen.getByRole('button', { name: /submit/i });
```

### Don't Wrap getBy* in waitFor

```typescript
// ❌ Wrong - waitFor is for side effects, not queries
await waitFor(() => screen.getByRole('button'));

// ✅ Correct - use findBy* for async queries
await screen.findByRole('button');
```

### Don't Use Multiple Assertions in waitFor

```typescript
// ❌ Wrong - only first failing assertion triggers retry
await waitFor(() => {
  expect(screen.getByText('A')).toBeVisible();
  expect(screen.getByText('B')).toBeVisible();
});

// ✅ Correct - single assertion per waitFor
await screen.findByText('A');
await screen.findByText('B');
```

## Debugging Queries

When queries fail, use `screen.debug()`:

```typescript
test('shows user name', () => {
  render(<UserProfile />);
  
  // Print entire DOM to console
  screen.debug();
  
  // Debug specific element
  screen.debug(screen.getByRole('main'));
  
  // Debug multiple elements
  screen.debug(screen.getAllByRole('listitem'));
  
  // Limit output length (default: 7000)
  screen.debug(undefined, 20000);
});
```

Use `logRoles` to discover available ARIA roles:

```typescript
import { logRoles } from '@testing-library/react';

test('find available roles', () => {
  const { container } = render(<MyComponent />);
  logRoles(container);
  // Output shows all roles and their elements:
  // button: <button>Submit</button>
  // textbox: <input type="text" />
  // heading: <h1>Title</h1>
});
```

Use `prettyDOM` for custom debugging:

```typescript
import { prettyDOM } from '@testing-library/react';

test('custom debug', () => {
  render(<MyComponent />);
  const element = screen.getByRole('dialog');
  
  // Get pretty-printed string (useful for logging)
  console.log(prettyDOM(element));
  
  // With options
  console.log(prettyDOM(element, 5000, { highlight: false }));
});
```

## Common ARIA Roles Reference

Quick reference for common implicit roles:

| Element | Role |
|---------|------|
| `<button>` | button |
| `<a href="...">` | link |
| `<input type="text">` | textbox |
| `<input type="checkbox">` | checkbox |
| `<input type="radio">` | radio |
| `<input type="number">` | spinbutton |
| `<select>` | combobox |
| `<textarea>` | textbox |
| `<h1>`-`<h6>` | heading |
| `<ul>`, `<ol>` | list |
| `<li>` | listitem |
| `<table>` | table |
| `<tr>` | row |
| `<td>` | cell |
| `<th>` | columnheader / rowheader |
| `<nav>` | navigation |
| `<main>` | main |
| `<header>` | banner |
| `<footer>` | contentinfo |
| `<aside>` | complementary |
| `<form>` | form (when named) |
| `<img alt="...">` | img |
