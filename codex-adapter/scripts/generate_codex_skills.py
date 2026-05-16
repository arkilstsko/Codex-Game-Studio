#!/usr/bin/env python3
"""Generate Codex Game Studio skills from the source workflow skills."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDIO_ROOT = ROOT / "codex-studio"
SOURCE_SKILLS = STUDIO_ROOT / "skills"
OUT_ROOT = ROOT / "codex-adapter"
OUT_SKILLS = OUT_ROOT / "skills"


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SLASH_REF_RE = re.compile(r"(?<!https:)`/([a-z0-9][a-z0-9-]*)`")
SLASH_TEXT_RE = re.compile(r"(?<![A-Za-z0-9_.~)-])/([a-z0-9][a-z0-9-]*)\b(?![A-Za-z0-9_.~/-])")
INSTALLED_REFERENCE_ROOT = "../ccgs-references/references"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip().strip('"').strip("'")
        data[key.strip()] = value
    return data, text[match.end() :]


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def rewrite_skill_refs(body: str, skill_names: set[str]) -> str:
    def repl_code(match: re.Match[str]) -> str:
        name = match.group(1)
        return f"`$ccgs-{name}`" if name in skill_names else match.group(0)

    def repl_text(match: re.Match[str]) -> str:
        name = match.group(1)
        return f"$ccgs-{name}" if name in skill_names else match.group(0)

    body = SLASH_REF_RE.sub(repl_code, body)
    body = SLASH_TEXT_RE.sub(repl_text, body)
    body = body.replace("codex-studio/settings.json", "codex-studio/hook-config.json")
    body = rewrite_reference_paths(body)
    body = rewrite_task_language(body)
    return body


def rewrite_reference_paths(body: str) -> str:
    replacements = {
        "codex-studio/docs/": f"{INSTALLED_REFERENCE_ROOT}/docs/",
        "codex-studio/agents/": f"{INSTALLED_REFERENCE_ROOT}/agents/",
        "codex-studio/rules/": f"{INSTALLED_REFERENCE_ROOT}/rules/",
        "codex-studio/hooks/": f"{INSTALLED_REFERENCE_ROOT}/hooks/",
        "codex-studio/skills/": f"{INSTALLED_REFERENCE_ROOT}/source-skills/",
        "codex-studio/skill-testing-framework/": f"{INSTALLED_REFERENCE_ROOT}/skill-testing-framework/",
        "codex-studio/agent-memory/": f"{INSTALLED_REFERENCE_ROOT}/agent-memory/",
        "codex-studio/hook-config.json": f"{INSTALLED_REFERENCE_ROOT}/hook-config.json",
        "codex-studio/statusline.sh": f"{INSTALLED_REFERENCE_ROOT}/statusline.sh",
        "Codex Skill Testing Framework/": f"{INSTALLED_REFERENCE_ROOT}/skill-testing-framework/",
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
    return body


def rewrite_task_language(body: str) -> str:
    body = re.sub(
        r"Use the Task tool to spawn each team member as a subagent:",
        "For each listed role, load the role reference and perform that role pass in the current Codex thread. Use Codex subagents only when the user explicitly asks for parallel agent work:",
        body,
    )
    body = re.sub(
        r"Use the Task tool to request sign-off in parallel:",
        "Load each listed role reference and perform the sign-off passes. Use Codex subagents only when explicitly available and requested:",
        body,
    )
    body = re.sub(
        r"Spawn `([^`]+)` via Task",
        r"Load the `\1` role reference and perform that role pass",
        body,
    )
    body = re.sub(
        r"spawn `([^`]+)` via Task",
        r"load the `\1` role reference and perform that role pass",
        body,
    )
    body = body.replace("via Task", "using the role-reference workflow")
    body = body.replace("Task tool", "Codex role-reference workflow")
    body = body.replace("actual role-reference passes", "role-reference passes")
    body = body.replace("Task calls", "role-reference passes")
    body = body.replace("Task call", "role-reference pass")
    body = body.replace("Task agents", "role-reference passes")
    body = body.replace("Task agent", "role-reference pass")
    body = body.replace("Task prompt", "role-reference prompt")
    body = body.replace("Task subagent", "role-reference pass")
    body = body.replace("SUBAGENT", "ROLE PASS")
    body = body.replace("separate independent Codex session", "focused role-reference pass in the current Codex thread")
    body = body.replace("spawning parallel Task agents", "running role-reference passes")
    body = body.replace("subagent_type:", "role:")
    body = body.replace("sub-agent", "role pass")
    body = body.replace("sub-agents", "role passes")
    body = body.replace("subagent", "role pass")
    body = body.replace("subagents", "role passes")
    body = body.replace("The orchestrator does NOT call Write directly", "Perform approved file writes in the current Codex thread")
    body = body.replace("writes are delegated to role passes", "writes are performed in the current Codex thread after approval")
    body = body.replace("multiple-choice: true", "single-choice: true")
    body = body.replace("multiSelect: true", "singleChoice: true")
    body = body.replace("multiSelect", "single-choice")
    body = body.replace("multi-tab", "multi-step")
    body = body.replace("with two tabs", "with two choices")
    body = re.sub(r"[Bb]atch up to 4", "Batch up to 3", body)
    body = body.replace("groups of 3-4", "groups of up to 3")
    return body


def rewrite_installed_reference_text(root: Path) -> None:
    suffixes = {".md", ".yaml", ".yml", ".json", ".sh", ".txt"}
    replacements = {
        "codex-studio/docs/": f"{INSTALLED_REFERENCE_ROOT}/docs/",
        "codex-studio/agents/": f"{INSTALLED_REFERENCE_ROOT}/agents/",
        "codex-studio/rules/": f"{INSTALLED_REFERENCE_ROOT}/rules/",
        "codex-studio/hooks/": f"{INSTALLED_REFERENCE_ROOT}/hooks/",
        "codex-studio/skills/": f"{INSTALLED_REFERENCE_ROOT}/source-skills/",
        "codex-studio/skill-testing-framework/": f"{INSTALLED_REFERENCE_ROOT}/skill-testing-framework/",
        "codex-studio/agent-memory/": f"{INSTALLED_REFERENCE_ROOT}/agent-memory/",
        "codex-studio/hook-config.json": f"{INSTALLED_REFERENCE_ROOT}/hook-config.json",
        "codex-studio/statusline.sh": f"{INSTALLED_REFERENCE_ROOT}/statusline.sh",
        "Codex Skill Testing Framework/": f"{INSTALLED_REFERENCE_ROOT}/skill-testing-framework/",
    }
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rewritten = text
        for old, new in replacements.items():
            rewritten = rewritten.replace(old, new)
        if rewritten != text:
            path.write_text(rewritten, encoding="utf-8")


def codex_prelude(source_name: str) -> str:
    return f"""## Codex Adapter

This is the Codex Game Studio workflow skill `{source_name}`.

Use the workflow below with these Codex mappings:

- Slash-command references are mapped to Codex skill invocations with the `ccgs-` prefix.
- `Read`, `Glob`, and `Grep` mean inspect files with `sed`, `find`, and `rg`.
- `Write` and `Edit` mean make file changes with `apply_patch`.
- `Bash` means use `exec_command`.
- `Web search` and `Web fetch` mean use Codex web/browser tools when available; prefer official engine documentation for engine lookups. If web tools are unavailable, ask the user for the source URL or state the limitation.
- `request_user_input` means use Codex's structured input tool when available: at most 3 questions, 2-3 choices per question, no multi-select. Otherwise ask concise plain-text questions.
- Installed reference root: `{INSTALLED_REFERENCE_ROOT}`. In this repo, the same files are mirrored under `codex-adapter/references/`.
- Role references are not native Codex agents. Simulate the named role locally using `{INSTALLED_REFERENCE_ROOT}/agents/`; use Codex subagents only when the user explicitly asks for parallel agent work. Load matching memory from `{INSTALLED_REFERENCE_ROOT}/agent-memory/` when it exists.
- Hook scripts and statusline settings from `references/hook-config.json` are reference checks. Treat them as reference checks unless you install separate Codex automation around them.

When this skill writes project artifacts, keep the original CCGS directory conventions (`design/`, `docs/`, `production/`, `src/`, `tests/`, `prototypes/`) unless the target project already has a stronger convention.

---

"""


def generate() -> None:
    skill_paths = sorted(SOURCE_SKILLS.glob("*/SKILL.md"))
    skill_names = {path.parent.name for path in skill_paths}

    if OUT_SKILLS.exists():
        shutil.rmtree(OUT_SKILLS)
    OUT_SKILLS.mkdir(parents=True)

    for source in skill_paths:
        source_name = source.parent.name
        raw = source.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)

        codex_name = f"ccgs-{source_name}"
        description = meta.get("description", f"Run the CCGS {source_name} workflow.")
        description = (
            f"Codex Game Studio workflow `/{source_name}`. "
            f"Use when the user asks for CCGS game-studio workflow `{codex_name}` or the original `/{source_name}` command. "
            f"{description}"
        )

        rewritten = rewrite_skill_refs(body, skill_names)
        output = (
            "---\n"
            f"name: {codex_name}\n"
            f"description: {yaml_quote(description)}\n"
            "---\n\n"
            + codex_prelude(source_name)
            + rewritten.lstrip()
        )

        target_dir = OUT_SKILLS / codex_name
        target_dir.mkdir()
        (target_dir / "SKILL.md").write_text(output, encoding="utf-8")

    references = OUT_ROOT / "references"
    if references.exists():
        shutil.rmtree(references)
    references.mkdir(parents=True)
    for name in ("agents", "docs", "rules", "hooks", "agent-memory"):
        src = STUDIO_ROOT / name
        if src.exists():
            shutil.copytree(src, references / name)

    source_skills = STUDIO_ROOT / "skills"
    if source_skills.exists():
        shutil.copytree(source_skills, references / "source-skills")

    testing_framework = STUDIO_ROOT / "skill-testing-framework"
    if testing_framework.exists():
        shutil.copytree(testing_framework, references / "skill-testing-framework")

    for name in ("hook-config.json", "statusline.sh"):
        src = STUDIO_ROOT / name
        if src.exists():
            shutil.copy2(src, references / name)

    engine_reference = ROOT / "docs" / "engine-reference"
    if engine_reference.exists():
        target = references / "docs" / "engine-reference"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(engine_reference, target)

    support = OUT_SKILLS / "ccgs-references"
    support.mkdir(exist_ok=True)
    (support / "SKILL.md").write_text(
        "---\n"
        "name: ccgs-references\n"
        'description: "Reference bundle for Codex Game Studio agents, docs, rules, hooks, memory, source skills, test specs, and engine references. Use when a CCGS skill needs role or rule context."\n'
        "---\n\n"
        "# CCGS References\n\n"
        "This support skill exists so local Codex installs can carry the original CCGS reference files.\n\n"
        "Load files from `references/agents/`, `references/agent-memory/`, `references/docs/`, `references/source-skills/`, `references/skill-testing-framework/`, `references/rules/`, `references/hooks/`, `references/hook-config.json`, or `references/statusline.sh` only when a workflow explicitly needs that detail.\n",
        encoding="utf-8",
    )
    shutil.copytree(references, support / "references")
    rewrite_installed_reference_text(support / "references")

    print(f"Generated {len(skill_paths)} workflow skills plus ccgs-references in {OUT_SKILLS}")


if __name__ == "__main__":
    generate()
