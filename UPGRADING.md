# Upgrading Codex Game Studio

This guide covers upgrading your existing game project repo from one version
of the template to the next.

**Find your current version** in your git log:
```bash
git log --oneline | grep -i "release\|setup"
```
Or check GitHub releases/tags if this template has published releases.

---

## Table of Contents

- [Upgrade Strategies](#upgrade-strategies)
- [v1.0.0-beta → v1.0](#v100-beta--v10)
- [v0.4.x → v1.0](#v04x--v10)
- [v0.4.0 → v0.4.1](#v040--v041)
- [v0.3.0 → v0.4.0](#v030--v040)
- [v0.2.0 → v0.3.0](#v020--v030)
- [v0.1.0 → v0.2.0](#v010--v020)

---

## Upgrade Strategies

There are three ways to pull in template updates. Choose based on how your
repo is set up.

### Strategy A — Git Remote Merge (recommended)

Best when: you cloned the template and have your own commits on top of it.

```bash
# Add the template as a remote (one-time setup)
git remote add template https://github.com/<your-org-or-user>/Codex-Game-Studio.git

# Fetch the new version
git fetch template main

# Merge into your branch
git merge template/main --allow-unrelated-histories
```

Git will flag conflicts only in files that both the template *and* you have
changed. Resolve each one — your game content goes in, structural improvements
come along for the ride. Then commit the merge.

**Tip:** The files most likely to conflict are `AGENTS.md` and
`codex-studio/docs/technical-preferences.md`, because you've filled them in with
your engine and project settings. Keep your content; accept the structural changes.

---

### Strategy B — Cherry-pick specific commits

Best when: you only want one specific feature (e.g., just the new skill, not
the full update).

```bash
git remote add template https://github.com/<your-org-or-user>/Codex-Game-Studio.git
git fetch template main

# Cherry-pick the specific commit(s) you want
git cherry-pick <commit-sha>
```

Commit SHAs for each version are listed in the version sections below.

---

### Strategy C — Manual file copy

Best when: you didn't use git to set up the template (just downloaded a zip).

1. Download or clone the new version alongside your repo.
2. Copy the files listed under **"Safe to overwrite"** directly.
3. For files under **"Merge carefully"**, open both versions side-by-side
   and manually merge the structural changes while keeping your content.

---

## v0.4.1

**Released:** 2026-04-02
**Key themes:** Art direction integration, asset specification pipeline

### What Changed

| Category | Changes |
|----------|---------|
| **New skill** | `$ccgs-art-bible` — guided section-by-section visual identity authoring (9 sections). Mandatory art-director Task spawn per section. AD-ART-BIBLE sign-off gate. Required at Technical Setup phase. |
| **New skill** | `$ccgs-asset-spec` — per-asset visual spec and AI generation prompt generator. Reads art bible + GDD/level/character docs. Writes `design/assets/specs/` files and `design/assets/asset-manifest.md`. Full/lean/solo modes. |
| **New director gates (3)** | `AD-CONCEPT-VISUAL` (brainstorm Phase 4), `AD-ART-BIBLE` (art bible sign-off), `AD-PHASE-GATE` (gate-check panel) |
| **`$ccgs-brainstorm` update** | Added `Task` to allowed-tools (was missing — blocked all director spawning). Art-director now spawns in parallel with creative-director after pillars lock. Visual Identity Anchor written to game-concept.md. |
| **`$ccgs-gate-check` update** | Art-director added as 4th parallel director (AD-PHASE-GATE). Visual artifact checks: Visual Identity Anchor (Concept gate), art bible (Technical Setup gate), AD-ART-BIBLE sign-off + character visual profiles (Pre-Production gate). |
| **`$ccgs-team-level` update** | Art-director added to Step 1 parallel spawn (visual direction before layout). Level-designer now receives art-director targets as explicit constraints. Step 4 art-director role corrected to production-concepts only. |
| **`$ccgs-team-narrative` update** | Art-director added to Phase 2 parallel spawn (character visual design, environmental storytelling, cinematic tone). |
| **`$ccgs-design-system` update** | Routing table expanded with art-director + technical-artist for Combat, UI, Dialogue, Animation/VFX, Character categories. Visual/Audio section now mandatory (with art-director Task spawn) for 7 system categories. |
| **`workflow-catalog.yaml`** | `$ccgs-art-bible` added to Technical Setup (required). `$ccgs-asset-spec` added to Pre-Production (optional, repeatable). |

### Files: Safe to Overwrite

**New files to add:**
```
codex-studio/skills/art-bible/SKILL.md
codex-studio/skills/asset-spec/SKILL.md
codex-studio/docs/director-gates.md
```

**Existing files to overwrite (no user content):**
```
codex-studio/skills/brainstorm/SKILL.md
codex-studio/skills/gate-check/SKILL.md
codex-studio/skills/team-level/SKILL.md
codex-studio/skills/team-narrative/SKILL.md
codex-studio/skills/design-system/SKILL.md
codex-studio/docs/workflow-catalog.yaml
README.md
UPGRADING.md
```

### Files: Merge Carefully

None — all changes are to infrastructure files with no user content.

---

## v1.0.0-beta → v1.0

**Released:** 2026-05-13
**Commit range:** `49d1e45..HEAD`
**Key themes:** New `$ccgs-vertical-slice` gate, skill polish & bug fixes, contributor docs

### What Changed

| Category | Changes |
|----------|---------|
| **New skill** | `$ccgs-vertical-slice` — Pre-Production gate that validates the full game loop with a production-quality end-to-end build before Production. Pairs with the overhauled `$ccgs-prototype` (concept validation right after `$ccgs-brainstorm`). |
| **New flow** | Entity inventory step in `$ccgs-map-systems` — surfaces all named entities up front for cleaner downstream GDD authoring. |
| **UX polish** | Added missing `request_user_input` widgets to 7 skills; comprehensive skill audit for consistency, prompts, and flow gaps; exposed `--review` flag in `argument-hints` for all `team-*` skills. |
| **Bug fixes** | `#21` log-agent hooks logged "unknown" `agent_type`; `#36` missing `allowed-tools` in `$ccgs-architecture-decision` and `$ccgs-story-done`; `#42` `rg --type gdscript` is invalid (now uses `--glob *.gd`); `#43` session-start preview showed oldest state instead of newest; `#45` duplicate `## 0.` heading and broken step numbering in `$ccgs-architecture-decision`. |
| **Project docs** | Added `CONTRIBUTING.md` (framework contribution guidelines) and `SECURITY.md` (coordinated disclosure policy). |
| **Counts/refs** | Synced agent/skill/hook counts across `WORKFLOW-GUIDE.md`, `README.md`, and agent rosters; fixed stale agent names and skill model-tier fields. |

---

### Files: Safe to Overwrite

**New files to add:**
```
codex-studio/skills/vertical-slice/SKILL.md
CONTRIBUTING.md
SECURITY.md
```

**Existing files to overwrite (no user content):**
- All files under `codex-studio/skills/` modified in the commit range (skill audit + request_user_input widgets + `--review` argument-hints)
- `codex-studio/hooks/log-agent.sh` (fix #21)
- `README.md`, `docs/WORKFLOW-GUIDE.md`, `docs/examples/skill-flow-diagrams.md`
- `UPGRADING.md`

---

### Files: Merge Carefully

None — all changes are to infrastructure files with no user content.

---

## v0.4.x → v1.0

**Released:** 2026-03-29
**Commit range:** `6c041ac..HEAD`
**Key themes:** Director gates system, gate intensity modes, Godot C# specialist

### What Changed

| Category | Changes |
|----------|---------|
| **New system** | Director gates — named review checkpoints shared across all workflow skills. Defined in `codex-studio/docs/director-gates.md` |
| **New feature** | Gate intensity modes: `full` (all director gates), `lean` (phase gates only), `solo` (no directors). Set globally via `production/review-mode.txt` during `$ccgs-start`, or override per-run with `--review [mode]` on any gate-using skill |
| **New agent** | `godot-csharp-specialist` — C# code quality in Godot 4 projects |
| **Skill updates (13)** | All gate-using skills now parse `--review [full\|lean\|solo]` and include it in their argument-hint: `brainstorm`, `map-systems`, `design-system`, `architecture-decision`, `create-architecture`, `create-epics`, `create-stories`, `sprint-plan`, `milestone-review`, `playtest-report`, `prototype`, `story-done`, `gate-check` |
| **`$ccgs-start` update** | Added Phase 3b — sets review mode during onboarding, writes `production/review-mode.txt` |
| **`$ccgs-setup-engine` update** | Language selection step for Godot (GDScript vs C#) |
| **Docs** | `director-gates.md` — full gate catalog; `WORKFLOW-GUIDE.md` — Director Review Modes section; `README.md` — review intensity customization |

---

### Files: Safe to Overwrite

**New files to add:**
```
codex-studio/agents/godot-csharp-specialist.md
codex-studio/docs/director-gates.md
```

**Existing files to overwrite (no user content):**
```
codex-studio/skills/brainstorm/SKILL.md
codex-studio/skills/map-systems/SKILL.md
codex-studio/skills/design-system/SKILL.md
codex-studio/skills/architecture-decision/SKILL.md
codex-studio/skills/create-architecture/SKILL.md
codex-studio/skills/create-epics/SKILL.md
codex-studio/skills/create-stories/SKILL.md
codex-studio/skills/sprint-plan/SKILL.md
codex-studio/skills/milestone-review/SKILL.md
codex-studio/skills/playtest-report/SKILL.md
codex-studio/skills/prototype/SKILL.md
codex-studio/skills/story-done/SKILL.md
codex-studio/skills/gate-check/SKILL.md
codex-studio/skills/start/SKILL.md
codex-studio/skills/quick-design/SKILL.md
codex-studio/skills/setup-engine/SKILL.md
README.md
docs/WORKFLOW-GUIDE.md
UPGRADING.md
```

---

### Files: Merge Carefully

No files require manual merging in this release. All changes are to infrastructure files with no user content.

---

### New Features

#### Director Gates System

All major workflow skills now reference named gate checkpoints defined in
`codex-studio/docs/director-gates.md`. Gates are identified by domain prefix and name
(e.g., `CD-CONCEPT`, `TD-ARCHITECTURE`, `LP-CODE-REVIEW`). Each gate defines
which director to spawn, what inputs to pass, what verdicts mean, and how
lean/solo modes affect it.

Skills spawn gates using `Task` with the gate ID and documented inputs, rather
than embedding director prompts inline. This keeps skill bodies clean and makes
gate behavior consistent across all workflow phases.

#### Gate Intensity Modes

Three modes let you control how much director review you get:

- **`full`** (default) — all director gates run at every review checkpoint
- **`lean`** — per-skill director reviews are skipped; phase gates at `$ccgs-gate-check` still run
- **`solo`** — no director gates anywhere; `$ccgs-gate-check` checks artifact existence only

Set globally during `$ccgs-start` (writes `production/review-mode.txt`). Override any
individual run with `--review [mode]` on any gate-using skill:

```
/design-system combat --review lean
/gate-check concept --review full
/brainstorm my-game-idea --review solo
```

---

### After Upgrading

1. Run `$ccgs-start` once to set your preferred review mode — or create `production/review-mode.txt` manually with `full`, `lean`, or `solo`.
2. If you're mid-project, review `codex-studio/docs/director-gates.md` to understand which gates apply to your current phase.
3. Run `/skill-test static all` to verify all skills pass structural checks.

---

## v0.4.0 → v0.4.1

**Released:** 2026-03-26
**Commit range:** `04ed5d5..HEAD`
**Key themes:** Genre-agnostic agents, new skills, skill fixes

### What Changed

| Category | Changes |
|----------|---------|
| **New skills (1)** | `$ccgs-consistency-check` — cross-GDD entity consistency scanner |
| **Skill fixes (all team-*)** | Added no-argument guards, formal `Verdict: COMPLETE / BLOCKED` keywords, per-step request_user_input gates, adjacent area dependency checks (team-level), ethics enforcement (team-live-ops), NO-GO path with Phase skip (team-release) |
| **Agent fixes (4)** | Genre-agnostic language in game-designer, systems-designer, economy-designer, live-ops-designer — removed RPG-specific terms |

---

### Files: Safe to Overwrite

**New files to add:**
```
codex-studio/skills/consistency-check/SKILL.md
```

**Existing files to overwrite (no user content):**
```
codex-studio/skills/team-combat/SKILL.md      ← no-arg guard, verdict keywords, gate improvements
codex-studio/skills/team-narrative/SKILL.md   ← no-arg guard, verdict keywords, gate improvements
codex-studio/skills/team-ui/SKILL.md          ← no-arg guard, verdict keywords, gate improvements
codex-studio/skills/team-release/SKILL.md     ← no-arg guard, verdict keywords, NO-GO path
codex-studio/skills/team-polish/SKILL.md      ← no-arg guard, verdict keywords, gate improvements
codex-studio/skills/team-audio/SKILL.md       ← no-arg guard, verdict keywords, gate improvements
codex-studio/skills/team-level/SKILL.md       ← no-arg guard, verdict keywords, adjacent area checks
codex-studio/skills/team-live-ops/SKILL.md    ← no-arg guard, verdict keywords, ethics enforcement
codex-studio/skills/team-qa/SKILL.md          ← no-arg guard, verdict keywords, gate improvements
codex-studio/skills/map-systems/SKILL.md      ← verdict keywords
codex-studio/skills/create-epics/SKILL.md     ← "May I write" protocol fix, verdict keywords
codex-studio/skills/create-stories/SKILL.md   ← verdict keywords
codex-studio/agents/game-designer.md          ← genre-agnostic language
codex-studio/agents/systems-designer.md       ← genre-agnostic language
codex-studio/agents/economy-designer.md       ← genre-agnostic language
codex-studio/agents/live-ops-designer.md      ← genre-agnostic language
```

---

### Files: Merge Carefully

No files require manual merging in this release. All changes are to infrastructure files with no user content.

---

### After Upgrading

1. Run `/skill-test catalog` to verify all skills are indexed.
2. Run `/skill-test lint [skill-name]` after any skill edits to check structural compliance.
3. If you've customized any team-* skills, review the updated versions — no-argument guard and `Verdict:` keywords are now required for all team-* skills.

---

## v0.3.0 → v0.4.0

**Released:** 2026-03-21
**Commit range:** `b1cad29..HEAD`
**Key themes:** Full UX/UI pipeline, complete story lifecycle, brownfield adoption, comprehensive QA/testing framework, pipeline integrity, 29 new skills

### What Changed

| Category | Changes |
|----------|---------|
| **New skills (17)** | `$ccgs-ux-design`, `$ccgs-ux-review`, `$ccgs-help`, `$ccgs-quick-design`, `$ccgs-review-all-gdds`, `$ccgs-story-readiness`, `$ccgs-story-done`, `$ccgs-sprint-status`, `$ccgs-adopt`, `$ccgs-create-architecture`, `$ccgs-create-control-manifest`, `$ccgs-create-epics`, `$ccgs-create-stories`, `$ccgs-dev-story`, `$ccgs-propagate-design-change`, `$ccgs-content-audit`, `$ccgs-architecture-review` |
| **New skills QA (12)** | `$ccgs-qa-plan`, `$ccgs-smoke-check`, `$ccgs-soak-test`, `$ccgs-regression-suite`, `$ccgs-test-setup`, `$ccgs-test-helpers`, `$ccgs-test-evidence-review`, `$ccgs-test-flakiness`, `$ccgs-skill-test`, `$ccgs-bug-triage`, `$ccgs-team-live-ops`, `$ccgs-team-qa` |
| **New hooks (4)** | `log-agent-stop.sh` — agent audit trail stop; `notify.sh` — Windows toast notifications; `post-compact.sh` — session recovery reminder after compaction; `validate-skill-change.sh` — advises `$ccgs-skill-test` after skill edits |
| **New templates (8)** | `ux-spec.md`, `hud-design.md`, `accessibility-requirements.md`, `interaction-pattern-library.md`, `player-journey.md`, `difficulty-curve.md`, and 2 adoption plan templates |
| **New infrastructure** | `workflow-catalog.yaml` (7-phase pipeline, read by `$ccgs-help`), `docs/architecture/tr-registry.yaml` (stable TR-IDs), `production/sprint-status.yaml` schema |
| **Skill updates** | `$ccgs-gate-check` — 3 gates now require UX artifacts; Pre-Production gate requires vertical slice (HARD gate) |
| **Skill updates** | `$ccgs-sprint-plan` — writes `sprint-status.yaml`; `$ccgs-sprint-status` reads it |
| **Skill updates** | `$ccgs-story-done` — 8-phase completion review, updates story file, surfaces next ready story |
| **Skill updates** | `$ccgs-design-review` — removed architecture gap check (wrong stage) |
| **Skill updates** | `$ccgs-team-ui` — full UX pipeline (ux-design → ux-review → team phases) |
| **Agent updates** | 14 specialist agents — `memory: project` added |
| **Agent updates** | `prototyper` — `isolation: worktree` (throwaway work in isolated git branch) |
| **Model routing** | Fast/Standard/Deep tier assignments documented in coordination rules; skills declare their tier in frontmatter |
| **Directory AGENTS.md** | Scaffolded `design/AGENTS.md`, `src/AGENTS.md`, `docs/AGENTS.md` — path-scoped instructions for each directory |
| **Pipeline integrity** | TR-ID stability, manifest versioning, ADR status gates, TR-ID reference not quote |
| **GDD template** | `## Game Feel` section added (input responsiveness, animation targets, impact moments) |

---

### Files: Safe to Overwrite

**New files to add:**
```
codex-studio/skills/ux-design/SKILL.md
codex-studio/skills/ux-review/SKILL.md
codex-studio/skills/help/SKILL.md
codex-studio/skills/quick-design/SKILL.md
codex-studio/skills/review-all-gdds/SKILL.md
codex-studio/skills/story-readiness/SKILL.md
codex-studio/skills/story-done/SKILL.md
codex-studio/skills/sprint-status/SKILL.md
codex-studio/skills/adopt/SKILL.md
codex-studio/skills/create-architecture/SKILL.md
codex-studio/skills/create-control-manifest/SKILL.md
codex-studio/skills/create-epics/SKILL.md
codex-studio/skills/create-stories/SKILL.md
codex-studio/skills/dev-story/SKILL.md
codex-studio/skills/propagate-design-change/SKILL.md
codex-studio/skills/content-audit/SKILL.md
codex-studio/skills/architecture-review/SKILL.md
codex-studio/skills/qa-plan/SKILL.md
codex-studio/skills/smoke-check/SKILL.md
codex-studio/skills/soak-test/SKILL.md
codex-studio/skills/regression-suite/SKILL.md
codex-studio/skills/test-setup/SKILL.md
codex-studio/skills/test-helpers/SKILL.md
codex-studio/skills/test-evidence-review/SKILL.md
codex-studio/skills/test-flakiness/SKILL.md
codex-studio/skills/skill-test/SKILL.md
codex-studio/skills/bug-triage/SKILL.md
codex-studio/skills/team-live-ops/SKILL.md
codex-studio/skills/team-qa/SKILL.md
codex-studio/hooks/log-agent-stop.sh
codex-studio/hooks/notify.sh
codex-studio/hooks/post-compact.sh
codex-studio/hooks/validate-skill-change.sh
codex-studio/docs/workflow-catalog.yaml
codex-studio/docs/templates/ux-spec.md
codex-studio/docs/templates/hud-design.md
codex-studio/docs/templates/accessibility-requirements.md
codex-studio/docs/templates/interaction-pattern-library.md
codex-studio/docs/templates/player-journey.md
codex-studio/docs/templates/difficulty-curve.md
design/AGENTS.md
src/AGENTS.md
docs/AGENTS.md
```

**Existing files to overwrite (no user content):**
```
codex-studio/skills/gate-check/SKILL.md
codex-studio/skills/sprint-plan/SKILL.md
codex-studio/skills/sprint-status/SKILL.md
codex-studio/skills/design-review/SKILL.md
codex-studio/skills/team-ui/SKILL.md
codex-studio/skills/story-readiness/SKILL.md
codex-studio/skills/story-done/SKILL.md
codex-studio/docs/templates/game-design-document.md    ← adds Game Feel section
README.md
docs/WORKFLOW-GUIDE.md
UPGRADING.md
```

**Agent files to overwrite** (if you haven't written custom prompts into them):
```
codex-studio/agents/prototyper.md         ← adds isolation: worktree
codex-studio/agents/art-director.md       ← adds memory: project
codex-studio/agents/audio-director.md     ← adds memory: project
codex-studio/agents/economy-designer.md   ← adds memory: project
codex-studio/agents/game-designer.md      ← adds memory: project
codex-studio/agents/gameplay-programmer.md ← adds memory: project
codex-studio/agents/lead-programmer.md    ← adds memory: project
codex-studio/agents/level-designer.md     ← adds memory: project
codex-studio/agents/narrative-director.md ← adds memory: project
codex-studio/agents/systems-designer.md   ← adds memory: project
codex-studio/agents/technical-artist.md   ← adds memory: project
codex-studio/agents/ui-programmer.md      ← adds memory: project
codex-studio/agents/ux-designer.md        ← adds memory: project
codex-studio/agents/world-builder.md      ← adds memory: project
```

---

### Files: Merge Carefully

#### `codex-studio/hook-config.json`

Four new hooks are registered in this version. If you haven't customized `hook-config.json`, overwriting is safe. Otherwise, add the following hook entries manually:

- `log-agent-stop.sh` — `SubagentStop` event (agent audit trail stop)
- `notify.sh` — `Notification` event (Windows toast notification)
- `post-compact.sh` — `PostCompact` event (session recovery reminder)
- `validate-skill-change.sh` — `PostToolUse` event filtered to `codex-studio/skills/` writes

#### Customized agent files

If you've added project-specific knowledge to agent `.md` files, do a diff and manually add the `memory: project` line to the YAML frontmatter where appropriate. Creative and technical director agents intentionally keep `memory: user` — only specialist agents get `memory: project`.

---

### New Features

#### Complete Story Lifecycle

Stories now have a formal lifecycle enforced by two skills:

- **`$ccgs-story-readiness`** — validates a story is implementation-ready before a developer picks it up. Checks Design (GDD req linked), Architecture (ADR accepted), Scope (criteria testable), and DoD (manifest version current). Verdict: READY / NEEDS WORK / BLOCKED.
- **`$ccgs-story-done`** — 8-phase completion review after implementation. Verifies each acceptance criterion, checks for GDD/ADR deviations, prompts code review, updates the story file to `Status: Complete`, and surfaces the next ready story.

Flow: `$ccgs-story-readiness` → implement → `$ccgs-story-done` → next story

#### Full UX/UI Pipeline

- **`$ccgs-ux-design`** — guided section-by-section UX spec authoring. Three modes: screen/flow, HUD, or interaction pattern library. Reads GDD UI requirements and player journey. Output to `design/ux/`.
- **`$ccgs-ux-review`** — validates UX specs against GDD alignment, accessibility tier, and pattern library. Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION.
- **`$ccgs-team-ui`** updated: Phase 1 now runs `$ccgs-ux-design` + `$ccgs-ux-review` as a hard gate before visual design begins.

#### Brownfield Adoption

**`$ccgs-adopt`** onboards existing projects to the template format. Audits internal structure of GDDs, ADRs, stories, systems-index, and infra. Classifies gaps (BLOCKING/HIGH/MEDIUM/LOW). Builds an ordered migration plan. Never regenerates existing artifacts — only fills gaps.

Argument modes: `full | gdds | adrs | stories | infra`

Also: `/design-system retrofit [path]` and `/architecture-decision retrofit [path]` detect existing files and add only missing sections.

#### Sprint Tracking YAML

`production/sprint-status.yaml` is now the authoritative story tracking format:
- Written by `$ccgs-sprint-plan` (initializes all stories) and `$ccgs-story-done` (sets status to `done`)
- Read by `$ccgs-sprint-status` (fast snapshot) and `$ccgs-help` (per-story status in production phase)
- Status values: `backlog | ready-for-dev | in-progress | review | done | blocked`
- Falls back gracefully to markdown scanning if file doesn't exist

#### `$ccgs-help` — Context-Aware Next Step

`$ccgs-help` reads your current stage and in-progress work, checks which artifacts are complete, and tells you exactly what to do next — one primary required step, plus optional opportunities. Distinct from `$ccgs-start` (first-time only) and `$ccgs-project-stage-detect` (full audit).

#### Comprehensive QA and Testing Framework

Nine new QA/testing skills covering the full testing lifecycle:

- **`$ccgs-test-setup`** — scaffolds the test framework and CI/CD pipeline for your engine
- **`$ccgs-test-helpers`** — generates engine-specific test helper libraries (GDUnit4, NUnit, etc.)
- **`$ccgs-qa-plan`** — generates a QA test plan for a sprint or feature, classifying stories by test type
- **`$ccgs-smoke-check`** — runs the critical path smoke test gate before QA hand-off
- **`$ccgs-soak-test`** — generates a soak test protocol for extended play sessions (stability, memory leaks)
- **`$ccgs-regression-suite`** — maps test coverage to GDD critical paths, identifies fixed bugs lacking regression tests
- **`$ccgs-test-evidence-review`** — quality review of test files and manual evidence documents
- **`$ccgs-test-flakiness`** — detects non-deterministic tests by reading CI run logs
- **`$ccgs-skill-test`** — validates skill files for structural compliance and behavioral correctness (three modes: lint, spec, catalog)

Also new: **`$ccgs-bug-triage`** re-evaluates all open bugs for priority, severity, and ownership.

#### Skill Validator (`$ccgs-skill-test`)

`$ccgs-skill-test` is a meta-skill for validating the harness itself. Run it after editing any skill file. Three modes:
- `lint` — validates YAML frontmatter and required fields
- `spec [skill-name]` — runs behavioral spec tests against a specific skill
- `catalog` — checks that all skills in `codex-studio/skills/` are indexed in the catalog

The new `validate-skill-change.sh` hook reminds you to run `$ccgs-skill-test` automatically when a skill file is modified.

#### Team Live-Ops and Team QA Orchestration

- **`$ccgs-team-live-ops`** — coordinates live-ops-designer + economy-designer + community-manager + analytics-engineer for post-launch content planning (seasonal events, battle pass, retention)
- **`$ccgs-team-qa`** — orchestrates qa-lead + qa-tester + gameplay-programmer + producer through a full QA cycle: strategy, execution, coverage, and sign-off

#### Model Tier Routing

Skills are now explicitly assigned to Fast, Standard, or Deep tiers based on task complexity. Read-only status checks use Fast; complex multi-document synthesis uses Deep; everything else defaults to Standard. Tier assignments are documented in `codex-studio/docs/coordination-rules.md`.

#### Directory AGENTS.md Files

Three new directory-scoped AGENTS.md files (`design/`, `src/`, `docs/`) provide path-specific instructions to agents working in those directories. These load automatically when Codex reads files in that directory.

---

### After Upgrading

1. **Verify new hooks** are registered in `codex-studio/hook-config.json` — check for all four: `log-agent-stop.sh`, `notify.sh`, `post-compact.sh`, `validate-skill-change.sh`.

2. **Test the audit trail** by spawning any subagent — both start and stop events should appear in `production/session-logs/`.

3. **Generate sprint-status.yaml** if you're in active production:
   ```
   /sprint-plan status
   ```

4. **Run `$ccgs-adopt`** if you have existing GDDs or ADRs that predate this template version — it will identify which sections need to be added without overwriting your content.

5. **Validate your skills** after any skill edits with `$ccgs-skill-test` — the new `validate-skill-change.sh` hook will automatically remind you to do this.

---

## v0.2.0 → v0.3.0

**Released:** 2026-03-09
**Commit range:** `e289ce9..HEAD`
**Key themes:** `$ccgs-design-system` GDD authoring, `$ccgs-map-systems` rename, custom status line

### Breaking Changes

#### `$ccgs-design-systems` renamed to `$ccgs-map-systems`

The `$ccgs-design-systems` skill was renamed to `$ccgs-map-systems` for clarity
(decomposing = *mapping*, not *designing*).

**Action required:** Update any documentation, notes, or scripts that invoke
`$ccgs-design-systems`. The new invocation is `$ccgs-map-systems`.

### What Changed

| Category | Changes |
|----------|---------|
| **New skills** | `$ccgs-design-system` (guided GDD authoring, section-by-section) |
| **Renamed skills** | `$ccgs-design-systems` → `$ccgs-map-systems` (breaking rename) |
| **New files** | `codex-studio/statusline.sh`, `codex-studio/hook-config.json` statusline config |
| **Skill updates** | `$ccgs-gate-check` — writes `production/stage.txt` on PASS, new phase definitions |
| **Skill updates** | `brainstorm`, `start`, `design-review`, `project-stage-detect`, `setup-engine` — cross-reference fixes |
| **Bug fixes** | `log-agent.sh`, `validate-commit.sh` — hook execution fixed |
| **Docs** | `UPGRADING.md` added, `README.md` updated, `WORKFLOW-GUIDE.md` updated |

---

### Files: Safe to Overwrite

**New files to add:**
```
codex-studio/skills/design-system/SKILL.md
codex-studio/statusline.sh
```

**Existing files to overwrite (no user content):**
```
codex-studio/skills/map-systems/SKILL.md      ← was design-systems/SKILL.md
codex-studio/skills/gate-check/SKILL.md
codex-studio/skills/brainstorm/SKILL.md
codex-studio/skills/start/SKILL.md
codex-studio/skills/design-review/SKILL.md
codex-studio/skills/project-stage-detect/SKILL.md
codex-studio/skills/setup-engine/SKILL.md
codex-studio/hooks/log-agent.sh
codex-studio/hooks/validate-commit.sh
README.md
docs/WORKFLOW-GUIDE.md
UPGRADING.md
```

**Delete (replaced by rename):**
```
codex-studio/skills/design-systems/   ← entire directory; replaced by map-systems/
```

---

### Files: Merge Carefully

#### `codex-studio/hook-config.json`

The new version adds a status line reference pointing to
`codex-studio/statusline.sh`. If you haven't customized `codex-studio/hook-config.json`, overwriting
is safe. Otherwise, add this block manually:

```json
"statusLine": {
  "script": "codex-studio/statusline.sh"
}
```

---

### New Features

#### Custom Status Line

`codex-studio/statusline.sh` displays a 7-stage production pipeline breadcrumb in
the terminal status line:

```
ctx: 42% | gpt-5 | Systems Design
```

In Production/Polish/Release stages, it also shows the active Epic/Feature/Task
from `production/session-state/active.md` if a `<!-- STATUS -->` block is present:

```
ctx: 42% | gpt-5 | Production | Combat System > Melee Combat > Hitboxes
```

The current stage is auto-detected from project artifacts, or can be pinned by
writing a stage name to `production/stage.txt`.

#### `$ccgs-gate-check` Stage Advancement

When a gate PASS verdict is confirmed, `$ccgs-gate-check` now writes the new stage
name to `production/stage.txt`. This immediately updates the status line for all
future sessions without requiring manual file edits.

---

### After Upgrading

1. **Delete the old skill directory:**
   ```bash
   rm -rf codex-studio/skills/design-systems/
   ```

2. **Test the status line** by starting a Codex session — you should see
   the stage breadcrumb in the terminal footer.

3. **Verify hook execution** still works:
   ```bash
   bash codex-studio/hooks/log-agent.sh '{}' '{}'
   bash codex-studio/hooks/validate-commit.sh '{}' '{}'
   ```

---

## v0.1.0 → v0.2.0

**Released:** 2026-02-21
**Commit range:** `ad540fe..e289ce9`
**Key themes:** Context Resilience, request_user_input integration, `$ccgs-map-systems` skill

### What Changed

| Category | Changes |
|----------|---------|
| **New skills** | `$ccgs-start` (onboarding), `$ccgs-map-systems` (systems decomposition), `$ccgs-design-system` (guided GDD authoring) |
| **New hooks** | `session-start.sh` (recovery), `detect-gaps.sh` (gap detection) |
| **New templates** | `systems-index.md`, 3 collaborative-protocol templates |
| **Context management** | Major rewrite — file-backed state strategy added |
| **Agent updates** | 14 design/creative agents — request_user_input integration |
| **Skill updates** | All 7 `team-*` skills + `brainstorm` — request_user_input at phase transitions |
| **AGENTS.md** | Slimmed from ~159 to ~60 lines; 5 doc imports instead of 10 |
| **Hook updates** | All 8 hooks — Windows compatibility fixes, new features |
| **Docs removed** | `docs/IMPROVEMENTS-PROPOSAL.md`, `docs/MULTI-STAGE-DOCUMENT-WORKFLOW.md` |

---

### Files: Safe to Overwrite

These are pure infrastructure — you have not customized them. Copy the new
versions directly with no risk to your project content.

**New files to add:**
```
codex-studio/skills/start/SKILL.md
codex-studio/skills/map-systems/SKILL.md
codex-studio/skills/design-system/SKILL.md
codex-studio/docs/templates/systems-index.md
codex-studio/docs/templates/collaborative-protocols/design-agent-protocol.md
codex-studio/docs/templates/collaborative-protocols/implementation-agent-protocol.md
codex-studio/docs/templates/collaborative-protocols/leadership-agent-protocol.md
codex-studio/hooks/detect-gaps.sh
codex-studio/hooks/session-start.sh
production/session-state/.gitkeep
docs/examples/README.md
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
.github/PULL_REQUEST_TEMPLATE.md
```

**Existing files to overwrite (no user content):**
```
codex-studio/skills/brainstorm/SKILL.md
codex-studio/skills/design-review/SKILL.md
codex-studio/skills/gate-check/SKILL.md
codex-studio/skills/project-stage-detect/SKILL.md
codex-studio/skills/setup-engine/SKILL.md
codex-studio/skills/team-audio/SKILL.md
codex-studio/skills/team-combat/SKILL.md
codex-studio/skills/team-level/SKILL.md
codex-studio/skills/team-narrative/SKILL.md
codex-studio/skills/team-polish/SKILL.md
codex-studio/skills/team-release/SKILL.md
codex-studio/skills/team-ui/SKILL.md
codex-studio/hooks/log-agent.sh
codex-studio/hooks/pre-compact.sh
codex-studio/hooks/session-stop.sh
codex-studio/hooks/validate-assets.sh
codex-studio/hooks/validate-commit.sh
codex-studio/hooks/validate-push.sh
codex-studio/rules/design-docs.md
codex-studio/docs/hooks-reference.md
codex-studio/docs/skills-reference.md
codex-studio/docs/quick-start.md
codex-studio/docs/directory-structure.md
codex-studio/docs/context-management.md
docs/COLLABORATIVE-DESIGN-PRINCIPLE.md
docs/WORKFLOW-GUIDE.md
README.md
```

**Agent files to overwrite** (if you haven't written custom prompts into them):
```
codex-studio/agents/art-director.md
codex-studio/agents/audio-director.md
codex-studio/agents/creative-director.md
codex-studio/agents/economy-designer.md
codex-studio/agents/game-designer.md
codex-studio/agents/level-designer.md
codex-studio/agents/live-ops-designer.md
codex-studio/agents/narrative-director.md
codex-studio/agents/producer.md
codex-studio/agents/systems-designer.md
codex-studio/agents/technical-director.md
codex-studio/agents/ux-designer.md
codex-studio/agents/world-builder.md
codex-studio/agents/writer.md
```

If you *have* customized agent prompts, see "Merge carefully" below.

---

### Files: Merge Carefully

These files contain both template structure and your project-specific content.
Do **not** overwrite them — merge the changes manually.

#### `AGENTS.md`

The template version was slimmed from ~159 lines to ~60 lines. The key
structural change: 5 doc imports were removed because they're auto-loaded
by Codex anyway (agent-roster, skills-reference, hooks-reference,
rules-reference, review-workflow).

**What to keep from your version:**
- The `## Technology Stack` section (your engine/language choices)
- Any project-specific additions you made

**What to adopt from the new version:**
- Slimmer imports list (drop the 5 redundant `@` imports if present)
- Updated collaboration protocol wording

#### `codex-studio/docs/technical-preferences.md`

If you ran `$ccgs-setup-engine`, this file has your engine config, naming
conventions, and performance budgets. Keep all of it. The template version
is just the empty placeholder.

#### `codex-studio/docs/templates/game-concept.md`

Minor structural update — a `## Next Steps` section was added pointing to
`$ccgs-map-systems`. Add that section to your copy if you want the updated
guidance, but it's not required.

#### `codex-studio/hook-config.json`

Check whether the new version adds any permission rules you want. The change
was minor (schema update). If you haven't customized your `hook-config.json`,
overwriting is safe.

#### Customized agent files

If you've added project-specific knowledge or custom behavior to any agent
`.md` file, do a diff and manually add the new request_user_input integration
sections rather than overwriting. The change in each agent is a standardized
collaborative protocol block at the end of the system prompt.

---

### Files: Delete

These files were removed in v0.2.0. If present in your repo, you can safely
delete them — they're replaced by better-organized alternatives.

```
docs/IMPROVEMENTS-PROPOSAL.md      → superseded by WORKFLOW-GUIDE.md
docs/MULTI-STAGE-DOCUMENT-WORKFLOW.md → content merged into context-management.md
```

---

### After Upgrading

1. **Run `$ccgs-project-stage-detect`** to verify the system reads your project
   correctly with the new detection logic.

2. **Run `$ccgs-start`** once if you haven't used it — it now correctly identifies
   your stage and skips onboarding steps you've already done.

3. **Check `production/session-state/`** exists and is gitignored:
   ```bash
   ls production/session-state/
   cat .gitignore | grep session-state
   ```

4. **Test hook execution** — if you're on Windows, verify the new hooks run
   without errors in Git Bash:
   ```bash
   bash codex-studio/hooks/detect-gaps.sh '{}' '{}'
   bash codex-studio/hooks/session-start.sh '{}' '{}'
   ```

---

*Each future version will have its own section in this file.*
