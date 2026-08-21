#!/usr/bin/env python3
"""Fail when a relative Markdown or HTML link points to a missing local file."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r'(?:href|src)="([^"]+)"')
EXCLUDED_PARTS = {
    ".git",
    ".next",
    ".venv",
    ".vinext",
    ".wrangler",
    "coverage",
    "dist",
    "node_modules",
    "out",
}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def missing_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    targets = MARKDOWN_LINK.findall(text) + HTML_LINK.findall(text)
    missing = []
    for raw_target in targets:
        target = normalize_target(raw_target)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local_part = unquote(target.split("#", 1)[0])
        if not local_part:
            continue
        resolved = (path.parent / local_part).resolve()
        if not resolved.exists():
            missing.append(target)
    return missing


def main() -> int:
    files = markdown_files()
    failures = [(path, target) for path in files for target in missing_links(path)]
    if failures:
        print("Broken internal links:", file=sys.stderr)
        for path, target in failures:
            print(f"- {path.relative_to(ROOT)} -> {target}", file=sys.stderr)
        return 1
    print(f"Validated internal links across {len(files)} Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
