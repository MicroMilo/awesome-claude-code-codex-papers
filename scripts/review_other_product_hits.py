#!/usr/bin/env python3
"""Record context review for non-ICLR industrial-product text hits.

This pass is intentionally explicit.  A product name in a reference list is
not evidence that the paper evaluated that product, so each current hit must
have a documented disposition rather than being silently dropped.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

if __package__:
    from .census_store import load_census, write_census
else:  # pragma: no cover - documented direct-script entry point
    from census_store import load_census, write_census

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "audit" / "2026-fulltext-scan.jsonl"


def normalize(value: str) -> str:
    return " ".join(value.split()).strip().casefold()


REFERENCE_ONLY = {
    (
        "FSE",
        normalize(
            "LLM-Assisted Input-Requirement-Aware Differential Testing of Array Programming Frameworks"
        ),
    ): (
        "The only OpenAI Codex hit is an entry in the References section (the "
        "OpenAI Codex Developer Documentation citation on page 23); the paper "
        "does not run, evaluate, host, or compare Codex CLI."
    ),
    (
        "AAAI",
        normalize(
            "AP2O-Coder: Adaptively Progressive Preference Optimization for Reducing Compilation and Runtime Errors in LLM-Generated Code"
        ),
    ): (
        "The only Claude Code hit is an Anthropic reference entry on page 8; the "
        "paper studies preference optimization for generated code and does not "
        "run, evaluate, host, or compare Claude Code."
    ),
    (
        "AAAI",
        normalize("Large Language Model Unlearning for Source Code"),
    ): (
        "The only Claude Code hit is an Anthropic reference entry on page 8; the "
        "paper studies source-code unlearning and does not run, evaluate, host, "
        "or compare Claude Code."
    ),
    (
        "AAAI",
        normalize(
            "SPAN: Benchmarking and Improving Cross-Calendar Temporal Reasoning of Large Language Models"
        ),
    ): (
        "The only Claude Code hit is a citation in the References section on page "
        "8; the paper evaluates temporal reasoning and does not run, evaluate, "
        "host, or compare Claude Code."
    ),
    (
        "IJCAI",
        normalize(
            "Visualizing Deep Agents in Long-Horizon Tasks: Towards Explainable and Trustworthy Agentic AI"
        ),
    ): (
        "Claude Code appears only as an example of result-oriented CLI tooling in "
        "Section 3.1. The evaluation compares the paper's 4D visualization with "
        "LangSmith linear traces and does not run or evaluate Claude Code."
    ),
}

INCLUDED = {
    (
        "IJCAI",
        normalize("Verifiable PDE Reasoning and Modeling with Neurosymbolics"),
    ): (
        "lean-refactor-2026",
        "Section 2.3 explicitly reports that Lean Refactor outperforms Claude Code "
        "on Lean proof refactoring. The official spotlight paper omits the Claude "
        "Code model and configuration, which remain recorded as not-reported.",
    ),
}


def latest_manifest() -> dict[tuple[str, str], dict[str, object]]:
    records: dict[tuple[str, str], dict[str, object]] = {}
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            records[(str(item["conference"]), normalize(str(item["title"])))] = item
    return records


def main() -> int:
    census = load_census()
    manifest = latest_manifest()
    reviewed = 0
    excluded = 0
    included_hits = 0
    affected_conferences: set[str] = set()
    missing: list[str] = []
    for conference in census.get("conferences", []):
        name = str(conference["conference"])
        if name == "ICLR":
            continue
        for paper in conference.get("papers", []):
            key = (name, normalize(str(paper["title"])))
            scan = manifest.get(key)
            if not scan or not scan.get("product_matches"):
                continue
            reviewed += 1
            affected_conferences.add(name)
            inclusion = INCLUDED.get(key)
            if inclusion is not None:
                catalog_id, reason = inclusion
                paper["product_review"] = {
                    "status": "promote-after-catalog-review",
                    "catalog_id": catalog_id,
                    "reason": reason,
                    "match_pages": sorted(
                        {
                            int(snippet["page"])
                            for snippets in scan.get("product_matches", {}).values()
                            for snippet in snippets
                            if str(snippet.get("page", "")).isdigit()
                        }
                    ),
                }
                included_hits += 1
                continue
            reason = REFERENCE_ONLY.get(key)
            if reason is None:
                missing.append(f"{name}: {paper['title']}")
                continue
            paper["disposition"] = "excluded"
            paper["disposition_reason"] = reason
            pages = sorted(
                {
                    int(snippet["page"])
                    for snippets in scan.get("product_matches", {}).values()
                    for snippet in snippets
                    if str(snippet.get("page", "")).isdigit()
                }
            )
            paper["product_review"] = {
                "status": "excluded-after-context-review",
                "reason": reason,
                "match_pages": pages,
            }
            excluded += 1

    if missing:
        raise RuntimeError("Unreviewed non-ICLR product hits: " + "; ".join(missing))
    census["non_iclr_product_hit_review"] = {
        "reviewed_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "product_hit_count": reviewed,
        "promote_after_catalog_review": included_hits,
        "excluded_after_context_review": excluded,
        "policy": "Every non-ICLR product-string hit must be mapped to an explicit context review before finalization.",
    }
    write_census(census, only=affected_conferences)
    print(
        f"Reviewed {reviewed} non-ICLR product hits: promote={included_hits}, excluded={excluded}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
