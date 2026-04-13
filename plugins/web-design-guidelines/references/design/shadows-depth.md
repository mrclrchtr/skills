# Shadows and Depth

## Layered Shadows

- SHOULD use at least two shadow layers: ambient (soft, diffuse) and direct (sharper, offset).
- Single-layer shadows look flat; layered shadows create more realistic depth.
- Ambient layer: larger blur, minimal offset, lower opacity.
- Direct layer: smaller blur, vertical offset, slightly higher opacity.

## Borders and Shadows Together

- SHOULD combine subtle borders with semi-transparent shadows for crisp edges.
- Shadows alone can look fuzzy at element boundaries; a 1px border adds definition.
- Match border color to the shadow tone or use a semi-transparent border that adapts to backgrounds.

## Nested Radii

- MUST make child border-radius less than or equal to parent border-radius.
- SHOULD align nested radii concentrically: inner radius = outer radius - padding.
- Mismatched radii create visual tension; concentric curves feel intentional.

## Elevation Consistency

- SHOULD establish a shadow scale (e.g., sm, md, lg) and use it consistently.
- Higher elevation = larger blur, greater offset, more layers.
- Interactive states (hover, active) can shift elevation to indicate responsiveness.

## Color and Hue

- SHOULD tint shadows toward the dominant hue on non-neutral backgrounds.
- Pure black or gray shadows on colored surfaces can look disconnected.
- Subtle hue matching makes shadows feel integrated with the surface.
