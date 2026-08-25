from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from scripts import check_links

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
        assert "CATALOG:COVERAGE:START" in text
        assert "views/by-domain.md" in text
        assert "views/by-conference.md" in text
        assert len(text.splitlines()) < 100


def test_every_paper_has_filterable_domain_and_conference() -> None:
    catalog = yaml.safe_load((ROOT / "data" / "papers.yaml").read_text(encoding="utf-8"))
    papers = catalog["papers"]

    assert len(papers) > 0
    assert sum(paper["year"] == 2026 for paper in papers) == len(papers)
    assert all(paper["conference"] for paper in papers)
    assert all(paper["domains"] for paper in papers)
    assert all(paper["source_type"] != "arxiv" for paper in papers)
    assert all("arxiv.org" not in paper["paper_url"] for paper in papers)
    assert all(
        product["product"] in {"claude-code", "codex-cli"}
        for paper in papers
        for product in paper["products"]
    )
    assert all(paper["classification"] in {"direct", "related", "evaluation"} for paper in papers)


def test_link_scan_excludes_dependencies_and_build_outputs(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "README.md").write_text("# Project\n", encoding="utf-8")
    for directory in ("node_modules", "dist", ".next", ".wrangler"):
        path = tmp_path / directory
        path.mkdir()
        (path / "README.md").write_text("[missing](missing.md)\n", encoding="utf-8")

    monkeypatch.setattr(check_links, "ROOT", tmp_path)

    assert check_links.markdown_files() == [tmp_path / "README.md"]
