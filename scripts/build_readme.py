#!/usr/bin/env python3
"""Generate catalog tables in README.md from data/papers.yaml."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
README_PATH = ROOT / "README.md"

SECTIONS = {
    "direct": ("<!-- CATALOG:DIRECT:START -->", "<!-- CATALOG:DIRECT:END -->"),
    "related": ("<!-- CATALOG:RELATED:START -->", "<!-- CATALOG:RELATED:END -->"),
    "evaluation": (
        "<!-- CATALOG:EVALUATION:START -->",
        "<!-- CATALOG:EVALUATION:END -->",
    ),
    "historical": (
        "<!-- CATALOG:HISTORICAL:START -->",
        "<!-- CATALOG:HISTORICAL:END -->",
    ),
}

PRODUCT_LABELS = {
    "claude-code": "Claude Code",
    "codex-cli": "Codex CLI",
    "openai-codex-model": "OpenAI Codex model",
}

CONTROL_LABELS = {
    "yes": "same",
    "no": "different",
    "unknown": "unknown",
}


def load_catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def format_paper(paper: dict) -> str:
    title = escape_cell(paper["title"])
    paper_link = f"[{title}]({paper['paper_url']})"
    artifact_url = paper.get("artifact_url")
    if artifact_url:
        paper_link += f"<br>[artifact]({artifact_url})"
    return paper_link


def format_products(paper: dict) -> str:
    rendered = []
    for item in paper["products"]:
        label = PRODUCT_LABELS[item["product"]]
        details = []
        if item["model"] not in {"not-reported", "not-applicable"}:
            details.append(item["model"])
        if item["version"] not in {"not-reported", "multiple"}:
            details.append(item["version"])
        if details:
            label += f" ({', '.join(details)})"
        rendered.append(escape_cell(label))
    return "<br>".join(rendered)


def format_venue(paper: dict) -> str:
    status = paper["publication_status"].replace("-", " ")
    return f"{escape_cell(paper['venue'])} {paper['year']}<br>{status}"


def format_method(paper: dict) -> str:
    method = escape_cell(paper["method"]["summary"])
    tags = paper["method"]["tags"]
    if tags:
        method += "<br>" + " ".join(f"`{tag}`" for tag in tags)
    return method


def format_controls(paper: dict) -> str:
    evidence = paper["evidence"]
    model = CONTROL_LABELS[evidence["same_model"]]
    budget = CONTROL_LABELS[evidence["same_budget"]]
    strength = evidence["strength"]
    return f"model: {model}<br>budget: {budget}<br>evidence: {strength}"


def generate_table(papers: list[dict]) -> str:
    if not papers:
        return "_No reviewed papers in this class yet._"

    header = (
        "| Paper | Venue | Product baseline | Task / benchmark | "
        "Method | Reported result | Controls |\n"
        "|---|---|---|---|---|---|---|"
    )
    rows = []
    for paper in sorted(papers, key=lambda item: (-item["year"], item["title"].lower())):
        task = (
            f"{escape_cell(paper['task']['summary'])}"
            f"<br>{escape_cell(paper['task']['benchmark'])}"
        )
        row = "| " + " | ".join(
            [
                format_paper(paper),
                format_venue(paper),
                format_products(paper),
                task,
                format_method(paper),
                escape_cell(paper["evidence"]["result"]),
                format_controls(paper),
            ]
        ) + " |"
        rows.append(row)
    return header + "\n" + "\n".join(rows)


def replace_section(readme: str, start: str, end: str, content: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{content}\n{end}"
    updated, count = pattern.subn(lambda _: replacement, readme)
    if count != 1:
        raise RuntimeError(f"Expected one README section for {start}, found {count}")
    return updated


def render_readme() -> str:
    catalog = load_catalog()
    readme = README_PATH.read_text(encoding="utf-8")
    papers = catalog["papers"]
    for classification, (start, end) in SECTIONS.items():
        selected = [paper for paper in papers if paper["classification"] == classification]
        readme = replace_section(readme, start, end, generate_table(selected))
    return readme


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when README.md does not match the generated catalog tables.",
    )
    args = parser.parse_args()

    rendered = render_readme()
    current = README_PATH.read_text(encoding="utf-8")
    if args.check:
        if rendered != current:
            print("README.md is stale; run `python scripts/build_readme.py`.", file=sys.stderr)
            return 1
        print("README.md catalog tables are current.")
        return 0

    README_PATH.write_text(rendered, encoding="utf-8")
    print(f"Updated {README_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
