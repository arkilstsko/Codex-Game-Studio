# Codex Notes for Codex Game Studio

This repo contains a Codex-oriented game studio workflow. Use the generated
skills from `codex-adapter/skills/` or the locally installed `$ccgs-*` skills.

## Command Mapping

- start workflow -> `$ccgs-start`
- brainstorm workflow -> `$ccgs-brainstorm`
- setup engine workflow -> `$ccgs-setup-engine`
- development story workflow -> `$ccgs-dev-story`
- story completion workflow -> `$ccgs-story-done`
- code review workflow -> `$ccgs-code-review`

All workflow skills use the same rule: prefix the workflow name with `$ccgs-`.

## Tool Mapping

- Codex `Read`, `Glob`, `Grep` -> Codex shell reads with `sed`, `find`, and `rg`
- Codex `Write`, `Edit` -> Codex `apply_patch`
- Codex `Bash` -> Codex `exec_command`
- Structured questions -> Codex `request_user_input` when available, otherwise concise chat questions
- Role passes -> simulate the named role locally from `codex-adapter/references/agents/`, unless the user explicitly asks for parallel/subagent work

## Hooks

The `codex-studio/hooks/` scripts are reference checks in Codex. They are not
automatically registered as Codex hooks by this adapter.

## References

Use these only when a workflow needs the detail:

- `codex-adapter/references/agents/`
- `codex-adapter/references/docs/`
- `codex-adapter/references/rules/`
- `codex-adapter/references/hooks/`
