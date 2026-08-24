#!/usr/bin/env python3
"""Freeze an auditable review of the pre-migration catalog."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
OUTPUT_PATH = ROOT / "data" / "audit" / "current-catalog-audit.yaml"

# These are first-party conference records already present in the repository
# or matched against the 2026 official census.  Entries not in this map are
# not promoted merely because their title resembles a conference paper.
OFFICIAL_RECORDS = {
    "qlcoder-2026": "official ICLR proceedings record",
    "rpg-zerorepo-2026": "official ICLR proceedings record",
    "artemis-2026": "official ICLR proceedings record matched by exact title; catalog URL must be replaced",
    "formact-2026": "official ICML poster/OpenReview record",
    "agents-md-impact-2026": "official ICSE JAWs workshop record",
    "terminal-bench-2-2026": "official ICLR proceedings record must be matched to the exact title/version",
    "engineering-pitfalls-2026": "official FSE industry-track record",
    "evodev-2026": "official ISSTA research-paper record",
    "toolleak-2026": "official ISSTA research-paper record",
    "execution-ablation-2026": "exact title matched in the official ISSTA accepted list; catalog URL still points to arXiv",
    "llm2ltac-2026": "official ASE research-paper record",
}


def audit_record(paper: dict) -> dict:
    paper_id = paper["id"]
    conference = paper.get("conference")
    year = paper.get("year")
    paper_url = paper.get("paper_url", "")
    arxiv_only = conference == "arXiv" or "arxiv.org" in paper_url
    issues: list[str] = []
    if year != 2026:
        issues.append("year is outside the 2026 migration scope")
    if arxiv_only:
        issues.append("current primary URL is arXiv; arXiv is not an accepted main-catalog source")
    if paper_id in OFFICIAL_RECORDS and "arxiv.org" in paper_url:
        issues.append(
            "formal conference record exists but paper_url must be replaced with the official conference record"
        )
    if any(product.get("model") == "not-reported" for product in paper.get("products", [])):
        issues.append("model field requires a full-text/appendix/artifact recheck")
    if any(product.get("version") == "not-reported" for product in paper.get("products", [])):
        issues.append("CLI/product version is not reported or not yet verified")
    if not paper.get("evidence", {}).get("source_location"):
        issues.append("evidence source_location is missing")

    if year != 2026:
        disposition = "excluded"
        reason = "Outside the requested 2026 conference scope."
    elif arxiv_only and paper_id not in OFFICIAL_RECORDS:
        disposition = "excluded"
        reason = "ArXiv-only record; no exact official 2026 conference record was found in the imported official census."
    elif paper_id in OFFICIAL_RECORDS:
        disposition = "pending"
        reason = OFFICIAL_RECORDS[paper_id]
    else:
        disposition = "pending"
        reason = "Formal conference status and product-level evidence require verification before import."

    return {
        "id": paper_id,
        "title": paper.get("title"),
        "original_conference": conference,
        "original_year": year,
        "original_paper_url": paper_url,
        "original_products": paper.get("products", []),
        "disposition": disposition,
        "reason": reason,
        "field_issues": issues,
        "official_record_note": OFFICIAL_RECORDS.get(paper_id),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    report = {
        "report_version": 1,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "source_catalog": "data/papers.yaml before the 2026 conference-only migration",
        "policy": {
            "arxiv_only": "excluded",
            "official_record_with_arxiv_primary_url": "retain as pending until paper_url is replaced",
            "uncertain_acceptance_or_full_text": "pending",
        },
        "papers": [audit_record(paper) for paper in catalog.get("papers", [])],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8"
    )
    counts = {}
    for paper in report["papers"]:
        counts[paper["disposition"]] = counts.get(paper["disposition"], 0) + 1
    print(f"Wrote {args.output.relative_to(ROOT)}: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
