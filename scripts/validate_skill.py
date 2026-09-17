#!/usr/bin/env python3
"""Validate this Agent Skill's structure, metadata, and local references."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Optional

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE.txt",
    "VERSION",
    "agents/openai.yaml",
    "references/human-writing.md",
    "references/diagram-policy.md",
    "references/quality-gate.md",
    "assets/templates/detailed-design.md",
    "scripts/lint_design_doc.py",
    "scripts/package_skill.py",
]

REQUIRED_DIRS = ["agents", "assets", "examples", "references", "scripts"]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
LOCAL_REF_RE = re.compile(
    r"`((?:agents|assets|examples|references|scripts)/[A-Za-z0-9_./-]+)`"
)


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by this package without a dependency."""

    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")

    data: dict[str, Any] = {}
    current_mapping: Optional[dict[str, str]] = None
    for raw_line in text[4:end].splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[:1].isspace():
            if current_mapping is None or ":" not in raw_line:
                raise ValueError(f"unsupported frontmatter line: {raw_line!r}")
            key, value = raw_line.strip().split(":", 1)
            current_mapping[key.strip()] = _unquote(value)
            continue
        if ":" not in raw_line:
            raise ValueError(f"invalid frontmatter line: {raw_line!r}")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = _unquote(value)
            current_mapping = None
        else:
            current_mapping = {}
            data[key] = current_mapping
    return data


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            errors.append(f"missing required directory: {rel}")

    skill = root / "SKILL.md"
    meta: dict[str, Any] = {}
    skill_text = ""
    if skill.is_file():
        try:
            skill_text = skill.read_text(encoding="utf-8")
            meta = parse_frontmatter(skill_text)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(str(exc))

    name = meta.get("name", "")
    description = meta.get("description", "")
    compatibility = meta.get("compatibility", "")
    if not isinstance(name, str) or not name:
        errors.append("frontmatter.name is required")
    elif len(name) > 64 or not NAME_RE.fullmatch(name):
        errors.append("frontmatter.name must be <=64 chars and lowercase kebab-case")
    elif root.name != name:
        errors.append(f"directory name '{root.name}' does not match skill name '{name}'")
    if not isinstance(description, str) or not description:
        errors.append("frontmatter.description is required")
    elif len(description) > 1024:
        errors.append("frontmatter.description must be <=1024 chars")
    if compatibility and (not isinstance(compatibility, str) or len(compatibility) > 500):
        errors.append("frontmatter.compatibility must be a string of <=500 chars")

    version_file = root / "VERSION"
    if version_file.is_file():
        version = version_file.read_text(encoding="utf-8").strip()
        if not VERSION_RE.fullmatch(version):
            errors.append("VERSION must contain a semantic version such as 1.2.3")
        metadata = meta.get("metadata", {})
        metadata_version = metadata.get("version") if isinstance(metadata, dict) else None
        if metadata_version and metadata_version != version:
            errors.append(
                f"frontmatter metadata.version '{metadata_version}' does not match VERSION '{version}'"
            )

    for rel in sorted(set(LOCAL_REF_RE.findall(skill_text))):
        if not (root / rel).is_file():
            errors.append(f"SKILL.md references a missing local file: {rel}")

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        text = openai_yaml.read_text(encoding="utf-8")
        for field in ("interface:", "display_name:", "short_description:", "default_prompt:"):
            if field not in text:
                errors.append(f"agents/openai.yaml is missing {field.rstrip(':')}")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Skill validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
