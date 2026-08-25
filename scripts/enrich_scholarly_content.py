#!/usr/bin/env python3
"""Resolve auditable abstracts and full text without changing venue identity.

The official conference record remains the acceptance/proceedings authority.
This enrichment layer queries scholarly indexes and curated overrides only for
content bytes.  Every accepted auxiliary source carries an explicit identity
match, version, provider, and discovery timestamp.

OpenAlex is queried in DOI batches of at most 100.  Results are checkpointed in
an append-only JSONL ledger, so interrupted runs resume without re-requesting
completed DOI records.  Candidate-only arXiv or institutional copies can be
added through ``data/audit/content-source-overrides.yaml`` after title/author
identity has been reviewed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

if __package__:
    from .census_store import load_conference, write_conference
    from .metadata_relevance import screen_metadata
    from .source_fetcher import JsonlLedger, RetryPolicy, StableFetcher, metadata_dict
else:  # pragma: no cover - documented direct-script entry point
    from census_store import load_conference, write_conference
    from metadata_relevance import screen_metadata
    from source_fetcher import JsonlLedger, RetryPolicy, StableFetcher, metadata_dict

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "data" / "audit" / "2026-scholarly-content.jsonl"
OVERRIDES_PATH = ROOT / "data" / "audit" / "content-source-overrides.yaml"
OPENALEX_URL = "https://api.openalex.org/works"
OPENALEX_SELECT = (
    "id,doi,title,publication_year,authorships,abstract_inverted_index,"
    "best_oa_location,locations,has_fulltext,content_urls"
)
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
ARXIV_ID_RE = re.compile(r"arxiv\.org/(?:pdf|abs)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)
VERSION_RANK = {
    "publishedVersion": 0,
    "acceptedVersion": 1,
    "submittedVersion": 2,
    "unknown": 3,
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def normalize_text(value: object) -> str:
    return " ".join(str(value).split()).strip()


def normalize_doi(value: object) -> str:
    match = DOI_RE.search(str(value or ""))
    return match.group(0).rstrip(".").casefold() if match else ""


def source_key(conference: str, doi: str) -> str:
    return f"{conference}:{normalize_doi(doi)}"


def chunks(values: list[str], size: int) -> Iterable[list[str]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def reconstruct_abstract(inverted_index: object) -> str:
    """Reconstruct OpenAlex's abstract while preserving token order."""

    if not isinstance(inverted_index, dict):
        return ""
    positioned: list[tuple[int, str]] = []
    for token, positions in inverted_index.items():
        if not isinstance(positions, list):
            continue
        for position in positions:
            if isinstance(position, int) and position >= 0:
                positioned.append((position, str(token)))
    positioned.sort(key=lambda item: item[0])
    return normalize_text(" ".join(token for _, token in positioned))


def provider_for_url(url: str) -> str:
    host = urlparse(url).netloc.casefold()
    if host.endswith("arxiv.org"):
        return "arxiv"
    if host.endswith("openalex.org"):
        return "openalex"
    if host.endswith("acm.org"):
        return "acm"
    return host.removeprefix("www.") or "unknown"


def normalize_version(value: object) -> str:
    version = str(value or "unknown")
    return version if version in VERSION_RANK else "unknown"


def openalex_content_sources(
    work: dict[str, Any], expected_doi: str, discovered_at: str
) -> list[dict[str, Any]]:
    actual_doi = normalize_doi(work.get("doi"))
    expected = normalize_doi(expected_doi)
    if not expected or actual_doi != expected:
        raise ValueError(f"OpenAlex DOI mismatch: expected {expected}, got {actual_doi}")

    sources: list[dict[str, Any]] = []
    work_url = str(work.get("id") or "")
    if work_url.startswith("https://"):
        sources.append(
            {
                "provider": "openalex",
                "url": work_url,
                "source_role": "metadata",
                "version": "metadata",
                "license": "not-reported",
                "identity_status": "verified",
                "identity_method": "exact-doi",
                "identity_value": expected,
                "discovered_at": discovered_at,
                "used_for": ["abstract"],
            }
        )

    seen_urls: set[str] = set()
    for location in work.get("locations") or []:
        if not isinstance(location, dict) or not location.get("is_oa"):
            continue
        pdf_url = str(location.get("pdf_url") or "")
        if not pdf_url.startswith("https://") or pdf_url in seen_urls:
            continue
        seen_urls.add(pdf_url)
        source = {
            "provider": provider_for_url(pdf_url),
            "url": pdf_url,
            "source_role": "full-text",
            "version": normalize_version(location.get("version")),
            "license": str(location.get("license") or "not-reported"),
            "identity_status": "verified",
            "identity_method": "openalex-location-for-exact-doi",
            "identity_value": expected,
            "discovered_at": discovered_at,
            "used_for": ["full-text", "evidence"],
        }
        landing_page_url = str(location.get("landing_page_url") or "")
        if landing_page_url.startswith("https://"):
            source["landing_page_url"] = landing_page_url
        sources.append(source)
    return sources


def openalex_record(
    conference: str,
    doi: str,
    work: dict[str, Any] | None,
    fetch: dict[str, Any],
) -> dict[str, Any]:
    key = source_key(conference, doi)
    if work is None:
        return {
            "source_key": key,
            "conference": conference,
            "doi": normalize_doi(doi),
            "provider": "openalex",
            "status": "not-found",
            "fetch": fetch,
        }
    discovered_at = str(fetch.get("retrieved_at") or utc_now())
    try:
        content_sources = openalex_content_sources(work, doi, discovered_at)
    except ValueError as error:
        return {
            "source_key": key,
            "conference": conference,
            "doi": normalize_doi(doi),
            "provider": "openalex",
            "status": "identity-mismatch",
            "reason": str(error),
            "fetch": fetch,
        }
    authors = [
        normalize_text(authorship.get("author", {}).get("display_name"))
        for authorship in work.get("authorships") or []
        if isinstance(authorship, dict)
        and normalize_text(authorship.get("author", {}).get("display_name"))
    ]
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    return {
        "source_key": key,
        "conference": conference,
        "doi": normalize_doi(doi),
        "provider": "openalex",
        "status": "matched",
        "openalex_id": work.get("id"),
        "title": normalize_text(work.get("title")),
        "publication_year": work.get("publication_year"),
        "authors": authors,
        "abstract": abstract,
        "content_sources": content_sources,
        "fetch": fetch,
    }


def fetch_openalex_records(
    conference: str,
    dois: list[str],
    ledger: JsonlLedger,
    fetcher: StableFetcher,
    *,
    batch_size: int,
    api_key: str | None,
) -> None:
    for batch_number, batch in enumerate(chunks(dois, batch_size), start=1):
        params: dict[str, Any] = {
            "filter": "doi:" + "|".join(batch),
            "per-page": len(batch),
            "select": OPENALEX_SELECT,
        }
        if api_key:
            params["api_key"] = api_key
        fetched = fetcher.request_bytes("GET", OPENALEX_URL, params=params, timeout=(15, 90))
        payload = json.loads(fetched.body)
        results = payload.get("results") if isinstance(payload, dict) else None
        if not isinstance(results, list):
            raise RuntimeError("OpenAlex response does not contain a results array")
        by_doi = {
            normalize_doi(work.get("doi")): work
            for work in results
            if isinstance(work, dict) and normalize_doi(work.get("doi"))
        }
        fetch = metadata_dict(fetched.metadata)
        for doi in batch:
            ledger.append(openalex_record(conference, doi, by_doi.get(doi), fetch))
        print(f"OpenAlex batch {batch_number}: requested={len(batch)}, matched={len(by_doi)}")


def load_overrides(path: Path = OVERRIDES_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sources = payload.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("content-source overrides must contain a sources list")
    return [item for item in sources if isinstance(item, dict)]


def official_identity_value(paper: dict[str, Any]) -> str:
    """Return the stable official identifier an auxiliary copy must bind to."""

    expected_doi = normalize_doi(paper.get("doi_url") or paper.get("official_url"))
    if expected_doi:
        return expected_doi
    for key in ("details_url", "official_url"):
        value = str(paper.get(key) or "")
        if value.startswith("https://"):
            return value
    return ""


def validate_override(override: dict[str, Any], paper: dict[str, Any]) -> dict[str, Any]:
    expected_identity = official_identity_value(paper)
    if not expected_identity:
        raise ValueError(f"official record lacks a stable identity: {override.get('title')}")
    expected_doi = normalize_doi(expected_identity)
    if expected_doi:
        override_doi = normalize_doi(override.get("doi"))
        if override_doi != expected_doi:
            raise ValueError(
                f"override DOI does not match official record: {override.get('title')}"
            )
    else:
        official_urls = {
            str(paper.get(key) or "")
            for key in ("details_url", "official_url")
            if str(paper.get(key) or "").startswith("https://")
        }
        override_official_url = str(override.get("official_url") or "")
        if override_official_url not in official_urls:
            raise ValueError(
                f"override official URL does not match census: {override.get('title')}"
            )
    if (
        normalize_text(override.get("title")).casefold()
        != normalize_text(paper.get("title")).casefold()
    ):
        raise ValueError(f"override title does not exactly match census: {override.get('title')}")
    source = dict(override.get("source") or {})
    if not str(source.get("url", "")).startswith("https://"):
        raise ValueError(f"override source is not HTTPS: {override.get('title')}")
    if source.get("identity_status") != "verified":
        raise ValueError(f"override source is not identity-verified: {override.get('title')}")
    if not normalize_text(source.get("identity_method")):
        raise ValueError(f"override source lacks an identity method: {override.get('title')}")
    if not normalize_text(source.get("identity_evidence")):
        raise ValueError(f"override source lacks identity evidence: {override.get('title')}")
    source.setdefault("identity_value", expected_identity)
    if str(source.get("identity_value")).casefold() != expected_identity.casefold():
        raise ValueError(
            f"override identity does not bind to the official record: {override.get('title')}"
        )
    source.setdefault("discovered_at", utc_now())
    source.setdefault("version", "unknown")
    source.setdefault("license", "not-reported")
    source.setdefault("used_for", ["full-text", "evidence"])
    return source


def merge_sources(current: object, additions: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    if isinstance(current, list):
        for source in current:
            if isinstance(source, dict) and source.get("url"):
                merged[str(source["url"])] = dict(source)
    for source in additions:
        if source.get("url"):
            source_url = str(source["url"])
            source_arxiv = ARXIV_ID_RE.search(source_url)
            if source_arxiv:
                for existing_url in list(merged):
                    existing_arxiv = ARXIV_ID_RE.search(existing_url)
                    if existing_arxiv and existing_arxiv.group(1) == source_arxiv.group(1):
                        del merged[existing_url]
            merged[source_url] = dict(source)
    return sorted(
        merged.values(),
        key=lambda source: (
            source.get("source_role") != "metadata",
            str(source.get("provider")),
            str(source.get("url")),
        ),
    )


def preferred_full_text_source(sources: object) -> dict[str, Any] | None:
    if not isinstance(sources, list):
        return None
    candidates = [
        source
        for source in sources
        if isinstance(source, dict)
        and source.get("source_role") == "full-text"
        and source.get("identity_status") == "verified"
        and str(source.get("url", "")).startswith("https://")
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda source: (
            VERSION_RANK.get(str(source.get("version")), 4),
            source.get("provider") == "acm",
            str(source.get("url")),
        ),
    )


def apply_metadata_screen(paper: dict[str, Any], abstract: str) -> None:
    screen = screen_metadata(str(paper.get("title", "")), abstract)
    for key, value in screen.items():
        paper[f"metadata_{key}"] = value
    review_status = str((paper.get("product_review") or {}).get("status", ""))
    if paper.get("full_text_scan") in {"scanned", "verified-manually"} or review_status:
        return
    paper["scan"] = {
        "status": "pending",
        "metadata_screen": screen,
        "metadata_screen_status": screen["screen_status"],
        "metadata_screen_reason": screen["screen_reason"],
        "metadata_screen_matches": screen["matched_terms"],
        "metadata_source": "identity-verified OpenAlex record for the official DOI",
    }
    if paper.get("disposition") in {"included", "duplicate"}:
        return
    if screen["screen_status"] == "filtered":
        paper["disposition"] = "excluded"
        paper["full_text_scan"] = "metadata-filtered"
        paper["disposition_reason"] = (
            f"{screen['screen_reason']} Decision used an identity-verified OpenAlex abstract "
            "for the official conference DOI; no PDF was requested."
        )
        paper["scan"]["status"] = "metadata-filtered"
        paper["scan"]["disposition"] = "excluded"
    else:
        paper["disposition"] = "pending"
        paper["full_text_scan"] = "pending"
        paper["disposition_reason"] = (
            f"{screen['screen_reason']} Identity-verified full-text evidence is still required "
            "before catalog import."
        )


def apply_enrichment(
    conference: dict[str, Any],
    latest: dict[str, dict[str, Any]],
    overrides: list[dict[str, Any]],
) -> dict[str, int]:
    name = str(conference["conference"])
    override_by_title = {
        normalize_text(item.get("title")).casefold(): item
        for item in overrides
        if item.get("conference") == name and normalize_text(item.get("title"))
    }
    stats = {
        "official_doi_records": 0,
        "openalex_matched": 0,
        "abstracts": 0,
        "verified_full_text_sources": 0,
        "overrides_applied": 0,
        "metadata_candidates": 0,
        "metadata_excluded": 0,
        "metadata_pending": 0,
    }
    for paper in conference.get("papers", []):
        if paper.get("disposition") == "duplicate":
            continue
        doi = normalize_doi(paper.get("doi_url") or paper.get("official_url"))
        additions: list[dict[str, Any]] = []
        record = None
        if doi:
            stats["official_doi_records"] += 1
            record = latest.get(source_key(name, doi))
        if record and record.get("status") == "matched":
            stats["openalex_matched"] += 1
            additions.extend(record.get("content_sources") or [])
            abstract = normalize_text(record.get("abstract"))
            if abstract:
                stats["abstracts"] += 1
                if not normalize_text(paper.get("abstract")):
                    paper["abstract"] = abstract
                    paper["abstract_source_url"] = record.get("openalex_id")
                    paper["abstract_source_type"] = "auxiliary-scholarly-metadata"
                    paper["abstract_source_provider"] = "openalex"
                    paper["abstract_source_version"] = "metadata"
                    paper["abstract_identity_status"] = "verified"
                    paper["abstract_identity_method"] = "exact-doi"
                apply_metadata_screen(paper, normalize_text(paper.get("abstract")))
                status = paper.get("metadata_screen_status")
                if status == "candidate":
                    stats["metadata_candidates"] += 1
                elif status == "filtered":
                    stats["metadata_excluded"] += 1
        override = override_by_title.get(normalize_text(paper.get("title")).casefold())
        if override:
            additions.append(validate_override(override, paper))
            stats["overrides_applied"] += 1
        if additions:
            paper["content_sources"] = merge_sources(paper.get("content_sources"), additions)
        preferred = preferred_full_text_source(paper.get("content_sources"))
        if preferred:
            paper["resolved_pdf_url"] = preferred["url"]
            paper["resolved_content_source"] = {
                key: preferred[key]
                for key in (
                    "provider",
                    "url",
                    "version",
                    "license",
                    "identity_status",
                    "identity_method",
                    "identity_value",
                    "discovered_at",
                )
                if key in preferred
            }
            stats["verified_full_text_sources"] += 1
        if paper.get("disposition") == "pending" and not paper.get("abstract"):
            stats["metadata_pending"] += 1

    counts = {
        disposition: sum(
            paper.get("disposition") == disposition for paper in conference.get("papers", [])
        )
        for disposition in ("included", "excluded", "pending", "duplicate")
    }
    conference.update({f"{key}_count": value for key, value in counts.items()})
    conference["metadata_screened_count"] = sum(
        paper.get("full_text_scan") == "metadata-filtered" for paper in conference.get("papers", [])
    )
    conference["scanned_count"] = sum(
        paper.get("full_text_scan") in {"scanned", "verified-manually"}
        for paper in conference.get("papers", [])
    )
    conference["scholarly_content_enrichment"] = {
        **stats,
        "updated_at": utc_now(),
        "acceptance_authority": "official conference/proceedings/publisher record",
        "content_policy": (
            "Auxiliary metadata/full text is accepted only with an explicit identity match; "
            "it never replaces the official acceptance source."
        ),
        "ledger": str(LEDGER_PATH.relative_to(ROOT)),
        "overrides": str(OVERRIDES_PATH.relative_to(ROOT)),
    }
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", required=True, help="Conference ID, for example KDD.")
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--no-fetch", action="store_true", help="Apply the existing ledger only.")
    parser.add_argument("--no-update", action="store_true", help="Do not rewrite the census shard.")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 100:
        parser.error("--batch-size must be between 1 and 100")

    conference = load_conference(args.conference)
    ledger = JsonlLedger(LEDGER_PATH)
    latest = ledger.latest()
    dois = sorted(
        {
            normalize_doi(paper.get("doi_url") or paper.get("official_url"))
            for paper in conference.get("papers", [])
            if paper.get("disposition") != "duplicate"
            and normalize_doi(paper.get("doi_url") or paper.get("official_url"))
        }
    )
    if not args.refresh:
        dois = [doi for doi in dois if source_key(args.conference, doi) not in latest]
    if args.limit:
        dois = dois[: args.limit]
    if dois and not args.no_fetch:
        fetcher = StableFetcher(
            user_agent=(
                "awesome-claude-code-codex-papers/0.4 "
                "(+https://github.com/MicroMilo/awesome-claude-code-codex-papers)"
            ),
            retry_policy=RetryPolicy(max_attempts=4),
            per_host_concurrency=1,
            per_host_min_interval=0.25,
        )
        fetch_openalex_records(
            args.conference,
            dois,
            ledger,
            fetcher,
            batch_size=args.batch_size,
            api_key=os.getenv("OPENALEX_API_KEY"),
        )
        latest = ledger.latest()
    elif dois and args.no_fetch:
        print(f"Skipped {len(dois)} unresolved DOI records because --no-fetch was set.")

    stats = apply_enrichment(conference, latest, load_overrides())
    if not args.no_update:
        destination = write_conference(conference)
        print(f"Updated {destination}")
    print("enrichment summary:", ", ".join(f"{key}={value}" for key, value in stats.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
