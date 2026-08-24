#!/usr/bin/env python3
"""Build the auditable 2026 conference census from first-party pages.

The census is intentionally separate from ``data/papers.yaml``.  The main
catalog contains only reviewed, in-scope papers; this file contains every
record found in the official conference lists, including exclusions and
pending records.

The script can use HTML snapshots in ``tmp/census`` (the default for a
repeatable local run) or fetch the official pages with ``--fetch``.  It does
not use arXiv as a conference paper list.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "tmp" / "census"
OUTPUT_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"

FETCHED_AT = datetime.now(UTC).replace(microsecond=0).isoformat()

REGISTRY: list[dict[str, object]] = [
    {
        "conference": "ASE",
        "official_url": "https://conf.researchr.org/track/ase-2026/ase-2026-research-track",
        "list_url": "https://conf.researchr.org/track/ase-2026/ase-2026-research-track",
        "snapshot": "ase-2026.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["Research Papers"],
        "notes": "The conference is scheduled for October 12–16, 2026; the official accepted-paper list is available, but the final proceedings are not yet complete.",
    },
    {
        "conference": "FSE",
        "official_url": "https://conf.researchr.org/track/fse-2026/fse-2026-research-papers",
        "list_url": "https://conf.researchr.org/track/fse-2026/fse-2026-research-papers",
        "snapshot": "fse-2026-research.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["Research Papers"],
        "notes": "The official track page is the acceptance/program source; ACM PACMSE is recorded as the proceedings destination when a DOI is available.",
    },
    {
        "conference": "ISSTA",
        "official_url": "https://conf.researchr.org/track/issta-2026/issta-2026-research-papers",
        "list_url": "https://conf.researchr.org/track/issta-2026/issta-2026-research-papers",
        "snapshot": "issta-2026-research.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["Research papers"],
        "notes": "The official track page exposes the accepted-paper list; papers without a first-party full-text link remain pending.",
    },
    {
        "conference": "ICSE",
        "official_url": "https://conf.researchr.org/track/icse-2026/icse-2026-research-track",
        "list_url": "https://conf.researchr.org/track/icse-2026/icse-2026-research-track",
        "snapshot": "icse-2026-research.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["Research Track"],
        "notes": "The ICSE site lists the research, SEIP, NIER, industry challenge, journal-first, demonstration, and education tracks together; track labels are preserved per record.",
    },
    {
        "conference": "ICML",
        "official_url": "https://icml.cc/",
        "list_url": "https://icml.cc/Downloads/2026",
        "snapshot": "icml-2026.html",
        "parser": "virtual",
        "status": "official-list",
        "tracks": ["Main Conference posters"],
        "notes": "The official ICML downloads page exposes the 2026 poster list. An official PDF URL is not exposed by every poster record; no arXiv fallback is used.",
    },
    {
        "conference": "ICLR",
        "official_url": "https://iclr.cc/Downloads/2026",
        "list_url": "https://proceedings.iclr.cc/paper_files/paper/2026",
        "downloads_url": "https://iclr.cc/Downloads/2026",
        "snapshot": "iclr-2026-proceedings.html",
        "parser": "iclr-proceedings",
        "status": "official-proceedings",
        "tracks": ["Conference"],
        "notes": "The official Downloads page exposes 5,513 2026 events; the main-conference proceedings index is used for the 5,351-paper conference census, with per-paper PDF links as first-party sources.",
    },
    {
        "conference": "AAAI",
        "official_url": "https://aaai.org/proceeding/aaai-40-2026/",
        "list_url": "https://aaai.org/proceeding/aaai-40-2026/",
        "snapshot": "aaai-40-2026.html",
        "parser": "aaai-ojs",
        "status": "official-proceedings",
        "tracks": ["AAAI-26 technical and special tracks included in the official proceedings"],
        "notes": "The official AAAI proceedings landing page links 48 OJS issues; issue and track labels are retained.",
    },
    {
        "conference": "NeurIPS",
        "official_url": "https://neurips.cc/",
        "list_url": "https://openreview.net/group?id=NeurIPS.cc%2F2026%2FConference",
        "parser": "pending",
        "status": "pending",
        "tracks": ["Conference"],
        "notes": "The official OpenReview group exists, but an accepted-paper list/proceedings was not released at the audit time; no preprint list is substituted.",
    },
    # Additional CCF-A candidates are registered explicitly so that their
    # absence is visible rather than silently omitted from the scope.
    {
        "conference": "IJCAI",
        "official_url": "https://2026.ijcai.org/",
        "list_url": "https://2026.ijcai.org/",
        "parser": "pending",
        "status": "pending",
        "tracks": ["Conference"],
        "notes": "Registered for the CCF-A extension pass; a complete first-party 2026 proceedings list was not imported in this run.",
    },
    {
        "conference": "KDD",
        "official_url": "https://www.kdd.org/kdd2026/",
        "list_url": "https://www.kdd.org/kdd2026/",
        "parser": "pending",
        "status": "pending",
        "tracks": ["Conference"],
        "notes": "Registered for the CCF-A extension pass; the official proceedings list still needs a dedicated source adapter.",
    },
    {
        "conference": "PLDI",
        "official_url": "https://pldi26.sigplan.org/track/pldi-2026-papers",
        "list_url": "https://pldi26.sigplan.org/track/pldi-2026-papers",
        "snapshot": "pldi-2026-research.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["PLDI Research Papers"],
        "notes": "The official PLDI Research Papers page exposes the 2026 accepted-paper list and DOI links; track labels are preserved per record.",
    },
    {
        "conference": "POPL",
        "official_url": "https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers",
        "list_url": "https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers",
        "snapshot": "popl-2026-research.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["POPL"],
        "notes": "The official POPL Research Papers page exposes the complete accepted-paper list with DOI links.",
    },
    {
        "conference": "OOPSLA",
        "official_url": "https://conf.researchr.org/track/splash-2026/oopsla-2026",
        "list_url": "https://conf.researchr.org/track/splash-2026/oopsla-2026",
        "snapshot": "oopsla-2026.html",
        "parser": "researchr",
        "status": "accepted-list",
        "tracks": ["OOPSLA"],
        "notes": "The official OOPSLA 2026 page exposes accepted papers from the 2026 review rounds; records remain tied to the official OOPSLA track.",
    },
]


def clean_text(value: str) -> str:
    return " ".join(value.split()).strip()


def fetch(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request_url = url
    if "aaai.org/proceeding/" in url and "?" not in url:
        request_url = f"{url}?audit=20260821"
    response = requests.get(
        request_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/139.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        timeout=90,
    )
    response.raise_for_status()
    destination.write_bytes(response.content)


def parse_iclr(path: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/paper_files/paper/2026/hash/" not in href or not href.endswith(
            "-Abstract-Conference.html"
        ):
            continue
        absolute = urljoin(str(registry["list_url"]), href)
        if absolute in seen:
            continue
        seen.add(absolute)
        digest = href.rsplit("/", 1)[-1].removesuffix("-Abstract-Conference.html")
        records.append(
            {
                "title": clean_text(link.get_text(" ", strip=True)),
                "official_url": absolute,
                "pdf_url": absolute.replace(
                    "-Abstract-Conference.html", "-Paper-Conference.pdf"
                ).replace("/hash/", "/file/"),
                "track": "Conference",
                "official_record_id": digest,
            }
        )
    return sorted(records, key=lambda item: str(item["title"]).lower())


def parse_virtual(path: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if not re.fullmatch(r"/virtual/2026/poster/[^/]+", href):
            continue
        absolute = urljoin(str(registry["list_url"]), href)
        if absolute in seen:
            continue
        seen.add(absolute)
        records.append(
            {
                "title": clean_text(link.get_text(" ", strip=True)),
                "official_url": absolute,
                "track": "Main Conference posters",
                "official_record_id": href.rsplit("/", 1)[-1],
            }
        )
    return sorted(records, key=lambda item: str(item["title"]).lower())


def parse_researchr(path: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    overview = soup.select_one("#event-overview")
    if overview is None:
        return []
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for row in overview.select("table tr"):
        title_link = row.find("a", href="#")
        if title_link is None:
            continue
        title = clean_text(title_link.get_text(" ", strip=True))
        track_node = row.select_one(".prog-track")
        track = clean_text(track_node.get_text(" ", strip=True)) if track_node else "Unknown track"
        detail = row.find("a", href=re.compile(r"/details/"))
        official_url = detail.get("href") if detail else str(registry["list_url"])
        record_id = row.find(attrs={"data-event-modal": True})
        event_id = record_id.get("data-event-modal") if record_id else None
        key = (title, track)
        if key in seen:
            continue
        seen.add(key)
        pdf_url = None
        doi_url = None
        for link in row.find_all("a", href=True):
            href = link["href"]
            if href.lower().endswith(".pdf") and "arxiv.org" not in href:
                pdf_url = href
            if "doi.org/" in href:
                doi_url = href
        record: dict[str, object] = {
            "title": title,
            "official_url": urljoin(str(registry["list_url"]), official_url),
            "track": track,
        }
        if event_id:
            record["official_record_id"] = event_id
        if pdf_url:
            record["pdf_url"] = pdf_url
        if doi_url:
            record["doi_url"] = doi_url
        records.append(record)
    return sorted(records, key=lambda item: str(item["title"]).lower())


def parse_aaai(landing_path: Path, issue_paths: list[tuple[str, Path]]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for issue_url, path in issue_paths:
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        for title_node in soup.select("h3.title"):
            title = clean_text(title_node.get_text(" ", strip=True))
            article_link = title_node.find("a", href=re.compile(r"/article/view/"))
            if not article_link:
                continue
            article_url = article_link["href"]
            article_id = article_url.rstrip("/").split("/")[-1]
            if article_id in seen:
                continue
            seen.add(article_id)
            pdf_link = title_node.find("a", href=re.compile(r"/article/view/.+/.+"))
            track_node = title_node.find_previous("h2")
            record: dict[str, object] = {
                "title": title,
                "official_url": urljoin(issue_url, article_url),
                "track": clean_text(track_node.get_text(" ", strip=True))
                if track_node
                else "Unknown track",
                "official_record_id": article_id,
            }
            if pdf_link and pdf_link["href"] != article_url:
                record["pdf_url"] = pdf_link["href"]
            records.append(record)
    return sorted(records, key=lambda item: str(item["title"]).lower())


def load_or_fetch_registry(fetch_pages: bool) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for item in REGISTRY:
        registry = dict(item)
        if registry["parser"] == "pending":
            registry["papers"] = []
            entries.append(registry)
            continue
        snapshot = registry.get("snapshot")
        if fetch_pages:
            if registry["parser"] == "aaai-ojs":
                landing = CACHE_DIR / str(snapshot)
                fetch(str(registry["list_url"]), landing)
                landing_soup = BeautifulSoup(landing.read_text(encoding="utf-8"), "html.parser")
                issue_urls = []
                for link in landing_soup.find_all("a", href=True):
                    href = link["href"]
                    if re.search(r"/issue/view/\d+", href) and "Vol 40 No." in clean_text(
                        link.get_text(" ", strip=True)
                    ):
                        issue_urls.append(urljoin(str(registry["list_url"]), href))
                issue_urls = list(dict.fromkeys(issue_urls))
                issue_paths: list[tuple[str, Path]] = []
                for issue_url in issue_urls:
                    issue_id = issue_url.rstrip("/").split("/")[-1]
                    issue_path = CACHE_DIR / f"aaai-40-2026-issue-{issue_id}.html"
                    fetch(issue_url, issue_path)
                    issue_paths.append((issue_url, issue_path))
                registry["issue_count"] = len(issue_paths)
                registry["papers"] = parse_aaai(landing, issue_paths)
            else:
                path = CACHE_DIR / str(snapshot)
                fetch(str(registry["list_url"]), path)
                registry["papers"] = parse_with_parser(str(registry["parser"]), path, registry)
        else:
            if not snapshot:
                registry["papers"] = []
            else:
                path = CACHE_DIR / str(snapshot)
                if not path.exists():
                    raise FileNotFoundError(
                        f"Missing {path}; run with --fetch or place an official HTML snapshot in tmp/census."
                    )
                if registry["parser"] == "aaai-ojs":
                    landing_soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
                    issue_paths = []
                    for link in landing_soup.find_all("a", href=True):
                        href = link["href"]
                        if re.search(r"/issue/view/\d+", href) and "Vol 40 No." in clean_text(
                            link.get_text(" ", strip=True)
                        ):
                            issue_urls = urljoin(str(registry["list_url"]), href)
                            issue_path = CACHE_DIR / (
                                f"aaai-40-2026-issue-{href.rstrip('/').split('/')[-1]}.html"
                            )
                            if issue_path.exists():
                                issue_paths.append((issue_urls, issue_path))
                    registry["issue_count"] = len(issue_paths)
                    registry["papers"] = parse_aaai(path, issue_paths)
                else:
                    registry["papers"] = parse_with_parser(str(registry["parser"]), path, registry)
        entries.append(registry)
    return entries


def parse_with_parser(
    parser: str, path: Path, registry: dict[str, object]
) -> list[dict[str, object]]:
    if parser == "iclr-proceedings":
        return parse_iclr(path, registry)
    if parser == "virtual":
        return parse_virtual(path, registry)
    if parser == "researchr":
        return parse_researchr(path, registry)
    raise ValueError(f"Unknown parser: {parser}")


def initial_disposition(record: dict[str, object], conference: str) -> tuple[str, str]:
    if not record.get("pdf_url"):
        return (
            "pending",
            "Official conference record found, but no first-party full-text PDF URL was exposed by the source adapter; arXiv is not used as a substitute.",
        )
    return (
        "pending",
        "Official record and full-text URL found; the full-text product/model scan has not been recorded yet.",
    )


def build_report(registries: list[dict[str, object]]) -> dict[str, object]:
    conferences: list[dict[str, object]] = []
    for registry in registries:
        papers = []
        seen_titles: dict[str, str] = {}
        for raw in registry.get("papers", []):
            title = str(raw["title"])
            normalized = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
            disposition, reason = initial_disposition(raw, str(registry["conference"]))
            if normalized in seen_titles:
                disposition = "duplicate"
                reason = f"Duplicate official title; first occurrence is {seen_titles[normalized]}."
            else:
                seen_titles[normalized] = str(raw.get("official_url", registry["list_url"]))
            paper = {
                "title": title,
                "official_url": raw.get("official_url", registry["list_url"]),
                "track": raw.get("track", "Unknown track"),
                "disposition": disposition,
                "disposition_reason": reason,
                "full_text_scan": "pending",
            }
            for field in ("pdf_url", "doi_url", "official_record_id"):
                if raw.get(field):
                    paper[field] = raw[field]
            papers.append(paper)
        counts = {
            name: sum(p["disposition"] == name for p in papers)
            for name in ["included", "excluded", "pending", "duplicate"]
        }
        conference_report = {
            "conference": registry["conference"],
            "year": 2026,
            "official_url": registry["official_url"],
            "list_url": registry["list_url"],
            "status": registry["status"],
            "tracks": registry["tracks"],
            "notes": registry["notes"],
            "fetched_at": FETCHED_AT,
            "paper_count": len(papers) if registry.get("parser") != "pending" else None,
            "scanned_count": 0,
            **{f"{key}_count": value for key, value in counts.items()},
            "papers": papers,
        }
        if registry.get("downloads_url"):
            conference_report["downloads_url"] = registry["downloads_url"]
        conferences.append(conference_report)
    return {
        "report_version": 1,
        "scope_year": 2026,
        "generated_at": FETCHED_AT,
        "scope": "Official 2026 conference records screened for Claude Code and Codex CLI product-level research.",
        "product_terms": [
            "Claude Code",
            "Claude-Code",
            "Claude Code CLI",
            "Codex CLI",
            "Codex-CLI",
            "Repo Codex",
            "OpenAI Codex",
            "Codex agent",
            "coding agent",
        ],
        "disposition_definitions": {
            "included": "Imported into the main catalog after official-source and full-text evidence review.",
            "excluded": "Official 2026 record reviewed and outside the product-level scope, with an explicit reason.",
            "pending": "Cannot be imported yet because acceptance, full text, or product/model evidence is incomplete.",
            "duplicate": "Duplicate official record or title; points to the first occurrence.",
        },
        "conferences": conferences,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fetch", action="store_true", help="Fetch official pages into tmp/census before parsing."
    )
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    try:
        registries = load_or_fetch_registry(args.fetch)
    except (FileNotFoundError, requests.RequestException) as error:
        print(f"census build failed: {error}", file=sys.stderr)
        return 1
    report = build_report(registries)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8"
    )
    totals = {name: 0 for name in ["included", "excluded", "pending", "duplicate"]}
    for conference in report["conferences"]:
        for name in totals:
            totals[name] += int(conference[f"{name}_count"])
    print(
        f"Wrote {args.output.relative_to(ROOT)}: "
        f"{sum(c['paper_count'] or 0 for c in report['conferences'])} records, "
        + ", ".join(f"{key}={value}" for key, value in totals.items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
