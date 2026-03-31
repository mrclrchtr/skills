import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
DESIGN_SKILL = ROOT / "skills" / "web-interface-guidelines-design" / "SKILL.md"
DESIGN_AGENT = ROOT / "skills" / "web-interface-guidelines-design" / "agents" / "openai.yaml"

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
