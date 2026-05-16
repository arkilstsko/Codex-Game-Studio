<p align="center">
  <h1 align="center">Codex Game Studio</h1>
  <p align="center">
    Turn a Codex session into a structured game development studio.
    <br />
    A further-developed Codex-first game production framework.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="codex-adapter/references/agents"><img src="https://img.shields.io/badge/role%20references-49-blueviolet" alt="49 Role References"></a>
  <a href="codex-adapter/skills"><img src="https://img.shields.io/badge/codex%20skills-74-green" alt="74 Codex Skills"></a>
  <a href="codex-adapter/references/hooks"><img src="https://img.shields.io/badge/reference%20hooks-12-orange" alt="12 Reference Hooks"></a>
  <a href="codex-adapter/references/rules"><img src="https://img.shields.io/badge/rules-11-red" alt="11 Rules"></a>
</p>

---

## Attribution

Codex Game Studio is a Codex-first adaptation and further development of
[Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios).

The original project, studio structure, agents, workflows, rules, templates,
and MIT license are credited to Donchitos. The original copyright notice is
preserved in [LICENSE](LICENSE).

---

## Why This Exists

AI can help build games, but game development needs more than one general
assistant. It needs scope control, design checks, production flow, technical
standards, QA, release discipline, and a way to keep decisions connected over
time.

Codex Game Studio gives Codex a studio-shaped workflow:

- Directors and leads as role references for strategic decisions
- Specialists for design, programming, art, audio, narrative, QA, and release
- Codex skills for each major phase from concept to launch
- Project templates for design docs, UX specs, ADRs, sprint plans, release
  checklists, playtest reports, and more
- Safety rules and hook scripts kept as reference checks for Codex workflows

The user stays in control. Codex provides structure, options, implementation,
review, and verification.

## What This Fork Adds

This repo is not only a command rename. It keeps the original studio idea while
making it practical to use and maintain in Codex:

- **Codex-native skill packaging** - 73 workflow skills are generated as
  installable `$ccgs-*` Codex skills plus a bundled `ccgs-references` support
  skill.
- **Self-contained installs** - generated skills use relative reference paths,
  so temp installs and normal `~/.codex/skills` installs resolve the same way.
- **Safer installer behavior** - `--replace` stages replacements through a temp
  copy and backup path instead of deleting the existing skill before copy
  success is known.
- **Codex-compatible interaction model** - legacy Task/subagent assumptions are
  rewritten into role-reference passes, and `request_user_input` guidance follows
  Codex's supported schema.
- **Validation and release hygiene** - `scripts/validate_repo.py`, a prepublish
  checklist, security reporting docs, and smoke-install checks help keep the
  generated bundle honest.
- **Project-ready template tree** - common game-development folders are tracked
  with `.gitkeep` files so new projects start with the expected structure.

---

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Codex skills** | 74 | 73 workflow skills plus `ccgs-references` for role/rule context |
| **Role references** | 49 | Original game-studio agent definitions adapted for Codex role simulation |
| **Agent memory** | 1 | Lead programmer memory reference carried into the installable bundle |
| **Reference hooks** | 12 | Original validation scripts kept as reference checks |
| **Rules** | 11 | Coding and design standards for gameplay, engine, AI, UI, networking, testing, narrative, shaders, and docs |
| **Templates** | 41 | Document templates for GDDs, ADRs, UX specs, sprint plans, test plans, release notes, patch notes, and more |

## Installation

Clone the repo:

```bash
git clone https://github.com/arkilstsko/Codex-Game-Studio.git my-game
cd my-game
```

Generate Codex skills:

```bash
python3 codex-adapter/scripts/generate_codex_skills.py
```

Install them into Codex:

```bash
python3 codex-adapter/scripts/install_codex_skills.py --replace
```

Restart Codex or start a new Codex thread so the `$ccgs-*` skills appear in the
available skill list.

Preview install changes without writing:

```bash
python3 codex-adapter/scripts/install_codex_skills.py --dry-run
```

Validate the repo and generated bundle:

```bash
python3 scripts/validate_repo.py
```

## Quick Start

After installation, start with:

```text
$ccgs-start
```

That guided onboarding flow detects where the project is and routes to the
right next workflow.

Common entry points:

```text
$ccgs-brainstorm open
$ccgs-setup-engine godot 4
$ccgs-project-stage-detect
$ccgs-prototype
$ccgs-dev-story
$ccgs-story-done
$ccgs-code-review
```

## Command Mapping

Original slash commands map directly to Codex skills:

```text
/start              -> $ccgs-start
/brainstorm         -> $ccgs-brainstorm
/setup-engine       -> $ccgs-setup-engine
/design-system      -> $ccgs-design-system
/create-architecture -> $ccgs-create-architecture
/dev-story          -> $ccgs-dev-story
/story-done         -> $ccgs-story-done
/code-review        -> $ccgs-code-review
/release-checklist  -> $ccgs-release-checklist
```

All generated skills use the same rule: replace `/command-name` with
`$ccgs-command-name`.

## Studio Roles

Codex does not use Codex subagents directly. The original agent files are
kept as role references and loaded when a workflow needs that perspective.

```
Tier 1 - Directors
  creative-director    technical-director    producer

Tier 2 - Department Leads
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

Tier 3 - Specialists
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

Engine-specific references are included for Godot, Unity, and Unreal Engine.

## Project Structure

```text
AGENTS.md                           # Codex workspace guidance
codex-adapter/
  README.md                         # Adapter usage
  scripts/
    generate_codex_skills.py         # Converts upstream skills to Codex skills
    install_codex_skills.py          # Installs generated skills into ~/.codex/skills
  skills/                           # Generated Codex skills
  references/
    agents/                         # Role reference files
    agent-memory/                   # Role memory files
    docs/                           # Workflow docs and templates
    hooks/                          # Reference validation scripts
    rules/                          # Coding and design rules
codex-studio/                       # Codex-native workflow source material
  agents/                           # Role source files
  agent-memory/                     # Role memory source files
  docs/                             # Workflow docs and templates
  hooks/                            # Reference validation scripts
  rules/                            # Coding and design rules
  skills/                           # Source workflow skills
  hook-config.json                  # Reference hook configuration
  skill-testing-framework/          # Optional quality specs for workflow maintainers
src/                                # Game source code
assets/                             # Art, audio, VFX, shaders, data files
design/                             # GDDs, narrative docs, level designs
docs/                               # Technical documentation and ADRs
tests/                              # Test suites
tools/                              # Build and pipeline tools
prototypes/                         # Throwaway prototypes
production/                         # Sprint plans, milestones, release tracking
```

## How It Works In Codex

Generated skills include a Codex adapter prelude that maps original tool names:

| Original tool concept | Codex equivalent |
|-----------------------|------------------|
| `Read`, `Glob`, `Grep` | Inspect files with `sed`, `find`, and `rg` |
| `Write`, `Edit` | Edit with `apply_patch` |
| `Bash` | Run commands with `exec_command` |
| `request_user_input` | Use Codex user input UI when available, otherwise concise chat questions |
| Codex subagents | Simulate the named role locally from reference files |
| Codex hooks | Treat as reference checks unless separately wired into automation |

The generated skills are intentionally conservative. They load role references
when a workflow needs a specialist perspective, but they do not assume that
Codex exposes a native Task-style subagent API in every environment.

## Workflow Phases

1. **Concept** - brainstorm, pillars, prototype direction
2. **Systems Design** - GDDs, system maps, UX specs
3. **Technical Setup** - architecture, ADRs, control manifests
4. **Pre-Production** - vertical slice, epics, stories, sprint plan
5. **Production** - implement stories, review, test, document
6. **Polish** - QA, performance, balance, accessibility, localization
7. **Release** - launch checklist, changelog, hotfix, day-one patch

## Collaboration Model

This is not an autopilot system.

The intended loop is:

1. Codex asks for missing context.
2. Codex presents options and tradeoffs.
3. The user chooses.
4. Codex drafts or implements.
5. Codex verifies the result.
6. The user approves scope and direction.

That keeps creative control with the user while making the process more
structured and repeatable.

## Project Status

The current focus is reliability and Codex-native usability:

- Install flow is tested with both default and temporary targets.
- Generated skills are checked for stale upstream tool assumptions.
- Reference hooks are documented as manual/reference scripts, not automatic
  runtime hooks.
- Engine reference workflows keep project output under `docs/engine-reference/`.

See [docs/ROADMAP.md](docs/ROADMAP.md) for planned next upgrades.

## License

MIT. See [LICENSE](LICENSE).

Original copyright notice:

```text
Copyright (c) 2026 Donchitos
```
