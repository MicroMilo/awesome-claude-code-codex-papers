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
import json
import re
import sys
from datetime import UTC, datetime
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

if __package__:
    from .census_store import CENSUS_DIR, write_census
else:  # pragma: no cover - documented direct-script entry point
    from census_store import CENSUS_DIR, write_census

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "tmp" / "census"

FETCHED_AT = datetime.now(UTC).replace(microsecond=0).isoformat()

IJCAI_TRACKS = [
    ("main-track", "Main Track"),
    ("special-track-on-ai-and-health", "Special Track on AI and Health"),
    ("special-track-on-ai-and-robotics", "Special Track on AI and Robotics"),
    ("special-track-on-ai-and-social-good", "Special Track on AI and Social Good"),
    (
        "special-track-on-ai4tech-ai-enabling-critical-technologies",
        "Special Track on AI4Tech: AI Enabling Critical Technologies",
    ),
    ("special-track-on-human-centred-ai", "Special Track on Human-Centred AI"),
    ("journal-track", "Journal Track"),
    ("sister-conferences-best-papers-track", "Sister Conferences Best Papers Track"),
    ("survey-track", "Survey Track"),
    ("early-career-spotlight", "Early Career Spotlight"),
    ("demonstrations-track", "Demonstrations Track"),
]

KDD_TRACK_LABELS = {
    "rtp": "Research",
    "ads": "Applied Data Science",
    "dtb": "Datasets and Benchmarks",
    "bsi": "Blue Sky Ideas",
    "ais": "AI for Sciences",
}

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
        "notes": "The official track page exposes the accepted-paper list; unresolved full text remains pending until an official or identity-verified copy is found.",
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
        "notes": "The official ICML downloads page exposes the 2026 poster list. An official PDF URL is not exposed by every poster record; auxiliary content requires a separate identity check.",
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
        "official_url": "https://2026.ijcai.org/accepted-papers/",
        "list_url": "https://2026.ijcai.org/accepted-papers/",
        "parser": "ijcai",
        "status": "accepted-list",
        "tracks": [label for _, label in IJCAI_TRACKS],
        "notes": "The official accepted-paper pages expose all 2026 tracks, abstracts, and conference-hosted preprint PDFs; track labels are preserved per record.",
    },
    {
        "conference": "KDD",
        "official_url": "https://kdd2026.kdd.org/",
        "list_url": "https://kdd2026.kdd.org/papers/",
        "snapshot": "kdd-2026-papers.html",
        "parser": "kdd",
        "status": "official-proceedings",
        "tracks": list(KDD_TRACK_LABELS.values()),
        "notes": "The official KDD papers page exposes both 2026 submission cycles, track labels, authors, and ACM DOI records. DOI-bound scholarly metadata supplies abstract triage; unresolved candidate full text remains pending.",
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


def is_first_party_pdf(value: object, official_url: object) -> bool:
    parsed = urlparse(str(value or ""))
    official_host = urlparse(str(official_url or "")).netloc.lower()
    allowed_hosts = {
        official_host,
        "dl.acm.org",
        "ieeexplore.ieee.org",
        "ojs.aaai.org",
        "proceedings.iclr.cc",
        "openreview.net",
        "ijcai-preprints.s3.us-west-1.amazonaws.com",
    }
    path = parsed.path.casefold()
    looks_like_pdf = path.endswith(".pdf") or (
        parsed.netloc.lower() == "dl.acm.org" and "/doi/pdf/" in path
    )
    return looks_like_pdf and parsed.netloc.lower() in allowed_hosts


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
            if is_first_party_pdf(href, registry["list_url"]):
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


def parse_ijcai(path: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    """Parse one official IJCAI track page, including its embedded abstracts."""

    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    track = str(registry.get("track_name") or "Unknown track")
    records: list[dict[str, object]] = []
    seen: set[str] = set()
    for item in soup.select("li.ij-paper"):
        title_node = item.select_one(".ij-ptitle")
        id_node = item.select_one(".ij-pid")
        if title_node is None or id_node is None:
            continue
        title = clean_text(title_node.get_text(" ", strip=True))
        record_id = clean_text(id_node.get_text(" ", strip=True)).lstrip("#")
        if not title or not record_id or record_id in seen:
            continue
        seen.add(record_id)
        record: dict[str, object] = {
            "title": title,
            "official_url": str(registry["list_url"]),
            "track": track,
            "official_record_id": record_id,
            "authors": [
                clean_text(node.get_text(" ", strip=True))
                for node in item.select(".ij-author")
                if clean_text(node.get_text(" ", strip=True))
            ],
        }
        abstract_node = item.select_one(".ij-abstract")
        abstract = clean_text(abstract_node.get_text(" ", strip=True)) if abstract_node else ""
        if abstract:
            record["abstract"] = abstract
            record["abstract_source_url"] = str(registry["list_url"])
        pdf_link = item.select_one(".ij-pdflink a[href]")
        if pdf_link and is_first_party_pdf(pdf_link.get("href"), registry["list_url"]):
            record["pdf_url"] = str(pdf_link["href"])
        keywords = [
            clean_text(node.get_text(" ", strip=True))
            for node in item.select(".ij-kw")
            if clean_text(node.get_text(" ", strip=True))
        ]
        if keywords:
            record["keywords"] = keywords
        records.append(record)
    return sorted(records, key=lambda item: str(item["title"]).casefold())


def parse_kdd(path: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    """Parse both official KDD 2026 paper cycles from their embedded JSON."""

    payload = path.read_text(encoding="utf-8", errors="ignore")
    records: list[dict[str, object]] = []
    for cycle_id, cycle_label in (("cycle1", "February Cycle"), ("cycle2", "July Cycle")):
        match = re.search(
            rf"const {cycle_id}Papers = (\[.*?\])\.map\(\(paper, index\)",
            payload,
            re.DOTALL,
        )
        if match is None:
            raise RuntimeError(f"Official KDD page is missing {cycle_id}Papers JSON")
        papers = json.loads(match.group(1))
        occurrences: dict[str, int] = {}
        for raw in papers:
            title = clean_text(unescape(str(raw.get("title", ""))))
            doi_url = str(raw.get("url", ""))
            doi_match = re.fullmatch(r"https://doi\.org/(10\.1145/.+)", doi_url)
            if not title or doi_match is None:
                continue
            doi = doi_match.group(1)
            occurrences[doi] = occurrences.get(doi, 0) + 1
            occurrence = occurrences[doi]
            record_id = f"{cycle_id}:{doi}"
            if occurrence > 1:
                record_id = f"{record_id}:duplicate-{occurrence}"
            track_code = str(raw.get("track", ""))
            track_label = KDD_TRACK_LABELS.get(track_code, track_code or "Unknown track")
            records.append(
                {
                    "title": title,
                    "official_url": doi_url,
                    "doi_url": doi_url,
                    "pdf_url": f"https://dl.acm.org/doi/pdf/{doi}",
                    "track": f"{cycle_label} · {track_label}",
                    "cycle": cycle_label,
                    "official_record_id": record_id,
                    "authors": clean_text(unescape(str(raw.get("authors", "")))),
                }
            )
    return sorted(records, key=lambda item: str(item["title"]).casefold())


def load_or_fetch_registry(fetch_pages: bool) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for item in REGISTRY:
        registry = dict(item)
        if registry["parser"] == "pending":
            registry["papers"] = []
            entries.append(registry)
            continue
        snapshot = registry.get("snapshot")
        if registry["parser"] == "ijcai":
            records: list[dict[str, object]] = []
            for track_slug, track_name in IJCAI_TRACKS:
                track_url = f"{registry['list_url']}?ijtrack={track_slug}"
                track_path = CACHE_DIR / f"ijcai-2026-{track_slug}.html"
                if fetch_pages:
                    fetch(track_url, track_path)
                if not track_path.exists():
                    raise FileNotFoundError(
                        f"Missing {track_path}; run with --fetch to acquire official IJCAI tracks."
                    )
                track_registry = {**registry, "list_url": track_url, "track_name": track_name}
                records.extend(parse_ijcai(track_path, track_registry))
            registry["papers"] = sorted(records, key=lambda item: str(item["title"]).casefold())
            entries.append(registry)
            continue
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
    if parser == "kdd":
        return parse_kdd(path, registry)
    raise ValueError(f"Unknown parser: {parser}")


def initial_disposition(record: dict[str, object], conference: str) -> tuple[str, str]:
    if not record.get("pdf_url"):
        return (
            "pending",
            "Official conference record found, but no official or identity-verified auxiliary full-text URL has been resolved yet.",
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
            for field in (
                "pdf_url",
                "doi_url",
                "official_record_id",
                "abstract",
                "abstract_source_url",
                "authors",
                "keywords",
                "cycle",
            ):
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
    parser.add_argument("--output-dir", type=Path, default=CENSUS_DIR)
    args = parser.parse_args()
    try:
        registries = load_or_fetch_registry(args.fetch)
    except (FileNotFoundError, requests.RequestException) as error:
        print(f"census build failed: {error}", file=sys.stderr)
        return 1
    report = build_report(registries)
    index_path = write_census(report, args.output_dir)
    totals = {name: 0 for name in ["included", "excluded", "pending", "duplicate"]}
    for conference in report["conferences"]:
        for name in totals:
            totals[name] += int(conference[f"{name}_count"])
    print(
        f"Wrote {index_path.relative_to(ROOT)} and {len(report['conferences'])} conference files: "
        f"{sum(c['paper_count'] or 0 for c in report['conferences'])} records, "
        + ", ".join(f"{key}={value}" for key, value in totals.items())
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
