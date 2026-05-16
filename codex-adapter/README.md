# Codex Adapter for Codex Game Studio

This adapter converts `codex-studio/skills/*/SKILL.md` workflows into installable
Codex skills named `ccgs-*`.

The generated skills include Codex-specific compatibility notes, relative
reference paths, and rewritten role workflow language so they can run from both
`~/.codex/skills` and temporary install targets.

## Generate

From the repo root:

```bash
python3 codex-adapter/scripts/generate_codex_skills.py
```

Generated skills are written to:

```text
codex-adapter/skills/
```

The adapter also copies the original CCGS agents, docs, rules, and hooks into
`codex-adapter/references/` and into the installable support skill:

```text
codex-adapter/skills/ccgs-references/references/
```

## Install Locally

```bash
python3 codex-adapter/scripts/install_codex_skills.py --replace
```

This copies the generated skills into `~/.codex/skills`, including
`ccgs-references`. Restart Codex or start a new thread for the generated skills
to appear in the available skill list.

Use `--dry-run` to preview changes, or `--target <dir>` to test installation in
a temporary directory.

## Invocation

Original slash commands map to Codex skills:

```text
/start         -> $ccgs-start
/brainstorm    -> $ccgs-brainstorm
/dev-story     -> $ccgs-dev-story
/story-done    -> $ccgs-story-done
```

Each generated skill includes a Codex adapter note that maps legacy tool
concepts to Codex equivalents and explains how to handle CCGS agents as role
references.

## Validate

From the repo root:

```bash
python3 scripts/validate_repo.py
```

The validator checks expected counts, stale upstream tool assumptions, generated
reference paths, and a temporary self-contained install layout.
