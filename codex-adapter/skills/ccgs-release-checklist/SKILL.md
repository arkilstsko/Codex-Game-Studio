---
name: ccgs-release-checklist
description: "Codex Game Studio workflow `/release-checklist`. Use when the user asks for CCGS game-studio workflow `ccgs-release-checklist` or the original `/release-checklist` command. Generates a comprehensive pre-release validation checklist covering build verification, certification requirements, store metadata, and launch readiness."
---

## Codex Adapter

This is the Codex Game Studio workflow skill `release-checklist`.

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

> **Explicit invocation only**: This skill should only run when the user explicitly requests it with `$ccgs-release-checklist`. Do not auto-invoke based on context matching.

## Phase 1: Parse Arguments

Read the argument for the target platform (`pc`, `console`, `mobile`, or `all`). If no platform is specified, default to `all`.

---

## Phase 2: Load Project Context

- Read `AGENTS.md` for project context, version information, and platform targets.
- Read the current milestone from `production/milestones/` to understand what features and content should be included in this release.

---

## Phase 3: Scan Codebase

Scan for outstanding issues:

- Count `TODO` comments
- Count `FIXME` comments
- Count `HACK` comments
- Note their locations and severity

Check for test results in any test output directories or CI logs if available.

---

## Phase 4: Generate the Release Checklist

```markdown
## Release Checklist: [Version] -- [Platform]
Generated: [Date]

### Codebase Health
- TODO count: [N] ([list top 5 if many])
- FIXME count: [N] ([list all -- these are potential blockers])
- HACK count: [N] ([list all -- these need review])

### Build Verification
- [ ] Clean build succeeds on all target platforms
- [ ] No compiler warnings (zero-warning policy)
- [ ] All assets included and loading correctly
- [ ] Build size within budget ([target size])
- [ ] Build version number correctly set ([version])
- [ ] Build is reproducible from tagged commit

### Quality Gates
- [ ] Zero S1 (Critical) bugs
- [ ] Zero S2 (Major) bugs -- or documented exceptions with producer approval
- [ ] All critical path features tested and signed off by QA
- [ ] Performance within budgets:
  - [ ] Target FPS met on minimum spec hardware
  - [ ] Memory usage within budget
  - [ ] Load times within budget
  - [ ] No memory leaks over extended play sessions
- [ ] No regression from previous build
- [ ] Soak test passed (4+ hours continuous play)

### Content Complete
- [ ] All placeholder assets replaced with final versions
- [ ] All TODO/FIXME in content files resolved or documented
- [ ] All player-facing text proofread
- [ ] All text localization-ready (no hardcoded strings)
- [ ] Audio mix finalized and approved
- [ ] Credits complete and accurate
```

Add platform-specific sections based on the argument:

**For `pc`:**
```markdown
### Platform Requirements: PC
- [ ] Minimum and recommended specs verified and documented
- [ ] Keyboard+mouse controls fully functional
- [ ] Controller support tested (Xbox, PlayStation, generic)
- [ ] Resolution scaling tested (1080p, 1440p, 4K, ultrawide)
- [ ] Windowed, borderless, and fullscreen modes working
- [ ] Graphics settings save and load correctly
- [ ] Steam/Epic/GOG SDK integrated and tested
- [ ] Achievements functional
- [ ] Cloud saves functional
- [ ] Steam Deck compatibility verified (if targeting)
```

**For `console`:**
```markdown
### Platform Requirements: Console
- [ ] TRC/TCR/Lotcheck requirements checklist complete
- [ ] Platform-specific controller prompts display correctly
- [ ] Suspend/resume works correctly
- [ ] User switching handled properly
- [ ] Network connectivity loss handled gracefully
- [ ] Storage full scenario handled
- [ ] Parental controls respected
- [ ] Platform-specific achievement/trophy integration tested
- [ ] First-party certification submission prepared
```

**For `mobile`:**
```markdown
### Platform Requirements: Mobile
- [ ] App store guidelines compliance verified
- [ ] All required device permissions justified and documented
- [ ] Privacy policy linked and accurate
- [ ] Data safety/nutrition labels completed
- [ ] Touch controls tested on multiple screen sizes
- [ ] Battery usage within acceptable range
- [ ] Background behavior correct (pause, resume, terminate)
- [ ] Push notification permissions handled correctly
- [ ] In-app purchase flow tested (if applicable)
- [ ] App size within store limits
```

**Store and launch sections (all platforms):**
```markdown
### Store / Distribution
- [ ] Store page metadata complete and proofread
  - [ ] Short description
  - [ ] Long description
  - [ ] Feature list
  - [ ] System requirements (PC)
- [ ] Screenshots up to date and per-platform resolution requirements met
- [ ] Trailers up to date
- [ ] Key art and capsule images current
- [ ] Age rating obtained and configured:
  - [ ] ESRB
  - [ ] PEGI
  - [ ] Other regional ratings as required
- [ ] Legal notices, EULA, and privacy policy in place
- [ ] Third-party license attributions complete
- [ ] Pricing configured for all regions

### Launch Readiness
- [ ] Analytics / telemetry verified and receiving data
- [ ] Crash reporting configured and dashboard accessible
- [ ] Day-one patch prepared and tested (if needed)
- [ ] On-call team schedule set for first 72 hours
- [ ] Community launch announcements drafted
- [ ] Press/influencer keys prepared for distribution
- [ ] Support team briefed on known issues and FAQ
- [ ] Rollback plan documented (if critical issues found post-launch)

### Go / No-Go: [READY / NOT READY]

**Rationale:**
[Summary of readiness assessment. List any blocking items that must be
resolved before launch. If NOT READY, list the specific items that need
resolution and estimated time to address them.]

**Sign-offs Required:**
- [ ] QA Lead
- [ ] Technical Director
- [ ] Producer
- [ ] Creative Director
```

---

## Phase 5: Save Checklist

Present the checklist to the user with: total checklist items, number of known blockers (FIXME/HACK counts, known bugs).

Ask: "May I write this to `production/releases/release-checklist-[version].md`?"

If yes, write the file, creating the directory if needed.

---

## Phase 6: Next Steps

- Run `$ccgs-gate-check` for a formal phase gate verdict before proceeding to release.
- Coordinate final sign-offs via `$ccgs-team-release`.
