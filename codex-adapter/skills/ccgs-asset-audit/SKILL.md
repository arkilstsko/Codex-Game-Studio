---
name: ccgs-asset-audit
description: "Codex Game Studio workflow `/asset-audit`. Use when the user asks for CCGS game-studio workflow `ccgs-asset-audit` or the original `/asset-audit` command. Audits game assets for compliance with naming conventions, file size budgets, format standards, and pipeline requirements. Identifies orphaned assets, missing references, and standard violations."
---

## Codex Adapter

This is the Codex Game Studio workflow skill `asset-audit`.

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

## Phase 1: Read Standards

Read the art bible or asset standards from the relevant design docs and the AGENTS.md naming conventions.

---

## Phase 2: Scan Asset Directories

Scan the target asset directory using Glob:

- `assets/art/**/*` for art assets
- `assets/audio/**/*` for audio assets
- `assets/vfx/**/*` for VFX assets
- `assets/shaders/**/*` for shaders
- `assets/data/**/*` for data files

---

## Phase 3: Run Compliance Checks

**Naming conventions:**
- Art: `[category]_[name]_[variant]_[size].[ext]`
- Audio: `[category]_[context]_[name]_[variant].[ext]`
- All files must be lowercase with underscores

**File standards:**
- Textures: Power-of-two dimensions, correct format (PNG for UI, compressed for 3D), within size budget
- Audio: Correct sample rate, format (OGG for SFX, OGG/MP3 for music), within duration limits
- Data: Valid JSON/YAML, schema-compliant

**Orphaned assets:** Search code for references to each asset file. Flag any with no references.

**Missing assets:** Search code for asset references and verify the files exist.

---

## Phase 4: Output Audit Report

```markdown
# Asset Audit Report -- [Category] -- [Date]

## Summary
- **Total assets scanned**: [N]
- **Naming violations**: [N]
- **Size violations**: [N]
- **Format violations**: [N]
- **Orphaned assets**: [N]
- **Missing assets**: [N]
- **Overall health**: [CLEAN / MINOR ISSUES / NEEDS ATTENTION]

## Naming Violations
| File | Expected Pattern | Issue |
|------|-----------------|-------|

## Size Violations
| File | Budget | Actual | Overage |
|------|--------|--------|---------|

## Format Violations
| File | Expected Format | Actual Format |
|------|----------------|---------------|

## Orphaned Assets (no code references found)
| File | Last Modified | Size | Recommendation |
|------|-------------|------|---------------|

## Missing Assets (referenced but not found)
| Reference Location | Expected Path |
|-------------------|---------------|

## Recommendations
[Prioritized list of fixes]

## Verdict: [COMPLIANT / WARNINGS / NON-COMPLIANT]
```

This skill is read-only — it produces a report but does not write files.

---

## Phase 5: Next Steps

- Fix naming violations using the patterns defined in AGENTS.md.
- Delete confirmed orphaned assets after manual review.
- Run `$ccgs-content-audit` to cross-check asset counts against GDD-specified requirements.
