#!/usr/bin/env python3
"""Record the human/context review of ICLR product-string hits.

The full-text scanner is intentionally recall-oriented: a product string in a
reference list or an author LLM-use disclosure is a hit, not an inclusion
decision.  This pass makes the review boundary explicit and turns every
non-promoted ICLR hit into an excluded record with a reason.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"
MANIFEST_PATH = ROOT / "data" / "audit" / "2026-fulltext-scan.jsonl"


def normalize(value: str) -> str:
    return " ".join(value.split()).strip().casefold()


INCLUDED_TITLES = {
    "Can Language Models Discover Scaling Laws?": "scaling-laws-2026",
    "Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing": "artemis-2026",
    "CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale": "cybergym-2026",
    "DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively": "deepscientist-2026",
    "DevOps-Gym: Benchmarking AI Agents in Software DevOps Cycle": "devops-gym-2026",
    "FeatureBench: Benchmarking Agentic Coding for Complex Feature Development": "featurebench-2026",
    "From Assistant to Independent Developer — Are GPTs Ready for Software Development?": "appforge-2026",
    "InnoGym: Benchmarking the Innovation Potential of AI Agents": "innogym-2026",
    "QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities": "qlcoder-2026",
    "RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation": "rpg-zerorepo-2026",
    "Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces": "terminal-bench-2-2026",
    "Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents": "helmsman-2026",
}


def latest_manifest() -> dict[tuple[str, str], dict[str, object]]:
    records: dict[tuple[str, str], dict[str, object]] = {}
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            records[(str(item["conference"]), normalize(str(item["title"])))] = item
    return records


def main() -> int:
    census = yaml.safe_load(CENSUS_PATH.read_text(encoding="utf-8"))
    manifest = latest_manifest()
    reviewed = 0
    excluded = 0
    included_hits = 0
    missing: list[str] = []
    for conference in census.get("conferences", []):
        if conference.get("conference") != "ICLR":
            continue
        for paper in conference.get("papers", []):
            scan = manifest.get(("ICLR", normalize(str(paper["title"]))))
            if not scan or not scan.get("product_matches"):
                continue
            reviewed += 1
            title = str(paper["title"])
            if title in INCLUDED_TITLES:
                included_hits += 1
                paper["product_review"] = {
                    "status": "promote-after-catalog-review",
                    "catalog_id": INCLUDED_TITLES[title],
                    "reason": "Full-text product hit was reviewed as an actual product evaluation, baseline, host, or product-level benchmark use.",
                    "match_pages": sorted(
                        {
                            int(snippet["page"])
                            for snippets in scan.get("product_matches", {}).values()
                            for snippet in snippets
                            if str(snippet.get("page", "")).isdigit()
                        }
                    ),
                }
                continue
            pages = sorted(
                {
                    int(snippet["page"])
                    for snippets in scan.get("product_matches", {}).values()
                    for snippet in snippets
                    if str(snippet.get("page", "")).isdigit()
                }
            )
            paper["disposition"] = "excluded"
            paper["disposition_reason"] = (
                "Full-text product-string hit reviewed as a reference/related-work mention, background discussion, "
                "or ancillary author code/writing assistance; no product-level baseline, evaluation, host configuration, "
                "or product-focused empirical analysis was found."
            )
            paper["product_review"] = {
                "status": "excluded-after-context-review",
                "reason": paper["disposition_reason"],
                "match_pages": pages,
            }
            excluded += 1
        if any(
            paper.get("disposition") == "pending"
            and paper.get("scan", {}).get("product_matches")
            and not paper.get("product_review")
            for paper in conference.get("papers", [])
        ):
            missing.append("ICLR product hit was not reviewed")

    if missing:
        raise RuntimeError("; ".join(missing))
    census["iclr_product_hit_review"] = {
        "reviewed_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "product_hit_count": reviewed,
        "promote_after_catalog_review": included_hits,
        "excluded_after_context_review": excluded,
        "policy": "Recall-oriented full-text hits require context review; incidental/reference/author-assistance mentions are excluded from the main catalog.",
    }
    CENSUS_PATH.write_text(
        yaml.safe_dump(census, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(f"Reviewed {reviewed} ICLR product hits: promote={included_hits}, excluded={excluded}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
