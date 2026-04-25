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

## 1. Detect the review target

| Input | Mode | How to gather |
|---|---|---|
| no args | code | `git diff --cached --stat` → `git diff --stat` → `git diff HEAD~1 --stat` — first non-empty wins |
| path to `.md` file | doc | read that file |
| other file/dir path | code | read files in scope |
| commit range (`abc..def`) | code | `git diff abc..def` + `git log --oneline abc..def` |
| PR number or URL | code | `gh pr diff <n>` + `gh pr view <n>` |
| `--branch <name>` | code | `git merge-base <name> HEAD` → `git diff <base>..HEAD` |

### Gathering commands (no args)

```bash
# Check what changed — staged first, then unstaged, then last commit
git diff --cached --stat
git diff --stat
git diff HEAD~1 --stat
```

Pick the **first non-empty** scope. If all three are empty, say so and stop.

For PR reviews, also gather context:

```bash
gh pr view <n> --json title,body,labels,additions,deletions,changedFiles
gh pr diff <n>
```

## 2. Read full files, not just diffs

A diff tells you what moved; surrounding code tells you whether it still makes sense. Without that context, you miss broken call sites, stale comments, and silent convention violations.

- For every changed file, read at least the modified function/class plus its immediate callers and callees.
- If the diff is > 800 lines, read the full files for the highest-risk changes. Skip mechanical changes (renames, formatting) unless they mask something.

## 3. Learn conventions before flagging them

Skim `CLAUDE.md`, `AGENTS.md`, or similar project instructions. Read sibling files in the same directory and the last few commits touching these files. "This doesn't match the codebase style" only lands as a finding when you can point to where the real style lives.

## 4. What counts as a finding

Flag something **only if** all of the following are true:

1. It meaningfully impacts correctness, security, performance, or maintainability.
2. It was **introduced by this change** — pre-existing issues are out of scope unless the change makes them worse.
3. It is discrete and actionable — the author can fix it in one focused pass.
4. It does not require assuming unstated intent or speculative downstream effects.
5. It does not demand a level of rigor not present in the rest of the codebase.
6. The author would likely fix it if they were made aware of it.
7. It is not clearly an intentional change by the original author.

**Do not flag:**

- Trivial style unless it obscures meaning or violates documented standards.
- Pre-existing bugs unrelated to this change.
- Things that "might" break something unless you can identify the specific code path that provably breaks.
- Hypothetical issues without a concrete scenario.
- Speculative downstream effects — you must be able to identify the code that is provably affected.

**How many findings to return:**
Output *all* findings that the original author would fix if they knew about it. Do not stop at the first qualifying finding. Continue until you've listed every qualifying issue. If there is nothing a person would definitely want to see and fix, prefer outputting no findings.

## 5. Review checklist

Check for:

- **Logic bugs** — wrong condition, off-by-one, missing null/undefined check, race condition.
- **Security** — injection, authz bypass, secret exposure (OWASP top 10 as a lens, not a checklist).
- **Convention violations** — only when you can cite the convention.
- **Missing or weak tests** — new behavior without test coverage.
- **Dead or unreachable code** introduced by this change.
- **Breaking changes** — removed exports, changed signatures, config format changes.

## 6. Finding format

Use this format for every finding:

```
### [P0–P3] Short imperative title

**File:** `path/to/file.ts:42-48`

What's wrong and why it matters — one paragraph, matter-of-fact tone.

If suggesting a fix, use an inline code block (≤ 3 lines). No commentary inside the block.
```

Priority levels:

| Priority | Meaning |
|---|---|
| **P0** | Drop everything. Blocks release, causes data loss or security breach. Universal — no assumptions about inputs needed. |
| **P1** | Urgent. Should fix before merge. Bugs that will bite under normal usage. |
| **P2** | Normal. Should fix eventually. Convention gaps, missing tests, minor issues. |
| **P3** | Nice to have. Small improvements, clarity, naming. |

**Tone & content rules:**
- Matter-of-fact, not accusatory or overly positive.
- No "Great job" or "Thanks for" — the user asked for findings, not compliments.
- Brief. One paragraph per finding. Do not introduce line breaks within the natural language flow unless necessary for a code fragment.
- The comment should clearly and explicitly communicate the scenarios, environments, or inputs necessary for the bug to arise. Immediately indicate if severity depends on these factors.
- The author should grasp the idea without close reading.
- Use ` ```suggestion ` blocks **only** for concrete replacement code (minimal lines; no commentary inside the block). Preserve the exact leading whitespace of replaced lines.
- Any code chunks should be ≤ 3 lines and wrapped in inline code tags or a code block.
- Avoid providing unnecessary location details in the comment body — rely on the file/line reference instead.

## 7. Overall verdict

After all findings, give a one-line verdict:

```
**Verdict:** PATCH IS CORRECT / PATCH HAS ISSUES — <1-sentence why>
```

Use **PATCH HAS ISSUES** if any P0 or P1 finding exists. Use **PATCH IS CORRECT** otherwise. "Correct" means existing code and tests will not break, and the patch is free of bugs and other blocking issues. Ignore non-blocking issues such as style, formatting, typos, documentation, and other nits.

## 8. Large diffs

When the diff spans many files or > 800 lines of real changes (not renames/formatting):

1. Read the diff stat to identify high-risk files (core logic, auth, data handling).
2. Prioritize P0/P1 coverage on those files.
3. Note in the report which files you reviewed deeply vs. skimmed.
4. If sub-agents are available, split by file group — one agent per group.

For purely mechanical changes (renames, formatting, generated code), say so and skip detailed review.

## 9. Document review

When the input is a `.md` file, review it as **target architecture** — the desired future state, not current code. Flagging "this doesn't match what's built yet" defeats the purpose; the author already knows.

Look for:
- **Completeness** — every stated requirement has a plausible implementation path.
- **Internal consistency** — no section contradicts another.
- **Feasibility** — realistic given the codebase, team, and constraints you can see.
- **Gaps** — error handling, migration/rollback, edge cases, observability, failure modes.

Report document findings using the same P0–P3 format, replacing file/line with section/heading.

## 10. Follow-up

After the report, ask what the user wants next:
- Fix the critical/high items
- Discuss a specific finding
- Expand scope to other files or branches