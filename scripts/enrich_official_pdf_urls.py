#!/usr/bin/env python3
"""Discover first-party PDF URLs from official conference full-text pages."""

from __future__ import annotations

import argparse
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"
_LOCAL = threading.local()


def session() -> requests.Session:
    value = getattr(_LOCAL, "session", None)
    if value is None:
        value = requests.Session()
        value.mount("https://", HTTPAdapter(pool_connections=4, pool_maxsize=4, max_retries=2))
        value.headers.update({"User-Agent": "awesome-coding-agent-papers-url-enricher/1.0"})
        _LOCAL.session = value
    return value


def acm_pdf_url(doi_url: object) -> str | None:
    """Derive ACM's first-party PDF endpoint from an official ACM DOI."""

    parsed = urlparse(str(doi_url or ""))
    doi = parsed.path.lstrip("/")
    if parsed.netloc.lower() not in {"doi.org", "dx.doi.org"} or not doi.startswith("10.1145/"):
        return None
    return f"https://dl.acm.org/doi/pdf/{doi}"


def discover(conference: str, record: dict[str, object], timeout: int) -> dict[str, object]:
    doi_url = str(record.get("doi_url", ""))
    if derived_pdf_url := acm_pdf_url(doi_url):
        return {
            "status": "found",
            "pdf_url": derived_pdf_url,
            "full_text_url": doi_url,
            "method": "official-acm-doi",
            "source_url": doi_url,
        }

    url = str(record.get("details_url") or record.get("official_url", ""))
    try:
        response = session().get(url, timeout=(15, timeout))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        citation_meta = soup.find("meta", attrs={"name": "citation_pdf_url"})
        pdf_url = (
            urljoin(url, str(citation_meta["content"]))
            if citation_meta and citation_meta.get("content")
            else None
        )
        full_text_url = None
        if conference == "AAAI":
            if not pdf_url:
                link = soup.select_one("a.obj_galley_link.pdf")
                pdf_url = urljoin(url, str(link.get("href"))) if link else None
        elif conference == "ICML":
            for link in soup.find_all("a", href=True):
                href = str(link["href"])
                if "openreview.net/forum?id=" in href:
                    full_text_url = href
                    parsed = urlparse(href)
                    query = parsed.query
                    match = re.search(r"(?:^|&)id=([^&]+)", query)
                    if match:
                        pdf_url = f"https://openreview.net/pdf?id={match.group(1)}"
                    break
        if not pdf_url:
            return {
                "status": "pending",
                "reason": "Official page did not expose a first-party PDF or OpenReview full-text link.",
            }
        result: dict[str, object] = {
            "status": "found",
            "pdf_url": pdf_url,
            "method": "official-page-metadata",
            "source_url": url,
        }
        if full_text_url:
            result["full_text_url"] = full_text_url
        return result
    except Exception as error:  # pragma: no cover - depends on official site state
        return {"status": "pending", "reason": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", action="append")
    parser.add_argument("--workers", type=int, default=48)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--pending-only",
        action="store_true",
        help="Only inspect records whose current disposition is pending.",
    )
    args = parser.parse_args()

    census = yaml.safe_load(CENSUS_PATH.read_text(encoding="utf-8"))
    selected = set(args.conference or ["AAAI", "ICML"])
    jobs = [
        (conference["conference"], paper)
        for conference in census.get("conferences", [])
        if conference["conference"] in selected
        for paper in conference.get("papers", [])
        if not paper.get("pdf_url")
        and (not args.pending_only or paper.get("disposition") == "pending")
    ]
    print(f"Enriching {len(jobs)} official records with first-party full-text URLs.")
    results: dict[tuple[str, str], dict[str, object]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(discover, conference, paper, args.timeout): (conference, paper["title"])
            for conference, paper in jobs
        }
        for index, future in enumerate(as_completed(futures), start=1):
            results[futures[future]] = future.result()
            if index % 100 == 0 or index == len(futures):
                print(f"completed {index}/{len(futures)}")

    found = 0
    failed = 0
    for conference in census.get("conferences", []):
        name = conference["conference"]
        for paper in conference.get("papers", []):
            result = results.get((name, paper["title"]))
            if not result:
                continue
            if result["status"] == "found":
                paper["pdf_url"] = result["pdf_url"]
                if result.get("full_text_url"):
                    paper["full_text_url"] = result["full_text_url"]
                paper["disposition_reason"] = (
                    "Official record and first-party full-text URL found; full-text product/model scan is pending."
                )
                paper["full_text_discovery"] = {
                    key: value for key, value in result.items() if key != "status"
                }
                found += 1
            else:
                paper["disposition_reason"] = result["reason"]
                paper["full_text_discovery"] = {
                    "reason": result["reason"],
                    "source_url": paper.get("details_url") or paper.get("official_url"),
                }
                failed += 1
        conference["pdf_url_count"] = sum(
            bool(paper.get("pdf_url")) for paper in conference.get("papers", [])
        )

    census["full_text_url_enrichment"] = {
        "audited_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "conferences": sorted(selected),
        "found": found,
        "not_found": failed,
        "policy": "Only official conference pages, official proceedings pages, and official OpenReview full text are accepted.",
    }
    CENSUS_PATH.write_text(
        yaml.safe_dump(census, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8"
    )
    print(f"full-text URL enrichment: found={found}, not_found={failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
