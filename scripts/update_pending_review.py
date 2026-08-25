#!/usr/bin/env python3
"""Classify unresolved conference records and surface direct-product candidates.

The full census remains the source of truth.  This pass adds an explicit,
auditable ``pending_review`` object to records whose official title or abstract
already names Claude Code or Codex, and writes a compact JSON summary for
humans and downstream website/report tooling.  It never promotes a paper and
never treats an auxiliary copy as conference-acceptance evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

if __package__:
    from .census_store import CENSUS_INDEX_PATH, load_census, write_census
else:  # pragma: no cover - documented direct-script entry point
    from census_store import CENSUS_INDEX_PATH, load_census, write_census

ROOT = Path(__file__).resolve().parents[1]
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
    resolved_source = (
        paper.get("resolved_content_source")
        if isinstance(paper.get("resolved_content_source"), dict)
        else {}
    )
    has_verified_content = bool(
        paper.get("resolved_pdf_url") and resolved_source.get("identity_status") == "verified"
    )
    challenge = bool(scan.get("challenge"))
    http_status = scan.get("http_status")
    if (challenge or http_status == 403 or "HTTP 403" in reason) and not has_verified_content:
        return (
            "official-source-challenge",
            "The publisher full-text endpoint returned an HTTP 403 challenge and no identity-verified open copy has been resolved.",
        )
    if not paper.get("pdf_url") and not has_verified_content:
        return (
            "full-text-not-resolved",
            "The official record proves acceptance, but no identity-verified full-text copy has been resolved yet.",
        )
    if paper.get("full_text_scan") == "pending":
        return (
            "full-text-scan-pending",
            reason
            or "An official or identity-verified full-text copy exists, but scanning has not completed.",
        )
    return ("manual-review-pending", reason or "The record still requires manual review.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, default=CENSUS_INDEX_PATH)
    parser.add_argument("--output", type=Path, default=SUMMARY_PATH)
    args = parser.parse_args()

    census = load_census(args.census)
    reviewed_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    blocker_counts: Counter[str] = Counter()
    conference_counts: Counter[str] = Counter()
    high_priority: list[dict[str, Any]] = []
    pending_total = 0
    affected_conferences: set[str] = set()

    for conference in census.get("conferences", []):
        conference_name = str(conference["conference"])
        for paper in conference.get("papers", []):
            if paper.get("disposition") != "pending":
                if paper.pop("pending_review", None) is not None:
                    affected_conferences.add(conference_name)
                continue
            pending_total += 1
            conference_counts[conference_name] += 1
            blocker, blocker_reason = blocker_for(paper)
            blocker_counts[blocker] += 1
            signals = direct_product_signals(paper)
            if not signals:
                if paper.pop("pending_review", None) is not None:
                    affected_conferences.add(conference_name)
                continue
            affected_conferences.add(conference_name)
            paper["pending_review"] = {
                "priority": "high",
                "status": "blocked-content-evidence",
                "signals": signals,
                "blocker": blocker,
                "reason": blocker_reason,
                "reviewed_at": reviewed_at,
                "policy": "No catalog promotion until product-level context is reviewed in official or identity-verified full text. Auxiliary copies never replace the official acceptance record.",
            }
            paper["disposition_reason"] = (
                "High-priority product candidate from the official title/abstract. "
                f"{blocker_reason} It remains pending until product-level evidence can be reviewed."
            )
            high_priority.append(
                {
                    "conference": conference_name,
                    "title": paper.get("title"),
                    "official_url": paper.get("details_url") or paper.get("official_url"),
                    "pdf_url": paper.get("pdf_url"),
                    "resolved_pdf_url": paper.get("resolved_pdf_url"),
                    "resolved_content_source": paper.get("resolved_content_source"),
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
        "policy": "Official conference/proceedings/OpenReview/publisher records establish acceptance. Identity-verified auxiliary copies may supply content evidence. A title/abstract hit never qualifies a paper by itself.",
    }
    census["pending_review_summary"] = {
        "reviewed_at": reviewed_at,
        "pending_record_count": pending_total,
        "high_priority_product_candidate_count": len(high_priority),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "summary_path": str(args.output.relative_to(ROOT)),
    }
    census["last_audited_at"] = reviewed_at

    write_census(census, args.census, only=affected_conferences)
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
