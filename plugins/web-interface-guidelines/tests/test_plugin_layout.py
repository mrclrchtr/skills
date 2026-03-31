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


class PluginLayoutTest(unittest.TestCase):
    def test_three_skill_plugin_contract(self):
        with PLUGIN_JSON.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)

        with self.subTest("defaultPrompt"):
            self.assertEqual(
                manifest["interface"]["defaultPrompt"],
                EXPECTED_DEFAULT_PROMPT,
            )

        with self.subTest("design skill SKILL.md"):
            self.assertTrue(DESIGN_SKILL.exists(), f"missing {DESIGN_SKILL}")

        with self.subTest("design skill openai.yaml"):
            self.assertTrue(DESIGN_AGENT.exists(), f"missing {DESIGN_AGENT}")
