import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
ROOT_MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
DESIGN_SKILL = ROOT / "skills" / "web-design-guidelines-design" / "SKILL.md"
DESIGN_AGENT = ROOT / "skills" / "web-design-guidelines-design" / "agents" / "openai.yaml"
APPLY_SKILL = ROOT / "skills" / "web-design-guidelines-apply" / "SKILL.md"
APPLY_AGENT = ROOT / "skills" / "web-design-guidelines-apply" / "agents" / "openai.yaml"
REVIEW_SKILL = ROOT / "skills" / "web-design-guidelines-review" / "SKILL.md"
REVIEW_AGENT = ROOT / "skills" / "web-design-guidelines-review" / "agents" / "openai.yaml"

EXPECTED_DEFAULT_PROMPT = [
    "Use $web-design-guidelines-design to define the visual direction for this UI before implementation.",
    "Use $web-design-guidelines-apply to build or update this UI with the shared design and interface guidelines.",
    "Use $web-design-guidelines-review to audit this UI or diff against the shared design and interface guidelines.",
]

EXPECTED_DESIGN_DESCRIPTION = (
    "Use when creating, redesigning, or restyling a UI and Codex should establish "
    "a clear design direction before implementation."
)

EXPECTED_AGENT_DEFAULT_PROMPT = (
    "Use $web-design-guidelines-design to define the visual direction for this UI before implementation."
)

EXPECTED_AGENT_METADATA = {
    DESIGN_AGENT: {
        "display_name": "Web Design Guidelines Design",
        "short_description": "Define a strong UI direction before implementation",
        "default_prompt": EXPECTED_AGENT_DEFAULT_PROMPT,
    },
    APPLY_AGENT: {
        "display_name": "Web Design Guidelines Apply",
        "short_description": "Build UI with the shared design and interface guidance",
        "default_prompt": "Use $web-design-guidelines-apply to build or update this UI with the shared design and interface guidelines.",
    },
    REVIEW_AGENT: {
        "display_name": "Web Design Guidelines Review",
        "short_description": "Audit UI code with findings-first web guidance",
        "default_prompt": "Use $web-design-guidelines-review to audit this UI or diff against the shared design and interface guidelines.",
    },
}

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

EXPECTED_DESIGN_REFERENCE_CONTENT = {
    "references/design/direction.md": [
        "# Design Direction",
        "purpose, audience, and tone",
        "2-3 distinct directions",
        "memorable differentiator",
    ],
    "references/design/typography-color.md": [
        "# Typography and Color",
        "typography as a first-class design choice",
        "interchangeable sans stacks",
        "purple-on-white startup gradients",
    ],
    "references/design/motion-composition.md": [
        "# Motion and Composition",
        "motion to reinforce hierarchy",
        "cause and effect",
        "gradients, texture, pattern, shadow, and depth",
    ],
    "references/design/anti-slop.md": [
        "# Anti-Slop",
        "interchangeable SaaS layouts",
        "Distinctive minimalism",
    ],
    "references/frameworks/react-next.md": [
        "# React and Next.js",
        "hydration-safe rendering",
        "controlled inputs",
        "uncontrolled inputs",
        "URL state",
        "loading primitives",
    ],
}

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

EXPECTED_SKILL_CONTRACT_MARKERS = {
    DESIGN_SKILL: [
        "Present two or three viable directions",
        "references/design/",
    ],
    APPLY_SKILL: [
        "references/core/",
        "references/frameworks/react-next.md",
    ],
    REVIEW_SKILL: [
        "file:line",
        "anti-patterns",
    ],
}

EXPECTED_SOURCE_NOTES_SNIPPETS = [
    "https://github.com/vercel-labs/web-interface-guidelines",
    "3f6b1449dee158479deb8019f6372ff85e663406",
    "https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design",
    "2d5c1bab92971bbdaecdb1767481973215ee7f2d",
    "organized for consumption by the skill files",
    "packaged for both Codex and Claude",
    ".claude-plugin/plugin.json",
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
            self.assertEqual(frontmatter["name"], "web-design-guidelines-design")
            self.assertEqual(frontmatter["description"], EXPECTED_DESIGN_DESCRIPTION)

        with self.subTest("design skill body"):
            self.assertIn("## Overview", body)
            self.assertIn("## Workflow", body)
            self.assertIn("## Guardrails", body)
            self.assertIn("two or three viable directions with trade-offs", body)

        with self.subTest("design agent interface"):
            self.assertEqual(agent["interface"], EXPECTED_AGENT_METADATA[DESIGN_AGENT])

        with self.subTest("apply agent interface"):
            apply_agent = parse_interface_yaml(APPLY_AGENT.read_text(encoding="utf-8"))
            self.assertEqual(
                apply_agent["interface"], EXPECTED_AGENT_METADATA[APPLY_AGENT]
            )

        with self.subTest("review agent interface"):
            review_agent = parse_interface_yaml(
                REVIEW_AGENT.read_text(encoding="utf-8")
            )
            self.assertEqual(
                review_agent["interface"], EXPECTED_AGENT_METADATA[REVIEW_AGENT]
            )

    def test_claude_plugin_manifest_and_marketplace_entry(self):
        with self.subTest("claude plugin manifest exists"):
            self.assertTrue(
                CLAUDE_PLUGIN_JSON.exists(), f"missing {CLAUDE_PLUGIN_JSON}"
            )

        claude_manifest = json.loads(CLAUDE_PLUGIN_JSON.read_text(encoding="utf-8"))
        with self.subTest("claude plugin manifest metadata"):
            self.assertEqual(claude_manifest["name"], "web-design-guidelines")
            self.assertRegex(
                claude_manifest["version"],
                r"^\d+\.\d+\.\d+$",
                "version must be a semver string",
            )
            self.assertEqual(
                claude_manifest["description"],
                "Design, implement, and review web interfaces with shared UI guidance",
            )
            self.assertEqual(claude_manifest["author"]["name"], "mrclrchtr")
            self.assertNotIn("interface", claude_manifest)
            self.assertNotIn("skills", claude_manifest)

        marketplace = json.loads(ROOT_MARKETPLACE_JSON.read_text(encoding="utf-8"))
        entry = next(
            item
            for item in marketplace["plugins"]
            if item["name"] == "web-design-guidelines"
        )

        with self.subTest("claude marketplace entry"):
            self.assertEqual(entry["source"], "./plugins/web-design-guidelines")
            self.assertEqual(
                entry["description"],
                "Design, implement, and review web interfaces with shared UI guidance",
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

    def test_design_and_framework_reference_content(self):
        for relative_path, snippets in EXPECTED_DESIGN_REFERENCE_CONTENT.items():
            path = ROOT / relative_path
            text = path.read_text(encoding="utf-8")

            with self.subTest(file=relative_path):
                for snippet in snippets:
                    self.assertIn(snippet, text)

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
            self.assertIn("`../../references/core/anti-patterns.md`", review_text)
            self.assertIn("`../../references/design/anti-slop.md`", review_text)
            for relative_path in REMOVED_REFERENCE_PATHS:
                self.assertNotIn(relative_path, review_text)

    def test_source_notes_provenance_and_adaptation(self):
        text = (ROOT / "references/source-notes.md").read_text(encoding="utf-8")

        for snippet in EXPECTED_SOURCE_NOTES_SNIPPETS:
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, text)

    def test_skill_contract_markers(self):
        for path, snippets in EXPECTED_SKILL_CONTRACT_MARKERS.items():
            text = path.read_text(encoding="utf-8")

            for snippet in snippets:
                with self.subTest(file=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

    def test_review_skill_keeps_findings_first_output_contract(self):
        review_text = REVIEW_SKILL.read_text(encoding="utf-8")

        self.assertIn("findings first", review_text)
        self.assertIn("grouped by file", review_text)
        self.assertIn("file:line", review_text)
