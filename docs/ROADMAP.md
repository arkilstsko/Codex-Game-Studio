# Roadmap

Codex Game Studio is currently focused on becoming a reliable Codex-first game
production framework rather than a simple port.

## Now

- Keep generated `$ccgs-*` skills self-contained and installable.
- Keep role references useful without assuming native subagent support.
- Maintain validation for stale upstream tool assumptions.
- Keep security, attribution, and release-readiness docs current.

## Next

- Add a small command index that groups skills by workflow phase and common
  user intent.
- Add example end-to-end project sessions for Godot, Unity, and Unreal.
- Add a smoke-test script that installs to a temp target and checks a shortlist
  of high-value skills for required references.
- Add a release note generator workflow around `production/releases/`.
- Expand `ccgs-help` so it can recommend the next skill from project files more
  precisely.

## Later

- Add optional Codex automation recipes for reference hooks.
- Add role memory for more leads than `lead-programmer`.
- Add engine-specific starter packs for common project layouts.
- Add CI that runs `scripts/validate_repo.py` on every pull request.
- Add a compatibility matrix for Codex app, Codex CLI, and local skill installs.

## Maintenance Principles

- Preserve upstream attribution and license history.
- Prefer Codex-native behavior over compatibility theater.
- Keep generated skills deterministic.
- Treat docs as product surface: commands shown in public docs should work.
- Keep user approval explicit before writes, branch changes, installs, or
  security-sensitive operations.
