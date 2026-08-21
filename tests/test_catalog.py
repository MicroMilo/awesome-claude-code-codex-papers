from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

from scripts import check_links
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


def test_readmes_are_concise_website_entry_points() -> None:
    website_url = "https://micromilo.github.io/awesome-claude-code-codex-papers/"
    for filename in ("README.md", "README.zh-CN.md"):
        text = (ROOT / filename).read_text(encoding="utf-8")
        assert website_url in text
        assert "CATALOG:DIRECT" not in text
        assert len(text.splitlines()) < 100


def test_link_scan_excludes_dependencies_and_build_outputs(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "README.md").write_text("# Project\n", encoding="utf-8")
    for directory in ("node_modules", "dist", ".next", ".wrangler"):
        path = tmp_path / directory
        path.mkdir()
        (path / "README.md").write_text("[missing](missing.md)\n", encoding="utf-8")

    monkeypatch.setattr(check_links, "ROOT", tmp_path)

    assert check_links.markdown_files() == [tmp_path / "README.md"]


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
