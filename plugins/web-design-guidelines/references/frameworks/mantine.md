# Mantine

- MUST use `createTheme` as the single source of truth for palette, radii, shadows, spacing, and component defaults.
- MUST use `ColorSchemeScript` in the HTML head to prevent flash of incorrect color scheme.
- MUST set `defaultRadius` in the theme rather than adding `radius` prop to every component.
- MUST use `autoContrast` or manual `--mantine-color-{name}-contrast` tokens to ensure text legibility on filled backgrounds.
- SHOULD customize components via `createTheme({ components: { ... } })` before resorting to `classNames`, `styles`, or CSS modules on individual instances.
- SHOULD follow the styling order of preference: theme defaults, then style props, then Styles API (`classNames` or `styles` prop), then CSS modules.
- SHOULD use Mantine's built-in color scheme system (`useMantineColorScheme`, `ColorSchemeScript`, `defaultColorScheme`) rather than rolling custom dark mode.
- SHOULD use Mantine spacing and size scale tokens (`xs` through `xl`) via style props rather than arbitrary pixel values.
- SHOULD use `Paper`, `Card`, `Modal`, `Drawer` for surface hierarchy rather than raw divs with box-shadow.
- SHOULD use Mantine form components (`TextInput`, `Select`, `Checkbox`, etc.) with proper `label`, `description`, and `error` props rather than building custom form controls.
- SHOULD use responsive syntax on style props (`py={{ base: "md", md: "xl" }}`) rather than media-query CSS for simple responsive adjustments.
- SHOULD bridge Mantine CSS variables to other tools (Tailwind, plain CSS) via a generated preset or manual token mapping rather than duplicating values.
- NEVER duplicate Mantine color values as hardcoded hex in component code; reference the palette or CSS variables.
