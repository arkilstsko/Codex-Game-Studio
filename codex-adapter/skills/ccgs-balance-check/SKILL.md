---
name: ccgs-balance-check
description: "Codex Game Studio workflow `/balance-check`. Use when the user asks for CCGS game-studio workflow `ccgs-balance-check` or the original `/balance-check` command. Analyzes game balance data files, formulas, and configuration to identify outliers, broken progressions, degenerate strategies, and economy imbalances. Use after modifying any balance-related data or design. Use when user says 'balance report', 'check game balance', 'run a balance check'."
---

## Codex Adapter

This is the Codex Game Studio workflow skill `balance-check`.

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

## Phase 1: Identify Balance Domain

Determine the balance domain from `$ARGUMENTS[0]`:

- **Combat** → weapon/ability DPS, time-to-kill, damage type interactions
- **Economy** → resource faucets/sinks, acquisition rates, item pricing
- **Progression** → XP/power curves, dead zones, power spikes
- **Loot** → rarity distribution, pity timers, inventory pressure
- **File path given** → load that file directly and infer domain from content

If no argument, ask the user which system to check.

---

## Phase 2: Read Data Files

Read relevant files from `assets/data/` and `design/balance/` for the identified domain.
Note every file read — they will appear in the Data Sources section of the report.

---

## Phase 3: Read Design Document

Read the GDD for the system from `design/gdd/` to understand intended design targets,
tuning knobs, and expected value ranges. This is the baseline for "correct" behaviour.

---

## Phase 4: Perform Analysis

Run domain-specific checks:

**Combat balance:**
- Calculate DPS for all weapons/abilities at each power tier
- Check time-to-kill at each tier
- Identify any options that dominate all others (strictly better)
- Check if defensive options can create unkillable states
- Verify damage type/resistance interactions are balanced

**Economy balance:**
- Map all resource faucets and sinks with flow rates
- Project resource accumulation over time
- Check for infinite resource loops
- Verify gold sinks scale with gold generation
- Check if any items are never worth purchasing

**Progression balance:**
- Plot the XP curve and power curve
- Check for dead zones (no meaningful progression for too long)
- Check for power spikes (sudden jumps in capability)
- Verify content gates align with expected player power
- Check if skip/grind strategies break intended pacing

**Loot balance:**
- Calculate expected time to acquire each rarity tier
- Check pity timer math
- Verify no loot is strictly useless at any stage
- Check inventory pressure vs acquisition rate

---

## Phase 5: Output the Analysis

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [HEALTHY / CONCERNS / CRITICAL ISSUES]

### Outliers Detected
| Item/Value | Expected Range | Actual | Issue |
|-----------|---------------|--------|-------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```

---

## Phase 6: Fix & Verify Cycle

After presenting the report, use `request_user_input`:
- Prompt: "Balance check complete. What would you like to do next?"
- Options:
  - `[A] Fix highest-priority issue now — walk me through it`
  - `[B] Save report to design/balance/balance-check-[system]-[date].md`
  - `[C] Stop here — I'll review the findings manually`

If [A]:
- Ask which issue to address first (refer to the Recommendations table by priority row)
- Guide the user to update the relevant data file in `assets/data/` or formula in `design/balance/`
- After each fix, offer to re-run the relevant balance checks to verify no new outliers were introduced
- If the fix changes a tuning knob defined in a GDD or referenced by an ADR, remind the user:
  > "This value is defined in a design document. Run `$ccgs-propagate-design-change [path]` on the affected GDD to find downstream impacts before committing."

If [B]:
- Write the report to `design/balance/balance-check-[system]-[date].md` (create the directory if needed). Use the current date for [date] in YYYY-MM-DD format.
- Confirm the file was written, then end with: "Re-run `$ccgs-balance-check` after fixes to verify."

If [C]:
- Summarize open issues and end with: "Re-run `$ccgs-balance-check` after fixes to verify."
