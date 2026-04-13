# Animation

## Core Principles

- MUST honor `prefers-reduced-motion` and provide a reduced-motion variant.
- SHOULD use motion only when it clarifies cause and effect or adds deliberate polish.
- SHOULD animate in response to user actions; avoid autoplay animations.
- SHOULD choose easing based on what changes (size, distance, trigger type).

## Implementation

- SHOULD prefer CSS transitions and animations first, the Web Animations API when it improves orchestration, and JavaScript-driven motion only when the other layers cannot express the interaction cleanly.
- MUST keep motion on compositor-friendly properties such as `transform` and `opacity` whenever possible.
- NEVER animate layout properties like `width`, `height`, `top`, `left`, `margin`, or `padding` when a transform-based effect will do.
- NEVER use `transition: all`; animate only the properties you intend to change.
- MUST keep motion interruptible by user input.
- SHOULD set `transform-origin` deliberately when scale, rotate, or pivot motion would otherwise feel off.

## SVG

- SHOULD treat SVG motion carefully: prefer transform, opacity, stroke, and viewBox-aware changes over path morphing or layout-dependent tricks.
- SHOULD apply CSS transforms to `<g>` wrappers and set `transform-box: fill-box; transform-origin: center;` to avoid Safari origin miscalculation.

## Text

- SHOULD animate a wrapper element instead of the text node itself to avoid anti-aliasing artifacts during transforms.
- MAY set `translateZ(0)` or `will-change: transform` to promote text to its own layer if artifacts persist.
