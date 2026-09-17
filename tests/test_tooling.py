from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path
from urllib.parse import unquote

from scripts.lint_design_doc import lint_markdown
from scripts.package_skill import build_package
from scripts.validate_skill import parse_frontmatter, validate

ROOT = Path(__file__).resolve().parents[1]


class SkillValidationTests(unittest.TestCase):
    def test_repository_is_valid(self) -> None:
        self.assertEqual([], validate(ROOT))

    def test_frontmatter_metadata_is_parsed(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)["metadata"]
        self.assertEqual("1.0.0", metadata["version"])
        self.assertEqual("Scorpio69t", metadata["author"])

    def test_relative_markdown_links_exist(self) -> None:
        import re

        link_pattern = re.compile(r"\[[^]]*\]\(([^)]+)\)")
        missing: list[str] = []
        for document in ROOT.rglob("*.md"):
            if any(part in {".git", "dist", "__pycache__"} for part in document.parts):
                continue
            text = document.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(text):
                target = raw_target.split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (document.parent / unquote(target)).resolve()
                if not resolved.exists():
                    missing.append(f"{document.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual([], missing)


class DocumentLinterTests(unittest.TestCase):
    def test_example_has_no_findings(self) -> None:
        findings = lint_markdown(ROOT / "examples" / "sample-detailed-design.md")
        self.assertEqual([], findings)

    def test_agent_like_phrase_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            document = Path(tmp) / "design.md"
            document.write_text("# Design\n\nThe agent should now continue.\n", encoding="utf-8")
            codes = {finding.code for finding in lint_markdown(document)}
        self.assertIn("AI001", codes)


class PackagingTests(unittest.TestCase):
    def test_archive_is_installable_and_excludes_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive, checksum = build_package(ROOT, Path(tmp))
            self.assertTrue(checksum.is_file())
            with zipfile.ZipFile(archive) as bundle:
                names = set(bundle.namelist())
            self.assertIn("technical-design-doc/SKILL.md", names)
            self.assertIn("technical-design-doc/references/quality-gate.md", names)
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in names))
            self.assertFalse(any(name.startswith("technical-design-doc/.github/") for name in names))


if __name__ == "__main__":
    unittest.main()
