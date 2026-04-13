# User Interactions

Patterns for simulating user interactions with userEvent.

## Setup (Required)

Always call `userEvent.setup()` before interactions:

```typescript
import userEvent from '@testing-library/user-event';

test('handles user input', async () => {
  const user = userEvent.setup();
  
  render(<MyComponent />);
  
  await user.click(button);
});
```

### Setup Options

```typescript
// With fake timers
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });

// Skip auto-await for pointer events
const user = userEvent.setup({ pointerEventsCheck: 0 });

// Custom delay between keystrokes
const user = userEvent.setup({ delay: 100 });
```

## Why userEvent Over fireEvent

`fireEvent` dispatches single DOM events. `userEvent` simulates complete user interactions:

| Action | fireEvent | userEvent |
|--------|-----------|-----------|
| Click | 1 click event | mousedown, focus, mouseup, click |
| Type | 1 change event | focus, keydown, keypress, input, keyup per char |
| Tab | No focus change | Proper focus management |

```typescript
// ❌ fireEvent - incomplete simulation
fireEvent.change(input, { target: { value: 'test' } });

// ✅ userEvent - realistic typing
await user.type(input, 'test');
```

## Typing

### Basic Typing

```typescript
const input = screen.getByRole('textbox');

await user.type(input, 'Hello World');
```

### Clear and Type

```typescript
// Clear existing value first
await user.clear(input);
await user.type(input, 'new value');
```

### Type with Special Keys

```typescript
// Enter key
await user.type(input, 'search{Enter}');

// With modifier keys
await user.type(input, '{Shift>}UPPERCASE{/Shift}');

// Backspace
await user.type(input, 'helllo{Backspace}');
```

## Clicking

### Basic Click

```typescript
await user.click(screen.getByRole('button'));
```

### Double Click

```typescript
await user.dblClick(element);
```

### Triple Click (Select All Text)

```typescript
await user.tripleClick(textInput);
```

### Right Click

```typescript
await user.pointer({ target: element, keys: '[MouseRight]' });
```

### Click with Modifiers

```typescript
// Ctrl+Click
await user.click(link, { ctrlKey: true });

// Shift+Click
await user.click(item, { shiftKey: true });
```

## Keyboard

### Press Keys

```typescript
// Single key
await user.keyboard('{Enter}');
await user.keyboard('{Escape}');
await user.keyboard('{Tab}');

// Key combinations
await user.keyboard('{Control>}a{/Control}'); // Ctrl+A
await user.keyboard('{Meta>}s{/Meta}');       // Cmd+S (Mac)
await user.keyboard('{Alt>}{Enter}{/Alt}');   // Alt+Enter
```

### Arrow Navigation

```typescript
await user.keyboard('{ArrowDown}');
await user.keyboard('{ArrowUp}');
await user.keyboard('{ArrowLeft}');
await user.keyboard('{ArrowRight}');
```

### Tab Navigation

```typescript
// Tab forward
await user.tab();

// Tab backward
await user.tab({ shift: true });
```

## Select/Dropdown

### Select by Value

```typescript
const select = screen.getByRole('combobox');

await user.selectOptions(select, 'option-value');
```

### Select by Label

```typescript
await user.selectOptions(select, screen.getByText('Option Label'));
```

### Multi-Select

```typescript
await user.selectOptions(multiSelect, ['option1', 'option2']);
```

### Deselect

```typescript
await user.deselectOptions(multiSelect, 'option1');
```

## Checkbox and Radio

### Toggle Checkbox

```typescript
const checkbox = screen.getByRole('checkbox', { name: /agree/i });

await user.click(checkbox);
expect(checkbox).toBeChecked();

await user.click(checkbox);
expect(checkbox).not.toBeChecked();
```

### Select Radio

```typescript
const radio = screen.getByRole('radio', { name: /monthly/i });

await user.click(radio);
expect(radio).toBeChecked();
```

## Hover

### Hover and Unhover

```typescript
const tooltip = screen.getByText('Info');

await user.hover(tooltip);
expect(await screen.findByRole('tooltip')).toBeInTheDocument();

await user.unhover(tooltip);
await waitForElementToBeRemoved(() => screen.queryByRole('tooltip'));
```

## Clipboard

### Copy and Paste

```typescript
// Select text and copy
await user.tripleClick(textElement);
await user.copy();

// Paste
await user.click(targetInput);
await user.paste();
```

### Cut

```typescript
await user.tripleClick(textElement);
await user.cut();
```

## File Upload

```typescript
const file = new File(['content'], 'test.txt', { type: 'text/plain' });
const input = screen.getByLabelText(/upload/i);

await user.upload(input, file);

expect(input.files[0]).toBe(file);
```

### Multiple Files

```typescript
const files = [
  new File(['a'], 'a.txt', { type: 'text/plain' }),
  new File(['b'], 'b.txt', { type: 'text/plain' }),
];

await user.upload(input, files);

expect(input.files).toHaveLength(2);
```

## Drag and Drop

```typescript
const source = screen.getByText('Drag me');
const target = screen.getByText('Drop here');

await user.pointer([
  { target: source, keys: '[MouseLeft>]' },
  { target },
  { keys: '[/MouseLeft]' },
]);
```

## Form Submission

### Full Form Flow

```typescript
test('submits form correctly', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  
  render(<ContactForm onSubmit={onSubmit} />);
  
  await user.type(screen.getByLabelText(/name/i), 'John Doe');
  await user.type(screen.getByLabelText(/email/i), 'john@example.com');
  await user.type(screen.getByLabelText(/message/i), 'Hello there!');
  
  await user.click(screen.getByRole('button', { name: /send/i }));
  
  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
      message: 'Hello there!',
    });
  });
});
```

### Submit with Enter

```typescript
await user.type(searchInput, 'query{Enter}');
```

## Accessibility Testing

### Focus Order

```typescript
test('has correct focus order', async () => {
  const user = userEvent.setup();
  
  render(<Form />);
  
  await user.tab();
  expect(screen.getByLabelText(/first name/i)).toHaveFocus();
  
  await user.tab();
  expect(screen.getByLabelText(/last name/i)).toHaveFocus();
  
  await user.tab();
  expect(screen.getByRole('button')).toHaveFocus();
});
```

### Keyboard Navigation

```typescript
test('dropdown navigable by keyboard', async () => {
  const user = userEvent.setup();
  
  render(<Dropdown options={['A', 'B', 'C']} />);
  
  await user.click(screen.getByRole('button'));
  
  // Navigate with arrows
  await user.keyboard('{ArrowDown}');
  expect(screen.getByText('A')).toHaveAttribute('data-highlighted');
  
  await user.keyboard('{ArrowDown}');
  expect(screen.getByText('B')).toHaveAttribute('data-highlighted');
  
  // Select with Enter
  await user.keyboard('{Enter}');
  expect(screen.getByRole('button')).toHaveTextContent('B');
});
```

## Common Patterns

### Clear and Fill

```typescript
async function fillInput(label: RegExp, value: string) {
  const user = userEvent.setup();
  const input = screen.getByLabelText(label);
  await user.clear(input);
  await user.type(input, value);
}
```

### Wait After Action

```typescript
await user.click(submitButton);

// Wait for side effect
await waitFor(() => {
  expect(mockFn).toHaveBeenCalled();
});

// Or wait for UI change
expect(await screen.findByText('Submitted')).toBeInTheDocument();
```
