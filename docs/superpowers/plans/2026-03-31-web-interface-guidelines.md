# Web Interface Guidelines Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign `plugins/web-interface-guidelines` into a three-skill plugin with a close-to-source shared reference corpus for design, implementation, and review.

**Architecture:** Keep the plugin repo-local and thin. Move most of the value into three focused skills plus a shared `references/` tree split into `core/`, `design/`, and `frameworks/`; use one lightweight Python structure test and the repo's skill validator to keep the layout, prompts, and critical contract markers from drifting.

**Tech Stack:** Markdown skills, YAML agent metadata, JSON plugin manifest, Python 3 `unittest`, Bash validation script

---

## File Map

### Create

- `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/SKILL.md`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/agents/openai.yaml`
- `plugins/web-interface-guidelines/references/core/interactions.md`
- `plugins/web-interface-guidelines/references/core/forms.md`
- `plugins/web-interface-guidelines/references/core/animation.md`
- `plugins/web-interface-guidelines/references/core/layout.md`
- `plugins/web-interface-guidelines/references/core/content-accessibility.md`
- `plugins/web-interface-guidelines/references/core/performance.md`
- `plugins/web-interface-guidelines/references/core/theming-copy.md`
- `plugins/web-interface-guidelines/references/core/anti-patterns.md`
- `plugins/web-interface-guidelines/references/design/direction.md`
- `plugins/web-interface-guidelines/references/design/typography-color.md`
- `plugins/web-interface-guidelines/references/design/motion-composition.md`
- `plugins/web-interface-guidelines/references/design/anti-slop.md`
- `plugins/web-interface-guidelines/references/frameworks/react-next.md`
- `plugins/web-interface-guidelines/tests/test_plugin_layout.py`

### Modify

- `plugins/web-interface-guidelines/.codex-plugin/plugin.json`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/SKILL.md`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/agents/openai.yaml`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/SKILL.md`
- `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/agents/openai.yaml`
- `plugins/web-interface-guidelines/references/source-notes.md`

### Delete

- `plugins/web-interface-guidelines/references/interactions.md`
- `plugins/web-interface-guidelines/references/forms.md`
- `plugins/web-interface-guidelines/references/content-accessibility.md`
- `plugins/web-interface-guidelines/references/layout-motion.md`
- `plugins/web-interface-guidelines/references/performance.md`
- `plugins/web-interface-guidelines/references/design-copywriting.md`

## Task 1: Establish the three-skill plugin contract

**Files:**
- Create: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`
- Create: `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/SKILL.md`
- Create: `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/agents/openai.yaml`
- Modify: `plugins/web-interface-guidelines/.codex-plugin/plugin.json`
- Test: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`

- [ ] **Step 1: Write the failing structure test**

```python
import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "plugins/web-interface-guidelines"


class WebInterfaceGuidelinesLayoutTest(unittest.TestCase):
    def test_manifest_advertises_three_modes(self) -> None:
        manifest = json.loads(
            (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            manifest["interface"]["defaultPrompt"],
            [
                "Use $web-interface-guidelines-design to define the visual direction for this UI before implementation.",
                "Use $web-interface-guidelines-apply to build or update this UI with the shared design and interface guidelines.",
                "Use $web-interface-guidelines-review to audit this UI or diff against the shared design and interface guidelines.",
            ],
        )

    def test_design_skill_exists_with_agent_metadata(self) -> None:
        self.assertTrue(
            (PLUGIN / "skills/web-interface-guidelines-design/SKILL.md").exists()
        )
        self.assertTrue(
            (
                PLUGIN
                / "skills/web-interface-guidelines-design/agents/openai.yaml"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify the current plugin fails**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: FAIL because `plugin.json` still advertises two prompts and the `web-interface-guidelines-design` skill files do not exist.

- [ ] **Step 3: Update the plugin manifest and scaffold the new design skill**

```json
{
  "name": "web-interface-guidelines",
  "version": "0.2.0",
  "description": "Design, implement, and review web interfaces with shared UI guidance",
  "skills": "./skills/",
  "interface": {
    "displayName": "Web Interface Guidelines",
    "shortDescription": "Design, apply, and review shared UI guidance",
    "longDescription": "Use focused skills to define UI direction, implement against shared interface standards, and audit existing UI with the same guidance.",
    "developerName": "mrclrchtr",
    "category": "Productivity",
    "capabilities": [
      "Interactive",
      "Write"
    ],
    "defaultPrompt": [
      "Use $web-interface-guidelines-design to define the visual direction for this UI before implementation.",
      "Use $web-interface-guidelines-apply to build or update this UI with the shared design and interface guidelines.",
      "Use $web-interface-guidelines-review to audit this UI or diff against the shared design and interface guidelines."
    ]
  }
}
```

```markdown
---
name: web-interface-guidelines-design
description: Use when creating, redesigning, or restyling a UI and Codex should establish a clear design direction before implementation.
---

# Web Interface Guidelines Design

## Overview

Establish a strong, explicit design direction before UI implementation begins. This skill exists to prevent generic design output and force an intentional point of view.

## Workflow

1. Identify the surface, audience, constraints, and product context.
2. Read the relevant files under `../../references/design/` and any core constraints that materially shape the direction.
3. Present two or three viable directions with trade-offs.
4. Recommend one direction and commit to it.
5. Name one memorable differentiator that should survive implementation.

## Guardrails

- Preserve an existing design system unless the user asks for a stronger redesign.
- Reject generic default SaaS aesthetics unless the host product already uses them intentionally.
- Keep aesthetic decisions compatible with accessibility, responsive behavior, and interaction rules.
```

```yaml
interface:
  display_name: "Web Interface Guidelines Design"
  short_description: "Define a UI direction before implementation"
  default_prompt: "Use $web-interface-guidelines-design to define the visual direction for this UI before implementation."
```

- [ ] **Step 4: Run the structure test again**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: PASS with `Ran 2 tests` and `OK`.

- [ ] **Step 5: Commit the scaffolding**

```bash
git add \
  plugins/web-interface-guidelines/.codex-plugin/plugin.json \
  plugins/web-interface-guidelines/skills/web-interface-guidelines-design/SKILL.md \
  plugins/web-interface-guidelines/skills/web-interface-guidelines-design/agents/openai.yaml \
  plugins/web-interface-guidelines/tests/test_plugin_layout.py
git commit -m "feat(web-interface-guidelines): add three-skill plugin contract"
```

## Task 2: Replace the flattened guidance with core references

**Files:**
- Modify: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`
- Create: `plugins/web-interface-guidelines/references/core/interactions.md`
- Create: `plugins/web-interface-guidelines/references/core/forms.md`
- Create: `plugins/web-interface-guidelines/references/core/animation.md`
- Create: `plugins/web-interface-guidelines/references/core/layout.md`
- Create: `plugins/web-interface-guidelines/references/core/content-accessibility.md`
- Create: `plugins/web-interface-guidelines/references/core/performance.md`
- Create: `plugins/web-interface-guidelines/references/core/theming-copy.md`
- Create: `plugins/web-interface-guidelines/references/core/anti-patterns.md`
- Delete: `plugins/web-interface-guidelines/references/interactions.md`
- Delete: `plugins/web-interface-guidelines/references/forms.md`
- Delete: `plugins/web-interface-guidelines/references/content-accessibility.md`
- Delete: `plugins/web-interface-guidelines/references/layout-motion.md`
- Delete: `plugins/web-interface-guidelines/references/performance.md`
- Delete: `plugins/web-interface-guidelines/references/design-copywriting.md`
- Test: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`

- [ ] **Step 1: Extend the test to require the new core inventory and reject the old flat files**

```python
    def test_core_reference_inventory_matches_the_new_layout(self) -> None:
        expected = {
            "references/core/interactions.md",
            "references/core/forms.md",
            "references/core/animation.md",
            "references/core/layout.md",
            "references/core/content-accessibility.md",
            "references/core/performance.md",
            "references/core/theming-copy.md",
            "references/core/anti-patterns.md",
        }
        legacy = {
            "references/interactions.md",
            "references/forms.md",
            "references/content-accessibility.md",
            "references/layout-motion.md",
            "references/performance.md",
            "references/design-copywriting.md",
        }

        for relpath in expected:
            self.assertTrue((PLUGIN / relpath).exists(), relpath)
        for relpath in legacy:
            self.assertFalse((PLUGIN / relpath).exists(), relpath)
```

- [ ] **Step 2: Run the test and verify it fails on the missing core files**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: FAIL on `test_core_reference_inventory_matches_the_new_layout` because the `references/core/` files do not exist yet and the legacy flat files still exist.

- [ ] **Step 3: Write the new core references and remove the superseded flat files**

```markdown
# plugins/web-interface-guidelines/references/core/interactions.md
# Interactions

## Keyboard

- MUST: Full keyboard support per WAI-ARIA APG.
- MUST: Visible focus rings using `:focus-visible`; use `:focus-within` for grouped controls.
- MUST: Manage focus deliberately in dialogs, popovers, drawers, and menus.
- NEVER: Remove outlines without a visible replacement.

## Targets and Input

- MUST: Hit targets reach at least 24px; mobile targets should reach 44px.
- MUST: Mobile inputs use at least 16px text or another deliberate anti-zoom strategy.
- NEVER: Disable browser zoom.
- MUST: Use `touch-action: manipulation` where it improves tap behavior.

## State and Navigation

- MUST: Persist shareable UI state in the URL when it affects navigation, tabs, filters, pagination, or expanded panels.
- MUST: Preserve expected Back and Forward scroll restoration.
- MUST: Use links for navigation so browser behaviors work naturally.
- NEVER: Replace navigation links with clickable `div` or `button` elements.

## Feedback

- MUST: Loading buttons keep the original label visible.
- SHOULD: Add a small delay and minimum visible duration for spinners and skeletons.
- SHOULD: Use optimistic updates when success is likely and reconcile on failure.
- MUST: Confirm destructive actions or provide a safe undo window.
- MUST: Announce important async updates with `aria-live`.
- SHOULD: Use the ellipsis character for follow-up actions and in-progress states.
```

```markdown
# plugins/web-interface-guidelines/references/core/forms.md
# Forms

- MUST: Every form control has a programmatic label.
- MUST: Enter submits the obvious single-input case; in `textarea`, keep Enter for new lines and use Cmd/Ctrl+Enter for submit.
- MUST: Keep submit enabled until the request starts; disable only while the request is in flight.
- MUST: Allow incomplete submission so validation can explain what is missing.
- MUST: Accept text first and validate after; do not block typing.
- MUST: Place validation errors next to the field and focus the first failing field on submit.
- MUST: Use meaningful `name`, `autocomplete`, `type`, and `inputmode` values.
- SHOULD: Use placeholders as examples, not labels, and end them with `…`.
- MUST: Preserve compatibility with password managers and one-time-code flows.
- MUST: Warn before navigation when unsaved input would be lost.
- MUST: Make checkbox and radio labels part of the hit target.
- MUST: Normalize inconsequential trailing whitespace when input methods add it automatically.
```

```markdown
# plugins/web-interface-guidelines/references/core/animation.md
# Animation

- MUST: Honor `prefers-reduced-motion` with a reduced or disabled variant.
- SHOULD: Prefer CSS, then Web Animations API, then JavaScript animation libraries.
- MUST: Animate compositor-friendly properties such as `transform` and `opacity`.
- NEVER: Animate layout properties such as `top`, `left`, `width`, or `height`.
- NEVER: Use `transition: all`.
- SHOULD: Animate only to clarify cause and effect or add deliberate delight.
- SHOULD: Match easing to the type of movement.
- MUST: Keep animations interruptible by user input.
- MUST: Set a correct `transform-origin`.
- MUST: For animated SVGs, prefer a `<g>` wrapper with `transform-box: fill-box`.
```

```markdown
# plugins/web-interface-guidelines/references/core/layout.md
# Layout

- SHOULD: Use optical alignment when perception beats geometry.
- MUST: Align every element intentionally to a grid, edge, baseline, or optical center.
- SHOULD: Balance icon and text lockups by adjusting weight, size, spacing, or color.
- MUST: Check narrow mobile widths, laptop widths, and ultra-wide layouts.
- MUST: Respect safe-area insets on devices with notches or system overlays.
- MUST: Avoid accidental overflow and unnecessary scrollbars.
- SHOULD: Prefer flex, grid, intrinsic sizing, and wrapping over JavaScript measurement.
- MUST: Treat empty, sparse, dense, and error states as layout states, not just content states.
```

```markdown
# plugins/web-interface-guidelines/references/core/content-accessibility.md
# Content and Accessibility

- SHOULD: Prefer inline help over tooltips.
- MUST: Keep page titles accurate to the current task and context.
- MUST: Provide a next step or recovery path on every screen.
- MUST: Design empty, sparse, dense, and error states explicitly.
- MUST: Use redundant status cues instead of color alone.
- MUST: Give icon-only controls descriptive accessible names.
- MUST: Prefer semantic HTML before ARIA-heavy custom UI.
- MUST: Keep headings ordered and provide a skip link on full pages.
- MUST: Hide decorative elements from assistive tech and name meaningful ones accurately.
- MUST: Make layouts resilient to short, average, and very long user-generated content.
- MUST: Format dates, numbers, times, and currency for the user's locale.
- MUST: Prefer explicit language settings over IP or location inference.
- SHOULD: Use non-breaking spaces where units, shortcuts, and product names should stay together.
```

```markdown
# plugins/web-interface-guidelines/references/core/performance.md
# Performance

- SHOULD: Test on constrained devices and browsers, not just a fast desktop browser.
- MUST: Profile with CPU and network throttling when interactions depend on rendering or network speed.
- MUST: Track and reduce expensive rerenders.
- MUST: Keep input handling cheap; prefer uncontrolled inputs when controlled inputs are not needed.
- MUST: Batch layout reads and writes to avoid forced reflow.
- SHOULD: Treat mutation round trips as interactive work that should stay under about 500 ms.
- MUST: Virtualize or otherwise contain very large lists.
- MUST: Reserve layout space for images and media to avoid CLS.
- MUST: Preload only above-the-fold media that is genuinely critical.
- SHOULD: Preconnect or preload fonts and external origins only when they materially improve the first render.
- MUST: Move long-running work off the main thread when it would block interaction.
```

```markdown
# plugins/web-interface-guidelines/references/core/theming-copy.md
# Theming and Copy

## Theming

- MUST: Set the appropriate `color-scheme` for dark themes.
- SHOULD: Match browser UI chrome with a `theme-color` that fits the page background.
- MUST: Keep contrast high enough for readable text and usable controls.
- SHOULD: Prefer APCA-style perceptual contrast checks when available.
- MUST: Increase contrast on hover, active, and focus states.
- SHOULD: Use layered shadows, crisp borders, and nested radii intentionally.

## Copy

- MUST: Use active voice and action-oriented labels.
- MUST: Prefer specific button labels over vague continuation labels.
- MUST: Keep nouns and terminology consistent across a flow.
- SHOULD: Prefer concise copy that helps the user act or understand.
- MUST: Error messages explain the problem and the next step.
- SHOULD: Use numerals for counts and keep number-unit formatting consistent.
- SHOULD: Use `&` instead of `and` where space is tight and meaning stays clear.
```

```markdown
# plugins/web-interface-guidelines/references/core/anti-patterns.md
# Anti-Patterns

- Flag `user-scalable=no` and `maximum-scale=1`.
- Flag `transition: all`.
- Flag `outline: none` or `outline-none` without a visible focus replacement.
- Flag icon buttons without `aria-label`.
- Flag form controls without labels.
- Flag navigation handled by clickable non-link elements.
- Flag images without dimensions when they affect layout.
- Flag large list rendering without virtualization or containment.
- Flag hard-coded date, time, or number formatting where locale-aware formatting is expected.
- Flag generic loading labels that remove the original action text.
```

```bash
rm \
  plugins/web-interface-guidelines/references/interactions.md \
  plugins/web-interface-guidelines/references/forms.md \
  plugins/web-interface-guidelines/references/content-accessibility.md \
  plugins/web-interface-guidelines/references/layout-motion.md \
  plugins/web-interface-guidelines/references/performance.md \
  plugins/web-interface-guidelines/references/design-copywriting.md
```

- [ ] **Step 4: Run the test again**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: PASS with `Ran 3 tests` and `OK`.

- [ ] **Step 5: Commit the reference restructure**

```bash
git add \
  plugins/web-interface-guidelines/references/core \
  plugins/web-interface-guidelines/tests/test_plugin_layout.py \
  plugins/web-interface-guidelines/references/source-notes.md \
  plugins/web-interface-guidelines/references
git commit -m "refactor(web-interface-guidelines): split core reference corpus"
```

## Task 3: Add design and framework-specific references

**Files:**
- Modify: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`
- Create: `plugins/web-interface-guidelines/references/design/direction.md`
- Create: `plugins/web-interface-guidelines/references/design/typography-color.md`
- Create: `plugins/web-interface-guidelines/references/design/motion-composition.md`
- Create: `plugins/web-interface-guidelines/references/design/anti-slop.md`
- Create: `plugins/web-interface-guidelines/references/frameworks/react-next.md`
- Modify: `plugins/web-interface-guidelines/references/source-notes.md`
- Test: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`

- [ ] **Step 1: Extend the test with design and framework reference expectations**

```python
    def test_design_and_framework_references_exist(self) -> None:
        expected = {
            "references/design/direction.md",
            "references/design/typography-color.md",
            "references/design/motion-composition.md",
            "references/design/anti-slop.md",
            "references/frameworks/react-next.md",
            "references/source-notes.md",
        }
        for relpath in expected:
            self.assertTrue((PLUGIN / relpath).exists(), relpath)
```

- [ ] **Step 2: Run the test and confirm it fails on the new reference files**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: FAIL on `test_design_and_framework_references_exist` because the design and framework files do not exist yet.

- [ ] **Step 3: Write the Anthropic-derived design refs, React/Next add-on, and explicit source notes**

```markdown
# plugins/web-interface-guidelines/references/design/direction.md
# Direction

- Start by identifying the purpose, audience, and tone of the interface.
- Commit to a clear design point of view instead of drifting toward generic defaults.
- Present two or three directions before implementation when the user asks for design work.
- Choose one memorable differentiator that should survive coding and polish.
- Match the strength of the visual system to the product context; distinctive does not always mean loud.
- In established products, preserve system conventions unless the user explicitly asks for a stronger redesign.
```

```markdown
# plugins/web-interface-guidelines/references/design/typography-color.md
# Typography and Color

- Make typography a first-class choice rather than falling back to common default stacks.
- Pair display and body typography intentionally when the surface supports it.
- Use CSS variables or a similarly centralized system for color and typography tokens.
- Favor palettes with a clear hierarchy over timid evenly distributed color.
- Keep text readable and contrast-safe while still committing to a point of view.
- Avoid overused AI-generated defaults such as interchangeable sans stacks and purple-on-white startup gradients.
```

```markdown
# plugins/web-interface-guidelines/references/design/motion-composition.md
# Motion and Composition

- Use motion to reinforce hierarchy, reveal structure, and clarify cause and effect.
- Prefer a few meaningful animated moments over scattered micro-interactions.
- Let composition carry personality through spacing, overlap, asymmetry, rhythm, and background treatment.
- Match implementation complexity to the design direction; maximalist interfaces need more choreography than restrained ones.
- Build atmosphere with gradients, texture, pattern, shadow, and depth instead of defaulting to flat backgrounds.
```

```markdown
# plugins/web-interface-guidelines/references/design/anti-slop.md
# Anti-Slop

- Do not ship interchangeable SaaS layouts that could belong to any product.
- Do not default to generic font stacks such as Inter, Arial, Roboto, or the system stack unless the host product already chose them intentionally.
- Do not rely on predictable component patterns when the brief leaves room for stronger composition.
- Do not converge on the same palette, motion style, or aesthetic direction across unrelated interfaces.
- Distinctive minimalism is valid; generic minimalism is not.
```

```markdown
# plugins/web-interface-guidelines/references/frameworks/react-next.md
# React and Next.js

- Treat hydration safety as a first-class concern for inputs and date or time rendering.
- Inputs with `value` need `onChange`; otherwise prefer `defaultValue`.
- Keep controlled input loops cheap and prefer uncontrolled inputs when control is unnecessary.
- Reflect shareable state in the URL with framework-appropriate routing patterns.
- Prefer built-in loading primitives such as Suspense and route-level loading states when they fit the app.
- Keep image dimensions explicit and use framework image helpers deliberately to prevent layout shift.
- Preload fonts and critical assets only when they materially improve the first paint.
```

```markdown
# plugins/web-interface-guidelines/references/source-notes.md
# Source Notes

## Upstream Sources

- Vercel interface guidance:
  - `https://github.com/vercel-labs/web-interface-guidelines`
  - pinned revision: `3f6b1449dee158479deb8019f6372ff85e663406`
  - role in this plugin: concrete interface rules, anti-patterns, and review discipline
- Anthropic frontend design guidance:
  - `https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design`
  - pinned revision: `2d5c1bab92971bbdaecdb1767481973215ee7f2d`
  - role in this plugin: design direction, anti-generic stance, and generation posture

## Local Adaptation Rules

- `references/core/` stays close to Vercel's rule granularity and is only reorganized by topic.
- `references/design/` preserves Anthropic's strongest aesthetic-direction guidance in local wording.
- `references/frameworks/react-next.md` holds React and Next.js specifics so the core remains framework-agnostic.
- Skill files stay concise and point into the shared references instead of duplicating the corpus.

## Intentional Omissions

- No Claude-specific wrapper files are added in this plugin.
- No marketplace integration is added in this iteration.
- No attempt is made to mirror the upstream repository layout exactly.
```

- [ ] **Step 4: Run the layout test again**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: PASS with `Ran 4 tests` and `OK`.

- [ ] **Step 5: Commit the design and framework references**

```bash
git add \
  plugins/web-interface-guidelines/references/design \
  plugins/web-interface-guidelines/references/frameworks \
  plugins/web-interface-guidelines/references/source-notes.md \
  plugins/web-interface-guidelines/tests/test_plugin_layout.py
git commit -m "feat(web-interface-guidelines): add design and framework guidance"
```

## Task 4: Rewrite the apply and review skills around the new corpus

**Files:**
- Modify: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/SKILL.md`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-design/agents/openai.yaml`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/SKILL.md`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/agents/openai.yaml`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/SKILL.md`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/agents/openai.yaml`
- Test: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`

- [ ] **Step 1: Extend the test to lock in the critical skill contract markers**

```python
    def test_skill_contract_markers_exist(self) -> None:
        design_skill = (
            PLUGIN / "skills/web-interface-guidelines-design/SKILL.md"
        ).read_text(encoding="utf-8")
        apply_skill = (
            PLUGIN / "skills/web-interface-guidelines-apply/SKILL.md"
        ).read_text(encoding="utf-8")
        review_skill = (
            PLUGIN / "skills/web-interface-guidelines-review/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Present two or three viable directions", design_skill)
        self.assertIn("references/design/", design_skill)
        self.assertIn("references/core/", apply_skill)
        self.assertIn("references/frameworks/react-next.md", apply_skill)
        self.assertIn("file:line", review_skill)
        self.assertIn("anti-patterns", review_skill)
```

- [ ] **Step 2: Run the test and confirm it fails before the skill rewrites**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: FAIL on `test_skill_contract_markers_exist` because the existing `apply` and `review` skills still point at the old flattened corpus and the design skill is only a scaffold.

- [ ] **Step 3: Rewrite all three skills and their agent metadata**

```markdown
---
name: web-interface-guidelines-design
description: Use when creating, redesigning, or restyling a UI and Codex should establish a clear design direction before implementation.
---

# Web Interface Guidelines Design

## Overview

Establish a strong design direction before implementation begins. Use this skill to prevent generic output and force an intentional point of view that can survive coding and review.

## Workflow

1. Identify the UI surface, audience, constraints, and host product conventions.
2. Read the relevant files under `../../references/design/` and only the core constraints that materially shape the direction.
3. Present two or three viable directions with trade-offs.
4. Recommend one direction and commit to it.
5. Name one memorable differentiator that should still be visible after implementation.

## Reference Map

- `../../references/design/direction.md`
- `../../references/design/typography-color.md`
- `../../references/design/motion-composition.md`
- `../../references/design/anti-slop.md`
- `../../references/core/layout.md`
- `../../references/core/content-accessibility.md`

## Guardrails

- Preserve established product systems unless the user asks for a stronger redesign.
- Distinctive minimalism is acceptable; generic output is not.
- Keep the chosen direction compatible with accessibility, responsive behavior, and interaction rules.
```

```markdown
---
name: web-interface-guidelines-apply
description: Use when building or modifying frontend UI and implementation choices should follow the shared design, interaction, accessibility, performance, and copy guidance.
---

# Web Interface Guidelines Apply

## Overview

Implement or update UI in a way that preserves the intended direction while meeting the shared interface standards.

## Workflow

1. Start from an approved design direction when one exists; otherwise infer one explicitly.
2. Read only the relevant files under `../../references/core/`, `../../references/design/`, and `../../references/frameworks/` for the current surface.
3. Implement semantics, keyboard support, loading states, error states, responsive behavior, and performance-sensitive choices together.
4. Before finishing, check empty, loading, dense, error, destructive, and narrow-width behavior.

## Reference Map

- `../../references/core/interactions.md`
- `../../references/core/forms.md`
- `../../references/core/animation.md`
- `../../references/core/layout.md`
- `../../references/core/content-accessibility.md`
- `../../references/core/performance.md`
- `../../references/core/theming-copy.md`
- `../../references/design/direction.md`
- `../../references/design/typography-color.md`
- `../../references/design/motion-composition.md`
- `../../references/design/anti-slop.md`
- `../../references/frameworks/react-next.md`

## Guardrails

- Prefer native semantics before ARIA-heavy custom controls.
- Preserve established product language and systems in existing products.
- Do not add decorative motion that fights the interaction model or ignores reduced-motion preferences.
- Avoid checklist recital; turn the guidance into integrated implementation choices.
```

```markdown
---
name: web-interface-guidelines-review
description: Use when reviewing existing frontend UI or UI code for issues in direction, interactions, accessibility, forms, motion, performance, or copy.
---

# Web Interface Guidelines Review

## Overview

Audit UI code or diffs against the shared guideline corpus with findings first, high signal, and minimal subjectivity.

## Review Workflow

1. Read only the files needed for the surface under review.
2. Prioritize `../../references/core/anti-patterns.md` and the relevant core guidance.
3. Output findings first, grouped by file, using `file:line`.
4. Classify each issue as bug, regression risk, or polish.
5. If nothing is provably wrong, say so explicitly and then note residual testing gaps.

## Reference Map

- `../../references/core/anti-patterns.md`
- `../../references/core/interactions.md`
- `../../references/core/forms.md`
- `../../references/core/animation.md`
- `../../references/core/layout.md`
- `../../references/core/content-accessibility.md`
- `../../references/core/performance.md`
- `../../references/core/theming-copy.md`
- `../../references/design/anti-slop.md`

## Guardrails

- Prefer concrete violations and anti-patterns over broad aesthetic commentary.
- Use design guidance only when the UI is clearly generic or undirected.
- Keep findings terse and actionable.
```

```yaml
# plugins/web-interface-guidelines/skills/web-interface-guidelines-design/agents/openai.yaml
interface:
  display_name: "Web Interface Guidelines Design"
  short_description: "Define a strong UI direction before implementation"
  default_prompt: "Use $web-interface-guidelines-design to define the visual direction for this UI before implementation."
```

```yaml
# plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/agents/openai.yaml
interface:
  display_name: "Web Interface Guidelines Apply"
  short_description: "Build UI with the shared design and interface guidance"
  default_prompt: "Use $web-interface-guidelines-apply to build or update this UI with the shared design and interface guidelines."
```

```yaml
# plugins/web-interface-guidelines/skills/web-interface-guidelines-review/agents/openai.yaml
interface:
  display_name: "Web Interface Guidelines Review"
  short_description: "Audit UI code with findings-first web guidance"
  default_prompt: "Use $web-interface-guidelines-review to audit this UI or diff against the shared design and interface guidelines."
```

- [ ] **Step 4: Run the layout test again**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: PASS with `Ran 5 tests` and `OK`.

- [ ] **Step 5: Commit the skill rewrites**

```bash
git add \
  plugins/web-interface-guidelines/skills/web-interface-guidelines-design \
  plugins/web-interface-guidelines/skills/web-interface-guidelines-apply \
  plugins/web-interface-guidelines/skills/web-interface-guidelines-review \
  plugins/web-interface-guidelines/tests/test_plugin_layout.py
git commit -m "feat(web-interface-guidelines): rewrite skill contracts"
```

## Task 5: Validate the finished plugin end to end

**Files:**
- Modify: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`
- Test: `plugins/web-interface-guidelines/tests/test_plugin_layout.py`
- Test: `scripts/validate-skills.sh`

- [ ] **Step 1: Add one final test that asserts the review skill preserves the terse findings-first output rule**

```python
    def test_review_skill_keeps_findings_first_output_contract(self) -> None:
        review_skill = (
            PLUGIN / "skills/web-interface-guidelines-review/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("findings first", review_skill)
        self.assertIn("grouped by file", review_skill)
        self.assertIn("file:line", review_skill)
```

- [ ] **Step 2: Run the Python test suite**

Run: `python3 -m unittest plugins/web-interface-guidelines/tests/test_plugin_layout.py -v`

Expected: PASS with `Ran 6 tests` and `OK`.

- [ ] **Step 3: Run the repo skill validator**

Run: `bash scripts/validate-skills.sh`

Expected: PASS and output ending with `All skills validated successfully.`

- [ ] **Step 4: Inspect the final diff before committing**

Run: `git diff --stat -- plugins/web-interface-guidelines docs/superpowers/plans/2026-03-31-web-interface-guidelines.md`

Expected: Shows the new design skill, the restructured references tree, the rewritten `apply` and `review` skills, the structure test, and no unrelated files.

- [ ] **Step 5: Commit the validation pass**

```bash
git add \
  plugins/web-interface-guidelines \
  docs/superpowers/plans/2026-03-31-web-interface-guidelines.md
git commit -m "test(web-interface-guidelines): validate redesigned plugin"
```
