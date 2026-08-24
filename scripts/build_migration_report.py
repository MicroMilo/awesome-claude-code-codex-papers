#!/usr/bin/env python3
"""Record exactly what the pre-migration catalog did to each old record."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OLD_AUDIT_PATH = ROOT / "data" / "audit" / "current-catalog-audit.yaml"
CATALOG_PATH = ROOT / "data" / "papers.yaml"
OUTPUT_PATH = ROOT / "data" / "audit" / "2026-main-catalog-migration.yaml"


def main() -> int:
    old_audit = yaml.safe_load(OLD_AUDIT_PATH.read_text(encoding="utf-8"))
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    current = {paper["id"]: paper for paper in catalog.get("papers", [])}
    records = []
    for old in old_audit.get("papers", []):
        paper_id = old["id"]
        new = current.get(paper_id)
        original_url = old.get("original_paper_url", "")
        arxiv_only = old.get("original_conference") == "arXiv" or "arxiv.org" in original_url
        record = {
            "id": paper_id,
            "title": old.get("title"),
            "original_conference": old.get("original_conference"),
            "original_year": old.get("original_year"),
            "original_paper_url": original_url,
            "original_disposition": old.get("disposition"),
            "arxiv_only_at_migration": arxiv_only,
        }
        if new:
            record.update(
                {
                    "final_disposition": "included",
                    "final_catalog_id": new["id"],
                    "final_conference": new["conference"],
                    "final_year": new["year"],
                    "final_paper_url": new["paper_url"],
                    "final_source_type": new["source_type"],
                    "change": "retained and promoted to an official 2026 conference source",
                }
            )
        else:
            record.update(
                {
                    "final_disposition": "removed-from-main-catalog",
                    "reason": (
                        "ArXiv-only or outside the requested official 2026 conference scope."
                        if arxiv_only or old.get("original_year") != 2026
                        else "Not promoted because official acceptance/full-text/product evidence was not sufficient for the main catalog."
                    ),
                }
            )
        records.append(record)

    retained = [record for record in records if record["final_disposition"] == "included"]
    removed = [record for record in records if record["final_disposition"] != "included"]
    report = {
        "report_version": 1,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source": "data/audit/current-catalog-audit.yaml",
        "old_record_count": len(records),
        "retained_count": len(retained),
        "removed_count": len(removed),
        "arxiv_only_removed_count": sum(record["arxiv_only_at_migration"] for record in removed),
        "retained_records": retained,
        "removed_records": removed,
    }
    OUTPUT_PATH.write_text(
        yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(
        f"Wrote {OUTPUT_PATH.relative_to(ROOT)}: retained={len(retained)}, "
        f"removed={len(removed)}, arxiv_only_removed={report['arxiv_only_removed_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
