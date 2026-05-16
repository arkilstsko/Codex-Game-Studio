#!/usr/bin/env python3
"""Install generated CCGS Codex skills."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ADAPTER_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ADAPTER_ROOT / "skills"
TARGET_SKILLS = Path.home() / ".codex" / "skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        type=Path,
        default=TARGET_SKILLS,
        help="Directory to install skills into. Defaults to ~/.codex/skills.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace existing generated ccgs-* skill directories.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not SOURCE_SKILLS.exists():
        raise SystemExit(
            "No generated skills found. Run codex-adapter/scripts/generate_codex_skills.py first."
        )

    target_root = args.target.expanduser()
    sources = [source for source in sorted(SOURCE_SKILLS.iterdir()) if source.is_dir()]

    print(f"Target: {target_root}")
    for source in sources:
        target = target_root / source.name
        action = "replace" if target.exists() else "install"
        print(f"- {action}: {source.name}")

    if args.dry_run:
        print("Dry run only; no files changed.")
        return

    existing = [source.name for source in sources if (target_root / source.name).exists()]
    if existing and not args.replace:
        names = ", ".join(existing[:8])
        more = "" if len(existing) <= 8 else f" and {len(existing) - 8} more"
        raise SystemExit(
            f"Refusing to replace existing skills without --replace: {names}{more}"
        )

    target_root.mkdir(parents=True, exist_ok=True)

    installed = 0
    for source in sources:
        target = target_root / source.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        installed += 1

    print(f"Installed {installed} CCGS Codex skills into {target_root}")
    print("Restart Codex or start a new thread for the generated skills to appear in the skill list.")


if __name__ == "__main__":
    main()
