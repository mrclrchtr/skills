# Mantine Testing Patterns

Testing Mantine UI components with React Testing Library (Mantine 7.x/8.x/9.x).

## Test Environment Setup

### Install Dependencies

```bash
# Vitest (recommended)
npm install -D vitest jsdom @testing-library/dom @testing-library/jest-dom @testing-library/react @testing-library/user-event

# Jest
npm install -D jest jest-environment-jsdom @testing-library/jest-dom @testing-library/react @testing-library/user-event
```

### Vitest Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './vitest.setup.mjs',
  },
});
```

### Mock Browser APIs

Mantine requires browser APIs that are not available in jsdom. Add these mocks to your setup file.

```typescript
// vitest.setup.mjs (Vitest)
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

const { getComputedStyle } = window;
window.getComputedStyle = (elt) => getComputedStyle(elt);
window.HTMLElement.prototype.scrollIntoView = () => {};

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

Object.defineProperty(document, 'fonts', {
  value: { addEventListener: vi.fn(), removeEventListener: vi.fn() },
});

class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

window.ResizeObserver = ResizeObserver;
```

```typescript
// jest.setup.js (Jest)
import '@testing-library/jest-dom';

const { getComputedStyle } = window;
window.getComputedStyle = (elt) => getComputedStyle(elt);
window.HTMLElement.prototype.scrollIntoView = () => {};

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

Object.defineProperty(document, 'fonts', {
  value: { addEventListener: jest.fn(), removeEventListener: jest.fn() },
});

class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

window.ResizeObserver = ResizeObserver;
```

## MantineProvider Wrapper

Always wrap components with MantineProvider in tests. Use `env="test"` to disable transitions and portals.

### Basic Test Utils Setup

```typescript
// src/test/test-utils.tsx
import { render as testingLibraryRender } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { theme } from '../theme';

export function render(ui: React.ReactNode) {
  return testingLibraryRender(<>{ui}</>, {
    wrapper: ({ children }: { children: React.ReactNode }) => (
      <MantineProvider theme={theme} env="test">
        {children}
      </MantineProvider>
    ),
  });
}

export * from '@testing-library/react';
export { render };
export { default as userEvent } from '@testing-library/user-event';
```

### What `env="test"` Disables

- **Transitions**: Mount/unmount delays that cause timing issues
- **Portals**: Content renders in place rather than document.body

Note: Do not use `env="test"` with end-to-end testing tools like Cypress or Playwright.

## Disable Transitions for Portal Components

If `env="test"` is insufficient (e.g., you need to test transition callbacks), manually disable transitions:

```typescript
import { render as testingLibraryRender } from '@testing-library/react';
import { createTheme, MantineProvider, mergeThemeOverrides, Modal, Drawer, Popover, Menu } from '@mantine/core';
import { theme } from '../theme';

const testTheme = mergeThemeOverrides(
  theme,
  createTheme({
    components: {
      Modal: Modal.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
      Drawer: Drawer.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
      Popover: Popover.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
      Menu: Menu.extend({
        defaultProps: { transitionProps: { duration: 0 } },
      }),
    },
  })
);

export function render(ui: React.ReactNode) {
  return testingLibraryRender(<>{ui}</>, {
    wrapper: ({ children }: { children: React.ReactNode }) => (
      <MantineProvider theme={testTheme}>
        {children}
      </MantineProvider>
    ),
  });
}
```

## Testing Modals

### Open and Close Modal

```typescript
import { render, screen, waitFor } from '../test/test-utils';
import userEvent from '@testing-library/user-event';

test('opens and closes modal', async () => {
  const user = userEvent.setup();
  
  render(<MyComponentWithModal />);
  
  // Open modal
  await user.click(screen.getByRole('button', { name: /open/i }));
  
  // Modal content visible
  expect(screen.getByRole('dialog')).toBeInTheDocument();
  expect(screen.getByText('Modal Title')).toBeInTheDocument();
  
  // Close modal
  await user.click(screen.getByRole('button', { name: /close/i }));
  
  // Modal gone
  await waitFor(() => {
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
```

### Close with Escape Key

```typescript
test('closes modal on escape', async () => {
  const user = userEvent.setup();
  
  render(<MyModal />);
  
  await user.click(screen.getByRole('button', { name: /open/i }));
  expect(screen.getByRole('dialog')).toBeInTheDocument();
  
  await user.keyboard('{Escape}');
  
  await waitFor(() => {
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
```

### Form Inside Modal

```typescript
import { within } from '@testing-library/react';

test('submits form in modal', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  
  render(<ModalWithForm onSubmit={onSubmit} />);
  
  await user.click(screen.getByRole('button', { name: /open/i }));
  
  const dialog = screen.getByRole('dialog');
  
  await user.type(within(dialog).getByLabelText(/name/i), 'John');
  await user.type(within(dialog).getByLabelText(/email/i), 'john@example.com');
  await user.click(within(dialog).getByRole('button', { name: /submit/i }));
  
  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      name: 'John',
      email: 'john@example.com',
    });
  });
});
```

## Testing Drawers

```typescript
test('opens drawer from left', async () => {
  const user = userEvent.setup();
  
  render(<Navigation />);
  
  await user.click(screen.getByRole('button', { name: /menu/i }));
  
  // Drawer content
  expect(screen.getByRole('navigation')).toBeInTheDocument();
  expect(screen.getByRole('link', { name: /home/i })).toBeInTheDocument();
});
```

## Testing Menus and Dropdowns

```typescript
test('selects menu item', async () => {
  const user = userEvent.setup();
  const onSelect = vi.fn();
  
  render(<ActionMenu onSelect={onSelect} />);
  
  // Open menu
  await user.click(screen.getByRole('button', { name: /actions/i }));
  
  // Click menu item
  await user.click(screen.getByRole('menuitem', { name: /delete/i }));
  
  expect(onSelect).toHaveBeenCalledWith('delete');
});
```

## Testing Select Components

### Verify Dropdown Open/Close State

```typescript
test('verifies dropdown opened state', async () => {
  const user = userEvent.setup();
  
  render(
    <Select
      name="age"
      label="Select your age"
      data={[
        { value: 'ok', label: 'I am 18 or older' },
        { value: 'not-ok', label: 'I am under 18' },
      ]}
    />
  );
  
  // Verify dropdown is closed (listbox has same name as textbox)
  expect(screen.queryByRole('listbox', { name: 'Select your age' })).toBeNull();
  
  // Open dropdown
  await user.click(screen.getByRole('textbox', { name: 'Select your age' }));
  
  // Verify dropdown is open
  expect(screen.getByRole('listbox', { name: 'Select your age' })).toBeVisible();
});
```

### Single Selection (Select, Autocomplete)

```typescript
test('selects option from dropdown', async () => {
  const user = userEvent.setup();
  
  render(
    <Select
      name="age"
      label="Select your age"
      data={[
        { value: 'ok', label: 'I am 18 or older' },
        { value: 'not-ok', label: 'I am under 18' },
      ]}
    />
  );
  
  // Open select (dropdown closes when option is selected)
  await user.click(screen.getByRole('textbox', { name: 'Select your age' }));
  
  // Select option
  await user.click(screen.getByRole('option', { name: 'I am 18 or older' }));
  
  // Verify displayed value
  expect(screen.getByRole('textbox')).toHaveValue('I am 18 or older');
  
  // Verify form value (hidden input)
  expect(document.querySelector('input[name="age"]')).toHaveValue('ok');
});
```

### Multiple Selection (MultiSelect, TagsInput)

```typescript
test('selects multiple options', async () => {
  const user = userEvent.setup();
  
  render(
    <MultiSelect
      name="groceries"
      label="Select groceries"
      data={[
        { value: 'banana', label: 'Banana' },
        { value: 'apple', label: 'Apple' },
        { value: 'orange', label: 'Orange' },
      ]}
    />
  );
  
  // Open dropdown (stays open after selection for multi-select)
  await user.click(screen.getByRole('textbox', { name: 'Select groceries' }));
  
  // Select multiple options
  await user.click(screen.getByRole('option', { name: 'Banana' }));
  await user.click(screen.getByRole('option', { name: 'Apple' }));
  
  // Verify form value (hidden input contains comma-separated values)
  expect(document.querySelector('input[name="groceries"]')).toHaveValue('banana,apple');
});
```

### Searchable Select

```typescript
test('filters and selects from searchable select', async () => {
  const user = userEvent.setup();
  
  render(<SearchableSelect options={countries} />);
  
  const combobox = screen.getByRole('textbox');
  
  // Type to filter
  await user.click(combobox);
  await user.type(combobox, 'ger');
  
  // Select filtered option
  await user.click(screen.getByRole('option', { name: /germany/i }));
  
  expect(combobox).toHaveValue('Germany');
});
```

## Testing Form Inputs

### TextInput with Validation

```typescript
test('shows validation error', async () => {
  const user = userEvent.setup();
  
  render(<EmailForm />);
  
  const input = screen.getByLabelText(/email/i);
  
  await user.type(input, 'invalid');
  await user.tab(); // Trigger blur validation
  
  expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
});
```

### NumberInput

```typescript
test('enters number value', async () => {
  const user = userEvent.setup();
  
  render(<QuantityInput />);
  
  const input = screen.getByRole('textbox', { name: /quantity/i });
  
  // Type value
  await user.clear(input);
  await user.type(input, '5');
  
  expect(input).toHaveValue('5');
});
```

### DatePickerInput

```typescript
test('selects date from calendar', async () => {
  const user = userEvent.setup();
  
  render(
    <DatePickerInput
      label="Pick date"
      placeholder="Select a date"
    />
  );
  
  // Open calendar
  await user.click(screen.getByRole('textbox', { name: 'Pick date' }));
  
  // Select a date (e.g., the 15th)
  await user.click(screen.getByRole('button', { name: /15/ }));
  
  // Verify input has a value
  expect(screen.getByRole('textbox')).not.toHaveValue('');
});
```

### Checkbox

```typescript
test('toggles checkbox', async () => {
  const user = userEvent.setup();
  
  render(<TermsCheckbox />);
  
  const checkbox = screen.getByRole('checkbox', { name: /agree/i });
  
  expect(checkbox).not.toBeChecked();
  
  await user.click(checkbox);
  expect(checkbox).toBeChecked();
  
  await user.click(checkbox);
  expect(checkbox).not.toBeChecked();
});
```

### Switch

```typescript
test('toggles switch', async () => {
  const user = userEvent.setup();
  const onChange = vi.fn();
  
  render(<NotificationSwitch onChange={onChange} />);
  
  await user.click(screen.getByRole('switch', { name: /notifications/i }));
  
  expect(onChange).toHaveBeenCalledWith(true);
});
```

## Testing Forms with useForm

### Form with Validation

```typescript
test('shows validation errors on invalid submit', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  
  function TestForm() {
    const form = useForm({
      initialValues: { email: '', name: '' },
      validate: {
        email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
        name: (value) => (value.length < 2 ? 'Name too short' : null),
      },
    });
    
    return (
      <form onSubmit={form.onSubmit(onSubmit)}>
        <TextInput label="Email" {...form.getInputProps('email')} />
        <TextInput label="Name" {...form.getInputProps('name')} />
        <Button type="submit">Submit</Button>
      </form>
    );
  }
  
  render(<TestForm />);
  
  // Submit without filling fields
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  // Validation errors appear
  expect(screen.getByText('Invalid email')).toBeInTheDocument();
  expect(screen.getByText('Name too short')).toBeInTheDocument();
  expect(onSubmit).not.toHaveBeenCalled();
  
  // Fill valid values
  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/name/i), 'John');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  expect(onSubmit).toHaveBeenCalledWith({ email: 'test@example.com', name: 'John' }, expect.anything());
});
```

### Form with Zod Schema Validation

```typescript
import { zodResolver } from 'mantine-form-zod-resolver';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2, { message: 'Name must have at least 2 characters' }),
  email: z.string().email({ message: 'Invalid email' }),
});

test('validates with zod schema', async () => {
  const user = userEvent.setup();
  
  function TestForm() {
    const form = useForm({
      initialValues: { name: '', email: '' },
      validate: zodResolver(schema),
    });
    
    return (
      <form onSubmit={form.onSubmit(() => {})}>
        <TextInput label="Name" {...form.getInputProps('name')} />
        <TextInput label="Email" {...form.getInputProps('email')} />
        <Button type="submit">Submit</Button>
      </form>
    );
  }
  
  render(<TestForm />);
  
  await user.type(screen.getByLabelText(/name/i), 'A');
  await user.type(screen.getByLabelText(/email/i), 'invalid');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  expect(screen.getByText('Name must have at least 2 characters')).toBeInTheDocument();
  expect(screen.getByText('Invalid email')).toBeInTheDocument();
});
```

## Testing Notifications

Ensure your app wraps components with `<Notifications />` at the root.

```typescript
test('shows success notification', async () => {
  const user = userEvent.setup();
  
  render(<SaveButton />);
  
  await user.click(screen.getByRole('button', { name: /save/i }));
  
  // Notification appears
  expect(await screen.findByRole('alert')).toHaveTextContent(/saved/i);
});

test('shows loading notification then updates to success', async () => {
  const user = userEvent.setup();
  
  render(<AsyncSaveButton />);
  
  await user.click(screen.getByRole('button', { name: /save/i }));
  
  // Loading notification appears
  expect(await screen.findByText(/loading/i)).toBeInTheDocument();
  
  // Wait for success notification
  expect(await screen.findByText(/saved successfully/i)).toBeInTheDocument();
});
```

## Testing Tooltips

```typescript
test('shows tooltip on hover', async () => {
  const user = userEvent.setup();
  
  render(<InfoButton />);
  
  await user.hover(screen.getByRole('button'));
  
  expect(await screen.findByRole('tooltip')).toHaveTextContent('More info');
  
  await user.unhover(screen.getByRole('button'));
  
  await waitFor(() => {
    expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
  });
});
```

## Testing with useDisclosure

Components using `useDisclosure` follow the same modal/drawer patterns:

```typescript
test('component using useDisclosure', async () => {
  const user = userEvent.setup();
  
  render(<DisclosureExample />);
  
  // Initially closed
  expect(screen.queryByText('Content')).not.toBeInTheDocument();
  
  // Open
  await user.click(screen.getByRole('button', { name: /show/i }));
  expect(screen.getByText('Content')).toBeInTheDocument();
  
  // Toggle
  await user.click(screen.getByRole('button', { name: /toggle/i }));
  expect(screen.queryByText('Content')).not.toBeInTheDocument();
});
```

## Testing Tabs

```typescript
test('switches between tabs', async () => {
  const user = userEvent.setup();
  
  render(
    <Tabs defaultValue="first">
      <Tabs.List>
        <Tabs.Tab value="first">First tab</Tabs.Tab>
        <Tabs.Tab value="second">Second tab</Tabs.Tab>
      </Tabs.List>
      <Tabs.Panel value="first">First panel content</Tabs.Panel>
      <Tabs.Panel value="second">Second panel content</Tabs.Panel>
    </Tabs>
  );
  
  // First panel visible by default
  expect(screen.getByText('First panel content')).toBeVisible();
  
  // Switch to second tab
  await user.click(screen.getByRole('tab', { name: 'Second tab' }));
  
  expect(screen.getByText('Second panel content')).toBeVisible();
  expect(screen.queryByText('First panel content')).not.toBeVisible();
});
```

## Testing Stepper

```typescript
test('navigates through stepper steps', async () => {
  const user = userEvent.setup();
  
  render(<MyStepperForm />);
  
  // First step visible
  expect(screen.getByText('Step 1 content')).toBeInTheDocument();
  
  // Click next
  await user.click(screen.getByRole('button', { name: /next/i }));
  
  expect(screen.getByText('Step 2 content')).toBeInTheDocument();
  
  // Click step directly (if allowStepClick enabled)
  await user.click(screen.getByText('Step 1'));
  
  expect(screen.getByText('Step 1 content')).toBeInTheDocument();
});
```

## Common Issues

### Portal Content Not Found

With `env="test"`, portals are disabled and content renders in place. Without it, portal content renders in document.body. Use `screen` queries (they search the whole document):

```typescript
// ✅ Correct - searches entire document
expect(screen.getByRole('dialog')).toBeInTheDocument();

// ❌ Wrong - only searches container
const { container } = render(<Modal />);
expect(container.querySelector('[role="dialog"]')); // May not find portal content
```

### Transitions Causing Flaky Tests

The primary fix is `env="test"` in MantineProvider. If tests are still flaky without it:

```typescript
// Wait for element to appear
expect(await screen.findByRole('dialog')).toBeInTheDocument();

// Wait for element to disappear
await waitFor(() => {
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
}, { timeout: 1000 });
```

### Why Tests Fail Without `env="test"`

Mantine's Transition component uses `setTimeout` to delay animation start. React Testing Library does not wait for `setTimeout` by default, causing assertions to run before the content appears in the DOM.

### Focus Trap Interference

Modals trap focus. Test keyboard navigation within the modal:

```typescript
test('tabs through modal fields', async () => {
  const user = userEvent.setup();
  
  render(<FormModal />);
  
  await user.click(screen.getByRole('button', { name: /open/i }));
  
  // First field focused
  expect(screen.getByLabelText(/first/i)).toHaveFocus();
  
  await user.tab();
  expect(screen.getByLabelText(/second/i)).toHaveFocus();
});
```

### Mantine 8.x Date Component Changes

In Mantine 8.x, `@mantine/dates` components call `onChange` with date strings instead of Date objects:

```typescript
// 7.x - onChange receives Date object
<DatePicker value={value} onChange={setValue} />

// 8.x - onChange receives string (e.g., '2024-08-21')
<DatePicker 
  value={value} 
  onChange={(val) => setValue(val ? new Date(val) : null)} 
/>
```

### Mantine 9.x Collapse Prop Change

In Mantine 9.x, the `in` prop was renamed to `expanded`:

```typescript
// 8.x (deprecated)
<Collapse in={opened}>...</Collapse>

// 9.x
<Collapse expanded={opened}>...</Collapse>
```
