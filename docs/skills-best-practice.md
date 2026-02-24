# Skills best practices (Agent Skills)

This doc consolidates practical guidance for authoring **Agent Skills** that are discoverable, reliable, and context-efficient across common ecosystems (Codex/Claude/AgentSkills).

## 1) Keep skills focused and discoverable

- **One job per skill.** If the skill regularly “branches” into unrelated tasks, split it.
- **Description drives discovery.** Many agents implicitly select skills based primarily on `description`, so write it like a search query:
  - Include **what** it does *and* **when** to use it.
  - Add concrete **keywords/triggers** (file types, tools, domains, “use when user mentions …”).
  - Prefer **third-person** phrasing (descriptions are often injected into a system prompt).
- **Boundaries matter.** Explicitly say when *not* to use the skill to avoid false positives.
- **Treat triggers as a product surface.** Most runtimes preload only `name` + `description`, so put primary triggers in `description` (not buried in the body).

### Writing effective descriptions

The `description` field is usually the highest-signal input for skill selection: it must be specific enough that an agent can confidently pick it from a large skill set.

Practical rules:
- Write in **third person**, present tense (“Extracts…”, “Generates…”, “Analyzes…”).
- Include **what** it does (primary actions) and **when** to use it (selection cues).
- Mention the most important **inputs** (file types, artifacts, domains) and (optionally) the expected **outputs**.
- Keep it **plain text** (many validators disallow markup-like content) and within your runtime’s length limits (commonly 1024 chars).
- Avoid vague descriptions (“Helps with documents”, “Processes data”, “Does stuff with files”).

Examples (effective):

```yaml
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDFs, forms, or document extraction.
```

```yaml
description: Generates descriptive git commit messages by analyzing diffs. Use when the user asks for commit message help or reviewing staged changes.
```

#### Trigger patterns (keywords to include in `description`)

Use a small set of high-signal triggers that reliably appear in real requests:
- **File types / extensions:** “PDF”, “.pdf”, “xlsx”, “CSV”, “OpenAPI”, “Terraform”.
- **Domain nouns:** “invoice”, “purchase order”, “SOC 2”, “S3 bucket policy”.
- **Task verbs:** “extract”, “normalize”, “validate”, “migrate”, “diff”, “triage”.
- **Tooling keywords:** “BigQuery”, “dbt”, “pytest”, “kubectl”, “pre-commit”.
- **Input shapes:** “pasted stack trace”, “HAR file”, “curl command”, “SQL query”.

Also include:
- **Negative triggers / boundaries:** “Not for …”, “Do not use when …” to avoid over-activation.
- **Synonyms (sparingly):** add 1–3 common alternates if they change selection (e.g., “S3 policy” + “bucket policy”).

## 2) Start with the standard format

At minimum, a skill is a directory with `SKILL.md` containing YAML frontmatter + Markdown body:

```yaml
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Common constraints (validate for your target platform/validator):
- `name`: lowercase letters/numbers/hyphens, max 64 chars; typically must match the parent directory name.
  - Some platforms disallow vendor-reserved words (e.g., `claude`, `anthropic`) and/or markup-like content.
- `description`: non-empty, max 1024 chars; often disallows markup-like content.
- Naming: prefer specific, action-oriented names; avoid vague buckets like `helper`, `utils`, or `tools`.

## 3) Use progressive disclosure to manage context

Agents typically preload only metadata (`name`, `description`) for all skills, then load `SKILL.md` only when activated, and load other files only when referenced.

Practical rules:
- Assume the model already knows the basics; only add context it *can’t* reliably infer from the request, codebase, or linked references.
- Once loaded, `SKILL.md` competes with conversation history and other context: keep it tight and skimmable.
- Keep the `SKILL.md` body **under ~500 lines**; split when it grows.
- Put deep detail in separate files (commonly `references/`, `assets/`, plus optional top-level guides like `FORMS.md`).
- Keep references **one hop from `SKILL.md`** (avoid `SKILL.md → advanced.md → details.md`).
- If a reference file is long, add a short **table of contents** at the top.
- For deterministic operations, prefer scripts: they can often be executed without loading their full contents, and only the output consumes tokens.
- Name files descriptively and organize directories by domain/feature (e.g., `reference/finance.md`, not `docs/file1.md`).
- Test “file access patterns” in real runs: confirm the agent can find and open the right files from `SKILL.md` without guessing paths.

## 4) Pick the right “degrees of freedom”

Match instruction specificity to task risk:
- **High freedom:** heuristics and flexible guidance (e.g., code review).
- **Medium freedom:** templates/pseudocode with parameters (e.g., report generation).
- **Low freedom:** exact commands/steps (e.g., migrations, production changes).

When there are multiple viable approaches, provide a **default** plus a small “escape hatch” for edge cases (don’t list five equivalent options).

## 5) Write workflows with feedback loops

For multi-step tasks, include a **sequential workflow** (and optionally a checklist the agent can copy and tick off). For quality-critical work, bake in a loop:

`run validator → fix issues → re-run validator → proceed only when passing`

## 6) If you include scripts, make them robust

- Prefer **instructions over scripts** unless you need deterministic behavior or external tooling.
- Scripts should **solve, not punt**: handle common errors (missing file, permissions, bad input) with clear messages and safe defaults.
- Don’t assume dependencies exist; document installs and required tools explicitly.
- Make execution intent explicit: “Run `scripts/foo.py` …” vs “See `scripts/foo.py` for …”.
- Avoid “magic numbers”; justify constants and configuration values.
- Use forward slashes in paths (`scripts/tool.py`), even for cross-platform skills.

## 7) Keep content maintainable

- Avoid time-sensitive instructions that will rot; if needed, isolate legacy guidance under an “Old patterns” / “Deprecated” section.
- Use consistent terminology (pick one term per concept).
- Prefer imperative steps with **explicit inputs/outputs**.
- Include concrete examples when output quality is format-sensitive.

## 8) Declare compatibility, tools, and policy where supported

- AgentSkills supports optional fields like `compatibility` and (experimental) `allowed-tools`.
- Codex supports optional `agents/openai.yaml` for UI metadata, dependency declarations, and invocation policy (e.g., disabling implicit invocation).
- If you reference MCP tools, use fully-qualified names where required (e.g., `ServerName:tool_name`) to avoid “tool not found” errors.
- If behavior depends on the runtime (network access, package installs), state assumptions and provide a fallback or “no-network” path.

## 9) Validate and test like a product

- Validate frontmatter and naming against the AgentSkills spec tooling (e.g., `skills-ref validate ./my-skill`).
- Create a small evaluation set (at least ~3 representative scenarios) before writing lots of prose.
- Test with the model(s) you’ll actually run; instruction needs differ by capability and cost.
- Iterate from real usage: observe how the agent navigates files and where it fails, then tighten structure, triggers, and guardrails.

## 10) Treat third-party skills as supply chain

If you install skills from a registry/CLI ecosystem, review contents before use and keep least-privilege defaults. Even with audits, you’re still responsible for what runs in your environment.

## Checklist

- [ ] `name` and `description` valid; `description` is third-person and specific (what + when + keywords + boundaries)
- [ ] `SKILL.md` is concise (<~500 lines) and uses progressive disclosure appropriately
- [ ] References are one hop from `SKILL.md`; long refs have a ToC
- [ ] Files are discoverable (descriptive names, sensible folders); agent can navigate paths in real runs
- [ ] Workflow is stepwise; quality-critical work has a validator loop
- [ ] Scripts (if any) handle errors, document dependencies, and make execution intent explicit
- [ ] Tool references are unambiguous (e.g., fully-qualified MCP tool names where required)
- [ ] Content avoids time-sensitive rot; terminology is consistent; examples/templates included where needed
- [ ] Skill is validated and tested on real scenarios/models

## Sources

- OpenAI Codex Skills docs: `https://developers.openai.com/codex/skills`
- Claude Skills best practices: `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
- Vercel Labs Skills CLI docs: `https://skills.sh/docs`
- AgentSkills specification: `https://agentskills.io/specification`
