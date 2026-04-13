# Tailwind Integration

- MUST bridge component library CSS variables to Tailwind theme tokens — via a generated CSS preset, a Tailwind config plugin, or a manual theme extension — rather than duplicating hex values.
- MUST keep dark mode variants synchronized with the component library's color scheme mechanism.
- MUST regenerate the bridge (preset file or theme extension) after changing the source palette in the component library's theme.
- SHOULD use Tailwind for layout utilities, one-off positioning, and custom property references, not for overriding component library internals.
- SHOULD use CSS custom property syntax (`bg-[var(--color-surface)]`) for semantic tokens not natively in the Tailwind theme.
- SHOULD define project-specific semantic tokens (surface, warning, destructive) in CSS custom properties rather than duplicating them in the Tailwind theme.
- SHOULD prefer component library style props for component-scoped styling and Tailwind for page-level layout and custom elements.
- NEVER hardcode hex values in Tailwind utilities when a CSS variable or theme token exists.
