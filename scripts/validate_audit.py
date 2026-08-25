#!/usr/bin/env python3
"""Validate the conference census, disposition ledger, and catalog boundary."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import yaml

if __package__:
    from .census_store import load_census
else:  # pragma: no cover - documented direct-script entry point
    from census_store import load_census

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
MANIFEST_PATH = ROOT / "data" / "audit" / "2026-fulltext-scan.jsonl"
PENDING_SUMMARY_PATH = ROOT / "data" / "audit" / "2026-pending-summary.json"
DISPOSITIONS = {"included", "excluded", "pending", "duplicate"}
SCAN_STATES = {"scanned", "metadata-filtered", "verified-manually", "pending"}


def normalize(value: object) -> str:
    return " ".join(str(value).split()).strip().casefold()


def latest_manifest() -> dict[tuple[str, str], dict]:
    records: dict[tuple[str, str], dict] = {}
    if not MANIFEST_PATH.exists():
        return records
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        records[(str(record.get("conference")), normalize(record.get("title")))] = record
    return records


def main() -> int:
    census = load_census()
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    manifest = latest_manifest()
    errors: list[str] = []
    census_records: dict[tuple[str, str], dict] = {}
    all_census_records: list[tuple[str, dict]] = []
    included_ids: set[str] = set()

    for conference in census.get("conferences", []):
        name = str(conference.get("conference", ""))
        papers = conference.get("papers", [])
        expected_count = conference.get("paper_count")
        if isinstance(expected_count, int) and expected_count != len(papers):
            errors.append(f"{name}: paper_count={expected_count} but records={len(papers)}")
        counts = Counter()
        for paper in papers:
            all_census_records.append((name, paper))
            key = (name, normalize(paper.get("title", "")))
            if key in census_records:
                canonical = census_records[key]
                if (
                    paper.get("disposition") != "duplicate"
                    and canonical.get("disposition") != "duplicate"
                ):
                    errors.append(f"duplicate census record: {name}: {paper.get('title')}")
                elif (
                    canonical.get("disposition") == "duplicate"
                    and paper.get("disposition") != "duplicate"
                ):
                    census_records[key] = paper
            else:
                census_records[key] = paper
            disposition = paper.get("disposition")
            counts[disposition] += 1
            if disposition not in DISPOSITIONS:
                errors.append(
                    f"{name}: invalid disposition for {paper.get('title')}: {disposition}"
                )
            if not str(paper.get("disposition_reason", "")).strip():
                errors.append(f"{name}: missing disposition_reason for {paper.get('title')}")
            scan_state = paper.get("full_text_scan")
            if scan_state not in SCAN_STATES:
                errors.append(
                    f"{name}: invalid full_text_scan for {paper.get('title')}: {scan_state}"
                )
            if disposition == "included":
                catalog_id = str(paper.get("catalog_id", "")).strip()
                if not catalog_id:
                    errors.append(f"{name}: included record lacks catalog_id: {paper.get('title')}")
                included_ids.add(catalog_id)
            if paper.get("official_url", "").startswith("https://arxiv.org"):
                errors.append(
                    f"{name}: arXiv cannot be the official census source: {paper.get('title')}"
                )
            content_sources = paper.get("content_sources", [])
            verified_urls = set()
            for source in content_sources if isinstance(content_sources, list) else []:
                if not isinstance(source, dict):
                    errors.append(f"{name}: invalid content source: {paper.get('title')}")
                    continue
                content_url = str(source.get("url", ""))
                if not content_url.startswith("https://"):
                    errors.append(f"{name}: non-HTTPS content source: {paper.get('title')}")
                if source.get("identity_status") != "verified":
                    errors.append(
                        f"{name}: unverified auxiliary content source: {paper.get('title')}"
                    )
                else:
                    verified_urls.add(content_url)
            resolved_pdf_url = str(paper.get("resolved_pdf_url", ""))
            if resolved_pdf_url and resolved_pdf_url not in verified_urls:
                errors.append(
                    f"{name}: resolved PDF is not identity-verified: {paper.get('title')}"
                )
        for disposition in DISPOSITIONS:
            actual = counts.get(disposition, 0)
            if conference.get(f"{disposition}_count", 0) != actual:
                errors.append(
                    f"{name}: {disposition}_count={conference.get(f'{disposition}_count', 0)} but derived={actual}"
                )
        derived_scanned = sum(
            paper.get("full_text_scan") in {"scanned", "verified-manually"} for paper in papers
        )
        if conference.get("scanned_count", 0) != derived_scanned:
            errors.append(
                f"{name}: scanned_count={conference.get('scanned_count', 0)} but derived={derived_scanned}"
            )

    catalog_papers = catalog.get("papers", [])
    catalog_ids = {str(paper.get("id")) for paper in catalog_papers}
    if catalog_ids != included_ids:
        errors.append(
            "catalog/census included ID mismatch: "
            f"catalog-only={sorted(catalog_ids - included_ids)}, census-only={sorted(included_ids - catalog_ids)}"
        )
    for paper in catalog_papers:
        if paper.get("year") != 2026 or paper.get("year_tag") != 2026:
            errors.append(f"catalog {paper.get('id')}: year is not 2026")
        if "arxiv.org" in urlparse(str(paper.get("paper_url", ""))).netloc.lower():
            errors.append(f"catalog {paper.get('id')}: arXiv primary URL")
        key = (str(paper.get("conference")), normalize(paper.get("title")))
        census_record = census_records.get(key)
        if not census_record or census_record.get("disposition") != "included":
            errors.append(f"catalog {paper.get('id')}: no included exact census record")

    for key, record in manifest.items():
        if record.get("product_matches"):
            census_record = census_records.get(key)
            if census_record and not census_record.get("product_review"):
                errors.append(
                    f"unreviewed product hit: {record.get('conference')}: {record.get('title')}"
                )

    total = sum(len(conference.get("papers", [])) for conference in census.get("conferences", []))
    if total != sum(
        conference.get("included_count", 0)
        + conference.get("excluded_count", 0)
        + conference.get("pending_count", 0)
        + conference.get("duplicate_count", 0)
        for conference in census.get("conferences", [])
    ):
        errors.append("global disposition counts do not sum to the official record count")

    if not PENDING_SUMMARY_PATH.exists():
        errors.append("missing compact pending summary")
    else:
        pending_summary = json.loads(PENDING_SUMMARY_PATH.read_text(encoding="utf-8"))
        pending_records = [
            (name, paper)
            for name, paper in all_census_records
            if paper.get("disposition") == "pending"
        ]
        if pending_summary.get("pending_record_count") != len(pending_records):
            errors.append(
                "pending summary count mismatch: "
                f"summary={pending_summary.get('pending_record_count')}, "
                f"census={len(pending_records)}"
            )
        blocker_total = sum(pending_summary.get("blocker_counts", {}).values())
        if blocker_total != len(pending_records):
            errors.append(
                f"pending blocker counts sum to {blocker_total}, expected {len(pending_records)}"
            )
        census_priority = {
            (name, normalize(paper.get("title")))
            for name, paper in pending_records
            if paper.get("pending_review", {}).get("priority") == "high"
        }
        summary_priority = {
            (str(item.get("conference")), normalize(item.get("title")))
            for item in pending_summary.get("high_priority_product_candidates", [])
        }
        if census_priority != summary_priority:
            errors.append(
                "priority pending mismatch: "
                f"summary-only={sorted(summary_priority - census_priority)}, "
                f"census-only={sorted(census_priority - summary_priority)}"
            )
        for item in pending_summary.get("high_priority_product_candidates", []):
            if not item.get("signals") or not item.get("blocker"):
                errors.append(
                    f"priority pending lacks signals/blocker: {item.get('conference')}: {item.get('title')}"
                )
            official_url = str(item.get("official_url", ""))
            if not official_url or "arxiv.org" in urlparse(official_url).netloc.lower():
                errors.append(
                    f"priority pending lacks a first-party record: {item.get('conference')}: {item.get('title')}"
                )

    if errors:
        print("Audit validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"Validated audit census: {total} official records, "
        f"{len(catalog_papers)} catalog records, {len(manifest)} latest full-text records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
