#!/usr/bin/env python3
"""Classify unresolved conference records and surface direct-product candidates.

The full census remains the source of truth.  This pass adds an explicit,
auditable ``pending_review`` object to records whose official title or abstract
already names Claude Code or Codex, and writes a compact JSON summary for
humans and downstream website/report tooling.  It never promotes a paper and
never treats arXiv as a full-text source.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"
SUMMARY_PATH = ROOT / "data" / "audit" / "2026-pending-summary.json"

PRODUCT_PATTERNS = {
    "claude-code": re.compile(r"\bclaude[ -]code(?:[ -]cli)?\b", re.IGNORECASE),
    "codex-cli": re.compile(
        r"\b(?:codex[ -]cli|openai[ -]codex|repo[ -]codex|codex[ -]agent|codex[ -]max)\b",
        re.IGNORECASE,
    ),
}


def normalized(value: object) -> str:
    return " ".join(str(value or "").split()).strip()


def direct_product_signals(paper: dict[str, Any]) -> list[dict[str, str]]:
    text = f"{normalized(paper.get('title'))}\n{normalized(paper.get('abstract'))}"
    signals: list[dict[str, str]] = []
    for product, pattern in PRODUCT_PATTERNS.items():
        matches: list[str] = []
        for match in pattern.finditer(text):
            value = normalized(match.group(0))
            if value.casefold() not in {item.casefold() for item in matches}:
                matches.append(value)
        if matches:
            signals.append({"product": product, "matched_text": "; ".join(matches)})
    return signals


def blocker_for(paper: dict[str, Any]) -> tuple[str, str]:
    scan = paper.get("scan") if isinstance(paper.get("scan"), dict) else {}
    reason = normalized(paper.get("disposition_reason") or scan.get("reason"))
    challenge = bool(scan.get("challenge"))
    http_status = scan.get("http_status")
    if challenge or http_status == 403 or "HTTP 403" in reason:
        return (
            "official-source-challenge",
            "The first-party full-text endpoint returned an HTTP 403 browser-verification challenge.",
        )
    if not paper.get("pdf_url"):
        return (
            "official-pdf-not-exposed",
            "The official conference record does not yet expose a first-party full-text PDF URL.",
        )
    if paper.get("full_text_scan") == "pending":
        return (
            "full-text-scan-pending",
            reason or "A first-party PDF exists, but the full-text scan has not completed.",
        )
    return ("manual-review-pending", reason or "The record still requires manual review.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, default=CENSUS_PATH)
    parser.add_argument("--output", type=Path, default=SUMMARY_PATH)
    args = parser.parse_args()

    census = yaml.safe_load(args.census.read_text(encoding="utf-8"))
    reviewed_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    blocker_counts: Counter[str] = Counter()
    conference_counts: Counter[str] = Counter()
    high_priority: list[dict[str, Any]] = []
    pending_total = 0

    for conference in census.get("conferences", []):
        conference_name = str(conference["conference"])
        for paper in conference.get("papers", []):
            if paper.get("disposition") != "pending":
                continue
            pending_total += 1
            conference_counts[conference_name] += 1
            blocker, blocker_reason = blocker_for(paper)
            blocker_counts[blocker] += 1
            signals = direct_product_signals(paper)
            if not signals:
                continue
            paper["pending_review"] = {
                "priority": "high",
                "status": "blocked-official-full-text",
                "signals": signals,
                "blocker": blocker,
                "reason": blocker_reason,
                "reviewed_at": reviewed_at,
                "policy": "No catalog promotion until first-party full text and product-level experimental context are reviewed; arXiv is not a substitute.",
            }
            paper["disposition_reason"] = (
                "High-priority product candidate from the official title/abstract. "
                f"{blocker_reason} Remains pending until first-party full text can be reviewed; "
                "arXiv is not used as a substitute."
            )
            high_priority.append(
                {
                    "conference": conference_name,
                    "title": paper.get("title"),
                    "official_url": paper.get("details_url") or paper.get("official_url"),
                    "pdf_url": paper.get("pdf_url"),
                    "signals": signals,
                    "blocker": blocker,
                    "blocker_reason": blocker_reason,
                    "abstract_source_url": paper.get("abstract_source_url"),
                }
            )

    conference_level_pending = [
        {
            "conference": conference["conference"],
            "official_url": conference.get("official_url"),
            "list_url": conference.get("list_url"),
            "status": conference.get("status"),
            "reason": conference.get("notes"),
        }
        for conference in census.get("conferences", [])
        if conference.get("status") == "pending"
    ]
    summary = {
        "scope_year": 2026,
        "reviewed_at": reviewed_at,
        "pending_record_count": pending_total,
        "high_priority_product_candidate_count": len(high_priority),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "conference_pending_counts": dict(sorted(conference_counts.items())),
        "high_priority_product_candidates": sorted(
            high_priority,
            key=lambda item: (str(item["conference"]), str(item["title"]).casefold()),
        ),
        "conference_level_pending": conference_level_pending,
        "policy": "Only official conference/proceedings/OpenReview records are used. A title/abstract product hit prioritizes review but never qualifies a paper for inclusion by itself.",
    }
    census["pending_review_summary"] = {
        "reviewed_at": reviewed_at,
        "pending_record_count": pending_total,
        "high_priority_product_candidate_count": len(high_priority),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "summary_path": str(args.output.relative_to(ROOT)),
    }
    census["last_audited_at"] = reviewed_at

    args.census.write_text(
        yaml.safe_dump(census, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"Pending review: total={pending_total}, high-priority={len(high_priority)}, "
        + ", ".join(f"{key}={value}" for key, value in sorted(blocker_counts.items()))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
