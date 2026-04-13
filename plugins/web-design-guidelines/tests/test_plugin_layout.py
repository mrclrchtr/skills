import json
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
REVIEW_COMMAND = ROOT / "commands" / "review.md"
UI_REVIEWER_AGENT = ROOT / "agents" / "ui-reviewer.md"
UNIFIED_SKILL_DIR = ROOT / "skills" / "web-design-guidelines"
DESIGN_REFERENCES = ROOT / "skills" / "web-design-guidelines-design" / "references"
APPLY_REFERENCES = ROOT / "skills" / "web-design-guidelines-apply" / "references"
REVIEW_REFERENCES = ROOT / "skills" / "web-design-guidelines-review" / "references"

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
    "references/frameworks/mantine.md",
    "references/frameworks/tailwind-integration.md",
]

EXPECTED_META_REFERENCE_FILES = [
    "references/source-notes.md",
]

EXPECTED_SKILL_CONTRACT_MARKERS = {
    DESIGN_SKILL: [
        "Present two or three viable directions",
        "references/design/",
        "project-local design system",
    ],
    APPLY_SKILL: [
        "references/core/",
        "references/frameworks/react-next.md",
        "project-local design system",
    ],
    REVIEW_SKILL: [
        "file:line",
        "anti-patterns",
        "project-local design system",
    ],
}


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
    def test_specialized_skill_plugin_contract(self):
        with PLUGIN_JSON.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)

        self.assertTrue(DESIGN_SKILL.exists(), f"missing {DESIGN_SKILL}")
        self.assertTrue(APPLY_SKILL.exists(), f"missing {APPLY_SKILL}")
        self.assertTrue(REVIEW_SKILL.exists(), f"missing {REVIEW_SKILL}")
        self.assertTrue(DESIGN_AGENT.exists(), f"missing {DESIGN_AGENT}")
        self.assertTrue(APPLY_AGENT.exists(), f"missing {APPLY_AGENT}")
        self.assertTrue(REVIEW_AGENT.exists(), f"missing {REVIEW_AGENT}")
        self.assertTrue(REVIEW_COMMAND.exists(), f"missing {REVIEW_COMMAND}")
        self.assertTrue(UI_REVIEWER_AGENT.exists(), f"missing {UI_REVIEWER_AGENT}")
        self.assertFalse(UNIFIED_SKILL_DIR.exists(), f"unexpected {UNIFIED_SKILL_DIR}")
        self.assertTrue(DESIGN_REFERENCES.is_symlink(), f"expected symlink: {DESIGN_REFERENCES}")
        self.assertTrue(APPLY_REFERENCES.is_symlink(), f"expected symlink: {APPLY_REFERENCES}")
        self.assertTrue(REVIEW_REFERENCES.is_symlink(), f"expected symlink: {REVIEW_REFERENCES}")

        design_frontmatter, design_body = parse_frontmatter(
            DESIGN_SKILL.read_text(encoding="utf-8")
        )
        design_agent = parse_interface_yaml(DESIGN_AGENT.read_text(encoding="utf-8"))
        apply_agent = parse_interface_yaml(APPLY_AGENT.read_text(encoding="utf-8"))
        review_agent = parse_interface_yaml(REVIEW_AGENT.read_text(encoding="utf-8"))

        self.assertEqual(manifest["interface"]["defaultPrompt"], EXPECTED_DEFAULT_PROMPT)
        self.assertEqual(design_frontmatter["name"], "web-design-guidelines-design")
        self.assertEqual(design_frontmatter["description"], EXPECTED_DESIGN_DESCRIPTION)
        self.assertIn("two or three viable directions with trade-offs", design_body)
        self.assertEqual(design_agent["interface"], EXPECTED_AGENT_METADATA[DESIGN_AGENT])
        self.assertEqual(apply_agent["interface"], EXPECTED_AGENT_METADATA[APPLY_AGENT])
        self.assertEqual(review_agent["interface"], EXPECTED_AGENT_METADATA[REVIEW_AGENT])

    def test_claude_plugin_manifest_and_marketplace_entry(self):
        self.assertTrue(CLAUDE_PLUGIN_JSON.exists(), f"missing {CLAUDE_PLUGIN_JSON}")

        claude_manifest = json.loads(CLAUDE_PLUGIN_JSON.read_text(encoding="utf-8"))
        self.assertEqual(claude_manifest["name"], "web-design-guidelines")
        self.assertRegex(claude_manifest["version"], r"^\d+\.\d+\.\d+$")
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

        self.assertEqual(entry["source"], "./plugins/web-design-guidelines")
        self.assertEqual(
            entry["description"],
            "Design, implement, and review web interfaces with shared UI guidance",
        )

    def test_shared_reference_corpus_layout(self):
        for relative_path in EXPECTED_CORE_REFERENCE_FILES + EXPECTED_DESIGN_AND_FRAMEWORK_REFERENCE_FILES + EXPECTED_META_REFERENCE_FILES:
            with self.subTest(file=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.exists(), f"missing {path}")

    def test_skill_contract_markers(self):
        for path, snippets in EXPECTED_SKILL_CONTRACT_MARKERS.items():
            text = path.read_text(encoding="utf-8")
            for snippet in snippets:
                with self.subTest(file=path.name, snippet=snippet):
                    self.assertIn(snippet, text)

    def test_review_command_and_agent_contract(self):
        command_text = REVIEW_COMMAND.read_text(encoding="utf-8")
        agent_text = UI_REVIEWER_AGENT.read_text(encoding="utf-8")

        self.assertIn("name: review", command_text)
        self.assertIn("ui-reviewer", command_text)
        self.assertIn("/web-design-guidelines:review", agent_text)
        self.assertIn("Invoke the `web-design-guidelines-review` skill", agent_text)
        self.assertNotIn("Invoke the `web-design-guidelines` skill. Use its **Review mode** workflow", agent_text)


if __name__ == "__main__":
    unittest.main()
