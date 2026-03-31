# Web Interface Guidelines Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a repo-local `web-interface-guidelines` plugin with two focused skills and shared reference material derived from the Vercel guideline corpus.

**Architecture:** Keep the plugin wrapper thin and put the real behavior in two small skills: one for applying the guidelines during implementation and one for reviewing existing UI. Store the imported guideline substance in shared topic references under the plugin so both skills can stay concise and specific.

**Tech Stack:** Codex plugin manifests, Markdown skills, repo-local Python scaffold scripts, YAML interface metadata

---

### Task 1: Scaffold the plugin and both skill directories

**Files:**
- Create: `plugins/web-interface-guidelines/.codex-plugin/plugin.json`
- Create: `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/`
- Create: `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/`

- [ ] **Step 1: Scaffold the plugin shell**

Run: `python3 /Users/mrclrchtr/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py web-interface-guidelines --path /Users/mrclrchtr/Development/mrclrchtr/skills/plugins --with-skills`

Expected: plugin root plus `.codex-plugin/plugin.json` and `skills/` directory created under `plugins/web-interface-guidelines/`

- [ ] **Step 2: Initialize the apply skill**

Run: `python3 skills/skill-creator/scripts/init_skill.py web-interface-guidelines-apply --path /Users/mrclrchtr/Development/mrclrchtr/skills/plugins/web-interface-guidelines/skills --resources references --interface display_name="Web Interface Guidelines Apply" --interface short_description="Apply Vercel-style UI guidelines" --interface default_prompt="Use $web-interface-guidelines-apply to build or update this UI with the shared web interface guidelines."`

Expected: `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/` created with `SKILL.md`, `agents/openai.yaml`, and `references/`

- [ ] **Step 3: Initialize the review skill**

Run: `python3 skills/skill-creator/scripts/init_skill.py web-interface-guidelines-review --path /Users/mrclrchtr/Development/mrclrchtr/skills/plugins/web-interface-guidelines/skills --resources references --interface display_name="Web Interface Guidelines Review" --interface short_description="Review UI against web guidelines" --interface default_prompt="Use $web-interface-guidelines-review to audit this UI against the shared web interface guidelines."`

Expected: `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/` created with `SKILL.md`, `agents/openai.yaml`, and `references/`

### Task 2: Replace generated templates with the actual skill content

**Files:**
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/SKILL.md`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/SKILL.md`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-apply/agents/openai.yaml`
- Modify: `plugins/web-interface-guidelines/skills/web-interface-guidelines-review/agents/openai.yaml`

- [ ] **Step 1: Write the apply skill**

Implement a concise skill that triggers when Codex is building or modifying frontend UI and needs to apply the imported guidelines. Keep the frontmatter to `name` and `description`, keep the body short, and link directly to the shared reference files.

- [ ] **Step 2: Write the review skill**

Implement a concise skill that triggers when Codex is auditing existing frontend UI and needs findings grounded in the imported guidelines. Make the body findings-first and explicitly require guideline-category grounding.

- [ ] **Step 3: Regenerate interface metadata if needed**

Run:
- `python3 skills/skill-creator/scripts/generate_openai_yaml.py plugins/web-interface-guidelines/skills/web-interface-guidelines-apply --interface display_name="Web Interface Guidelines Apply" --interface short_description="Apply Vercel-style UI guidelines" --interface default_prompt="Use $web-interface-guidelines-apply to build or update this UI with the shared web interface guidelines."`
- `python3 skills/skill-creator/scripts/generate_openai_yaml.py plugins/web-interface-guidelines/skills/web-interface-guidelines-review --interface display_name="Web Interface Guidelines Review" --interface short_description="Review UI against web guidelines" --interface default_prompt="Use $web-interface-guidelines-review to audit this UI against the shared web interface guidelines."`

Expected: `agents/openai.yaml` matches the finished skill text and complies with the generator constraints.

### Task 3: Add the shared reference corpus and tidy the plugin manifest

**Files:**
- Create: `plugins/web-interface-guidelines/references/interactions.md`
- Create: `plugins/web-interface-guidelines/references/forms.md`
- Create: `plugins/web-interface-guidelines/references/content-accessibility.md`
- Create: `plugins/web-interface-guidelines/references/layout-motion.md`
- Create: `plugins/web-interface-guidelines/references/performance.md`
- Create: `plugins/web-interface-guidelines/references/design-copywriting.md`
- Create: `plugins/web-interface-guidelines/references/source-notes.md`
- Modify: `plugins/web-interface-guidelines/.codex-plugin/plugin.json`

- [ ] **Step 1: Write the topic references**

Paraphrase and reorganize the Vercel source into small topic files that both skills can reference directly. Do not dump the raw fetched page into one file.

- [ ] **Step 2: Adjust `plugin.json` minimally**

Keep the plugin name normalized and retain placeholder-heavy metadata, but make sure `skills` points at `./skills/` and the manifest stays structurally valid for Codex plugin discovery.

### Task 4: Validate the finished plugin and skills

**Files:**
- Verify: `plugins/web-interface-guidelines/`

- [ ] **Step 1: Validate each skill**

Run:
- `python3 skills/skill-creator/scripts/quick_validate.py plugins/web-interface-guidelines/skills/web-interface-guidelines-apply`
- `python3 skills/skill-creator/scripts/quick_validate.py plugins/web-interface-guidelines/skills/web-interface-guidelines-review`

Expected: both validations pass.

- [ ] **Step 2: Review the final tree**

Run: `fd -a . plugins/web-interface-guidelines`

Expected: plugin manifest, two skills, and shared references are present in the expected locations.

- [ ] **Step 3: Summarize any gaps**

If forward-testing with subagents was not performed, note that explicitly as a remaining validation gap rather than implying the skills were pressure-tested.
