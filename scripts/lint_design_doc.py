#!/usr/bin/env python3
"""Heuristic linter for AI-generated technical design Markdown.

This script intentionally produces review hints rather than pass/fail architecture
judgments. It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Finding:
    severity: str
    line: int
    code: str
    message: str


AI_PHRASES = {
    "AI001": [
        r"in order to achieve",
        r"based on the above",
        r"it should be noted that",
        r"according to the actual situation",
        r"provides? (?:a )?strong support",
        r"lays? (?:a )?solid foundation",
        r"can be further optimized",
        r"the agent should",
        r"you can consider",
        r"we can consider",
        r"next we (?:need|should|will)",
        r"基于(?:以上|上述)(?:内容|设计|分析)?",
        r"需要注意的是",
        r"在实际实施过程中",
        r"根据实际情况",
        r"可以进一步优化",
        r"(?:智能体|Agent)(?:需要|应该|将)",
        r"下一步(?:需要|应该|将)",
        r"可以考虑",
        r"提供[^\n，。]{0,20}有力支撑",
        r"奠定[^\n，。]{0,20}(?:坚实|扎实)基础",
    ],
    "AI002": [
        r"highly (?:available|scalable|reliable|efficient|flexible)",
        r"efficient, stable and reliable",
        r"unified, efficient",
        r"全面赋能",
        r"灵活扩展",
        r"统一、高效、稳定(?:、|和)可靠",
    ],
}

VAGUE_HEADINGS = {
    "design details",
    "technical implementation",
    "other considerations",
    "optimization",
    "others",
    "miscellaneous",
    "设计细节",
    "技术实现",
    "其他考虑",
    "优化",
    "其他",
    "其它",
    "杂项",
}


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def lint_ai_phrases(text: str) -> list[Finding]:
    out: list[Finding] = []
    for code, patterns in AI_PHRASES.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                out.append(
                    Finding(
                        "warning",
                        line_number(text, match.start()),
                        code,
                        f"agent-like or low-information phrase: {match.group(0)!r}",
                    )
                )
    return out


def lint_headings(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not m:
            continue
        title = re.sub(r"^\d+(?:\.\d+)*[.)]?\s*", "", m.group(1)).strip().lower()
        if title in VAGUE_HEADINGS:
            out.append(Finding("hint", i, "DOC001", f"vague heading: {m.group(1)!r}"))
    return out


def lint_bullet_walls(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    start = None
    count = 0
    for i, line in enumerate(lines + [""], 1):
        if re.match(r"^\s*(?:[-*+] |\d+[.)] )", line):
            if start is None:
                start = i
            count += 1
        elif not line.strip() and count:
            if count >= 8:
                out.append(
                    Finding(
                        "hint",
                        start or i,
                        "DOC002",
                        f"bullet wall contains {count} consecutive items; consider grouping, prose, or a table",
                    )
                )
            start = None
            count = 0
        elif count:
            # Wrapped bullet text is allowed; continue until blank or a new structural block.
            if re.match(r"^#{1,6}\s", line) or line.startswith("```"):
                if count >= 8:
                    out.append(
                        Finding("hint", start or i, "DOC002", f"bullet wall contains {count} consecutive items")
                    )
                start = None
                count = 0
    return out


def extract_fenced_blocks(lines: list[str]):
    in_block = False
    lang = ""
    start = 0
    body: list[str] = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^```\s*([A-Za-z0-9_-]*)", line)
        if m and not in_block:
            in_block = True
            lang = m.group(1).lower()
            start = i
            body = []
            continue
        if in_block and line.startswith("```"):
            yield lang, start, i, body
            in_block = False
            lang = ""
            body = []
            continue
        if in_block:
            body.append(line)


def lint_mermaid(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    blocks = list(extract_fenced_blocks(lines))
    for lang, start, end, body in blocks:
        if lang != "mermaid":
            continue
        text = "\n".join(body)
        # Approximate nodes via declarations/references. Deliberately conservative.
        ids = set()
        for match in re.finditer(r"(?m)(?:^|\s)([A-Za-z_][A-Za-z0-9_-]*)\s*(?:\[|\(|\{|\[\[)", text):
            ids.add(match.group(1))
        state_names = set(re.findall(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*-->", text))
        ids |= state_names
        if len(ids) > 18:
            out.append(
                Finding(
                    "warning",
                    start,
                    "DIA001",
                    f"Mermaid diagram appears dense ({len(ids)} primary identifiers); consider splitting the view",
                )
            )
        elif len(ids) > 12:
            out.append(
                Finding(
                    "hint",
                    start,
                    "DIA002",
                    f"Mermaid diagram has about {len(ids)} primary identifiers; verify readability",
                )
            )

        # Reading-guide heuristic: search a short range after the fence.
        after = "\n".join(lines[end : min(len(lines), end + 10)]).lower()
        if len(ids) >= 6 and not any(key in after for key in ["reading guide", "读图", "图解", "关键点"]):
            out.append(
                Finding(
                    "hint",
                    end,
                    "DIA003",
                    "non-trivial Mermaid diagram has no nearby reading-guide marker",
                )
            )
    return out


def lint_plantuml(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    blocks = list(extract_fenced_blocks(lines))
    for lang, start, end, body in blocks:
        if lang not in {"plantuml", "puml"}:
            continue
        text = "\n".join(body)
        participants = set(
            m.group(2) or m.group(1)
            for m in re.finditer(
                r"(?m)^\s*(?:actor|participant|database|queue|collections?|boundary|control|entity)\s+(?:\"([^\"]+)\"|([A-Za-z_][A-Za-z0-9_]*))",
                text,
            )
        )
        if len(participants) > 8:
            out.append(
                Finding(
                    "hint",
                    start,
                    "DIA004",
                    f"PlantUML sequence has {len(participants)} participants; consider splitting or abstracting low-level dependencies",
                )
            )
        if "->" in text and not re.search(r"\b(alt|group|loop|opt|break|critical)\b", text) and len(text.splitlines()) > 18:
            out.append(
                Finding(
                    "hint",
                    start,
                    "DIA005",
                    "long sequence contains no explicit alternative/grouping; verify that failure paths are represented",
                )
            )
        after = "\n".join(lines[end : min(len(lines), end + 10)]).lower()
        if len(participants) >= 5 and not any(key in after for key in ["reading guide", "读图", "图解", "关键点"]):
            out.append(Finding("hint", end, "DIA006", "non-trivial sequence has no nearby reading-guide marker"))
    return out


def lint_markdown(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    findings: list[Finding] = []
    findings += lint_ai_phrases(text)
    findings += lint_headings(lines)
    findings += lint_bullet_walls(lines)
    findings += lint_mermaid(lines)
    findings += lint_plantuml(lines)
    return sorted(findings, key=lambda f: (f.line, f.code))


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristic technical-design Markdown linter")
    parser.add_argument("file", type=Path)
    parser.add_argument("--strict", action="store_true", help="return non-zero when warnings are found")
    args = parser.parse_args()

    if not args.file.is_file():
        parser.error(f"not a file: {args.file}")

    findings = lint_markdown(args.file)
    if not findings:
        print("No heuristic findings.")
        return 0

    for f in findings:
        print(f"{args.file}:{f.line}: {f.severity} {f.code}: {f.message}")

    warnings = sum(f.severity == "warning" for f in findings)
    hints = sum(f.severity == "hint" for f in findings)
    print(f"\n{warnings} warning(s), {hints} hint(s). Review manually; this tool is intentionally heuristic.")
    return 1 if args.strict and warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
