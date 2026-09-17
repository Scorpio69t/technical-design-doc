#!/usr/bin/env python3
"""Build a deterministic, installable ZIP of the Agent Skill."""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path

INCLUDED_FILES = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE.txt",
    "VERSION",
    "CHANGELOG.md",
]
INCLUDED_DIRS = ["agents", "assets", "examples", "references", "scripts"]
EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def iter_package_files(root: Path):
    for rel in INCLUDED_FILES:
        path = root / rel
        if path.is_file():
            yield path
    for directory in INCLUDED_DIRS:
        base = root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if EXCLUDED_PARTS.intersection(path.parts) or path.suffix in EXCLUDED_SUFFIXES:
                continue
            yield path


def build_package(root: Path, output_dir: Path) -> tuple[Path, Path]:
    root = root.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        raise ValueError(f"invalid VERSION: {version!r}")

    archive = output_dir / f"technical-design-doc-{version}.zip"
    prefix = "technical-design-doc"
    files = sorted(set(iter_package_files(root)), key=lambda path: path.relative_to(root).as_posix())
    if not files:
        raise ValueError("no files selected for packaging")

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in files:
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{relative}", date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            bundle.writestr(info, path.read_bytes())

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(f"{archive.suffix}.sha256")
    with checksum.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"{digest}  {archive.name}\n")
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("dist"),
        help="directory for the ZIP and SHA-256 file (default: dist)",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    archive, checksum = build_package(root, args.output_dir.resolve())
    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
