#!/usr/bin/env python3
"""Validate the paper catalog against its schema and project invariants."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
SCHEMA_PATH = ROOT / "data" / "schema.json"


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
    arxiv_ids = [paper["arxiv_id"] for paper in papers if paper.get("arxiv_id")]
    for duplicate in duplicate_values(arxiv_ids):
        errors.append(f"duplicate arXiv id: {duplicate}")
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
