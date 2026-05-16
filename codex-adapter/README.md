# Codex Adapter for Codex Game Studio

This adapter converts the original `codex-studio/skills/*/SKILL.md` workflows into
Codex skills named `ccgs-*`.

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

Original Codex slash commands map to Codex skills:

```text
/start         -> $ccgs-start
/brainstorm    -> $ccgs-brainstorm
/dev-story     -> $ccgs-dev-story
/story-done    -> $ccgs-story-done
```

Each generated skill includes a Codex adapter note that maps Codex tools
to Codex tools and explains how to handle CCGS agents as role references.
