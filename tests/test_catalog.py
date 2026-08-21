from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

from scripts.discover_candidates import parse_feed

ROOT = Path(__file__).resolve().parents[1]


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_catalog_is_valid() -> None:
    result = run_script("validate.py")
    assert result.returncode == 0, result.stderr


def test_generated_readme_is_current() -> None:
    result = run_script("build_readme.py", "--check")
    assert result.returncode == 0, result.stderr


def test_arxiv_feed_parser_strips_version_and_normalizes_text() -> None:
    feed = ElementTree.fromstring(
        """<feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
          <id>https://arxiv.org/abs/2608.12345v2</id>
          <title>A  Product-Level\n  Study</title>
          <summary>Tests   Claude Code.</summary>
          <published>2026-08-20T00:00:00Z</published>
          <author><name>Ada Researcher</name></author>
        </entry>
        </feed>"""
    )
    parsed = parse_feed(ElementTree.tostring(feed))
    assert parsed == [
        {
            "arxiv_id": "2608.12345",
            "title": "A Product-Level Study",
            "summary": "Tests Claude Code.",
            "authors": ["Ada Researcher"],
            "published": "2026-08-20T00:00:00Z",
            "url": "https://arxiv.org/abs/2608.12345",
        }
    ]
