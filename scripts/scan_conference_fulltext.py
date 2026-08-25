#!/usr/bin/env python3
"""Scan official conference PDFs for industrial coding-agent evidence.

The scanner keeps PDFs out of the repository.  It stores only a compact audit
manifest (page-level snippets, extraction method, and model candidates) and
updates the census disposition. Records with official title/abstract metadata
use a high-recall gate before a PDF request; ``--pdf-scope all`` disables that
optimization. If the official metadata is missing, the record is ``pending``
rather than silently triggering a full-PDF crawl. A product hit is deliberately
left pending for human/context review; absence of a product hit after
successful full-text extraction is recorded as an explicit exclusion.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

if __package__:
    from .census_store import CENSUS_INDEX_PATH, load_census, write_census
    from .metadata_relevance import screen_metadata
    from .source_fetcher import FetchError, RetryPolicy, StableFetcher, metadata_dict
else:  # pragma: no cover - exercised by the documented direct-script command
    from census_store import CENSUS_INDEX_PATH, load_census, write_census
    from metadata_relevance import screen_metadata
    from source_fetcher import FetchError, RetryPolicy, StableFetcher, metadata_dict

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "audit" / "2026-fulltext-scan.jsonl"
ICLR_DETAIL_RE = re.compile(
    r"^https://proceedings\.iclr\.cc/paper_files/paper/2026/hash/[0-9a-f]+-Abstract-Conference\.html$",
    re.IGNORECASE,
)

PRODUCT_PATTERNS = {
    "claude-code": re.compile(r"\bclaude[ -]code(?:[ -]cli)?\b", re.IGNORECASE),
    "codex-cli": re.compile(
        r"\b(?:codex[ -]cli|codex-cli|repo[ -]codex|openai[ -]codex)\b", re.IGNORECASE
    ),
    "codex-agent": re.compile(r"\bcodex[ -]agent\b", re.IGNORECASE),
}
GENERIC_PATTERN = re.compile(r"\bcoding[ -]agent(?:s)?\b", re.IGNORECASE)
MODEL_PATTERNS = [
    re.compile(
        r"\b(?:gpt|o)[ -]?\d+(?:\.\d+)?(?:[- ][a-z0-9]+)*(?:-\d{4}-\d{2}-\d{2})?\b", re.IGNORECASE
    ),
    re.compile(
        r"\bclaude[ -](?:opus|sonnet|haiku)[ -]?\d+(?:[.-]\d+)*(?:[- ][a-z0-9]+)*\b", re.IGNORECASE
    ),
]


def normalize(value: str) -> str:
    return " ".join(value.split()).strip()


def extract_official_abstract(payload: bytes) -> str:
    soup = BeautifulSoup(payload, "html.parser")
    node = soup.select_one(".paper-abstract")
    if node is not None:
        return normalize(node.get_text(" ", strip=True))
    description = soup.select_one('meta[name="description"]')
    return normalize(str(description.get("content", ""))) if description else ""


def extract_pdf_text(payload: bytes) -> tuple[str, str]:
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-", "-"],
            input=payload,
            capture_output=True,
            check=True,
            timeout=120,
        )
        text = result.stdout.decode("utf-8", errors="replace")
        if text.strip():
            return text, "pdftotext"
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(payload))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\f".join(pages), "pypdf"
    except Exception as error:  # pragma: no cover - depends on malformed external PDFs
        raise RuntimeError(f"PDF text extraction failed: {error}") from error


def snippets_for_pattern(
    pages: list[str], pattern: re.Pattern[str], limit: int = 4
) -> list[dict[str, Any]]:
    snippets: list[dict[str, Any]] = []
    for page_number, page in enumerate(pages, start=1):
        for match in pattern.finditer(page):
            start = max(0, match.start() - 180)
            end = min(len(page), match.end() + 240)
            snippets.append(
                {
                    "page": page_number,
                    "match": normalize(match.group(0)),
                    "snippet": normalize(page[start:end]),
                }
            )
            if len(snippets) >= limit:
                return snippets
    return snippets


def model_candidates(text: str) -> list[str]:
    found: list[str] = []
    for pattern in MODEL_PATTERNS:
        for match in pattern.finditer(text):
            candidate = normalize(match.group(0))
            if candidate.lower() not in {item.lower() for item in found}:
                found.append(candidate)
    return found[:80]


def scan_record(
    conference: str,
    record: dict[str, Any],
    timeout: int,
    fetcher: StableFetcher | None = None,
    *,
    metadata_first: bool = True,
    pdf_scope: str = "metadata",
) -> dict[str, Any]:
    title = str(record.get("title", ""))
    pdf_url = record.get("pdf_url")
    result: dict[str, Any] = {
        "conference": conference,
        "title": title,
        "official_url": record.get("official_url"),
        "pdf_url": pdf_url,
    }
    active_fetcher = fetcher or StableFetcher(
        user_agent="awesome-coding-agent-papers-fulltext/2.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=3),
        per_host_concurrency=1,
        per_host_min_interval=0.5,
    )
    if metadata_first and pdf_scope == "metadata":
        metadata_result = {
            key.removeprefix("metadata_"): value
            for key, value in record.items()
            if key.startswith("metadata_")
        }
        metadata_fetch: dict[str, Any] | None = None
        abstract = record.get("abstract")
        if not metadata_result and isinstance(abstract, str) and abstract.strip():
            metadata_result = screen_metadata(title, abstract)
        elif (
            not metadata_result
            and conference == "ICLR"
            and ICLR_DETAIL_RE.match(str(record.get("official_url", "")))
        ):
            try:
                metadata_response = active_fetcher.request_bytes(
                    "GET",
                    str(record["official_url"]),
                    timeout=(15, timeout),
                )
                abstract = extract_official_abstract(metadata_response.body)
                metadata_result = screen_metadata(title, abstract)
                metadata_fetch = metadata_dict(metadata_response.metadata)
            except (FetchError, RuntimeError) as error:
                result.update(
                    {
                        "status": "pending",
                        "reason": (
                            "Official abstract fetch failed; metadata-first policy did not request the PDF: "
                            f"{error}"
                        ),
                        "error_class": getattr(error, "error_class", "metadata-error"),
                        "challenge": getattr(error, "challenge", False),
                        "attempts": getattr(error, "attempts", None),
                        "http_status": getattr(error, "status_code", None),
                    }
                )
                return result
        elif not metadata_result:
            metadata_result = screen_metadata(title, None)
        if metadata_result:
            screen_status = metadata_result.get("screen_status", metadata_result.get("status"))
            screen_reason = metadata_result.get("screen_reason", metadata_result.get("reason"))
            result["metadata_screen"] = metadata_result
            if metadata_fetch:
                result["metadata_fetch"] = metadata_fetch
            result.update(
                {
                    "metadata_screen_status": screen_status,
                    "metadata_screen_reason": screen_reason,
                    "metadata_screen_matches": metadata_result.get("matched_terms", []),
                }
            )
            if screen_status == "filtered":
                result.update(
                    {
                        "status": "metadata-filtered",
                        "disposition": "excluded",
                        "reason": (
                            f"{screen_reason} PDF download was not requested by the metadata-first policy."
                        ),
                    }
                )
                return result
            if screen_status == "pending":
                result.update(
                    {
                        "status": "pending",
                        "reason": (
                            f"{screen_reason} PDF download was not requested by the metadata-first policy."
                        ),
                    }
                )
                return result
        elif metadata_first and pdf_scope == "metadata":
            result.update(
                {
                    "status": "pending",
                    "reason": (
                        "Official title/abstract metadata was not available; PDF download was not requested "
                        "by the metadata-first policy."
                    ),
                }
            )
            return result
    if not pdf_url:
        result.update(
            {
                "status": "pending",
                "reason": "No first-party PDF URL was exposed by the official list adapter after metadata screening.",
            }
        )
        return result
    try:
        fetched = active_fetcher.request_bytes(
            "GET",
            str(pdf_url),
            timeout=(15, timeout),
        )
        payload = fetched.body
        if "pdf" not in fetched.metadata.content_type.lower() and not payload.startswith(b"%PDF"):
            raise RuntimeError(
                f"source returned {fetched.metadata.content_type or 'unknown'} instead of PDF"
            )
        if not payload:
            raise RuntimeError("empty PDF response")
        text, extraction_method = extract_pdf_text(payload)
    except (FetchError, RuntimeError) as error:  # pragma: no cover - external source state
        result.update(
            {
                "status": "pending",
                "reason": str(error),
                "error_class": getattr(error, "error_class", "content-or-extraction-error"),
                "challenge": getattr(error, "challenge", False),
                "attempts": getattr(error, "attempts", None),
                "http_status": getattr(error, "status_code", None),
            }
        )
        return result

    pages = text.split("\f")
    product_matches: dict[str, list[dict[str, Any]]] = {}
    for product, pattern in PRODUCT_PATTERNS.items():
        hits = snippets_for_pattern(pages, pattern)
        if hits:
            product_matches[product] = hits
    product_model_candidates = {
        product: model_candidates(" ".join(str(hit["snippet"]) for hit in hits))
        for product, hits in product_matches.items()
    }
    generic_hits = snippets_for_pattern(pages, GENERIC_PATTERN)
    result.update(
        {
            "status": "scanned",
            "extraction_method": extraction_method,
            "page_count": len(pages),
            "text_chars": len(text),
            "product_matches": product_matches,
            "product_model_candidates": product_model_candidates,
            "generic_coding_agent_matches": generic_hits,
            "model_candidates": model_candidates(text),
            "fetch": metadata_dict(fetched.metadata),
        }
    )
    if product_matches:
        result["disposition"] = "pending"
        result["reason"] = (
            "Target industrial-product text was found; product context and exact experimental evidence require review before import."
        )
    else:
        result["disposition"] = "excluded"
        result["reason"] = (
            "Full-text scan found no Claude Code/Codex CLI product string; generic coding-agent or model/API mentions do not qualify for the main catalog."
        )
    return result


def record_key(conference: str, title: str) -> tuple[str, str]:
    return conference, normalize(title).casefold()


def update_census(census: dict[str, Any], results: list[dict[str, Any]]) -> None:
    by_key = {record_key(item["conference"], item["title"]): item for item in results}
    for conference in census.get("conferences", []):
        conference_name = conference["conference"]
        for paper in conference.get("papers", []):
            result = by_key.get(record_key(conference_name, paper["title"]))
            if not result:
                continue
            paper["full_text_scan"] = result["status"]
            paper["scan"] = {
                key: value
                for key, value in result.items()
                if key not in {"conference", "title", "official_url", "pdf_url"}
            }
            result_disposition = result.get("disposition")
            current_disposition = paper.get("disposition")
            context_review = paper.get("product_review", {})
            review_status = str(context_review.get("status", ""))
            reviewed_exclusion = review_status.startswith("excluded-after-context-review")
            if result_disposition == "excluded":
                if current_disposition not in {"included", "duplicate"} and not reviewed_exclusion:
                    paper["disposition"] = "excluded"
                    paper["disposition_reason"] = result["reason"]
            elif result_disposition == "pending":
                # A stale scan checkpoint must not undo a catalog promotion or
                # a later context review. Unreviewed records may advance to
                # pending when their PDF/metadata attempt fails.
                if current_disposition not in {"included", "duplicate"} and not reviewed_exclusion:
                    paper["disposition"] = "pending"
                    paper["disposition_reason"] = result["reason"]
        counts = {
            name: sum(paper["disposition"] == name for paper in conference.get("papers", []))
            for name in ["included", "excluded", "pending", "duplicate"]
        }
        conference["scanned_count"] = sum(
            paper.get("full_text_scan") == "scanned" for paper in conference.get("papers", [])
        )
        conference["metadata_screened_count"] = sum(
            paper.get("full_text_scan") == "metadata-filtered"
            for paper in conference.get("papers", [])
        )
        for name, value in counts.items():
            conference[f"{name}_count"] = value


def latest_manifest_records() -> dict[tuple[str, str], dict[str, Any]]:
    if not MANIFEST_PATH.exists():
        return {}
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        records[record_key(record["conference"], record["title"])] = record
    return records


def append_manifest(results: list[dict[str, Any]]) -> None:
    if not results:
        return
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("a", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", action="append", help="Only scan these conference IDs.")
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--per-host-concurrency", type=int, default=2)
    parser.add_argument("--per-host-delay", type=float, default=0.5)
    parser.add_argument(
        "--limit", type=int, default=0, help="Scan at most this many records; 0 means all."
    )
    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="Skip official records without a first-party PDF URL; they remain pending in the census.",
    )
    parser.add_argument("--no-update", action="store_true", help="Only write the JSONL manifest.")
    parser.add_argument(
        "--pdf-scope",
        choices=["metadata", "all"],
        default="metadata",
        help="Use official title/abstract triage before PDF downloads (default) or scan every PDF.",
    )
    parser.add_argument(
        "--no-metadata-first",
        action="store_true",
        help="Disable the ICLR metadata-first gate and use the legacy PDF-first behavior.",
    )
    parser.add_argument(
        "--skip-known-challenges",
        action="store_true",
        help="Do not retry records whose latest fetch is an explicit browser-verification challenge.",
    )
    args = parser.parse_args()
    if not CENSUS_INDEX_PATH.exists():
        print(f"Missing {CENSUS_INDEX_PATH}", file=sys.stderr)
        return 1
    census = load_census()
    manifest_records = latest_manifest_records()
    if manifest_records:
        update_census(census, list(manifest_records.values()))
    allowed = set(args.conference or [])
    jobs: list[tuple[str, dict[str, Any]]] = []
    for conference in census.get("conferences", []):
        name = str(conference["conference"])
        if allowed and name not in allowed:
            continue
        for paper in conference.get("papers", []):
            if paper.get("disposition") == "duplicate":
                continue
            if paper.get("full_text_scan") in {"scanned", "verified-manually"}:
                continue
            previous = manifest_records.get(record_key(name, paper["title"]))
            if previous and previous.get("status") in {"scanned", "metadata-filtered"}:
                continue
            if args.skip_known_challenges and previous and previous.get("challenge"):
                continue
            if args.pdf_only and not paper.get("pdf_url"):
                continue
            jobs.append((name, paper))
    if args.limit:
        jobs = jobs[: args.limit]
    print(f"Scanning {len(jobs)} official PDF records with {args.workers} workers.")
    fetcher = StableFetcher(
        user_agent="awesome-coding-agent-papers-fulltext/2.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=max(1, args.retries)),
        per_host_concurrency=max(1, args.per_host_concurrency),
        per_host_min_interval=max(0.0, args.per_host_delay),
    )
    results: list[dict[str, Any]] = []
    checkpoint: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(
                scan_record,
                conference,
                paper,
                args.timeout,
                fetcher,
                metadata_first=not args.no_metadata_first,
                pdf_scope=args.pdf_scope,
            ): (
                conference,
                paper["title"],
            )
            for conference, paper in jobs
        }
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            checkpoint.append(result)
            if len(checkpoint) >= 100:
                append_manifest(checkpoint)
                checkpoint.clear()
            if index % 25 == 0 or index == len(futures):
                print(f"completed {index}/{len(futures)}")
    results.sort(key=lambda item: record_key(item["conference"], item["title"]))
    append_manifest(checkpoint)
    if not args.no_update:
        update_census(census, results)
        write_census(census)
    counts: dict[str, int] = {}
    for result in results:
        key = result.get("disposition", result.get("status", "pending"))
        counts[key] = counts.get(key, 0) + 1
    print("scan summary:", ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
