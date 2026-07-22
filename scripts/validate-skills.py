#!/usr/bin/env python3
"""
Validate SKILL.md files in the repository.

Checks:
  1. YAML frontmatter is valid and contains required fields
  2. All referenced files (references:) exist on disk
  3. SKILL.md body is non-empty
  4. Tags follow naming conventions

Exit code: 0 = all good, 1 = errors found.
"""

import os
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FIELDS = ["name", "description", "version", "tags"]
SKILL_DIRS = ["skills/godot-agentic", "skills/godot-marl-dev"]


def validate_skill(skill_dir: Path) -> list[str]:
    """Validate a single SKILL.md. Returns list of error messages."""
    errors = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return [f"SKILL.md not found in {skill_dir}"]

    content = skill_md.read_text(encoding="utf-8")

    # Parse frontmatter
    if not content.startswith("---\n"):
        errors.append(f"{skill_md}: missing YAML frontmatter (must start with ---)")
        return errors

    try:
        end = content.index("\n---\n", 4)
        frontmatter_text = content[4:end]
        meta = yaml.safe_load(frontmatter_text)
    except ValueError:
        errors.append(f"{skill_md}: malformed frontmatter (no closing ---)")
        return errors
    except yaml.YAMLError as e:
        errors.append(f"{skill_md}: YAML parse error: {e}")
        return errors

    if not isinstance(meta, dict):
        errors.append(f"{skill_md}: frontmatter is not a mapping")
        return errors

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in meta:
            errors.append(f"{skill_md}: missing required field '{field}'")

    # Validate name
    name = meta.get("name", "")
    if " " in name:
        errors.append(f"{skill_md}: name contains spaces: '{name}'")
    if not name.replace("-", "").replace("_", "").isalnum():
        errors.append(f"{skill_md}: name has invalid characters: '{name}'")

    # Validate version (semver)
    version = str(meta.get("version", ""))
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        errors.append(f"{skill_md}: version not semver: '{version}'")

    # Validate description
    desc = meta.get("description", "")
    if not desc or len(desc) < 10:
        errors.append(f"{skill_md}: description too short ({len(desc)} chars)")

    # Validate tags (lowercase, no spaces)
    tags = meta.get("tags", [])
    if not isinstance(tags, list):
        errors.append(f"{skill_md}: tags must be a list")
    else:
        for tag in tags:
            if " " in tag:
                errors.append(f"{skill_md}: tag contains space: '{tag}'")

    # Check referenced files exist
    refs = meta.get("references", [])
    if isinstance(refs, list):
        for ref in refs:
            ref_path = skill_dir / ref
            if not ref_path.exists():
                errors.append(f"{skill_md}: reference not found: '{ref}'")

    # Check body is non-empty
    body_start = content.find("\n---\n", 4) + 5
    body = content[body_start:].strip()
    if not body:
        errors.append(f"{skill_md}: body is empty")

    return errors


def main() -> int:
    all_errors = []

    for rel_dir in SKILL_DIRS:
        skill_dir = REPO_ROOT / rel_dir
        if not skill_dir.exists():
            all_errors.append(f"Skill directory not found: {skill_dir}")
            continue
        errors = validate_skill(skill_dir)
        all_errors.extend(errors)

    if not all_errors:
        print("All skills validated successfully")
        return 0

    print(f"{len(all_errors)} validation error(s):", file=sys.stderr)
    for err in all_errors:
        print(f"  - {err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
