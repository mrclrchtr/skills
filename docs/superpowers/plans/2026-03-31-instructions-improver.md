# Instructions Improver Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a repo-local dual-platform `instructions-improver` plugin for Codex and Claude that audits, proposes, and applies targeted updates to `AGENTS.md`, `CLAUDE.md`, and `.claude.local.md` while enforcing the `AGENTS.md`-canonical relation model.

**Architecture:** Keep the feature single-sourced in `plugins/instructions-improver/`. A small tested Python helper performs deterministic file discovery, role classification, relation checks, and routing hints; the shared skill and Claude command consume that helper and stay focused on reporting, diff proposal, and approved edits. Repo-level marketplace metadata and validation scripts expose the same plugin cleanly to both Claude and Codex.

**Tech Stack:** Markdown skills, JSON plugin manifests, Python 3 (`argparse`, `json`, `pathlib`, `unittest`), Bash validation scripts

---

## File Map

### Create

- `plugins/instructions-improver/.codex-plugin/plugin.json`
- `plugins/instructions-improver/.claude-plugin/plugin.json`
- `plugins/instructions-improver/commands/revise-instructions.md`
- `plugins/instructions-improver/scripts/instruction_docs_analyzer.py`
- `plugins/instructions-improver/skills/instructions-improver/SKILL.md`
- `plugins/instructions-improver/skills/instructions-improver/agents/openai.yaml`
- `plugins/instructions-improver/skills/instructions-improver/references/file-roles.md`
- `plugins/instructions-improver/skills/instructions-improver/references/quality-rubric.md`
- `plugins/instructions-improver/tests/test_instruction_docs_analyzer.py`
- `plugins/instructions-improver/tests/test_plugin_metadata.py`
- `plugins/instructions-improver/tests/fixtures/linked/AGENTS.md`
- `plugins/instructions-improver/tests/fixtures/linked/CLAUDE.md`
- `plugins/instructions-improver/tests/fixtures/missing-ref/AGENTS.md`
- `plugins/instructions-improver/tests/fixtures/missing-ref/CLAUDE.md`
- `plugins/instructions-improver/tests/fixtures/duplicate-shared/AGENTS.md`
- `plugins/instructions-improver/tests/fixtures/duplicate-shared/CLAUDE.md`
- `plugins/instructions-improver/tests/fixtures/local-misfiled/.claude.local.md`
- `.agents/plugins/marketplace.json`

### Modify

- `.claude-plugin/marketplace.json`
- `README.md`
- `scripts/validate-skills.sh`

## Task 1: Build the deterministic analyzer helper

**Files:**
- Create: `plugins/instructions-improver/scripts/instruction_docs_analyzer.py`
- Create: `plugins/instructions-improver/tests/test_instruction_docs_analyzer.py`
- Create: `plugins/instructions-improver/tests/fixtures/linked/AGENTS.md`
- Create: `plugins/instructions-improver/tests/fixtures/linked/CLAUDE.md`
- Create: `plugins/instructions-improver/tests/fixtures/missing-ref/AGENTS.md`
- Create: `plugins/instructions-improver/tests/fixtures/missing-ref/CLAUDE.md`
- Create: `plugins/instructions-improver/tests/fixtures/duplicate-shared/AGENTS.md`
- Create: `plugins/instructions-improver/tests/fixtures/duplicate-shared/CLAUDE.md`
- Create: `plugins/instructions-improver/tests/fixtures/local-misfiled/.claude.local.md`
- Test: `plugins/instructions-improver/tests/test_instruction_docs_analyzer.py`

- [ ] **Step 1: Create fixture docs that express the relation rules**

````markdown
# plugins/instructions-improver/tests/fixtures/linked/AGENTS.md
# Shared Instructions

- Run `mise install` before local validation.
- Use `bash scripts/validate-skills.sh` before committing skill changes.
```

```markdown
# plugins/instructions-improver/tests/fixtures/linked/CLAUDE.md
@AGENTS.md

## Claude Notes

- Prefer `/plugin` commands when testing Claude plugin behavior.
```

```markdown
# plugins/instructions-improver/tests/fixtures/missing-ref/AGENTS.md
# Shared Instructions

- Shared commands belong here.
```

```markdown
# plugins/instructions-improver/tests/fixtures/missing-ref/CLAUDE.md
## Claude Notes

- This file forgot to load the shared instructions.
```

```markdown
# plugins/instructions-improver/tests/fixtures/duplicate-shared/AGENTS.md
# Shared Instructions

- Run `bash scripts/validate-skills.sh` before committing skill changes.
```

```markdown
# plugins/instructions-improver/tests/fixtures/duplicate-shared/CLAUDE.md
@AGENTS.md

## Claude Notes

- Run `bash scripts/validate-skills.sh` before committing skill changes.
```

```markdown
# plugins/instructions-improver/tests/fixtures/local-misfiled/.claude.local.md
# Local Notes

- Every teammate must run `mise install` before editing this repo.
```
````

- [ ] **Step 2: Write the failing analyzer tests first**

```python
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "plugins/instructions-improver/scripts"))

from instruction_docs_analyzer import analyze_repo  # noqa: E402


class InstructionDocsAnalyzerTest(unittest.TestCase):
    def test_linked_fixture_has_no_relation_findings(self) -> None:
        report = analyze_repo(ROOT / "plugins/instructions-improver/tests/fixtures/linked")
        self.assertEqual(
            [finding["code"] for finding in report["findings"]],
            [],
        )

    def test_missing_ref_fixture_flags_missing_agents_reference(self) -> None:
        report = analyze_repo(ROOT / "plugins/instructions-improver/tests/fixtures/missing-ref")
        self.assertIn(
            "missing_agents_reference",
            [finding["code"] for finding in report["findings"]],
        )

    def test_duplicate_fixture_flags_duplicate_shared_content(self) -> None:
        report = analyze_repo(ROOT / "plugins/instructions-improver/tests/fixtures/duplicate-shared")
        self.assertIn(
            "duplicate_shared_content",
            [finding["code"] for finding in report["findings"]],
        )

    def test_local_fixture_flags_shared_content_in_local_file(self) -> None:
        report = analyze_repo(ROOT / "plugins/instructions-improver/tests/fixtures/local-misfiled")
        self.assertIn(
            "shared_content_in_local_file",
            [finding["code"] for finding in report["findings"]],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests to verify they fail before implementation**

Run: `python3 -m unittest discover -s plugins/instructions-improver/tests -p 'test_instruction_docs_analyzer.py' -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'instruction_docs_analyzer'`

- [ ] **Step 4: Implement the helper with discovery, classification, and finding codes**

```python
#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


SUPPORTED_FILENAMES = ("AGENTS.md", "CLAUDE.md", ".claude.local.md")
SHARED_HINTS = ("must ", "every teammate", "run `", "shared", "team")


def classify_path(path: Path) -> str:
    if path.name == "AGENTS.md":
        return "canonical_shared"
    if path.name == "CLAUDE.md":
        return "claude_project"
    return "claude_local"


def discover_files(repo_root: Path) -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    for candidate in sorted(repo_root.rglob("*")):
        if candidate.is_file() and candidate.name in SUPPORTED_FILENAMES:
            files.append(
                {
                    "path": candidate.relative_to(repo_root).as_posix(),
                    "role": classify_path(candidate),
                    "content": candidate.read_text(encoding="utf-8"),
                }
            )
    return files


def analyze_repo(repo_root: Path) -> dict[str, object]:
    files = discover_files(repo_root)
    by_name = {item["path"]: item for item in files}
    findings: list[dict[str, str]] = []

    agents_files = [item for item in files if item["role"] == "canonical_shared"]
    claude_files = [item for item in files if item["role"] == "claude_project"]
    local_files = [item for item in files if item["role"] == "claude_local"]

    if agents_files and claude_files:
        for claude_file in claude_files:
            if "@AGENTS.md" not in claude_file["content"]:
                findings.append(
                    {
                        "code": "missing_agents_reference",
                        "path": claude_file["path"],
                        "message": "CLAUDE.md should load @AGENTS.md when both files exist.",
                    }
                )

    shared_lines = set()
    for agents_file in agents_files:
        shared_lines.update(
            line.strip()
            for line in agents_file["content"].splitlines()
            if line.strip().startswith("- ")
        )

    for claude_file in claude_files:
        duplicate_lines = [
            line.strip()
            for line in claude_file["content"].splitlines()
            if line.strip() in shared_lines
        ]
        if duplicate_lines:
            findings.append(
                {
                    "code": "duplicate_shared_content",
                    "path": claude_file["path"],
                    "message": f"Move duplicated shared lines into AGENTS.md only: {duplicate_lines[0]}",
                }
            )

    for local_file in local_files:
        lowered = local_file["content"].lower()
        if any(hint in lowered for hint in SHARED_HINTS):
            findings.append(
                {
                    "code": "shared_content_in_local_file",
                    "path": local_file["path"],
                    "message": "Move team-shared guidance out of .claude.local.md.",
                }
            )

    return {"files": by_name, "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()

    report = analyze_repo(Path(args.root).resolve())
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for finding in report["findings"]:
            print(f'{finding["code"]}: {finding["path"]} - {finding["message"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run the analyzer tests again and verify they pass**

Run: `python3 -m unittest discover -s plugins/instructions-improver/tests -p 'test_instruction_docs_analyzer.py' -v`

Expected: PASS with 4 tests run and 0 failures

- [ ] **Step 6: Commit the helper foundation**

```bash
git add plugins/instructions-improver/scripts/instruction_docs_analyzer.py \
  plugins/instructions-improver/tests/test_instruction_docs_analyzer.py \
  plugins/instructions-improver/tests/fixtures
git commit -m "feat(instructions-improver): add relation analyzer helper"
```

## Task 2: Add dual-platform plugin metadata and marketplace registration

**Files:**
- Create: `plugins/instructions-improver/.codex-plugin/plugin.json`
- Create: `plugins/instructions-improver/.claude-plugin/plugin.json`
- Create: `plugins/instructions-improver/tests/test_plugin_metadata.py`
- Create: `.agents/plugins/marketplace.json`
- Modify: `.claude-plugin/marketplace.json`
- Test: `plugins/instructions-improver/tests/test_plugin_metadata.py`

- [ ] **Step 1: Write failing metadata tests**

```python
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]


class PluginMetadataTest(unittest.TestCase):
    def test_codex_plugin_manifest_exists(self) -> None:
        manifest_path = ROOT / "plugins/instructions-improver/.codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "instructions-improver")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_claude_plugin_manifest_exists(self) -> None:
        manifest_path = ROOT / "plugins/instructions-improver/.claude-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "instructions-improver")
        self.assertEqual(manifest["version"], "1.0.0")

    def test_codex_marketplace_points_at_plugin(self) -> None:
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        entry = next(item for item in marketplace["plugins"] if item["name"] == "instructions-improver")
        self.assertEqual(entry["source"]["path"], "./plugins/instructions-improver")

    def test_claude_marketplace_points_at_plugin(self) -> None:
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        entry = next(item for item in marketplace["plugins"] if item["name"] == "instructions-improver")
        self.assertEqual(entry["source"], "./plugins/instructions-improver")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the metadata tests and verify they fail**

Run: `python3 -m unittest discover -s plugins/instructions-improver/tests -p 'test_plugin_metadata.py' -v`

Expected: FAIL with `FileNotFoundError` for the missing plugin manifests

- [ ] **Step 3: Create the Codex plugin manifest**

```json
{
  "name": "instructions-improver",
  "version": "1.0.0",
  "description": "Audit and improve AGENTS.md and Claude instruction files while keeping file roles and relations clean.",
  "author": {
    "name": "mrclrchtr",
    "url": "https://github.com/mrclrchtr"
  },
  "repository": "https://github.com/mrclrchtr/skills",
  "license": "MIT",
  "keywords": ["instructions", "agents", "claude", "codex", "documentation"],
  "skills": "./skills/",
  "interface": {
    "displayName": "Instructions Improver",
    "shortDescription": "Maintain AGENTS.md and CLAUDE.md",
    "longDescription": "Audit, propose, and apply targeted improvements to AGENTS.md, CLAUDE.md, and .claude.local.md while preserving the AGENTS.md canonical model.",
    "developerName": "mrclrchtr",
    "category": "Productivity",
    "capabilities": ["Interactive", "Write"],
    "websiteURL": "https://github.com/mrclrchtr/skills",
    "privacyPolicyURL": "https://github.com/mrclrchtr/skills",
    "termsOfServiceURL": "https://github.com/mrclrchtr/skills",
    "defaultPrompt": [
      "Use $instructions-improver to audit AGENTS.md and CLAUDE.md.",
      "Use $instructions-improver to fix AGENTS.md and CLAUDE.md relations.",
      "Use $instructions-improver to propose session learnings for shared docs."
    ],
    "brandColor": "#1F6FEB"
  }
}
```

- [ ] **Step 4: Create the Claude plugin manifest and register both marketplaces**

```json
{
  "name": "instructions-improver",
  "description": "Audit and improve AGENTS.md, CLAUDE.md, and .claude.local.md with an AGENTS.md-first relation model.",
  "version": "1.0.0",
  "author": {
    "name": "mrclrchtr"
  }
}
```

```json
{
  "name": "mrclrchtr-codex",
  "interface": {
    "displayName": "mrclrchtr Codex Plugins"
  },
  "plugins": [
    {
      "name": "instructions-improver",
      "source": {
        "source": "local",
        "path": "./plugins/instructions-improver"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

```json
{
  "name": "instructions-improver",
  "source": "./plugins/instructions-improver",
  "description": "Audit and improve AGENTS.md, CLAUDE.md, and .claude.local.md with an AGENTS.md-first relation model.",
  "keywords": ["instructions", "agents", "claude", "codex"]
}
```

- [ ] **Step 5: Run the metadata tests again and verify they pass**

Run: `python3 -m unittest discover -s plugins/instructions-improver/tests -p 'test_plugin_metadata.py' -v`

Expected: PASS with 4 tests run and 0 failures

- [ ] **Step 6: Commit the plugin packaging layer**

```bash
git add plugins/instructions-improver/.codex-plugin/plugin.json \
  plugins/instructions-improver/.claude-plugin/plugin.json \
  plugins/instructions-improver/tests/test_plugin_metadata.py \
  .agents/plugins/marketplace.json \
  .claude-plugin/marketplace.json
git commit -m "feat(instructions-improver): add plugin manifests and marketplaces"
```

## Task 3: Write the shared skill and reference docs

**Files:**
- Create: `plugins/instructions-improver/skills/instructions-improver/SKILL.md`
- Create: `plugins/instructions-improver/skills/instructions-improver/agents/openai.yaml`
- Create: `plugins/instructions-improver/skills/instructions-improver/references/file-roles.md`
- Create: `plugins/instructions-improver/skills/instructions-improver/references/quality-rubric.md`
- Test: `plugins/instructions-improver/skills/instructions-improver/SKILL.md`

- [ ] **Step 1: Write the file-role reference**

```markdown
# File Roles

## AGENTS.md

- Canonical shared instruction source
- Shared commands, repo workflow, architecture notes, cross-agent rules
- Should not contain Claude-only or local-only guidance

## CLAUDE.md

- Claude-facing shim plus Claude-only additions
- Must load `@AGENTS.md` when both files exist
- Should not duplicate shared guidance from `AGENTS.md`

## .claude.local.md

- Personal local override layer
- Machine-specific and personal workflow notes only
- Must not contain team-shared instructions or secrets
```

- [ ] **Step 2: Write the quality rubric reference**

```markdown
# Quality Rubric

Score every discovered instruction file against these checks:

1. Role clarity: the file content matches its intended role
2. Actionability: commands and rules are specific and executable
3. Currency: stale workflows are called out
4. Conciseness: obvious prompt bloat is flagged
5. Relation hygiene: shared, Claude-specific, and local-only guidance live in the right file

Always report:

- Files found
- Relation findings
- File-by-file quality notes
- Recommended moves or additions
- Minimal diffs before any edit
```

- [ ] **Step 3: Write the shared skill that uses the helper**

````markdown
---
name: instructions-improver
description: Audit and improve AGENTS.md, CLAUDE.md, and .claude.local.md. Use when the user asks to check, update, sync, or fix instruction files or their relations across Codex and Claude.
---

# Instructions Improver

Use `AGENTS.md` as the canonical shared source. Treat `CLAUDE.md` as a Claude-specific shim that should load `@AGENTS.md` when both files exist. Treat `.claude.local.md` as a local-only override layer.

## Workflow

1. Run the helper first:

```bash
python3 plugins/instructions-improver/scripts/instruction_docs_analyzer.py --root . --format json
```

2. Read the relevant files named in the helper output.
3. Produce an audit report before editing:
   - Files found
   - Relation findings
   - Quality notes
   - Minimal proposed diffs
4. Ask for approval before editing any file.
5. In apply or sync mode:
   - preserve existing structure
   - keep edits minimal
   - avoid duplicating shared content
   - keep Claude-specific notes in `CLAUDE.md`
   - keep personal notes in `.claude.local.md`

## Required behaviors

- If both `AGENTS.md` and `CLAUDE.md` exist and `CLAUDE.md` does not load `@AGENTS.md`, propose adding it.
- If `CLAUDE.md` duplicates shared command lists from `AGENTS.md`, propose deleting the duplicates instead of expanding `AGENTS.md`.
- If `.claude.local.md` contains team-shared guidance, propose moving it to `AGENTS.md`.
- Never make large rewrites when a targeted diff is enough.
```
````

- [ ] **Step 4: Add UI metadata for the skill**

```yaml
interface:
  display_name: "Instructions Improver"
  short_description: "Audit AGENTS.md and CLAUDE.md"
  default_prompt: "Use $instructions-improver to audit AGENTS.md, CLAUDE.md, and .claude.local.md and propose minimal relation fixes."
```

- [ ] **Step 5: Validate the skill directly**

Run: `uvx --from "git+https://github.com/agentskills/agentskills.git@b7442eb9acf4c05545ea9c26b139acbda15eb718#subdirectory=skills-ref" skills-ref validate plugins/instructions-improver/skills/instructions-improver`

Expected: PASS with a valid skill report for `plugins/instructions-improver/skills/instructions-improver`

- [ ] **Step 6: Commit the skill content**

```bash
git add plugins/instructions-improver/skills/instructions-improver
git commit -m "feat(instructions-improver): add shared audit skill"
```

## Task 4: Add the Claude session-end command

**Files:**
- Create: `plugins/instructions-improver/commands/revise-instructions.md`
- Test: `plugins/instructions-improver/scripts/instruction_docs_analyzer.py`

- [ ] **Step 1: Write the Claude command**

````markdown
---
description: Update AGENTS.md, CLAUDE.md, and .claude.local.md with durable learnings from this session
allowed-tools: Read, Edit, Glob, Bash
---

Review the current session for durable learnings about working in this repository.

## Step 1: Run the relation helper

```bash
python3 plugins/instructions-improver/scripts/instruction_docs_analyzer.py --root . --format json
```

## Step 2: Decide destination by file role

- `AGENTS.md`: shared workflows, commands, durable repo-wide gotchas
- `CLAUDE.md`: Claude-specific usage notes and the `@AGENTS.md` shim
- `.claude.local.md`: personal local-only preferences

## Step 3: Draft concise updates

Keep additions brief. Use one line per durable concept when possible.

## Step 4: Show diffs before editing

For each target file, show:

- why the addition belongs there
- the exact diff to apply

## Step 5: Apply only after approval

Never edit the files until the user approves the proposed changes.
```
````

- [ ] **Step 2: Smoke-test the helper output that the command depends on**

Run: `python3 plugins/instructions-improver/scripts/instruction_docs_analyzer.py --root plugins/instructions-improver/tests/fixtures/missing-ref --format text`

Expected: output contains `missing_agents_reference: CLAUDE.md`

- [ ] **Step 3: Commit the Claude command**

```bash
git add plugins/instructions-improver/commands/revise-instructions.md
git commit -m "feat(instructions-improver): add Claude revise command"
```

## Task 5: Integrate repo validation and user-facing docs

**Files:**
- Modify: `scripts/validate-skills.sh`
- Modify: `README.md`
- Test: `scripts/validate-skills.sh`

- [ ] **Step 1: Extend skill validation to include plugin-contained skills**

```bash
skill_manifests=()
if command -v fd >/dev/null 2>&1; then
  while IFS= read -r manifest; do
    skill_manifests+=("${manifest}")
  done < <(
    {
      fd --type file --glob "SKILL.md" skills 2>/dev/null
      fd --type file --glob "SKILL.md" plugins/*/skills 2>/dev/null
    } | sort -u
  )
else
  while IFS= read -r manifest; do
    skill_manifests+=("${manifest}")
  done < <(
    {
      find skills -type f -name "SKILL.md" 2>/dev/null
      find plugins -path "*/skills/*/SKILL.md" -type f 2>/dev/null
    } | sort -u
  )
fi
```

- [ ] **Step 2: Update the README install and usage sections**

````markdown
This repo now also ships the `instructions-improver` plugin under `plugins/instructions-improver/`.

### Claude Code Plugin Marketplace

```bash
/plugin install instructions-improver@mrclrchtr-skills
```

### Use

- `$instructions-improver` — Audit or sync `AGENTS.md`, `CLAUDE.md`, and `.claude.local.md`
- `/project:revise-instructions` — Propose durable session learnings for the right instruction file
```
````

- [ ] **Step 3: Run the full verification suite**

Run: `python3 -m unittest discover -s plugins/instructions-improver/tests -p 'test_*.py' -v`

Expected: PASS with the analyzer and metadata tests succeeding

Run: `bash scripts/validate-skills.sh`

Expected: PASS and includes `plugins/instructions-improver/skills/instructions-improver`

Run: `jq empty plugins/instructions-improver/.codex-plugin/plugin.json`

Expected: exit code 0

Run: `jq empty plugins/instructions-improver/.claude-plugin/plugin.json`

Expected: exit code 0

Run: `jq empty .agents/plugins/marketplace.json`

Expected: exit code 0

Run: `jq empty .claude-plugin/marketplace.json`

Expected: exit code 0

- [ ] **Step 4: Commit the repo integration changes**

```bash
git add scripts/validate-skills.sh README.md
git commit -m "chore(instructions-improver): document and validate plugin skill"
```

## Spec Coverage Check

- Dual-platform repo-local plugin: covered by Task 2 manifest and marketplace work.
- Shared single-source implementation: covered by Task 1 helper and Task 3 shared skill.
- `AGENTS.md` canonical relation model: covered by Task 1 findings and Task 3 required behaviors.
- Audit-first with explicit apply or sync: covered by Task 3 workflow and Task 4 command behavior.
- Support for `AGENTS.md`, `CLAUDE.md`, `.claude.local.md`: covered by Task 1 fixtures and analyzer.
- Claude session-end revision flow: covered by Task 4.
- Repo validation and discoverability: covered by Task 5.

## Placeholder Scan

- No deferred implementation markers are allowed during execution.
- If the chosen manifest or marketplace schema differs at implementation time, update the plan before coding rather than improvising.

## Type Consistency Check

- Helper filename is always `plugins/instructions-improver/scripts/instruction_docs_analyzer.py`.
- Main helper entrypoint is always `analyze_repo`.
- Role names are always `canonical_shared`, `claude_project`, and `claude_local`.
- Finding codes are always `missing_agents_reference`, `duplicate_shared_content`, and `shared_content_in_local_file`.
