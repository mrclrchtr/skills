# Instructions Improver Design

## Summary

Build a repo-local dual-platform plugin named `instructions-improver` that helps maintain shared and Claude-specific instruction files.

The plugin must work for both Codex and Claude while keeping the actual maintenance behavior single-sourced. It should audit and improve:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude.local.md`

The default behavior is audit-first: discover files, assess quality, analyze relations, and propose minimal diffs. Editing is a separate explicit action. The plugin must also support a session-end maintenance flow that captures durable learnings from the current session and proposes concise doc updates.

## Goals

- Provide one shared plugin implementation usable from both Codex and Claude.
- Treat `AGENTS.md` as the canonical shared instruction source.
- Treat `CLAUDE.md` as a Claude-specific shim that should load `@AGENTS.md` when both files exist.
- Keep local Claude files personal and out of shared docs.
- Detect duplication, missing references, stale instructions, and misfiled content.
- Prefer minimal, targeted edits over large rewrites.

## Non-Goals

- Managing arbitrary documentation files outside the three supported Claude/Codex instruction file types.
- Silent auto-rewrites without an explicit apply step.
- Heavy normalization that replaces a project's existing document structure when smaller edits are enough.
- Full semantic synchronization across every possible agent ecosystem in v1.

## User Model

The plugin supports two primary workflows:

1. Audit mode
   - Scan the repo for supported instruction files.
   - Classify each file by role.
   - Score quality and relation health.
   - Propose minimal edits as diffs.
   - Stop before editing.
2. Apply or sync mode
   - Reuse the audit findings.
   - Apply only approved edits.
   - Normalize relations between files.
   - Preserve existing structure where possible.

The plugin also provides a session-end revision flow that reflects on the current session and proposes concise additions to the right file instead of dumping all learnings into one place.

## Canonical File Roles

### `AGENTS.md`

Canonical shared instruction source for the repo.

Content that belongs here:

- Shared workflow instructions
- Tooling and command conventions
- Repo-wide architecture and structure notes
- Cross-agent working rules that are not Claude-specific
- Durable gotchas relevant to any compatible agent

Content that should not primarily live here:

- Claude-only interaction guidance
- Personal local preferences

### `CLAUDE.md`

Claude-facing shim plus Claude-only guidance.

If both `AGENTS.md` and `CLAUDE.md` exist, `CLAUDE.md` should include `@AGENTS.md` so Claude Code loads the shared instruction set automatically. The rest of `CLAUDE.md` should stay limited to Claude-specific additions, for example:

- Claude command shortcuts or interaction patterns
- Claude-specific workflow notes
- Claude-specific local file conventions

`CLAUDE.md` should not duplicate substantial shared content that already lives in `AGENTS.md`.

### `.claude.local.md`

Local personal override layer.

Content that belongs here:

- Personal workflow preferences
- Machine-specific notes
- Local-only reminders

Content that should not live here:

- Team-shared instructions
- Secrets
- Broad project architecture notes that future teammates need

## Relation Rules

The plugin should evaluate and enforce these relation rules:

1. If both `AGENTS.md` and `CLAUDE.md` exist, `CLAUDE.md` should reference `@AGENTS.md`.
2. Shared instructions should live in `AGENTS.md`, not be duplicated in `CLAUDE.md`.
3. Claude-only guidance should stay in `CLAUDE.md` rather than polluting `AGENTS.md`.
4. Personal local guidance should stay in `.claude.local.md`.
5. If `CLAUDE.md` exists without `AGENTS.md`, the plugin may suggest creating `AGENTS.md` when shared content is clearly present.
6. If `AGENTS.md` exists without `CLAUDE.md`, the plugin may suggest adding a lightweight `CLAUDE.md` shim when Claude-specific guidance or explicit loading behavior would help.

## Discovery Scope

V1 discovery should include:

- Root `AGENTS.md`
- Root `CLAUDE.md`
- Nested `CLAUDE.md`
- Nested `.claude.local.md`

V1 should not attempt broad support for arbitrary alternative filenames. The behavior should be optimized for the filenames above, while staying compatible with the user's Codex setup where `CLAUDE.md` is a fallback-loaded project doc.

## Quality Assessment

Each discovered file should be assessed against concise criteria:

- Role clarity: the file contains the kind of information expected for that file type
- Actionability: commands and instructions are executable and specific
- Currency: content appears current for the codebase
- Conciseness: no obvious prompt bloat or repeated boilerplate
- Relation hygiene: shared, Claude-specific, and local-only content are placed correctly

The plugin should produce a report with:

- Files found
- Relation findings
- File-by-file quality notes
- Recommended additions or moves
- Proposed diffs for each file that should change

## Editing Policy

The plugin must be conservative when editing:

- Default to no edits without explicit approval
- Show targeted diffs before editing
- Preserve the existing section structure when reasonable
- Prefer adding or relocating concise lines or short sections over full rewrites
- Avoid duplicate additions
- Avoid moving speculative information into shared files

## Plugin Architecture

Use one shared plugin directory:

- `plugins/instructions-improver/`

Inside that directory:

- `.codex-plugin/plugin.json` for Codex metadata
- `.claude-plugin/plugin.json` for Claude metadata
- `skills/instructions-improver/` for the shared primary skill
- `commands/` for Claude-facing command entrypoints
- `references/` for quality criteria and relation rules
- Optional `scripts/` only if deterministic discovery or diff helpers are needed

The actual maintenance logic and guidance should live in shared skill and reference content, not be duplicated per platform. Platform-specific manifests and commands should be thin adapters.

## V1 Plugin Surface

### Shared skill

`instructions-improver`

Responsibilities:

- Discover supported instruction files
- Assess quality and relation health
- Propose minimal diffs
- Apply approved changes
- Run explicit sync behavior for relations

### Claude command

A session-end command similar in spirit to `revise-claude-md`, but expanded to:

- Consider `AGENTS.md`, `CLAUDE.md`, and `.claude.local.md`
- Route findings to the correct file by role
- Keep additions concise and durable

### Optional helpers

Small helper scripts are allowed if they clearly improve deterministic discovery or relation checking. They are not required for v1 if the skill alone can express the workflow reliably.

## Example Findings the Plugin Should Flag

- `CLAUDE.md` exists but does not load `@AGENTS.md`
- `CLAUDE.md` duplicates command lists already present in `AGENTS.md`
- `AGENTS.md` contains Claude-only interaction notes
- `.claude.local.md` contains shared team workflow rules
- Shared docs contain verbose one-off debugging notes instead of durable guidance
- Commands are present but stale or no longer executable

## Testing Strategy

V1 verification should focus on fixture-style scenarios:

- Only `AGENTS.md`
- Only `CLAUDE.md`
- Both `AGENTS.md` and `CLAUDE.md` with correct linkage
- Both files with duplicated content
- Presence of `.claude.local.md` with properly isolated local content
- Missing or incorrect `@AGENTS.md` references
- Apply flow preserves unrelated document content

If scripts are introduced, they should be tested directly. If the plugin remains prompt-first, verification can focus on fixture docs and dry-run diff generation.

## Risks and Mitigations

- Drift between Codex and Claude packaging
  - Mitigation: keep shared logic in one skill and use thin manifests.
- Over-aggressive rewriting
  - Mitigation: diff-first workflow and targeted edits only.
- Ambiguity about what content belongs in which file
  - Mitigation: encode explicit file-role and relation rules in references.
- Prompt bloat from over-documentation
  - Mitigation: optimize for concise additions and deduplication.

## Open Decisions Resolved

- Packaging: repo-local dual-platform plugin
- Operating model: both audit-first and explicit apply or sync
- File scope: `AGENTS.md`, `CLAUDE.md`, `.claude.local.md`
- Canonical relation model: `AGENTS.md` is canonical; `CLAUDE.md` is a Claude-specific shim plus additions

## Implementation Boundary for the Next Plan

The next implementation plan should cover:

- Scaffolding the dual-platform plugin directory
- Defining manifests for both platforms
- Writing the shared `instructions-improver` skill
- Writing relation and quality reference docs
- Adding the Claude session-end command
- Deciding whether helper scripts are necessary after the shared skill is drafted
