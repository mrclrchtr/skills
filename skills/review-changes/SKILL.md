---
name: review-changes
description: >
  Use when the user asks to review code, audit changes, check a PR or commit,
  look over a file or directory, review a design/architecture document, or says
  "what do you think of this", "check this", "anything wrong here", "review before merge".
  Execute directly — no brainstorming, no interactive questions.
---

# Code Review

Review and report. Skip the brainstorming; the user wants findings, not a conversation.

## Scope detection

| Input | Mode | Scope |
|---|---|---|
| no args | code | staged → unstaged → last commit (first non-empty wins) |
| path to `.md` file | doc | that file |
| other file/dir path | code | that path |
| commit range (`abc..def`) | code | `git diff` for the range |
| PR number or URL | code | `gh pr diff <n>` + `gh pr view <n>` for context |

For local code reviews with no args, run `git diff --cached --name-only` then `git diff --name-only` to pick the scope. If nothing has changed, say so and stop.

## Code review

1. **Read full files, not just diffs.** A diff tells you what moved; the surrounding file tells you whether it still makes sense. Without that context, you miss broken call sites, stale comments, and silent convention violations.
2. **Learn the project's conventions before flagging them.** Skim `CLAUDE.md`, sibling files in the same directory, and the last few commits touching these files. "This doesn't match the codebase style" only lands as a finding when you can point to where the real style lives.
3. **Review for:** logic bugs, security (OWASP top 10), convention violations, missing or weak tests, accessibility gaps, and dead/unreachable code introduced by the change.
4. **When the diff is large** (many files, or files much bigger than fit comfortably in one read), split the files into groups and dispatch parallel sub-agents — one per group, each returning findings in the report format below. This keeps each agent's context focused and avoids truncating important files. If sub-agents aren't available, review serially and say so.

## Document review

**Treat the document as target architecture — the desired future state, not current code.** Flagging "this doesn't match what's built yet" defeats the purpose; the author already knows. Review the document on its own terms.

Look for:
- **Completeness** — every stated requirement has a plausible implementation path.
- **Internal consistency** — no section contradicts another.
- **Feasibility** — realistic given the codebase, team, and constraints you can see.
- **Gaps** — error handling, migration/rollback, edge cases, observability, failure modes.

## Report format

Group findings by severity — it lets the reader triage without re-reading. Each finding: `file:line` (or section) + what's wrong + why it matters. Skip the finding if you can't say why it matters.

- **Critical** — must fix before merge: bugs, security, data loss, broken call sites.
- **High** — should fix: convention violations, missing tests for new behavior, accessibility.
- **Medium** — worth improving: clarity, minor deviations, small refactors.
- **Positive** — 2-3 things done well, briefly. Reinforces patterns worth repeating.

Omit empty severity levels. After the findings, ask what the user wants next: fix the critical/high items, discuss a specific finding, or expand scope.
