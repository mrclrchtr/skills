import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
DESIGN_SKILL = ROOT / "skills" / "web-interface-guidelines-design" / "SKILL.md"
DESIGN_AGENT = ROOT / "skills" / "web-interface-guidelines-design" / "agents" / "openai.yaml"
APPLY_SKILL = ROOT / "skills" / "web-interface-guidelines-apply" / "SKILL.md"
REVIEW_SKILL = ROOT / "skills" / "web-interface-guidelines-review" / "SKILL.md"

EXPECTED_DEFAULT_PROMPT = [
    "Use $web-interface-guidelines-design to define the visual direction for this UI before implementation.",
    "Use $web-interface-guidelines-apply to build or update this UI with the shared design and interface guidelines.",
    "Use $web-interface-guidelines-review to audit this UI or diff against the shared design and interface guidelines.",
]

EXPECTED_DESIGN_DESCRIPTION = (
    "Use when creating, redesigning, or restyling a UI and Codex should establish "
    "a clear design direction before implementation."
)

EXPECTED_AGENT_DEFAULT_PROMPT = (
    "Use $web-interface-guidelines-design to define the visual direction for this UI before implementation."
)

EXPECTED_CORE_REFERENCE_FILES = [
    "references/core/interactions.md",
    "references/core/forms.md",
    "references/core/animation.md",
    "references/core/layout.md",
    "references/core/content-accessibility.md",
    "references/core/performance.md",
    "references/core/theming-copy.md",
    "references/core/anti-patterns.md",
]

EXPECTED_DESIGN_AND_FRAMEWORK_REFERENCE_FILES = [
    "references/design/direction.md",
    "references/design/typography-color.md",
    "references/design/motion-composition.md",
    "references/design/anti-slop.md",
    "references/frameworks/react-next.md",
    "references/source-notes.md",
]

EXPECTED_LEGACY_REFERENCE_FILES = [
    "references/interactions.md",
    "references/forms.md",
    "references/content-accessibility.md",
    "references/layout-motion.md",
    "references/performance.md",
    "references/design-copywriting.md",
]

EXPECTED_APPLY_CORE_REFERENCES = [
    "../../references/core/interactions.md",
    "../../references/core/forms.md",
    "../../references/core/animation.md",
    "../../references/core/layout.md",
    "../../references/core/content-accessibility.md",
    "../../references/core/performance.md",
    "../../references/core/theming-copy.md",
]

EXPECTED_REVIEW_CORE_REFERENCES = EXPECTED_APPLY_CORE_REFERENCES + [
    "../../references/core/anti-patterns.md",
]

REMOVED_REFERENCE_PATHS = [
    "../../references/interactions.md",
    "../../references/forms.md",
    "../../references/content-accessibility.md",
    "../../references/layout-motion.md",
    "../../references/performance.md",
    "../../references/design-copywriting.md",
]


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError("missing frontmatter start marker")

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError as exc:
        raise AssertionError("missing frontmatter end marker") from exc

    metadata = {}
    for line in lines[1:end_index]:
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')

    body = "\n".join(lines[end_index + 1 :])
    return metadata, body


def parse_interface_yaml(text):
    interface = {}
    in_interface = False

    for line in text.splitlines():
        if not line.strip():
            continue
        if line == "interface:":
            in_interface = True
            continue
        if in_interface and line.startswith("  "):
            key, value = line.strip().split(":", 1)
            interface[key.strip()] = value.strip().strip('"')
            continue
        if in_interface:
            break

    return {"interface": interface}


class PluginLayoutTest(unittest.TestCase):
    def test_three_skill_plugin_contract(self):
        with PLUGIN_JSON.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)

        with self.subTest("design skill exists"):
            self.assertTrue(DESIGN_SKILL.exists(), f"missing {DESIGN_SKILL}")

        skill_text = DESIGN_SKILL.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(skill_text)

        with self.subTest("design agent exists"):
            self.assertTrue(DESIGN_AGENT.exists(), f"missing {DESIGN_AGENT}")

        agent_text = DESIGN_AGENT.read_text(encoding="utf-8")
        agent = parse_interface_yaml(agent_text)

        with self.subTest("defaultPrompt"):
            self.assertEqual(
                manifest["interface"]["defaultPrompt"],
                EXPECTED_DEFAULT_PROMPT,
            )

        with self.subTest("design skill frontmatter"):
            self.assertEqual(frontmatter["name"], "web-interface-guidelines-design")
            self.assertEqual(frontmatter["description"], EXPECTED_DESIGN_DESCRIPTION)

        with self.subTest("design skill body"):
            self.assertIn("## Overview", body)
            self.assertIn("## Workflow", body)
            self.assertIn("## Guardrails", body)
            self.assertIn("two or three viable directions with trade-offs", body)

        with self.subTest("design agent interface"):
            self.assertEqual(
                agent["interface"]["display_name"],
                "Web Interface Guidelines Design",
            )
            self.assertEqual(
                agent["interface"]["short_description"],
                "Define a UI direction before implementation",
            )
            self.assertEqual(
                agent["interface"]["default_prompt"],
                EXPECTED_AGENT_DEFAULT_PROMPT,
            )

    def test_core_reference_corpus_layout(self):
        for relative_path in EXPECTED_CORE_REFERENCE_FILES:
            with self.subTest(file=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.exists(), f"missing {path}")

    def test_design_and_framework_reference_layout(self):
        for relative_path in EXPECTED_DESIGN_AND_FRAMEWORK_REFERENCE_FILES:
            with self.subTest(file=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.exists(), f"missing {path}")

    def test_legacy_reference_paths_removed(self):
        for relative_path in EXPECTED_LEGACY_REFERENCE_FILES:
            with self.subTest(file=relative_path):
                path = ROOT / relative_path
                self.assertFalse(
                    path.exists(), f"legacy file should be removed: {path}"
                )

    def test_apply_and_review_skill_reference_maps(self):
        apply_text = APPLY_SKILL.read_text(encoding="utf-8")
        review_text = REVIEW_SKILL.read_text(encoding="utf-8")

        with self.subTest("apply skill core references"):
            for relative_path in EXPECTED_APPLY_CORE_REFERENCES:
                self.assertIn(relative_path, apply_text)
            self.assertIn("`../../references/core/`", apply_text)
            for relative_path in REMOVED_REFERENCE_PATHS:
                self.assertNotIn(relative_path, apply_text)

        with self.subTest("review skill core references"):
            for relative_path in EXPECTED_REVIEW_CORE_REFERENCES:
                self.assertIn(relative_path, review_text)
            self.assertIn("`../../references/core/`", review_text)
            for relative_path in REMOVED_REFERENCE_PATHS:
                self.assertNotIn(relative_path, review_text)
