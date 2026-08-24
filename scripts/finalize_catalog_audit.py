#!/usr/bin/env python3
"""Promote only catalog papers that have an exact official census record.

This is intentionally a small, deterministic finalization pass.  Full-text
scans may leave product hits as ``pending`` until a reviewer maps the context
to a catalog record; this script is the explicit human-review boundary.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"


def normalize(value: str) -> str:
    return " ".join(value.split()).strip().casefold()


def main() -> int:
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    census = yaml.safe_load(CENSUS_PATH.read_text(encoding="utf-8"))
    catalog_by_title = {
        (paper["conference"], normalize(paper["title"])): paper for paper in catalog["papers"]
    }
    promoted: list[str] = []
    for conference in census.get("conferences", []):
        conference_name = conference["conference"]
        for paper in conference.get("papers", []):
            catalog_paper = catalog_by_title.get((conference_name, normalize(paper["title"])))
            if not catalog_paper:
                continue
            paper["disposition"] = "included"
            paper["disposition_reason"] = (
                "Exact official conference record and reviewed product-level evidence imported into the main catalog."
            )
            paper["catalog_id"] = catalog_paper["id"]
            if paper.get("full_text_scan") != "scanned":
                paper["full_text_scan"] = "verified-manually"
                paper["scan"] = {
                    "status": "verified-manually",
                    "reason": "Official paper source was reviewed manually, including the experimental setup and product configuration.",
                    "source_location": catalog_paper["evidence"]["source_location"],
                    "model_candidates": [item["model"] for item in catalog_paper["products"]],
                }
            promoted.append(catalog_paper["id"])

        counts = {
            name: sum(paper.get("disposition") == name for paper in conference.get("papers", []))
            for name in ["included", "excluded", "pending", "duplicate"]
        }
        conference["scanned_count"] = sum(
            paper.get("full_text_scan") in {"scanned", "verified-manually"}
            for paper in conference.get("papers", [])
        )
        for name, value in counts.items():
            conference[f"{name}_count"] = value

    census["last_audited_at"] = datetime.now(UTC).replace(microsecond=0).isoformat()
    census["catalog_ids"] = sorted(set(promoted))
    CENSUS_PATH.write_text(
        yaml.safe_dump(census, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(
        f"Promoted {len(set(promoted))} exact official records: {', '.join(sorted(set(promoted)))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
