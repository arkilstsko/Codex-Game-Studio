---
name: ccgs-patch-notes
description: "Codex Game Studio workflow `/patch-notes`. Use when the user asks for CCGS game-studio workflow `ccgs-patch-notes` or the original `/patch-notes` command. Generate player-facing patch notes from git history, sprint data, and internal changelogs. Translates developer language into clear, engaging player communication."
---

## Codex Adapter

This is the Codex Game Studio workflow skill `patch-notes`.

Use the workflow below with these Codex mappings:

- Slash-command references are mapped to Codex skill invocations with the `ccgs-` prefix.
- `Read`, `Glob`, and `Grep` mean inspect files with `sed`, `find`, and `rg`.
- `Write` and `Edit` mean make file changes with `apply_patch`.
- `Bash` means use `exec_command`.
- `Web search` and `Web fetch` mean use Codex web/browser tools when available; prefer official engine documentation for engine lookups. If web tools are unavailable, ask the user for the source URL or state the limitation.
- `request_user_input` means use Codex's structured input tool when available: at most 3 questions, 2-3 choices per question, no multi-select. Otherwise ask concise plain-text questions.
- Installed reference root: `../ccgs-references/references`. In this repo, the same files are mirrored under `codex-adapter/references/`.
- Role references are not native Codex agents. Simulate the named role locally using `../ccgs-references/references/agents/`; use Codex subagents only when the user explicitly asks for parallel agent work. Load matching memory from `../ccgs-references/references/agent-memory/` when it exists.
- Hook scripts and statusline settings from `references/hook-config.json` are reference checks. Treat them as reference checks unless you install separate Codex automation around them.

When this skill writes project artifacts, keep the original CCGS directory conventions (`design/`, `docs/`, `production/`, `src/`, `tests/`, `prototypes/`) unless the target project already has a stronger convention.

---

## Phase 1: Parse Arguments

- `version`: the release version to generate notes for (e.g., `1.2.0`)
- `--style`: output style — `brief` (bullet points), `detailed` (with context), `full` (with developer commentary). Default: `detailed`.

If no version is provided, ask the user before proceeding.

---

## Phase 2: Gather Change Data

- Read the internal changelog at `production/releases/[version]/changelog.md` if it exists
- Also check `docs/CHANGELOG.md` for the relevant version entry
- Run `git log` between the previous release tag and current tag/HEAD as a fallback
- Read sprint retrospectives in `production/sprints/` for context
- Read any balance change documents in `design/balance/`
- Read bug fix records from QA if available

**If no changelog data is available** (neither `production/releases/[version]/changelog.md`
nor a `docs/CHANGELOG.md` entry for this version exists, and git log is empty or unavailable):

> "No changelog data found for [version]. Run `$ccgs-changelog [version]` first to generate the
> internal changelog, then re-run `$ccgs-patch-notes [version]`."

Verdict: **BLOCKED** — stop here without generating notes.

---

## Phase 2b: Detect Tone Guide and Template

**Tone guide detection** — before drafting notes, check for writing style guidance:

1. Check `../ccgs-references/references/docs/technical-preferences.md` for any "tone", "voice", or "style"
   fields or sections.
2. Check `docs/PATCH-NOTES-STYLE.md` if it exists.
3. Check `design/community/tone-guide.md` if it exists.
4. If any source contains tone/voice/style instructions, extract them and apply
   them to the language and framing of the generated notes.
5. If no tone guidance is found anywhere, default to:
   player-friendly, non-technical language; enthusiastic but not hyperbolic;
   focus on what the player experiences, not what the developer changed.

**Template detection** — check whether a patch notes template exists:

1. Glob for `docs/patch-notes-template.md` and `../ccgs-references/references/docs/templates/patch-notes-template.md`.
2. If found at either location, read it and use it as the output structure for Phase 4
   instead of the built-in style templates (Brief / Detailed / Full). Fill in the
   template's sections with the categorized data.
3. If not found, use the built-in style templates as defined in Phase 4.

---

## Phase 3: Categorize and Translate

Categorize all changes into player-facing categories:

- **New Content**: new features, maps, characters, items, modes
- **Gameplay Changes**: balance adjustments, mechanic changes, progression changes
- **Quality of Life**: UI improvements, convenience features, accessibility
- **Bug Fixes**: grouped by system (combat, UI, networking, etc.)
- **Performance**: optimization improvements players might notice
- **Known Issues**: transparency about unresolved problems

Translate developer language to player language:

- "Refactored damage calculation pipeline" → "Improved hit detection accuracy"
- "Fixed null reference in inventory manager" → "Fixed a crash when opening inventory"
- "Reduced GC allocations in combat loop" → "Improved combat performance"
- Remove purely internal changes that don't affect players
- Preserve specific numbers for balance changes (damage: 50 → 45)

---

## Phase 4: Generate Patch Notes

### Brief Style
```markdown
# Patch [Version] — [Title]

**New**
- [Feature 1]
- [Feature 2]

**Changes**
- [Balance/mechanic change with before → after values]

**Fixes**
- [Bug fix 1]
- [Bug fix 2]

**Known Issues**
- [Issue 1]
```

### Detailed Style
```markdown
# Patch [Version] — [Title]
*[Date]*

## Highlights
[1-2 sentence summary of the most exciting changes]

## New Content
### [Feature Name]
[2-3 sentences describing the feature and why players should be excited]

## Gameplay Changes
### Balance
| Change | Before | After | Reason |
| ---- | ---- | ---- | ---- |
| [Item/ability] | [old value] | [new value] | [brief rationale] |

### Mechanics
- **[Change]**: [explanation of what changed and why]

## Quality of Life
- [Improvement with context]

## Bug Fixes
### Combat
- Fixed [description of what players experienced]

### UI
- Fixed [description]

### Networking
- Fixed [description]

## Performance
- [Improvement players will notice]

## Known Issues
- [Issue and workaround if available]
```

### Full Style
Includes everything from Detailed, plus:
```markdown
## Developer Commentary
### [Topic]
> [Developer insight into a major change — why it was made, what was considered,
> what the team learned. Written in first-person team voice.]
```

---

## Phase 5: Review Output

Check the generated notes for:

- No internal jargon (replace technical terms with player-friendly language)
- No references to internal systems, tickets, or sprint numbers
- Balance changes include before/after values
- Bug fixes describe the player experience, not the technical cause
- Tone matches the game's voice (adjust formality based on game style)

---

## Phase 6: Save Patch Notes

Present the completed patch notes to the user along with: a count of changes by category, and any internal changes that were excluded (for review).

Ask: "May I write these patch notes to `docs/patch-notes/[version].md`?"

If yes, write the file to `docs/patch-notes/[version].md`, creating the directory
if needed. Also write to `production/releases/[version]/patch-notes.md` as the
internal archive copy.

---

## Phase 7: Next Steps

Verdict: **COMPLETE** — patch notes generated and saved.

- Run `$ccgs-release-checklist` to verify all other release gates are met before publishing.
- Share the patch notes draft with the community-manager for tone review before posting publicly.
