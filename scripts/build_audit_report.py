#!/usr/bin/env python3
"""Render the human-readable summary for the machine-readable audit census."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"
CATALOG_PATH = ROOT / "data" / "papers.yaml"
OUTPUT_PATH = ROOT / "docs" / "2026-conference-census.md"
PENDING_SUMMARY_PATH = ROOT / "data" / "audit" / "2026-pending-summary.json"


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    census = yaml.safe_load(CENSUS_PATH.read_text(encoding="utf-8"))
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    conferences = census.get("conferences", [])
    records = [paper for conference in conferences for paper in conference.get("papers", [])]
    included = [paper for paper in records if paper.get("disposition") == "included"]
    excluded = [paper for paper in records if paper.get("disposition") == "excluded"]
    pending = [paper for paper in records if paper.get("disposition") == "pending"]
    duplicate = [paper for paper in records if paper.get("disposition") == "duplicate"]
    reasons = Counter(
        cell(paper.get("disposition_reason", "not recorded")) for paper in excluded + pending
    )
    pending_summary = (
        json.loads(PENDING_SUMMARY_PATH.read_text(encoding="utf-8"))
        if PENDING_SUMMARY_PATH.exists()
        else {}
    )

    lines = [
        "# 2026 conference census and full-text audit",
        "",
        f"> Last audited: `{census.get('last_audited_at', census.get('generated_at', 'not recorded'))}`",
        ">",
        "> The main catalog is deliberately narrow: only 2026 records with a first-party conference/proceedings/OpenReview source and reviewed Claude Code or Codex CLI product evidence are imported.",
        "",
        "The complete per-paper record is in [`data/audit/2026-conference-census.yaml`](../data/audit/2026-conference-census.yaml). Every official-list record has an explicit `included`, `excluded`, `pending`, or `duplicate` disposition; no arXiv list is used as a conference census. ICLR records may also carry `full_text_scan: metadata-filtered`: the official abstract was screened and the PDF was intentionally not requested because it had no high-recall coding-agent signal.",
        "",
        "## Conference totals",
        "",
        "| Conference | Official source | Status | Total | Scanned | Metadata-screened | Included | Excluded | Pending | Duplicate |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for conference in conferences:
        lines.append(
            f"| {cell(conference['conference'])} | [official]({conference['official_url']}) | "
            f"{cell(conference.get('status', 'not recorded'))} | "
            f"{cell(conference.get('paper_count') if conference.get('paper_count') is not None else 'pending')} | "
            f"{conference.get('scanned_count', 0)} | {conference.get('metadata_screened_count', 0)} | "
            f"{conference.get('included_count', 0)} | "
            f"{conference.get('excluded_count', 0)} | {conference.get('pending_count', 0)} | "
            f"{conference.get('duplicate_count', 0)} |"
        )

    iclr = next((item for item in conferences if item.get("conference") == "ICLR"), None)
    if iclr and iclr.get("downloads_event_count") is not None:
        lines.extend(
            [
                "",
                "ICLR's official [Downloads/2026](https://iclr.cc/Downloads/2026) page exposed "
                f"{iclr['downloads_event_count']} events; the main-paper census uses "
                f"{iclr.get('paper_count', 'pending')} proceedings records after excluding "
                "tutorials, talks, workshops, and demonstrations from the paper total. "
                f"The exported official list contains {iclr.get('downloads_export_record_count', 'not recorded')} "
                "paper records.",
            ]
        )

    lines.extend(
        [
            "",
            "## Global disposition",
            "",
            f"- Official-list records: **{len(records)}**",
            f"- Included in the main catalog: **{len(included)}**",
            f"- Explicitly excluded after full-text/source review: **{len(excluded)}**",
            f"- Pending because official full text, acceptance status, or product context is incomplete: **{len(pending)}**",
            f"- Duplicate official records: **{len(duplicate)}**",
            f"- Main catalog records: **{len(catalog.get('papers', []))}**",
            "",
            "## Included records",
            "",
            "| Catalog ID | Conference | Paper | Official record | Product / exact model | Evidence location |",
            "|---|---|---|---|---|---|",
        ]
    )
    catalog_by_id = {paper["id"]: paper for paper in catalog.get("papers", [])}
    for conference in conferences:
        conference_name = conference["conference"]
        for paper in conference.get("papers", []):
            if paper.get("disposition") != "included":
                continue
            catalog_paper = catalog_by_id.get(paper.get("catalog_id", ""), {})
            products = (
                "; ".join(
                    f"{item['product']} = {item['model']}"
                    for item in catalog_paper.get("products", [])
                )
                or "not recorded"
            )
            lines.append(
                f"| `{cell(paper.get('catalog_id', 'not recorded'))}` | {cell(conference_name)} | "
                f"{cell(paper.get('title', ''))} | [official]({paper.get('official_url', '')}) | "
                f"{cell(products)} | {cell(catalog_paper.get('evidence', {}).get('source_location', 'not recorded'))} |"
            )

    lines.extend(
        [
            "",
            "## Excluded and pending evidence",
            "",
            "The YAML report retains the title, official URL, track, scan status, and reason for every excluded or pending record. The most common reasons in this run are:",
            "",
        ]
    )
    for reason, count in reasons.most_common(20):
        lines.append(f"- **{count}** — {reason}")
    if len(reasons) > 20:
        lines.append(
            f"- **{len(reasons) - 20}** additional distinct reasons are retained in the YAML report."
        )

    high_priority = pending_summary.get("high_priority_product_candidates", [])
    lines.extend(
        [
            "",
            "## Priority pending queue",
            "",
            "A product name in an official title or abstract is a prioritization signal, not inclusion evidence. These records remain pending until first-party full text and the exact product/model context can be reviewed.",
            "",
            f"- Pending paper records: **{pending_summary.get('pending_record_count', len(pending))}**",
            f"- High-priority direct-product candidates: **{len(high_priority)}**",
            "- arXiv fallbacks used: **0**",
            "",
            "| Conference | Paper | Official record | Product signal | Current blocker |",
            "|---|---|---|---|---|",
        ]
    )
    for item in high_priority:
        signals = "; ".join(
            f"{signal['product']}: {signal['matched_text']}" for signal in item.get("signals", [])
        )
        lines.append(
            f"| {cell(item.get('conference', ''))} | {cell(item.get('title', ''))} | "
            f"[official]({item.get('official_url', '')}) | {cell(signals)} | "
            f"{cell(item.get('blocker_reason', item.get('blocker', '')))} |"
        )
    if not high_priority:
        lines.append("| — | No direct-product pending candidates recorded | — | — | — |")

    conference_pending = pending_summary.get("conference_level_pending", [])
    lines.extend(
        [
            "",
            "### Conference-level pending",
            "",
        ]
    )
    for item in conference_pending:
        lines.append(
            f"- **{cell(item.get('conference', ''))}** — {cell(item.get('reason', 'not recorded'))} "
            f"([official]({item.get('list_url') or item.get('official_url', '')}))"
        )

    lines.extend(
        [
            "",
            "## Audit artifacts",
            "",
            "- [`data/audit/current-catalog-audit.yaml`](../data/audit/current-catalog-audit.yaml) — field-by-field audit of the pre-migration 32-record catalog.",
            "- [`data/audit/2026-fulltext-scan.jsonl`](../data/audit/2026-fulltext-scan.jsonl) — page-level snippets, extraction method, product hits, and model candidates for official PDFs; PDFs are not committed.",
            "- [`data/audit/2026-pending-summary.json`](../data/audit/2026-pending-summary.json) — compact blocker counts and the high-priority direct-product pending queue.",
            f"- [`data/papers.yaml`](../data/papers.yaml) — the {len(catalog.get('papers', []))} records promoted into the current official-source main catalog after this audit.",
            "",
            "## Source policy",
            "",
            "Conference pages, official proceedings, official OpenReview conference records, and official publisher pages are accepted as primary sources. ArXiv-only records are excluded from the main catalog; an arXiv URL can never satisfy the primary-source requirement.",
            "",
        ]
    )
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
