# Lead Programmer — Agent Memory

## Skill Authoring Conventions

### Frontmatter
- Codex-facing workflow skills use only stable metadata fields: `name`,
  `description`, `argument-hint`, and `user-invocable`.
- Legacy tool policy fields such as `allowed-tools`, `tools`, and
  `disallowedTools` are non-binding in Codex and should not be used in new
  source skill or role frontmatter.
- `request_user_input` is a body-level usage pattern. Codex supports at most 3
  questions per call, with 2-3 choices per question. Each choice needs a
  `label` and `description`; multi-select is not supported.

### File Layout
- Skills live in `../ccgs-references/references/source-skills/<name>/SKILL.md` (subdirectory per skill, never flat .md)
- Section headers use `##` for phases, `###` for sub-sections
- Phase names follow "Phase N: Verb Noun" pattern (e.g., "Phase 1: Find the Story")
- Output format templates go in fenced code blocks

### Known Canonical Paths (verify before referencing in new skills)
- Tech debt register: `docs/tech-debt-register.md` (NOT `production/tech-debt.md`)
- Sprint files: `production/sprints/`
- Epic story files: `production/epics/[epic-slug]/story-[NNN]-[slug].md`
- Control manifest: `docs/architecture/control-manifest.md`
- Session state: `production/session-state/active.md`
- Systems index: `design/gdd/systems-index.md`
- Engine reference: `docs/engine-reference/[engine]/VERSION.md`

### Skills Completed
- `story-done` — end-of-story completion handshake (Phase 1-8, writes story file)
