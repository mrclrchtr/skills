# Mantine Testing Patterns

Testing Mantine UI components with React Testing Library.

## MantineProvider Wrapper

Always wrap components with MantineProvider in tests. Use `env="test"` to disable animations.

### Basic Test Utils Setup

```typescript
// src/test/test-utils.tsx
import { render as testingLibraryRender, RenderOptions } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { theme } from '../theme';

export function render(ui: React.ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return testingLibraryRender(ui, {
    wrapper: ({ children }) => (
      <MantineProvider theme={theme} env="test">
        {children}
      </MantineProvider>
    ),
    ...options,
  });
}

export * from '@testing-library/react';
export { render };
export { default as userEvent } from '@testing-library/user-event';
```

## Disable Transitions for Portals

Modal, Drawer, Popover, and other portal components use transitions that interfere with tests. Disable them:

```typescript
import { createTheme, mergeThemeOverrides, Modal, Drawer, Popover, Menu } from '@mantine/core';
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

export function render(ui: React.ReactElement) {
  return testingLibraryRender(ui, {
    wrapper: ({ children }) => (
      <MantineProvider theme={testTheme} env="test">
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

```typescript
test('selects option from dropdown', async () => {
  const user = userEvent.setup();
  
  render(<CountrySelect />);
  
  // Open select
  await user.click(screen.getByRole('combobox', { name: /country/i }));
  
  // Select option
  await user.click(screen.getByRole('option', { name: /germany/i }));
  
  // Verify selection
  expect(screen.getByRole('combobox')).toHaveTextContent('Germany');
});
```

### Searchable Select

```typescript
test('filters and selects from searchable select', async () => {
  const user = userEvent.setup();
  
  render(<SearchableSelect options={countries} />);
  
  const combobox = screen.getByRole('combobox');
  
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
test('increments number input', async () => {
  const user = userEvent.setup();
  
  render(<QuantityInput />);
  
  const input = screen.getByRole('textbox', { name: /quantity/i });
  
  // Type value
  await user.clear(input);
  await user.type(input, '5');
  
  expect(input).toHaveValue('5');
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

## Testing Notifications

```typescript
import { notifications } from '@mantine/notifications';

test('shows success notification', async () => {
  const user = userEvent.setup();
  
  render(<SaveButton />);
  
  await user.click(screen.getByRole('button', { name: /save/i }));
  
  // Notification appears
  expect(await screen.findByRole('alert')).toHaveTextContent(/saved/i);
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

## Common Issues

### Portal Content Not Found

Portal content renders in document.body, not the component tree. Use `screen` queries (they search the whole document):

```typescript
// ✅ Correct - searches entire document
expect(screen.getByRole('dialog')).toBeInTheDocument();

// ❌ Wrong - only searches container
const { container } = render(<Modal />);
expect(container.querySelector('[role="dialog"]')); // May not find portal content
```

### Transitions Causing Flaky Tests

Always disable transitions in test theme (see setup above). If tests are still flaky:

```typescript
await waitFor(() => {
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
}, { timeout: 1000 });
```

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
