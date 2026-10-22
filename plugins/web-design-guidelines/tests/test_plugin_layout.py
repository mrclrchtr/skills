import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
CODEX_PLUGIN_JSON = ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
SKILL_DIR = ROOT / "skills" / "web-design-guidelines"
SKILL = SKILL_DIR / "SKILL.md"
SKILL_AGENT = SKILL_DIR / "agents" / "openai.yaml"
REVIEW_COMMAND = ROOT / "commands" / "review.md"
REVIEW_HELPER = ROOT / "skills" / "review" / "SKILL.md"
UI_REVIEWER_AGENT = ROOT / "agents" / "ui-reviewer.md"


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

    return interface


class PluginLayoutTest(unittest.TestCase):
    def test_unified_skill_discovery_and_prompts(self):
        skill_names = {
            path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(skill_names, {"web-design-guidelines", "review"})
        metadata, _ = parse_frontmatter(SKILL.read_text(encoding="utf-8"))
        self.assertEqual(metadata["name"], SKILL_DIR.name)
        self.assertTrue(metadata["description"])

        manifest = json.loads(CODEX_PLUGIN_JSON.read_text(encoding="utf-8"))
        self.assertEqual((ROOT / manifest["skills"]).resolve(), ROOT / "skills")
        agent = parse_interface_yaml(SKILL_AGENT.read_text(encoding="utf-8"))
        self.assertTrue(agent["display_name"])
        self.assertTrue(agent["short_description"])
        prompts = [*manifest["interface"]["defaultPrompt"], agent["default_prompt"]]
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                self.assertEqual(
                    re.findall(r"\$([a-z0-9-]+)", prompt),
                    [metadata["name"]],
                    "every default prompt must invoke the unified skill",
                )

    def test_manifests_and_marketplace_stay_in_sync(self):
        claude = json.loads(CLAUDE_PLUGIN_JSON.read_text(encoding="utf-8"))
        codex = json.loads(CODEX_PLUGIN_JSON.read_text(encoding="utf-8"))
        marketplace = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
        entry = next(
            item for item in marketplace["plugins"]
            if item["name"] == "web-design-guidelines"
        )

        self.assertEqual(claude["name"], ROOT.name)
        self.assertEqual(codex["name"], claude["name"])
        self.assertRegex(claude["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(codex["description"], claude["description"])
        self.assertEqual(entry["description"], claude["description"])
        self.assertEqual((REPO_ROOT / entry["source"]).resolve(), ROOT)
        self.assertNotIn("interface", claude)
        self.assertNotIn("skills", claude)
        self.assertIn(
            f"## Version\n\n{claude['version']}",
            (ROOT / "README.md").read_text(encoding="utf-8"),
        )

    def test_all_mapped_references_resolve_to_shared_corpus(self):
        references = SKILL_DIR / "references"
        self.assertTrue(references.is_symlink())
        self.assertEqual(references.resolve(strict=True), ROOT / "references")
        mapped = set(re.findall(
            r"`(references/[a-z0-9/.-]+\.md)`",
            SKILL.read_text(encoding="utf-8"),
        ))
        corpus = {
            str(path.relative_to(ROOT))
            for path in (ROOT / "references").rglob("*.md")
        }
        self.assertTrue(corpus)
        self.assertEqual(mapped, corpus, "reference map must expose the full corpus")
        for relative_path in mapped:
            with self.subTest(reference=relative_path):
                self.assertEqual(
                    (SKILL_DIR / relative_path).resolve(strict=True),
                    (ROOT / relative_path).resolve(strict=True),
                )

    def test_review_shortcut_uses_unified_review_mode(self):
        agent_text = UI_REVIEWER_AGENT.read_text(encoding="utf-8")
        self.assertIn("Invoke the `web-design-guidelines` skill", agent_text)
        self.assertIn("**Review mode**", agent_text)
        self.assertIn("read-only", agent_text)
        for path in (REVIEW_COMMAND, REVIEW_HELPER):
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("name: review", text)
                self.assertIn("web-design-guidelines:ui-reviewer", text)

    def test_active_entrypoints_do_not_invoke_removed_skills(self):
        paths = [
            REPO_ROOT / "README.md", ROOT / "README.md", SKILL, SKILL_AGENT,
            REVIEW_COMMAND, REVIEW_HELPER, UI_REVIEWER_AGENT, CODEX_PLUGIN_JSON,
        ]
        obsolete_invocation = re.compile(
            r"(?:\$|--skill |Invoke (?:the )?`)"
            r"web-design-guidelines-(?:design|apply|review)\b"
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertNotRegex(path.read_text(encoding="utf-8"), obsolete_invocation)
        for mode in ("design", "apply", "review"):
            self.assertFalse((ROOT / "skills" / f"web-design-guidelines-{mode}").exists())


if __name__ == "__main__":
    unittest.main()
