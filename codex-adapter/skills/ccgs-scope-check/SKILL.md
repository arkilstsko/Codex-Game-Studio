---
name: ccgs-scope-check
description: "Codex Game Studio workflow `/scope-check`. Use when the user asks for CCGS game-studio workflow `ccgs-scope-check` or the original `/scope-check` command. Analyze a feature or sprint for scope creep by comparing current scope against the original plan. Flags additions, quantifies bloat, and recommends cuts. Use when user says 'any scope creep', 'scope review', 'are we staying in scope'."
---

## Codex Adapter

This is the Codex Game Studio workflow skill `scope-check`.

Use the workflow below with these Codex mappings:

- Slash-command references are mapped to Codex skill invocations with the `ccgs-` prefix.
- `Read`, `Glob`, and `Grep` mean inspect files with `sed`, `find`, and `rg`.
- `Write` and `Edit` mean make file changes with `apply_patch`.
- `Bash` means use `exec_command`.
- `Web search` and `Web fetch` mean use Codex web/browser tools when available; prefer official engine documentation for engine lookups. If web tools are unavailable, ask the user for the source URL or state the limitation.
- `request_user_input` means use Codex's structured input tool when available: at most 3 questions, 2-3 choices per question, no multi-select. Otherwise ask concise plain-text questions.
- Installed reference root: `~/.codex/skills/ccgs-references/references`. In this repo, the same files are mirrored under `codex-adapter/references/`.
- Role references are not native Codex agents. Simulate the named role locally using `references/agents/`; use Codex subagents only when the user explicitly asks for parallel agent work. Load matching memory from `references/agent-memory/` when it exists.
- Hook scripts and statusline settings from `references/hook-config.json` are reference checks. Treat them as reference checks unless you install separate Codex automation around them.

When this skill writes project artifacts, keep the original CCGS directory conventions (`design/`, `docs/`, `production/`, `src/`, `tests/`, `prototypes/`) unless the target project already has a stronger convention.

---

# Scope Check

This skill is read-only — it reports findings but writes no files.

Compares original planned scope against current state to detect, quantify, and triage
scope creep.

**Argument:** `$ARGUMENTS[0]` — feature name, sprint number, or milestone name.

---

## Phase 1: Find the Original Plan

Locate the baseline scope document for the given argument:

- **Feature name** → read `design/gdd/[feature].md` or matching file in `design/`
- **Sprint number** (e.g., `sprint-3`) → read `production/sprints/sprint-03.md` or similar
- **Milestone** → read `production/milestones/[name].md`

If the document is not found, report the missing file and stop. Do not proceed without
a baseline to compare against.

---

## Phase 2: Read the Current State

Check what has actually been implemented or is in progress:

- Scan the codebase for files related to the feature/sprint
- Read git log for commits related to this work (`git log --oneline --since=[start-date]`)
- Check for TODO/FIXME comments that indicate unfinished scope additions
- Check active sprint plan if the feature is mid-sprint

---

## Phase 3: Compare Original vs Current Scope

Produce the comparison report:

```markdown
## Scope Check: [Feature/Sprint Name]
Generated: [Date]

### Original Scope
[List of items from the original plan]

### Current Scope
[List of items currently implemented or in progress]

### Scope Additions (not in original plan)
| Addition | Source | When | Justified? | Effort |
|----------|--------|------|------------|--------|
| [item] | [commit/person] | [date] | [Yes/No/Unclear] | [S/M/L] |

### Scope Removals (in original but dropped)
| Removed Item | Reason | Impact |
|-------------|--------|--------|
| [item] | [why removed] | [what's affected] |

### Bloat Score
- Original items: [N]
- Current items: [N]
- Items added: [N] (+[X]%)
- Items removed: [N]
- Net scope change: [+/-N] ([X]%)

### Risk Assessment
- **Schedule Risk**: [Low/Medium/High] — [explanation]
- **Quality Risk**: [Low/Medium/High] — [explanation]
- **Integration Risk**: [Low/Medium/High] — [explanation]

### Recommendations
1. **Cut**: [Items that should be removed to stay on schedule]
2. **Defer**: [Items that can move to a future sprint/version]
3. **Keep**: [Additions that are genuinely necessary]
4. **Flag**: [Items that need a decision from producer/creative-director]
```

---

## Phase 4: Verdict

Assign a canonical verdict based on net scope change:

| Net Change | Verdict | Meaning |
|-----------|---------|---------|
| ≤10% | **PASS** | On Track — within acceptable variance |
| 10–25% | **CONCERNS** | Minor Creep — manageable with targeted cuts |
| 25–50% | **FAIL** | Significant Creep — must cut or formally extend timeline |
| >50% | **FAIL** | Out of Control — stop, re-plan, escalate to producer |

Output the verdict prominently:

```
**Scope Verdict: [PASS / CONCERNS / FAIL]**
Net change: [+X%] — [On Track / Minor Creep / Significant Creep / Out of Control]
```

---

## Phase 5: Next Steps

After presenting the report, offer concrete follow-up:

- **PASS** → no action required. Suggest re-running before next milestone.
- **CONCERNS** → offer to identify the 2–3 additions with best cut ratio. Reference `$ccgs-sprint-plan update` to formally re-scope.
- **FAIL** → recommend escalating to producer. Reference `$ccgs-sprint-plan update` for re-planning or `$ccgs-estimate` to re-baseline timeline.

Always end with:
> "Run `$ccgs-scope-check [name]` again after cuts are made to verify the verdict improves."

---

### Rules

- Scope creep is additions without corresponding cuts or timeline extensions
- Not all additions are bad — some are discovered requirements. But they must be acknowledged and accounted for
- When recommending cuts, prioritize preserving the core player experience over nice-to-haves
- Always quantify scope changes — "it feels bigger" is not actionable, "+35% items" is
