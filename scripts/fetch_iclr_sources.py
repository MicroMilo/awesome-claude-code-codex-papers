#!/usr/bin/env python3
"""Fetch ICLR 2026 official sources into resumable, auditable artifacts.

The main proceedings index is the authority for the conference-paper census.
The Downloads export provides track-aware event data, while OpenReview is an
optional metadata/review enrichment source.  A challenge on one source is
recorded as ``pending`` and does not cause another source to be silently
substituted.
"""

from __future__ import annotations

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

if __package__:
    from .metadata_relevance import SCREEN_VERSION, screen_metadata
    from .source_fetcher import (
        FetchError,
        JsonlLedger,
        RetryPolicy,
        StableFetcher,
        metadata_dict,
        sha256_bytes,
        utc_now,
    )
else:  # pragma: no cover - exercised by the documented direct-script command
    from metadata_relevance import SCREEN_VERSION, screen_metadata
    from source_fetcher import (
        FetchError,
        JsonlLedger,
        RetryPolicy,
        StableFetcher,
        metadata_dict,
        sha256_bytes,
        utc_now,
    )

ROOT = Path(__file__).resolve().parents[1]
YEAR = 2026
PROCEEDINGS_INDEX_URL = f"https://proceedings.iclr.cc/paper_files/paper/{YEAR}"
DOWNLOADS_URL = f"https://iclr.cc/Downloads/{YEAR}"
OPENREVIEW_NOTES_URL = "https://api2.openreview.net/notes"
OPENREVIEW_VENUE_ID = f"ICLR.cc/{YEAR}/Conference"
PAPER_LINK_RE = re.compile(
    rf"/paper_files/paper/{YEAR}/hash/([0-9a-f]+)-Abstract-Conference\.html$",
    re.IGNORECASE,
)
TRACK_FIELDS = {
    "posters": "posters",
    "tutorials": "tutorials",
    "invited-talks": "invited_talks",
    "workshops": "workshops",
    "demonstrations": "demonstrations",
}
FORMAT_IDS = {"csv": "0", "xls": "1", "xlsx": "2", "tsv": "3", "ods": "4", "json": "5", "yaml": "6"}


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".part")
    partial.write_bytes(payload)
    partial.replace(path)


def parse_proceedings_index(payload: bytes) -> list[dict[str, Any]]:
    """Parse the official proceedings book without inferring paper status."""

    soup = BeautifulSoup(payload, "html.parser")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for link in soup.find_all("a", href=True):
        href = urljoin(PROCEEDINGS_INDEX_URL + "/", str(link["href"]))
        match = PAPER_LINK_RE.search(href)
        if not match or href in seen:
            continue
        title = normalize_text(link.get_text(" ", strip=True))
        if not title:
            continue
        seen.add(href)
        records.append(
            {
                "paper_id": match.group(1).lower(),
                "title": title,
                "official_url": href,
                "conference": "ICLR",
                "venue": "ICLR Conference",
                "year": YEAR,
                "track": "Conference",
            }
        )
    return records


def parse_proceedings_detail(payload: bytes, detail_url: str) -> dict[str, Any]:
    soup = BeautifulSoup(payload, "html.parser")
    heading = soup.find("h1")
    title = normalize_text(heading.get_text(" ", strip=True)) if heading else ""
    abstract_node = soup.select_one(".paper-abstract")
    abstract = normalize_text(abstract_node.get_text(" ", strip=True)) if abstract_node else ""
    if not abstract:
        description = soup.select_one('meta[name="description"]')
        abstract = normalize_text(str(description.get("content", ""))) if description else ""
    pdf_url = ""
    supplementary_url = ""
    for link in soup.find_all("a", href=True):
        href = urljoin(detail_url, str(link["href"]))
        if re.search(r"-Paper-Conference\.pdf$", href, re.IGNORECASE):
            pdf_url = href
        elif re.search(r"-(?:Supplemental|Supplementary).*\.pdf$", href, re.IGNORECASE):
            supplementary_url = href
    return {
        "title": title,
        "abstract": abstract,
        "pdf_url": pdf_url,
        "supplementary_url": supplementary_url,
    }


def build_download_payload(token: str, tracks: list[str]) -> dict[str, str]:
    payload = {
        "csrfmiddlewaretoken": token,
        "format": FORMAT_IDS["json"],
        "resource": "0",
        "submitaction": "Download Data",
    }
    for track in tracks:
        payload[TRACK_FIELDS[track]] = "on"
    return payload


def source_base_record(
    *,
    source_key: str,
    source_kind: str,
    source_url: str,
    status: str,
    paper_key: str | None = None,
    reason: str | None = None,
    metadata: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "source_key": source_key,
        "source_kind": source_kind,
        "source_url": source_url,
        "status": status,
    }
    if paper_key:
        record["paper_key"] = paper_key
    if reason:
        record["reason"] = reason
    if metadata:
        record.update(
            {
                "http_status": metadata.get("status_code"),
                "content_type": metadata.get("content_type"),
                "etag": metadata.get("etag"),
                "last_modified": metadata.get("last_modified"),
                "sha256": metadata.get("sha256"),
                "byte_size": metadata.get("byte_size"),
                "attempts": metadata.get("attempts"),
                "retrieved_at": metadata.get("retrieved_at"),
            }
        )
    record.update(extra)
    return record


def fetch_proceedings(
    *,
    fetcher: StableFetcher,
    ledger: JsonlLedger,
    raw_dir: Path,
    output: Path,
    pdf_dir: Path,
    workers: int,
    offset: int,
    limit: int,
    refresh: bool,
    metadata_only: bool,
    fetch_pdfs: bool,
    pdf_scope: str,
) -> dict[str, Any]:
    index_raw = raw_dir / "proceedings-index.html"
    if index_raw.exists() and not refresh:
        index_payload = index_raw.read_bytes()
        index_status = "cached"
        index_meta = {"sha256": sha256_bytes(index_payload), "byte_size": len(index_payload)}
    else:
        fetched = fetcher.request_bytes("GET", PROCEEDINGS_INDEX_URL)
        index_payload = fetched.body
        atomic_write(index_raw, index_payload)
        index_status = "success"
        index_meta = metadata_dict(fetched.metadata)
        ledger.append(
            source_base_record(
                source_key=f"iclr:{YEAR}:proceedings:index",
                source_kind="official-proceedings-index",
                source_url=PROCEEDINGS_INDEX_URL,
                status="success",
                metadata=index_meta,
                local_path=str(index_raw.relative_to(ROOT)),
                parser_version="iclr-source-fetcher/2",
            )
        )

    records = parse_proceedings_index(index_payload)
    previous = load_jsonl(output)
    previous_by_key = {item.get("paper_key"): item for item in previous if item.get("paper_key")}
    start = max(0, offset)
    selected = records[start:] if limit <= 0 else records[start : start + limit]

    def fetch_one(record: dict[str, Any]) -> dict[str, Any]:
        paper_key = f"iclr:{YEAR}:proceedings:{record['paper_id']}"
        existing = previous_by_key.get(paper_key)
        existing_screen_status = existing.get("metadata_screen_status") if existing else None
        existing_pdf_ready = existing and existing.get("pdf_status") in {"success", "cached"}
        existing_pdf_done = bool(
            not fetch_pdfs
            or pdf_scope == "all"
            and existing_pdf_ready
            or pdf_scope == "metadata"
            and existing_screen_status in {"filtered", "pending"}
            or pdf_scope == "metadata"
            and existing_screen_status == "candidate"
            and existing_pdf_ready
        )
        if (
            existing
            and existing.get("detail_status") == "success"
            and existing.get("pdf_url")
            and not refresh
            and existing_pdf_done
        ):
            return existing
        result: dict[str, Any] = {
            **record,
            "paper_key": paper_key,
            "detail_status": "not-requested",
        }
        if metadata_only:
            return result
        try:
            fetched = fetcher.request_bytes("GET", record["official_url"])
            detail_raw = raw_dir / "details" / f"{record['paper_id']}.html"
            atomic_write(detail_raw, fetched.body)
            detail = parse_proceedings_detail(fetched.body, record["official_url"])
            result.update(detail)
            screen = screen_metadata(record["title"], detail.get("abstract"))
            result.update({f"metadata_{key}": value for key, value in screen.items()})
            result["detail_status"] = "success" if detail.get("pdf_url") else "pending"
            if not detail.get("pdf_url"):
                result["detail_reason"] = (
                    "Official proceedings page did not expose a conference PDF link."
                )
            detail_key = f"{paper_key}:detail"
            ledger.append(
                source_base_record(
                    source_key=detail_key,
                    source_kind="official-proceedings-detail",
                    source_url=record["official_url"],
                    status=result["detail_status"],
                    paper_key=paper_key,
                    reason=result.get("detail_reason"),
                    metadata=metadata_dict(fetched.metadata),
                    local_path=str(detail_raw.relative_to(ROOT)),
                    parser_version="iclr-source-fetcher/2",
                    title=record["title"],
                    abstract_chars=screen["abstract_chars"],
                    metadata_screen_status=screen["screen_status"],
                    metadata_screen_reason=screen["screen_reason"],
                    pdf_url=detail.get("pdf_url"),
                )
            )
            pdf_candidate = screen["screen_status"] == "candidate"
            should_fetch_pdf = (
                fetch_pdfs and detail.get("pdf_url") and (pdf_scope == "all" or pdf_candidate)
            )
            if fetch_pdfs and detail.get("pdf_url") and not should_fetch_pdf:
                if existing and existing.get("pdf_status") in {"success", "cached"}:
                    result["pdf_status"] = existing["pdf_status"]
                    result["pdf_reason"] = (
                        "A PDF was already cached before the metadata screen; no new PDF request was made."
                    )
                elif screen["screen_status"] == "filtered":
                    result["pdf_status"] = "skipped"
                    result["pdf_reason"] = (
                        "Metadata screen found no high-recall coding-agent, code, software-engineering, "
                        "or language-model combination; PDF download was not requested."
                    )
                else:
                    result["pdf_status"] = "pending"
                    result["pdf_reason"] = (
                        "Metadata screen could not establish relevance because the official abstract was missing; "
                        "use --pdf-scope all to force a full-text acquisition."
                    )
                ledger.append(
                    source_base_record(
                        source_key=f"{paper_key}:pdf",
                        source_kind="official-proceedings-pdf",
                        source_url=str(detail["pdf_url"]),
                        status=result["pdf_status"],
                        paper_key=paper_key,
                        reason=result["pdf_reason"],
                        parser_version="iclr-source-fetcher/2",
                        title=record["title"],
                        metadata_screen_version=SCREEN_VERSION,
                        metadata_screen_status=screen["screen_status"],
                    )
                )
            elif should_fetch_pdf:
                pdf_path = pdf_dir / f"{record['paper_id']}.pdf"
                try:
                    pdf_meta = fetcher.download(
                        str(detail["pdf_url"]),
                        pdf_path,
                        expected_prefix=b"%PDF",
                        refresh=refresh,
                    )
                    result["pdf_status"] = (
                        "cached" if pdf_meta.content_type == "cached" else "success"
                    )
                    result["pdf_path"] = str(pdf_path.relative_to(ROOT))
                    ledger.append(
                        source_base_record(
                            source_key=f"{paper_key}:pdf",
                            source_kind="official-proceedings-pdf",
                            source_url=str(detail["pdf_url"]),
                            status=result["pdf_status"],
                            paper_key=paper_key,
                            metadata=metadata_dict(pdf_meta),
                            local_path=result["pdf_path"],
                            parser_version="iclr-source-fetcher/2",
                            title=record["title"],
                        )
                    )
                except FetchError as error:
                    result["pdf_status"] = "pending"
                    result["pdf_reason"] = str(error)
                    ledger.append(
                        source_base_record(
                            source_key=f"{paper_key}:pdf",
                            source_kind="official-proceedings-pdf",
                            source_url=str(detail["pdf_url"]),
                            status="pending",
                            paper_key=paper_key,
                            reason=str(error),
                            parser_version="iclr-source-fetcher/2",
                            title=record["title"],
                            error_class=error.error_class,
                            challenge=error.challenge,
                            attempts=error.attempts,
                        )
                    )
            return result
        except FetchError as error:
            result["detail_status"] = "pending"
            result["detail_reason"] = str(error)
            ledger.append(
                source_base_record(
                    source_key=f"{paper_key}:detail",
                    source_kind="official-proceedings-detail",
                    source_url=record["official_url"],
                    status="pending",
                    paper_key=paper_key,
                    reason=str(error),
                    parser_version="iclr-source-fetcher/2",
                    title=record["title"],
                    error_class=error.error_class,
                    challenge=error.challenge,
                    http_status=error.status_code,
                    attempts=error.attempts,
                )
            )
            return result

    results: dict[str, dict[str, Any]] = {}
    if selected and not metadata_only:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
            futures = {
                executor.submit(fetch_one, record): record["paper_id"] for record in selected
            }
            for future in as_completed(futures):
                result = future.result()
                results[result["paper_key"]] = result
    elif selected:
        for record in selected:
            result = fetch_one(record)
            results[result["paper_key"]] = result

    inventory: list[dict[str, Any]] = []
    for record in records:
        key = f"iclr:{YEAR}:proceedings:{record['paper_id']}"
        inventory.append(
            results.get(key) or previous_by_key.get(key) or {**record, "paper_key": key}
        )
    write_jsonl(output, inventory)
    return {
        "source": "proceedings",
        "status": "success",
        "index_status": index_status,
        "official_count": len(records),
        "details_offset": start,
        "details_requested": len(selected) if not metadata_only else 0,
        "details_success": sum(item.get("detail_status") == "success" for item in inventory),
        "metadata_screened": sum(
            item.get("metadata_screen_status") in {"candidate", "filtered", "pending"}
            for item in inventory
        ),
        "metadata_candidates": sum(
            item.get("metadata_screen_status") == "candidate" for item in inventory
        ),
        "metadata_filtered": sum(
            item.get("metadata_screen_status") == "filtered" for item in inventory
        ),
        "metadata_pending": sum(
            item.get("metadata_screen_status") == "pending" for item in inventory
        ),
        "pdf_scope": pdf_scope,
        "pdf_requested": sum(
            item.get("pdf_status") in {"success", "cached", "pending"}
            and item.get("metadata_screen_status") == "candidate"
            for item in inventory
        ),
        "pdf_skipped": sum(item.get("pdf_status") == "skipped" for item in inventory),
        "pdf_success": sum(item.get("pdf_status") in {"success", "cached"} for item in inventory),
        "output": str(output.relative_to(ROOT)),
        "index_sha256": index_meta["sha256"],
    }


def fetch_downloads_export(
    *,
    fetcher: StableFetcher,
    ledger: JsonlLedger,
    raw_dir: Path,
    tracks: list[str],
    refresh: bool,
) -> dict[str, Any]:
    slug = "-".join(tracks)
    raw_path = raw_dir / f"downloads-{slug}.json"
    if raw_path.exists() and not refresh:
        payload = raw_path.read_bytes()
        status = "cached"
        metadata = {"sha256": sha256_bytes(payload), "byte_size": len(payload)}
    else:
        page = fetcher.request_bytes("GET", DOWNLOADS_URL)
        soup = BeautifulSoup(page.body, "html.parser")
        token = soup.select_one("input[name=csrfmiddlewaretoken]")
        if token is None or not token.get("value"):
            raise RuntimeError("ICLR Downloads page did not expose a CSRF token")
        exported = fetcher.request_bytes(
            "POST",
            DOWNLOADS_URL,
            data=build_download_payload(str(token["value"]), tracks),
            headers={"Referer": DOWNLOADS_URL},
            timeout=(15.0, 300.0),
        )
        if "text/html" in exported.metadata.content_type.lower():
            raise RuntimeError("ICLR Downloads returned HTML instead of the requested export")
        payload = exported.body
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError as error:
            raise RuntimeError("ICLR Downloads export was not valid JSON") from error
        if not isinstance(parsed, list):
            raise RuntimeError("ICLR Downloads JSON export did not contain a list")
        atomic_write(raw_path, payload)
        status = "success"
        metadata = metadata_dict(exported.metadata)
        ledger.append(
            source_base_record(
                source_key=f"iclr:{YEAR}:downloads:json:{slug}",
                source_kind="official-downloads-export",
                source_url=DOWNLOADS_URL,
                status="success",
                metadata=metadata,
                local_path=str(raw_path.relative_to(ROOT)),
                parser_version="iclr-source-fetcher/2",
                format="json",
                tracks=tracks,
                record_count=len(parsed),
            )
        )
    parsed = json.loads(payload)
    return {
        "source": "downloads",
        "status": "success",
        "cache_status": status,
        "tracks": tracks,
        "record_count": len(parsed),
        "sha256": metadata["sha256"],
        "output": str(raw_path.relative_to(ROOT)),
    }


def fetch_openreview_notes(
    *,
    fetcher: StableFetcher,
    ledger: JsonlLedger,
    raw_dir: Path,
    limit: int,
    page_size: int,
    refresh: bool,
) -> dict[str, Any]:
    page_size = max(1, min(page_size, 1000))
    records: list[dict[str, Any]] = []
    offset = 0
    while limit <= 0 or len(records) < limit:
        page_number = offset // page_size
        raw_path = raw_dir / "openreview" / f"notes-{page_number:04d}.json"
        try:
            if raw_path.exists() and not refresh:
                payload = raw_path.read_bytes()
                page_metadata = {"sha256": sha256_bytes(payload), "byte_size": len(payload)}
            else:
                fetched = fetcher.request_bytes(
                    "GET",
                    OPENREVIEW_NOTES_URL,
                    params={
                        "venueid": OPENREVIEW_VENUE_ID,
                        "limit": page_size,
                        "offset": offset,
                        "count": "true",
                    },
                )
                payload = fetched.body
                page_metadata = metadata_dict(fetched.metadata)
                atomic_write(raw_path, payload)
            data = json.loads(payload)
            notes = data.get("notes", [])
            if not isinstance(notes, list):
                raise RuntimeError("OpenReview response did not contain a notes list")
            ledger.append(
                source_base_record(
                    source_key=f"iclr:{YEAR}:openreview:notes:{page_number}",
                    source_kind="openreview-api-v2",
                    source_url=OPENREVIEW_NOTES_URL,
                    status="success",
                    metadata=page_metadata,
                    local_path=str(raw_path.relative_to(ROOT)),
                    parser_version="iclr-source-fetcher/2",
                    venue_id=OPENREVIEW_VENUE_ID,
                    offset=offset,
                    limit=page_size,
                    record_count=len(notes),
                    total=data.get("count"),
                )
            )
            for note in notes:
                content = note.get("content", {}) if isinstance(note, dict) else {}
                title_value = content.get("title", "") if isinstance(content, dict) else ""
                if isinstance(title_value, dict):
                    title_value = title_value.get("value", "")
                note_id = str(note.get("id", ""))
                records.append(
                    {
                        "paper_key": f"iclr:{YEAR}:openreview:{note_id}",
                        "conference": "ICLR",
                        "venue": "ICLR Conference",
                        "year": YEAR,
                        "title": normalize_text(str(title_value)),
                        "official_url": f"https://openreview.net/forum?id={note_id}",
                        "pdf_url": f"https://openreview.net/pdf?id={note_id}",
                        "openreview_id": note_id,
                        "source_type": "openreview-conference",
                    }
                )
                if limit > 0 and len(records) >= limit:
                    break
            if not notes or len(notes) < page_size:
                break
            offset += page_size
        except (FetchError, json.JSONDecodeError, RuntimeError) as error:
            ledger.append(
                source_base_record(
                    source_key=f"iclr:{YEAR}:openreview:notes:{page_number}",
                    source_kind="openreview-api-v2",
                    source_url=OPENREVIEW_NOTES_URL,
                    status="pending",
                    reason=str(error),
                    parser_version="iclr-source-fetcher/2",
                    venue_id=OPENREVIEW_VENUE_ID,
                    offset=offset,
                    limit=page_size,
                    error_class=getattr(error, "error_class", "parse-error"),
                    challenge=getattr(error, "challenge", False),
                    http_status=getattr(error, "status_code", None),
                    attempts=getattr(error, "attempts", None),
                )
            )
            return {
                "source": "openreview",
                "status": "pending",
                "reason": str(error),
                "records": len(records),
                "venue_id": OPENREVIEW_VENUE_ID,
            }
    output = raw_dir / "openreview" / "notes-normalized.jsonl"
    write_jsonl(output, records)
    return {
        "source": "openreview",
        "status": "success",
        "records": len(records),
        "venue_id": OPENREVIEW_VENUE_ID,
        "output": str(output.relative_to(ROOT)),
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    payload = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    atomic_write(path, payload.encode("utf-8"))


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", choices=["proceedings", "downloads", "openreview", "all"], default="proceedings"
    )
    parser.add_argument("--track", action="append", choices=sorted(TRACK_FIELDS), default=None)
    parser.add_argument(
        "--offset", type=int, default=0, help="Skip this many proceedings records before batching."
    )
    parser.add_argument(
        "--limit", type=int, default=0, help="Limit detail/API records after --offset; 0 means all."
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument("--per-host-concurrency", type=int, default=2)
    parser.add_argument("--per-host-delay", type=float, default=0.35)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--fetch-pdfs", action="store_true")
    parser.add_argument(
        "--pdf-scope",
        choices=["metadata", "all"],
        default="metadata",
        help="When --fetch-pdfs is set, download only metadata candidates (default) or every paper.",
    )
    parser.add_argument("--raw-dir", type=Path, default=Path("tmp/crawl/iclr-2026/raw"))
    parser.add_argument("--pdf-dir", type=Path, default=Path("tmp/crawl/iclr-2026/pdfs"))
    parser.add_argument("--manifest", type=Path, default=Path("data/audit/2026-source-fetch.jsonl"))
    parser.add_argument(
        "--output", type=Path, default=Path("tmp/crawl/iclr-2026/proceedings.jsonl")
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    raw_dir = resolve_path(args.raw_dir)
    pdf_dir = resolve_path(args.pdf_dir)
    manifest_path = resolve_path(args.manifest)
    output = resolve_path(args.output)
    policy = RetryPolicy(max_attempts=max(1, args.retries))
    fetcher = StableFetcher(
        user_agent="awesome-claude-code-codex-papers-source-fetcher/1.0 (+official-source-audit)",
        retry_policy=policy,
        per_host_concurrency=max(1, args.per_host_concurrency),
        per_host_min_interval=max(0.0, args.per_host_delay),
    )
    ledger = JsonlLedger(manifest_path)
    summary: dict[str, Any] = {
        "conference": "ICLR",
        "year": YEAR,
        "started_at": utc_now(),
        "manifest": str(manifest_path.relative_to(ROOT)),
        "sources": [],
    }
    if args.source in {"proceedings", "all"}:
        summary["sources"].append(
            fetch_proceedings(
                fetcher=fetcher,
                ledger=ledger,
                raw_dir=raw_dir,
                output=output,
                pdf_dir=pdf_dir,
                workers=args.workers,
                offset=args.offset,
                limit=args.limit,
                refresh=args.refresh,
                metadata_only=args.metadata_only,
                fetch_pdfs=args.fetch_pdfs,
                pdf_scope=args.pdf_scope,
            )
        )
    if args.source in {"downloads", "all"}:
        tracks = args.track or ["posters"]
        summary["sources"].append(
            fetch_downloads_export(
                fetcher=fetcher,
                ledger=ledger,
                raw_dir=raw_dir,
                tracks=tracks,
                refresh=args.refresh,
            )
        )
    if args.source in {"openreview", "all"}:
        summary["sources"].append(
            fetch_openreview_notes(
                fetcher=fetcher,
                ledger=ledger,
                raw_dir=raw_dir,
                limit=args.limit,
                page_size=args.page_size,
                refresh=args.refresh,
            )
        )
    summary["finished_at"] = utc_now()
    summary_path = raw_dir.parent / "fetch-summary.json"
    atomic_write(summary_path, json.dumps(summary, ensure_ascii=False, indent=2).encode("utf-8"))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
