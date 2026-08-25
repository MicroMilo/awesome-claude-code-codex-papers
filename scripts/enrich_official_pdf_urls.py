#!/usr/bin/env python3
"""Discover first-party PDF URLs from official conference and publisher pages."""

from __future__ import annotations

import argparse
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup

if __package__:
    from .census_store import load_census, write_census
    from .source_fetcher import FetchError, RetryPolicy, StableFetcher, metadata_dict
else:  # pragma: no cover - documented direct-script entry point
    from census_store import load_census, write_census
    from source_fetcher import FetchError, RetryPolicy, StableFetcher, metadata_dict


def acm_pdf_url(doi_url: object) -> str | None:
    """Derive ACM's first-party PDF endpoint from an official ACM DOI."""

    parsed = urlparse(str(doi_url or ""))
    doi = parsed.path.lstrip("/")
    if parsed.netloc.lower() not in {"doi.org", "dx.doi.org"} or not doi.startswith("10.1145/"):
        return None
    return f"https://dl.acm.org/doi/pdf/{doi}"


def acm_doi_from_url(value: object) -> str | None:
    parsed = urlparse(str(value or ""))
    if parsed.netloc.lower() != "dl.acm.org":
        return None
    match = re.search(r"/doi/(?:abs/|full/|pdf/)?(10\.1145/[^/?#]+)", parsed.path)
    return f"https://doi.org/{match.group(1)}" if match else None


def accepted_direct_pdf(page_url: str, candidate: str) -> str | None:
    absolute = urljoin(page_url, candidate)
    parsed = urlparse(absolute)
    page_host = urlparse(page_url).netloc.lower()
    host = parsed.netloc.lower()
    if "arxiv.org" in host or not parsed.path.casefold().endswith(".pdf"):
        return None
    first_party_hosts = {
        page_host,
        "dl.acm.org",
        "ojs.aaai.org",
        "proceedings.iclr.cc",
        "openreview.net",
    }
    return absolute if host in first_party_hosts else None


def discover_from_page(conference: str, page_url: str, payload: bytes) -> dict[str, Any]:
    soup = BeautifulSoup(payload, "html.parser")
    citation_meta = soup.find("meta", attrs={"name": "citation_pdf_url"})
    if citation_meta and citation_meta.get("content"):
        return {
            "status": "found",
            "pdf_url": urljoin(page_url, str(citation_meta["content"])),
            "method": "official-page-citation-metadata",
            "source_url": page_url,
        }

    if conference == "AAAI":
        galley = soup.select_one("a.obj_galley_link.pdf[href]")
        if galley:
            return {
                "status": "found",
                "pdf_url": urljoin(page_url, str(galley["href"])),
                "method": "official-aaai-ojs-galley",
                "source_url": page_url,
            }

    page_host = urlparse(page_url).netloc.lower()
    researchr_page = (
        "researchr.org" in page_host
        or page_host.endswith(".sigplan.org")
        or page_host.endswith(".splashcon.org")
    )
    links = []
    if researchr_page:
        for label in soup.select("label.control-label"):
            label_text = " ".join(label.get_text(" ", strip=True).split())
            if label_text in {"Link to Publication", "DOI"}:
                links.extend(label.parent.find_all("a", href=True))
    else:
        links = soup.find_all("a", href=True)

    doi_urls: list[str] = []
    direct_pdfs: list[str] = []
    openreview_url = None
    for link in links:
        href = urljoin(page_url, str(link["href"]))
        parsed = urlparse(href)
        if parsed.netloc.lower() in {"doi.org", "dx.doi.org"}:
            doi_urls.append(href)
        elif derived_doi := acm_doi_from_url(href):
            doi_urls.append(derived_doi)
        if direct_pdf := accepted_direct_pdf(page_url, href):
            direct_pdfs.append(direct_pdf)
        if parsed.netloc.lower() == "openreview.net" and parsed.path == "/forum":
            openreview_url = href

    for doi_url in dict.fromkeys(doi_urls):
        if pdf_url := acm_pdf_url(doi_url):
            return {
                "status": "found",
                "pdf_url": pdf_url,
                "full_text_url": doi_url,
                "doi_url": doi_url,
                "method": "official-page-acm-doi",
                "source_url": page_url,
            }
    if direct_pdfs:
        return {
            "status": "found",
            "pdf_url": direct_pdfs[0],
            "method": "official-page-first-party-pdf-link",
            "source_url": page_url,
        }
    if conference == "ICML" and openreview_url:
        note_id = parse_qs(urlparse(openreview_url).query).get("id", [""])[0]
        if note_id:
            return {
                "status": "found",
                "pdf_url": f"https://openreview.net/pdf?id={note_id}",
                "full_text_url": openreview_url,
                "method": "official-page-openreview-link",
                "source_url": page_url,
            }
    return {
        "status": "pending",
        "reason": "Official page did not expose a first-party PDF, ACM DOI, or OpenReview full-text link.",
        "source_url": page_url,
    }


def discover(
    conference: str,
    record: dict[str, Any],
    fetcher: StableFetcher,
    timeout: int,
) -> dict[str, Any]:
    doi_url = str(record.get("doi_url", ""))
    if derived_pdf_url := acm_pdf_url(doi_url):
        return {
            "status": "found",
            "pdf_url": derived_pdf_url,
            "full_text_url": doi_url,
            "doi_url": doi_url,
            "method": "official-acm-doi",
            "source_url": doi_url,
        }

    page_url = str(record.get("details_url") or record.get("official_url", ""))
    if not page_url:
        return {"status": "pending", "reason": "Official record URL is missing."}
    try:
        fetched = fetcher.request_bytes("GET", page_url, timeout=(15, timeout))
        result = discover_from_page(conference, page_url, fetched.body)
        result["fetch"] = metadata_dict(fetched.metadata)
        return result
    except FetchError as error:  # pragma: no cover - depends on official site state
        return {
            "status": "pending",
            "reason": str(error),
            "source_url": error.url,
            "http_status": error.status_code,
            "attempts": error.attempts,
            "error_class": error.error_class,
            "challenge": error.challenge,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", action="append")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--per-host-concurrency", type=int, default=2)
    parser.add_argument("--per-host-delay", type=float, default=0.4)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Recheck records previously enriched from an official page and remove stale discoveries.",
    )
    parser.add_argument(
        "--pending-only",
        action="store_true",
        help="Only inspect records whose current disposition is pending.",
    )
    args = parser.parse_args()

    census = load_census()
    selected = set(args.conference or ["AAAI", "ICML"])
    if args.refresh:
        for conference in census.get("conferences", []):
            if conference["conference"] not in selected:
                continue
            for paper in conference.get("papers", []):
                discovery = paper.get("full_text_discovery")
                if not isinstance(discovery, dict) or not str(
                    discovery.get("method", "")
                ).startswith("official-page-"):
                    continue
                for field in ("pdf_url", "full_text_url", "doi_url"):
                    if discovery.get(field) and paper.get(field) == discovery.get(field):
                        paper.pop(field, None)
                paper.pop("full_text_discovery", None)

    jobs = [
        (conference["conference"], paper)
        for conference in census.get("conferences", [])
        if conference["conference"] in selected
        for paper in conference.get("papers", [])
        if (args.refresh or not paper.get("pdf_url"))
        and (not args.pending_only or paper.get("disposition") == "pending")
    ]
    fetcher = StableFetcher(
        user_agent="awesome-coding-agent-papers-url-enricher/2.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=max(1, args.retries)),
        per_host_concurrency=max(1, args.per_host_concurrency),
        per_host_min_interval=max(0.0, args.per_host_delay),
    )
    print(f"Enriching {len(jobs)} official records with first-party full-text URLs.")
    results: dict[tuple[str, str], dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(discover, conference, paper, fetcher, args.timeout): (
                conference,
                paper["title"],
            )
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
                for field in ("full_text_url", "doi_url"):
                    if result.get(field):
                        paper[field] = result[field]
                paper["disposition_reason"] = (
                    "Official record and first-party full-text URL found; full-text product/model scan is pending."
                )
                paper["full_text_discovery"] = {
                    key: value for key, value in result.items() if key != "status"
                }
                found += 1
            else:
                paper["disposition_reason"] = str(result["reason"])
                paper["full_text_discovery"] = {
                    key: value for key, value in result.items() if key != "status"
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
        "policy": "Only official conference pages, official proceedings pages, official publisher pages, and official OpenReview full text are accepted.",
    }
    write_census(census, only=selected)
    print(f"full-text URL enrichment: found={found}, not_found={failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
