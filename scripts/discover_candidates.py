#!/usr/bin/env python3
"""Find recent arXiv papers that mention Claude Code or Codex CLI."""

from __future__ import annotations

import argparse
import os
import re
import ssl
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree

import certifi
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def parse_feed(payload: bytes) -> list[dict[str, object]]:
    root = ElementTree.fromstring(payload)
    papers = []
    for entry in root.findall(f"{ATOM}entry"):
        identifier = entry.findtext(f"{ATOM}id", "").rsplit("/", 1)[-1]
        arxiv_id = re.sub(r"v\d+$", "", identifier)
        authors = [
            normalize_text(author.findtext(f"{ATOM}name", ""))
            for author in entry.findall(f"{ATOM}author")
        ]
        papers.append(
            {
                "arxiv_id": arxiv_id,
                "title": normalize_text(entry.findtext(f"{ATOM}title", "")),
                "summary": normalize_text(entry.findtext(f"{ATOM}summary", "")),
                "authors": authors,
                "published": entry.findtext(f"{ATOM}published", ""),
                "url": f"https://arxiv.org/abs/{arxiv_id}",
            }
        )
    return papers


def fetch_candidates(max_results: int) -> list[dict[str, object]]:
    query = 'all:"Claude Code" OR all:"Codex CLI"'
    parameters = urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    request = Request(
        f"{ARXIV_API}?{parameters}",
        headers={"User-Agent": "awesome-claude-code-codex-papers/0.1"},
    )
    tls_context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, timeout=30, context=tls_context) as response:
        return parse_feed(response.read())


def existing_arxiv_ids() -> set[str]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        catalog = yaml.safe_load(handle)
    return {paper["arxiv_id"] for paper in catalog["papers"] if paper.get("arxiv_id")}


def recent_untracked(
    papers: list[dict[str, object]], known: set[str], days: int
) -> list[dict[str, object]]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    selected = []
    for paper in papers:
        published = datetime.fromisoformat(str(paper["published"]).replace("Z", "+00:00"))
        if paper["arxiv_id"] not in known and published >= cutoff:
            selected.append(paper)
    return selected


def render_report(papers: list[dict[str, object]], days: int, total_candidates: int) -> str:
    header = (
        "# Weekly paper candidates\n\n"
        f"Automated arXiv discovery for exact mentions of `Claude Code` or `Codex CLI` "
        f"during the last {days} days. Candidates require manual product-level evidence review.\n\n"
        f"Showing the newest {len(papers)} of {total_candidates} untracked candidate(s).\n\n"
    )
    if not papers:
        return header + "No untracked candidates were found.\n"

    sections = []
    for paper in papers:
        authors = ", ".join(paper["authors"][:5])
        if len(paper["authors"]) > 5:
            authors += ", et al."
        published = str(paper["published"])[:10]
        summary = str(paper["summary"])
        if len(summary) > 500:
            summary = summary[:497].rstrip() + "..."
        sections.append(
            f"## [{paper['title']}]({paper['url']})\n\n"
            f"- arXiv: `{paper['arxiv_id']}`\n"
            f"- Published: {published}\n"
            f"- Authors: {authors}\n\n"
            f"{summary}\n\n"
            "Review checklist: product actually executed · evidence class · model/version · "
            "budget · result location · official artifact\n"
        )
    return header + "\n".join(sections)


def write_github_output(count: int) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        raise RuntimeError("GITHUB_OUTPUT is not set")
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write(f"count={count}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--max-results", type=int, default=100)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--output", type=Path, default=Path("candidate-report.md"))
    parser.add_argument("--github-output", action="store_true")
    args = parser.parse_args()

    candidates = recent_untracked(
        fetch_candidates(args.max_results), existing_arxiv_ids(), args.days
    )
    candidates.sort(key=lambda paper: str(paper["published"]), reverse=True)
    visible = candidates[: args.limit]
    args.output.write_text(render_report(visible, args.days, len(candidates)), encoding="utf-8")
    if args.github_output:
        write_github_output(len(candidates))
    print(
        f"Found {len(candidates)} untracked candidate(s); "
        f"wrote the newest {len(visible)} to {args.output}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
