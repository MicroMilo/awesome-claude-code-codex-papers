#!/usr/bin/env python3
"""Merge newly published Researchr accepted-paper lists into the live census."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

if __package__:
    from .build_conference_census import initial_disposition, parse_researchr
    from .source_fetcher import RetryPolicy, StableFetcher, metadata_dict
else:  # pragma: no cover - documented direct-script entry point
    from build_conference_census import initial_disposition, parse_researchr
    from source_fetcher import RetryPolicy, StableFetcher, metadata_dict

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"
CACHE_DIR = ROOT / "tmp" / "census"

VENUES: dict[str, dict[str, Any]] = {
    "PLDI": {
        "official_url": "https://pldi26.sigplan.org/track/pldi-2026-papers",
        "list_url": "https://pldi26.sigplan.org/track/pldi-2026-papers",
        "snapshot": "pldi-2026-research.html",
        "tracks": ["PLDI Research Papers"],
        "notes": "The official PLDI Research Papers page exposes the 2026 accepted-paper list and DOI links; track labels are preserved per record.",
    },
    "POPL": {
        "official_url": "https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers",
        "list_url": "https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers",
        "snapshot": "popl-2026-research.html",
        "tracks": ["POPL"],
        "notes": "The official POPL Research Papers page exposes the complete accepted-paper list with DOI links.",
    },
    "OOPSLA": {
        "official_url": "https://conf.researchr.org/track/splash-2026/oopsla-2026",
        "list_url": "https://conf.researchr.org/track/splash-2026/oopsla-2026",
        "snapshot": "oopsla-2026.html",
        "tracks": ["OOPSLA"],
        "notes": "The official OOPSLA 2026 page exposes accepted papers from the 2026 review rounds; records remain tied to the official OOPSLA track.",
    },
}


def normalize(value: object) -> str:
    return " ".join(str(value or "").split()).strip().casefold()


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
    for field in ("pdf_url", "doi_url", "official_record_id"):
        if raw.get(field):
            record[field] = raw[field]
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", action="append", choices=sorted(VENUES))
    parser.add_argument("--no-fetch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--retries", type=int, default=4)
    args = parser.parse_args()

    selected = set(args.conference or VENUES)
    audited_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    fetcher = StableFetcher(
        user_agent="awesome-coding-agent-papers-researchr/1.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=max(1, args.retries)),
        per_host_concurrency=1,
        per_host_min_interval=0.5,
    )
    parsed: dict[str, tuple[list[dict[str, Any]], dict[str, Any] | None]] = {}
    for conference in selected:
        venue = VENUES[conference]
        snapshot = CACHE_DIR / str(venue["snapshot"])
        fetch_metadata = None
        if not args.no_fetch:
            fetched = fetcher.request_bytes(
                "GET", str(venue["list_url"]), timeout=(15, args.timeout)
            )
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes(fetched.body)
            fetch_metadata = metadata_dict(fetched.metadata)
        if not snapshot.exists():
            raise FileNotFoundError(f"Missing official snapshot: {snapshot}")
        records = parse_researchr(snapshot, venue)
        if not records:
            raise RuntimeError(f"Official {conference} page yielded no accepted-paper records")
        parsed[conference] = (records, fetch_metadata)
        print(f"{conference}: parsed {len(records)} official records")

    if args.dry_run:
        return 0

    census = yaml.safe_load(CENSUS_PATH.read_text(encoding="utf-8"))
    by_conference = {item["conference"]: item for item in census.get("conferences", [])}
    for conference in selected:
        venue = VENUES[conference]
        records, fetch_metadata = parsed[conference]
        section = by_conference.get(conference)
        if section is None:
            section = {"conference": conference, "year": 2026, "papers": []}
            census.setdefault("conferences", []).append(section)
        existing = {
            (normalize(item.get("title")), normalize(item.get("track"))): item
            for item in section.get("papers", [])
        }
        merged: list[dict[str, Any]] = []
        for raw in records:
            key = (normalize(raw.get("title")), normalize(raw.get("track")))
            merged.append(existing.get(key) or new_record(raw, conference, str(venue["list_url"])))
        section.update(
            {
                "official_url": venue["official_url"],
                "list_url": venue["list_url"],
                "status": "accepted-list",
                "tracks": venue["tracks"],
                "notes": venue["notes"],
                "fetched_at": audited_at,
                "paper_count": len(merged),
                "papers": merged,
            }
        )
        if fetch_metadata:
            section["list_fetch"] = fetch_metadata
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

    census["last_audited_at"] = audited_at
    CENSUS_PATH.write_text(
        yaml.safe_dump(census, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
