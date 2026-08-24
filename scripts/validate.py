#!/usr/bin/env python3
"""Validate the paper catalog against its schema and project invariants."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
SCHEMA_PATH = ROOT / "data" / "schema.json"
FULLTEXT_MANIFEST_PATH = ROOT / "data" / "audit" / "2026-fulltext-scan.jsonl"

ALLOWED_CONFERENCES = {
    "AAAI",
    "ASE",
    "FSE",
    "ICLR",
    "ICML",
    "ICSE",
    "ISSTA",
    "NeurIPS",
    "IJCAI",
    "KDD",
    "PLDI",
    "POPL",
    "OOPSLA",
}


def load_files() -> tuple[dict, dict]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        catalog = yaml.safe_load(handle)
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    return catalog, schema


def format_path(path: object) -> str:
    parts = list(path)
    return ".".join(str(part) for part in parts) or "<root>"


def schema_errors(catalog: dict, schema: dict) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(catalog), key=lambda error: list(error.path))
    return [f"{format_path(error.path)}: {error.message}" for error in errors]


def duplicate_values(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def invariant_errors(catalog: dict) -> list[str]:
    errors = []
    papers = catalog.get("papers", [])

    for duplicate in duplicate_values([paper.get("id", "") for paper in papers]):
        errors.append(f"duplicate paper id: {duplicate}")
    for duplicate in duplicate_values([paper.get("title", "") for paper in papers]):
        errors.append(f"duplicate paper title: {duplicate}")
    dois = [paper["doi"].lower() for paper in papers if paper.get("doi")]
    for duplicate in duplicate_values(dois):
        errors.append(f"duplicate DOI: {duplicate}")

    for paper in papers:
        paper_id = paper.get("id", "<missing-id>")
        classification = paper.get("classification")
        artifact_status = paper.get("artifact_status")
        artifact_url = paper.get("artifact_url")
        products = paper.get("products", [])
        product_ids = [item.get("product") for item in products]

        for duplicate in duplicate_values(product_ids):
            errors.append(f"{paper_id}: duplicate product entry: {duplicate}")

        if classification == "direct":
            direct_products = {"claude-code", "codex-cli"}
            has_baseline = any(
                item.get("role") == "baseline" and item.get("product") in direct_products
                for item in products
            )
            if not has_baseline:
                errors.append(f"{paper_id}: direct entries require a product baseline")

        historical_products = {"openai-codex-model"}
        has_historical_product = any(
            item.get("product") in historical_products for item in products
        )
        if classification == "historical" and not has_historical_product:
            errors.append(f"{paper_id}: historical entries require a historical product")
        if classification != "historical" and has_historical_product:
            errors.append(f"{paper_id}: historical products must use historical classification")

        if artifact_status in {"official", "community"} and not artifact_url:
            errors.append(f"{paper_id}: {artifact_status} artifact requires artifact_url")
        if artifact_status == "not-found" and artifact_url:
            errors.append(f"{paper_id}: not-found artifact cannot include artifact_url")

        comparison_scope = paper.get("evidence", {}).get("comparison_scope")
        expected_scopes = {
            "direct": {"product-level", "configuration-ablation"},
            "related": {"component-level", "configuration-ablation"},
            "evaluation": {"benchmark-only"},
            "historical": {"historical-model"},
        }
        if comparison_scope not in expected_scopes.get(classification, set()):
            errors.append(
                f"{paper_id}: comparison scope {comparison_scope!r} does not match "
                f"classification {classification!r}"
            )

        if paper.get("year") != 2026 or paper.get("year_tag") != 2026:
            errors.append(f"{paper_id}: main catalog is restricted to year 2026")
        if paper.get("conference") not in ALLOWED_CONFERENCES:
            errors.append(f"{paper_id}: conference is not an allowed 2026 conference")
        if paper.get("conference_tag") != paper.get("conference"):
            errors.append(f"{paper_id}: conference_tag must equal conference")
        if paper.get("audit_status") != "included":
            errors.append(f"{paper_id}: only audit_status=included may enter the main catalog")
        if paper.get("source_type") not in {
            "official-conference",
            "official-proceedings",
            "openreview-conference",
            "official-publisher",
        }:
            errors.append(f"{paper_id}: source_type must identify an official conference source")
        source_host = urlparse(paper.get("paper_url", "")).netloc.lower()
        if "arxiv.org" in source_host:
            errors.append(f"{paper_id}: arXiv cannot be the primary paper source")
        if any(not item.get("model", "").strip() for item in products):
            errors.append(f"{paper_id}: model cannot be empty")
        if any(
            item.get("product") in {"claude-code", "codex-cli"}
            and not paper.get("evidence", {}).get("source_location", "").strip()
            for item in products
        ):
            errors.append(f"{paper_id}: product claims require evidence.source_location")

    errors.extend(model_manifest_errors(papers))

    return errors


def model_manifest_errors(papers: list[dict]) -> list[str]:
    """Reject ``not-reported`` when the recorded full-text scan found models."""

    if not FULLTEXT_MANIFEST_PATH.exists():
        return []
    records = {}
    for line in FULLTEXT_MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        key = (record.get("conference"), " ".join(record.get("title", "").split()).casefold())
        records[key] = record
    errors = []
    for paper in papers:
        key = (paper.get("conference"), " ".join(paper.get("title", "").split()).casefold())
        record = records.get(key)
        if not record or record.get("status") != "scanned":
            continue
        candidates = record.get("model_candidates", [])
        if candidates and all(
            item.get("model") == "not-reported" for item in paper.get("products", [])
        ):
            errors.append(
                f"{paper.get('id')}: model=not-reported conflicts with full-text model candidates: "
                + ", ".join(candidates[:6])
            )
    return errors


def main() -> int:
    catalog, schema = load_files()
    errors = schema_errors(catalog, schema) + invariant_errors(catalog)
    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    classes = Counter(paper["classification"] for paper in catalog["papers"])
    summary = ", ".join(f"{name}={count}" for name, count in sorted(classes.items()))
    print(f"Validated {len(catalog['papers'])} papers ({summary}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
