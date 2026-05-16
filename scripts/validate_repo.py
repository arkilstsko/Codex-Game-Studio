#!/usr/bin/env python3
"""Repository sanity checks for Codex Game Studio."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_UPSTREAM_REFERENCES = {
    ROOT / "README.md",
    ROOT / "NOTICE",
}
EXPECTED_COUNTS = {
    "source_skills": 73,
    "generated_skills": 74,
    "agents": 49,
    "hooks": 12,
    "rules": 11,
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def text_files() -> list[Path]:
    suffixes = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix in suffixes or path.name in {"CODEOWNERS", "LICENSE", "NOTICE"}:
            files.append(path)
    return files


def count(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def check_counts(errors: list[str]) -> None:
    actual = {
        "source_skills": count("codex-studio/skills/*/SKILL.md"),
        "generated_skills": count("codex-adapter/skills/*/SKILL.md"),
        "agents": count("codex-studio/agents/*.md"),
        "hooks": count("codex-studio/hooks/*"),
        "rules": count("codex-studio/rules/*"),
    }
    for key, expected in EXPECTED_COUNTS.items():
        if actual[key] != expected:
            errors.append(f"{key}: expected {expected}, got {actual[key]}")


def check_generated_frontmatter(errors: list[str]) -> None:
    for path in ROOT.glob("codex-adapter/skills/*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append(f"{rel(path)} missing valid frontmatter")


def check_references(errors: list[str]) -> None:
    required = [
        "codex-adapter/skills/ccgs-start/SKILL.md",
        "codex-adapter/skills/ccgs-dev-story/SKILL.md",
        "codex-adapter/skills/ccgs-references/references/agents/lead-programmer.md",
        "codex-adapter/skills/ccgs-references/references/agent-memory/lead-programmer/MEMORY.md",
        "codex-adapter/skills/ccgs-references/references/source-skills/dev-story/SKILL.md",
        "codex-adapter/skills/ccgs-references/references/skill-testing-framework/catalog.yaml",
        "codex-adapter/skills/ccgs-references/references/docs/engine-reference/godot/VERSION.md",
        "codex-adapter/skills/ccgs-references/references/hook-config.json",
        "codex-adapter/skills/ccgs-references/references/statusline.sh",
        "codex-studio/hook-config.json",
        "codex-studio/docs/AGENTS-local-template.md",
    ]
    for item in required:
        if not (ROOT / item).exists():
            errors.append(f"missing required file: {item}")


def check_stale_text(errors: list[str]) -> None:
    stale_patterns = [
        re.compile(r"\." + "claude" + r"\b"),
        re.compile(r"\b" + "CLAUDE" + r"\.md\b"),
        re.compile(r"Donchitos/" + "Codex-Code-Game-Studios"),
        re.compile(r"claude" + r" --version"),
        re.compile(r"@anthropic-ai/" + "claude" + r"-code"),
        re.compile(r"YOUR" + r"-ORG"),
        re.compile(r"production\$ccgs-"),
        re.compile(r"design/[A-Za-z0-9_-]*\$ccgs-"),
        re.compile(r"tests\$ccgs-"),
    ]
    for path in text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in stale_patterns:
            if pattern.search(text):
                errors.append(f"{rel(path)} contains stale text matching {pattern.pattern}")

        if "Claude" in text and path not in ALLOWED_UPSTREAM_REFERENCES and path != Path(__file__).resolve():
            errors.append(f"{rel(path)} contains upstream product reference outside attribution files")


def check_generated_runtime_text(errors: list[str]) -> None:
    task_blockers = [
        "MUST issue actual Task calls",
        "Do NOT simulate",
        "subagent_type:",
        "Task tool",
        "multiSelect",
        "multi-tab",
        "Batch up to 4",
        "batch up to 4",
        "groups of 3-4",
    ]
    for path in ROOT.glob("codex-adapter/skills/ccgs-*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        for blocker in task_blockers:
            if blocker in text:
                errors.append(f"{rel(path)} contains non-Codex Task blocker: {blocker}")
        source_refs = [
            "codex-studio/docs/",
            "codex-studio/agents/",
            "codex-studio/skills/",
            "codex-studio/skill-testing-framework/",
            "Codex Skill Testing Framework/",
        ]
        if any(ref in text for ref in source_refs):
            errors.append(f"{rel(path)} contains source-tree reference instead of installed reference root")

    support_root = ROOT / "codex-adapter/skills/ccgs-references/references"
    for path in support_root.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(ref in text for ref in source_refs):
            errors.append(f"{rel(path)} contains source-tree reference inside install bundle")


def main() -> int:
    errors: list[str] = []
    check_counts(errors)
    check_generated_frontmatter(errors)
    check_references(errors)
    check_stale_text(errors)
    check_generated_runtime_text(errors)

    if errors:
        print("Repo validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repo validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
