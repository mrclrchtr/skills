# User Interactions

Patterns for simulating user interactions with userEvent.

## Setup (Required)

Always call `userEvent.setup()` before interactions. This creates a session that shares keyboard and mouse state across actions, simulating realistic user behavior.

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
import { userEvent, PointerEventsCheckLevel } from '@testing-library/user-event';

// With fake timers (Jest)
const user = userEvent.setup({
  advanceTimers: (ms) => jest.advanceTimersByTime(ms),
});

// With fake timers (Vitest)
const user = userEvent.setup({
  advanceTimers: vi.advanceTimersByTime,
});

// Custom delay between events (useful for debounce/throttle testing)
const user = userEvent.setup({ delay: 100 });

// Skip pointer-events checks (for elements with pointer-events: none)
const user = userEvent.setup({
  pointerEventsCheck: PointerEventsCheckLevel.Never,
});

// Skip hover on click actions
const user = userEvent.setup({ skipHover: true });

// Enable clipboard writing for copy/paste tests
const user = userEvent.setup({ writeToClipboard: true });

// Respect file input accept attribute
const user = userEvent.setup({ applyAccept: true });
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

`type()` clicks the element first (gaining focus), then types character by character:

```typescript
const input = screen.getByRole('textbox');

await user.type(input, 'Hello World');
```

### Type Options

```typescript
// Skip the initial click (element must already have focus)
await user.type(input, 'text', { skipClick: true });

// Keep modifier keys held after typing
await user.type(input, '{Shift>}CAPS', { skipAutoClose: true });
// Shift is still held after type completes
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

Use `keyboard()` for direct key input on the currently focused element. Unlike `type()`, it does not click the element first.

### Key Syntax Reference

```typescript
// Press and release a key
await user.keyboard('a');           // Type 'a'
await user.keyboard('{Enter}');     // Press Enter

// Hold modifier with {Key>} and release with {/Key}
await user.keyboard('{Shift>}');    // Press and hold Shift
await user.keyboard('a');           // Type 'A' (shifted)
await user.keyboard('{/Shift}');    // Release Shift

// Combined in one call
await user.keyboard('{Control>}a{/Control}');  // Ctrl+A
await user.keyboard('{Alt>}{Tab}{/Alt}');      // Alt+Tab
```

### Common Keys

```typescript
// Navigation
await user.keyboard('{Enter}');
await user.keyboard('{Escape}');
await user.keyboard('{Tab}');
await user.keyboard('{Backspace}');
await user.keyboard('{Delete}');
await user.keyboard('{End}');
await user.keyboard('{Home}');

// Arrow keys
await user.keyboard('{ArrowDown}');
await user.keyboard('{ArrowUp}');
await user.keyboard('{ArrowLeft}');
await user.keyboard('{ArrowRight}');
```

### Keyboard Shortcuts

```typescript
// Select all (Ctrl+A / Cmd+A)
await user.keyboard('{Control>}a{/Control}');

// Copy (Ctrl+C)
await user.keyboard('{Control>}c{/Control}');

// Paste (Ctrl+V)
await user.keyboard('{Control>}v{/Control}');

// Save (Cmd+S on Mac)
await user.keyboard('{Meta>}s{/Meta}');

// Alt+Enter
await user.keyboard('{Alt>}{Enter}{/Alt}');
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

expect(select).toHaveValue('option-value');
```

### Select by Visible Text

```typescript
// Select using the displayed text instead of value
await user.selectOptions(select, 'Los Angeles');

// Value is set to the option's value attribute
expect(select).toHaveValue('la');
```

### Select by Element Reference

```typescript
await user.selectOptions(select, screen.getByText('Option Label'));
```

### Multi-Select

```typescript
const multiSelect = screen.getByRole('listbox');

await user.selectOptions(multiSelect, ['option1', 'option2', 'option3']);

const options = screen.getAllByRole('option');
expect(options[0]).toBeChecked();
expect(options[1]).toBeChecked();
```

### Deselect

```typescript
// Deselect specific options in multi-select
await user.deselectOptions(multiSelect, ['option2']);

expect(screen.getByRole('option', { name: 'Option 2' })).not.toBeChecked();
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

For clipboard operations, enable clipboard writing in setup:

```typescript
const user = userEvent.setup({ writeToClipboard: true });
```

### Copy and Paste

```typescript
// Select all text and copy
const input = screen.getByRole('textbox');
input.focus();
await user.keyboard('{Control>}a{/Control}');
await user.copy();

// Paste into another element
const target = screen.getByTestId('target');
target.focus();
await user.paste();

expect(target).toHaveValue('copied text');
```

### Copy-Paste Workflow

```typescript
test('copy-paste workflow', async () => {
  const user = userEvent.setup({ writeToClipboard: true });

  render(
    <>
      <input data-testid="source" defaultValue="Source text" />
      <input data-testid="target" />
    </>
  );

  const source = screen.getByTestId('source');
  const target = screen.getByTestId('target');

  // Select all and copy from source
  source.focus();
  await user.keyboard('{Control>}a{/Control}');
  await user.copy();

  // Paste to target
  target.focus();
  await user.paste();

  expect(target).toHaveValue('Source text');
});
```

### Paste with Specific Content

```typescript
// Paste specific text (ignores clipboard)
await user.paste('pasted content');
```

### Cut

```typescript
await user.tripleClick(textElement);
await user.cut();
```

## File Upload

### Single File

```typescript
const file = new File(['content'], 'test.txt', { type: 'text/plain' });
const input = screen.getByLabelText(/upload/i);

await user.upload(input, file);

expect(input.files).toHaveLength(1);
expect(input.files[0]).toBe(file);
expect(input.files[0].name).toBe('test.txt');
```

### Multiple Files

```typescript
// Input must have multiple attribute
render(<input type="file" multiple data-testid="file-input" />);

const files = [
  new File(['content 1'], 'file1.txt', { type: 'text/plain' }),
  new File(['content 2'], 'file2.txt', { type: 'text/plain' }),
  new File(['content 3'], 'file3.txt', { type: 'text/plain' }),
];

await user.upload(screen.getByTestId('file-input'), files);

const input = screen.getByTestId('file-input');
expect(input.files).toHaveLength(3);
expect(Array.from(input.files).map((f) => f.name)).toEqual([
  'file1.txt',
  'file2.txt',
  'file3.txt',
]);
```

### Respecting Accept Attribute

```typescript
// Enable accept attribute validation
const user = userEvent.setup({ applyAccept: true });

render(<input type="file" accept="image/*" data-testid="file-input" />);

const imageFile = new File(['image'], 'photo.png', { type: 'image/png' });
const textFile = new File(['text'], 'doc.txt', { type: 'text/plain' });

await user.upload(screen.getByTestId('file-input'), [imageFile, textFile]);

const input = screen.getByTestId('file-input');
// Only image file accepted
expect(input.files).toHaveLength(1);
expect(input.files[0].name).toBe('photo.png');
```

## Drag and Drop

### Basic Drag and Drop

```typescript
const draggable = screen.getByTestId('draggable');
const dropzone = screen.getByTestId('dropzone');

await user.pointer([
  { target: draggable },
  '[MouseLeft>]',     // Press left button
  { target: dropzone },
  '[/MouseLeft]',     // Release left button
]);
```

### Drag and Drop with File

For file drag-and-drop, combine `pointer` with `fireEvent.drop`:

```typescript
test('drag and drop file upload', async () => {
  const handleDrop = vi.fn((e) => e.preventDefault());
  const user = userEvent.setup();

  render(
    <div
      data-testid="dropzone"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      Drop files here
    </div>
  );

  const file = new File(['content'], 'file.txt', { type: 'text/plain' });
  const dropzone = screen.getByTestId('dropzone');

  // Simulate drag hover
  await user.pointer([{ target: dropzone }]);

  // Trigger drop with file
  fireEvent.drop(dropzone, {
    dataTransfer: { files: [file] },
  });

  expect(handleDrop).toHaveBeenCalled();
});
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

## Pointer API

Low-level pointer control for complex interactions:

### Pointer Press and Release

```typescript
await user.pointer([
  { target: screen.getByRole('button') },
  '[MouseLeft>]',   // Press left button
  '[/MouseLeft]',   // Release left button
]);
```

### Pointer Movement

```typescript
const handleMouseMove = vi.fn();

render(
  <div onMouseMove={handleMouseMove} style={{ width: 500, height: 500 }} />
);

await user.pointer([
  { coords: { x: 100, y: 100 } },
  { coords: { x: 200, y: 200 } },
  { coords: { x: 300, y: 300 } },
]);

expect(handleMouseMove).toHaveBeenCalledTimes(3);
```

## Common Patterns

### Clear and Fill Helper

```typescript
async function fillInput(
  user: ReturnType<typeof userEvent.setup>,
  label: RegExp,
  value: string
) {
  const input = screen.getByLabelText(label);
  await user.clear(input);
  await user.type(input, value);
}

// Usage
test('fills form', async () => {
  const user = userEvent.setup();
  render(<MyForm />);

  await fillInput(user, /email/i, 'test@example.com');
});
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

### Autocomplete Component

```typescript
test('autocomplete interaction', async () => {
  const user = userEvent.setup({ delay: 50 });

  render(<Autocomplete suggestions={['Apple', 'Banana', 'Cherry']} />);

  const input = screen.getByRole('combobox');

  // Type to show suggestions
  await user.type(input, 'a');

  await waitFor(() => {
    expect(screen.getByRole('listbox')).toBeInTheDocument();
  });

  // Navigate with arrow keys
  await user.keyboard('{ArrowDown}');
  await user.keyboard('{ArrowDown}');

  // Select with Enter
  await user.keyboard('{Enter}');

  expect(input).toHaveValue('Banana');
});
```

### Modal Dialog Workflow

```typescript
test('modal dialog workflow', async () => {
  const user = userEvent.setup();

  render(<App />);

  // Open modal
  await user.click(screen.getByRole('button', { name: /open modal/i }));

  await waitFor(() => {
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  // Interact with modal content
  await user.type(screen.getByLabelText(/name/i), 'John Doe');

  // Close with Escape
  await user.keyboard('{Escape}');

  await waitFor(() => {
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
```

### State Sharing Across Actions

The user instance maintains keyboard and pointer state:

```typescript
const user = userEvent.setup();

// Shift is held across multiple keyboard calls
await user.keyboard('[ShiftLeft>]'); // Press Shift (held)
await user.click(element);            // Click with shiftKey: true
await user.keyboard('[/ShiftLeft]');  // Release Shift
```
