#!/usr/bin/env python3
"""Refresh IJCAI, KDD, and NeurIPS from first-party 2026 sources.

IJCAI and KDD now expose official paper lists that were unavailable when the
original census was built. This script merges those records without resetting
existing audit decisions. NeurIPS remains a publication-status check until its
official OpenReview group releases public accepted submissions.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

if __package__:
    from .build_conference_census import (
        IJCAI_TRACKS,
        REGISTRY,
        initial_disposition,
        parse_ijcai,
        parse_kdd,
    )
    from .census_store import load_census, write_census
    from .source_fetcher import RetryPolicy, StableFetcher, metadata_dict
else:  # pragma: no cover - documented direct-script entry point
    from build_conference_census import (
        IJCAI_TRACKS,
        REGISTRY,
        initial_disposition,
        parse_ijcai,
        parse_kdd,
    )
    from census_store import load_census, write_census
    from source_fetcher import RetryPolicy, StableFetcher, metadata_dict

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "tmp" / "census"
SUPPORTED = {"IJCAI", "KDD", "NeurIPS"}


def normalize(value: object) -> str:
    return " ".join(str(value or "").split()).strip().casefold()


def registry_for(conference: str) -> dict[str, Any]:
    return next(dict(item) for item in REGISTRY if item["conference"] == conference)


def new_record(raw: dict[str, Any], conference: str, list_url: str) -> dict[str, Any]:
    disposition, reason = initial_disposition(raw, conference)
    record: dict[str, Any] = {
        "title": raw["title"],
        "official_url": raw.get("official_url", list_url),
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
            record[field] = raw[field]
    return record


def merge_record(
    current: dict[str, Any] | None, raw: dict[str, Any], conference: str, list_url: str
) -> dict[str, Any]:
    if current is None:
        return new_record(raw, conference, list_url)
    current["title"] = raw["title"]
    current["official_url"] = raw.get("official_url", list_url)
    current["track"] = raw.get("track", "Unknown track")
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
            current[field] = raw[field]
    return current


def mark_duplicate_records(records: list[dict[str, Any]]) -> None:
    seen: dict[str, str] = {}
    for record in records:
        key = normalize(record.get("title"))
        first = seen.get(key)
        if first is None:
            seen[key] = str(record.get("official_record_id") or record.get("official_url"))
            continue
        if record.get("disposition") == "included":
            raise RuntimeError(f"Duplicate official title is already included: {record['title']}")
        record["disposition"] = "duplicate"
        record["disposition_reason"] = f"Duplicate official title; first occurrence is {first}."
        record["full_text_scan"] = "duplicate"


def fetch_ijcai(
    fetcher: StableFetcher, timeout: int, no_fetch: bool
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    venue = registry_for("IJCAI")
    records: list[dict[str, Any]] = []
    fetches: list[dict[str, Any]] = []
    for track_slug, track_name in IJCAI_TRACKS:
        track_url = f"{venue['list_url']}?{urlencode({'ijtrack': track_slug})}"
        snapshot = CACHE_DIR / f"ijcai-2026-{track_slug}.html"
        if not no_fetch:
            fetched = fetcher.request_bytes("GET", track_url, timeout=(15, timeout))
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes(fetched.body)
            fetches.append({"track": track_name, **metadata_dict(fetched.metadata)})
        if not snapshot.exists():
            raise FileNotFoundError(f"Missing official IJCAI snapshot: {snapshot}")
        track_registry = {**venue, "list_url": track_url, "track_name": track_name}
        records.extend(parse_ijcai(snapshot, track_registry))
    ids = [str(item.get("official_record_id", "")) for item in records]
    if len(records) != len(set(ids)):
        raise RuntimeError("Official IJCAI track pages yielded duplicate paper identifiers")
    return sorted(records, key=lambda item: normalize(item["title"])), fetches


def fetch_kdd(
    fetcher: StableFetcher, timeout: int, no_fetch: bool
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    venue = registry_for("KDD")
    snapshot = CACHE_DIR / str(venue["snapshot"])
    fetches: list[dict[str, Any]] = []
    if not no_fetch:
        fetched = fetcher.request_bytes("GET", str(venue["list_url"]), timeout=(15, timeout))
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(fetched.body)
        fetches.append(metadata_dict(fetched.metadata))
    if not snapshot.exists():
        raise FileNotFoundError(f"Missing official KDD snapshot: {snapshot}")
    return parse_kdd(snapshot, venue), fetches


def refresh_neurips_status(
    section: dict[str, Any], fetcher: StableFetcher, timeout: int, audited_at: str
) -> None:
    group_id = "NeurIPS.cc/2026/Conference"
    url = f"https://api2.openreview.net/groups?{urlencode({'id': group_id})}"
    fetched = fetcher.request_bytes("GET", url, timeout=(15, timeout))
    payload = json.loads(fetched.body)
    groups = payload.get("groups", [])
    if len(groups) != 1:
        raise RuntimeError("Official NeurIPS OpenReview group was not returned uniquely")
    content = groups[0].get("content", {})
    public_submissions = bool(content.get("public_submissions", {}).get("value"))
    existing_papers = list(section.get("papers", []))
    if existing_papers:
        raise RuntimeError(
            "Refusing to replace an existing NeurIPS census with a publication-status "
            "check; use an accepted-list adapter once official records are public."
        )
    section.update(
        {
            "official_url": "https://neurips.cc/",
            "list_url": "https://openreview.net/group?id=NeurIPS.cc%2F2026%2FConference",
            "status": "pending",
            "tracks": ["Conference"],
            "fetched_at": audited_at,
            "paper_count": None,
            "notes": (
                "The official OpenReview group is registered, but public submissions and an accepted-paper list are not released. No preprint list is substituted."
                if not public_submissions
                else "The official OpenReview group now exposes submissions, but an accepted-paper-only census still requires confirmation before import."
            ),
            "source_check": {
                "group_id": group_id,
                "public_submissions": public_submissions,
                "fetch": metadata_dict(fetched.metadata),
            },
            "papers": [],
            "scanned_count": 0,
            "metadata_screened_count": 0,
            "included_count": 0,
            "excluded_count": 0,
            "pending_count": 0,
            "duplicate_count": 0,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", action="append", choices=sorted(SUPPORTED))
    parser.add_argument("--no-fetch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--retries", type=int, default=4)
    args = parser.parse_args()

    selected = set(args.conference or SUPPORTED)
    audited_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    fetcher = StableFetcher(
        user_agent="awesome-coding-agent-papers-official-lists/1.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=max(1, args.retries)),
        per_host_concurrency=1,
        per_host_min_interval=0.5,
    )
    parsed: dict[str, tuple[list[dict[str, Any]], list[dict[str, Any]]]] = {}
    if "IJCAI" in selected:
        parsed["IJCAI"] = fetch_ijcai(fetcher, args.timeout, args.no_fetch)
        print(f"IJCAI: parsed {len(parsed['IJCAI'][0])} official records")
    if "KDD" in selected:
        parsed["KDD"] = fetch_kdd(fetcher, args.timeout, args.no_fetch)
        print(f"KDD: parsed {len(parsed['KDD'][0])} official records")
    if args.dry_run:
        return 0

    census = load_census()
    by_conference = {str(item["conference"]): item for item in census.get("conferences", [])}
    for conference, (records, fetches) in parsed.items():
        venue = registry_for(conference)
        section = by_conference.get(conference)
        if section is None:
            section = {"conference": conference, "year": 2026, "papers": []}
            census.setdefault("conferences", []).append(section)
            by_conference[conference] = section
        current_by_id = {
            str(item.get("official_record_id")): item
            for item in section.get("papers", [])
            if item.get("official_record_id")
        }
        current_by_title = {
            normalize(item.get("title")): item for item in section.get("papers", [])
        }
        merged = [
            merge_record(
                current_by_id.get(str(raw.get("official_record_id")))
                or current_by_title.get(normalize(raw.get("title"))),
                raw,
                conference,
                str(venue["list_url"]),
            )
            for raw in records
        ]
        mark_duplicate_records(merged)
        current_ids = {id(item) for item in merged}
        removed_included = [
            item
            for item in section.get("papers", [])
            if id(item) not in current_ids and item.get("disposition") == "included"
        ]
        if removed_included:
            raise RuntimeError(
                f"Official {conference} refresh omitted previously included records: "
                + ", ".join(str(item.get("title")) for item in removed_included)
            )
        section.update(
            {
                "official_url": venue["official_url"],
                "list_url": venue["list_url"],
                "status": venue["status"],
                "tracks": venue["tracks"],
                "notes": venue["notes"],
                "fetched_at": audited_at,
                "paper_count": len(merged),
                "papers": merged,
                "list_fetches": fetches,
            }
        )
        counts = {
            disposition: sum(item.get("disposition") == disposition for item in merged)
            for disposition in ("included", "excluded", "pending", "duplicate")
        }
        section["scanned_count"] = sum(
            item.get("full_text_scan") in {"scanned", "verified-manually"} for item in merged
        )
        section["metadata_screened_count"] = sum(
            item.get("full_text_scan") == "metadata-filtered" for item in merged
        )
        section["pdf_url_count"] = sum(bool(item.get("pdf_url")) for item in merged)
        for disposition, count in counts.items():
            section[f"{disposition}_count"] = count

    if "NeurIPS" in selected:
        section = by_conference.get("NeurIPS")
        if section is None:
            section = {"conference": "NeurIPS", "year": 2026, "papers": []}
            census.setdefault("conferences", []).append(section)
        refresh_neurips_status(section, fetcher, args.timeout, audited_at)
        print("NeurIPS: accepted list is still pending")

    census["last_audited_at"] = audited_at
    write_census(census, only=selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
