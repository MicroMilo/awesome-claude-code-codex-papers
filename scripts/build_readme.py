#!/usr/bin/env python3
"""Build README stats, paper dossiers, research views, and JSON exports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "papers.yaml"
CENSUS_INDEX_PATH = ROOT / "data" / "audit" / "2026-conference-census" / "index.yaml"
PENDING_SUMMARY_PATH = ROOT / "data" / "audit" / "2026-pending-summary.json"
README_PATH = ROOT / "README.md"
README_ZH_PATH = ROOT / "README.zh-CN.md"

GENERATED_NOTICE = "<!-- Generated from data/papers.yaml; do not edit by hand. -->"

STATS_MARKERS = ("<!-- CATALOG:STATS:START -->", "<!-- CATALOG:STATS:END -->")
COVERAGE_MARKERS = (
    "<!-- CATALOG:COVERAGE:START -->",
    "<!-- CATALOG:COVERAGE:END -->",
)

DOMAIN_LABELS = {
    "software-engineering": "Software Engineering",
    "security": "Security",
    "systems-performance": "Systems & Performance",
    "machine-learning": "Machine Learning",
    "scientific-computing": "Scientific Computing",
    "formal-methods": "Formal Methods",
    "web-ui": "Web & UI",
    "documents": "Documents",
}

DOMAIN_LABELS_ZH = {
    "software-engineering": "软件工程",
    "security": "安全",
    "systems-performance": "系统与性能",
    "machine-learning": "机器学习",
    "scientific-computing": "科学计算",
    "formal-methods": "形式化方法",
    "web-ui": "Web 与 UI",
    "documents": "文档",
}

CONFERENCE_ORDER = [
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
]

PRODUCT_LABELS = {
    "claude-code": "Claude Code",
    "codex-cli": "Codex CLI",
}

CLASS_LABELS = {
    "direct": "Direct comparison",
    "related": "Related method",
    "evaluation": "Evaluation only",
}

CLASS_LABELS_ZH = {
    "direct": "直接对比",
    "related": "相关方法",
    "evaluation": "仅评测",
}

CONTROL_LABELS = {
    "yes": "same",
    "no": "different",
    "unknown": "unknown",
}

TABLE_HEADERS = {
    "en": [
        "System / paper",
        "Venue",
        "Product baseline",
        "Task",
        "What changed",
        "Reported evidence",
        "Controls",
    ],
    "zh": ["系统 / 论文", "会议", "产品 baseline", "任务", "新增方法", "论文结果", "可比性"],
}


def load_catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def paper_detail_link(paper: dict, root_prefix: str = "") -> str:
    return f"{root_prefix}papers/{paper['id']}.md"


def format_system_paper(paper: dict, root_prefix: str = "") -> str:
    system = escape_cell(paper["system"])
    links = [f"[paper]({paper['paper_url']})"]
    if paper.get("artifact_url"):
        links.append(f"[artifact]({paper['artifact_url']})")
    return f"**[{system}]({paper_detail_link(paper, root_prefix)})**<br>" + " · ".join(links)


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


def generate_table(papers: list[dict], language: str = "en", root_prefix: str = "") -> str:
    if not papers:
        return "_No reviewed papers in this class yet._"

    headers = TABLE_HEADERS[language]
    header = "| " + " | ".join(headers) + " |\n" + "|" + "---|" * len(headers)
    rows = []
    for paper in sorted(papers, key=lambda item: (-item["year"], item["system"].lower())):
        row = (
            "| "
            + " | ".join(
                [
                    format_system_paper(paper, root_prefix),
                    format_venue(paper),
                    format_products(paper),
                    escape_cell(paper["task"]["summary"]),
                    format_method(paper),
                    escape_cell(paper["evidence"]["result"]),
                    format_controls(paper),
                ]
            )
            + " |"
        )
        rows.append(row)
    return header + "\n" + "\n".join(rows)


def generate_stats(catalog: dict) -> str:
    papers = catalog["papers"]
    census_index = yaml.safe_load(CENSUS_INDEX_PATH.read_text(encoding="utf-8"))
    official_records = sum(
        int(item.get("record_count", 0)) for item in census_index.get("conference_files", [])
    )
    tracked_conferences = len(census_index.get("conference_files", []))
    direct = sum(paper["classification"] == "direct" for paper in papers)
    artifacts = sum(paper["artifact_status"] == "official" for paper in papers)
    domains = len({domain for paper in papers for domain in paper["domains"]})
    reviewed = catalog["reviewed_at"]
    badges = [
        ("papers", len(papers), "16616a"),
        ("official records indexed", f"{official_records:,}", "0f766e"),
        ("direct comparisons", direct, "dc6b46"),
        ("official artifacts", artifacts, "2563eb"),
        ("domains", domains, "4bcbd5"),
        ("conference series tracked", tracked_conferences, "7c3aed"),
        ("reviewed", reviewed, "475569"),
    ]
    images = []
    for label, value, color in badges:
        encoded_label = str(label).replace(" ", "%20")
        encoded_value = str(value).replace("-", "--").replace(",", "%2C")
        images.append(
            f'<img alt="{label}: {value}" '
            f'src="https://img.shields.io/badge/{encoded_label}-{encoded_value}-{color}">'
        )
    return '<p align="center">\n  ' + "\n  ".join(images) + "\n</p>"


def generate_coverage(catalog: dict, language: str) -> str:
    papers = catalog["papers"]
    domain_counts: dict[str, int] = defaultdict(int)
    conference_counts: dict[str, int] = defaultdict(int)
    for paper in papers:
        conference_counts[paper["conference"]] += 1
        for domain in paper["domains"]:
            domain_counts[domain] += 1

    labels = DOMAIN_LABELS_ZH if language == "zh" else DOMAIN_LABELS
    domain_items = " · ".join(
        f"<code>{labels[domain]} · {domain_counts[domain]}</code>"
        for domain in DOMAIN_LABELS
        if domain_counts[domain]
    )
    conference_items = " · ".join(
        f"<code>{conference} · {conference_counts[conference]}</code>"
        for conference in CONFERENCE_ORDER
        if conference_counts[conference]
    )
    domain_title = "研究领域" if language == "zh" else "Research domains"
    conference_title = "会议 / 来源" if language == "zh" else "Conferences / sources"
    return (
        '<p align="center">\n'
        f'  <a href="views/by-domain.md"><strong>{domain_title}</strong></a><br>\n'
        f"  {domain_items}<br><br>\n"
        f'  <a href="views/by-conference.md"><strong>{conference_title}</strong></a><br>\n'
        f"  {conference_items}\n"
        "</p>"
    )


def replace_section(text: str, start: str, end: str, content: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{content}\n{end}"
    updated, count = pattern.subn(lambda _: replacement, text)
    if count != 1:
        raise RuntimeError(f"Expected one generated section for {start}, found {count}")
    return updated


def render_marked_readme(path: Path, catalog: dict, language: str) -> str:
    text = path.read_text(encoding="utf-8")
    text = replace_section(text, *STATS_MARKERS, generate_stats(catalog))
    return replace_section(text, *COVERAGE_MARKERS, generate_coverage(catalog, language))


def short_authors(paper: dict) -> str:
    authors = paper["authors"]
    if len(authors) <= 3:
        return ", ".join(authors)
    return f"{', '.join(authors[:3])}, et al. ({len(authors)} authors)"


def artifact_label(paper: dict) -> str:
    status = paper["artifact_status"]
    if status == "not-found":
        return "Not found during the latest review"
    label = "Official artifact" if status == "official" else "Community artifact"
    return f"[{label}]({paper['artifact_url']})"


def render_paper_page(paper: dict) -> str:
    evidence = paper["evidence"]
    identifiers = []
    if paper.get("doi"):
        identifiers.append(f"[DOI:{paper['doi']}](https://doi.org/{paper['doi']})")
    if not identifiers:
        identifiers.append("Official conference source")

    product_rows = []
    for product in paper["products"]:
        product_rows.append(
            "| "
            + " | ".join(
                [
                    PRODUCT_LABELS[product["product"]],
                    product["role"],
                    escape_cell(product["model"]),
                    escape_cell(product["version"]),
                ]
            )
            + " |"
        )

    tags = " ".join(f"`{tag}`" for tag in paper["method"]["tags"]) or "None"
    published = paper.get("published_at", "Not recorded")
    artifact_item = (
        f"- [Artifact]({paper['artifact_url']})"
        if paper.get("artifact_url")
        else "- No official artifact was found during the latest review."
    )
    return f"""{GENERATED_NOTICE}

[← Paper index](README.md) · [Home](../README.md)

# {paper["system"]}

## {paper["title"]}

| Field | Value |
|---|---|
| Authors | {escape_cell(", ".join(paper["authors"]))} |
| Conference | {escape_cell(paper["conference"])} |
| Venue | {escape_cell(paper["venue"])} {paper["year"]} ({paper["publication_status"]}) |
| Domains | {escape_cell(", ".join(DOMAIN_LABELS[domain] for domain in paper["domains"]))} |
| Evidence class | {CLASS_LABELS[paper["classification"]]} |
| First published | {published} |
| Identifiers | {" · ".join(identifiers)} |
| Artifact | {artifact_label(paper)} |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
{chr(10).join(product_rows)}

## Task

**Task.** {paper["task"]["summary"]}

**Benchmark or scale.** {paper["task"]["benchmark"]}

## Method

{paper["method"]["summary"]}

**Tags.** {tags}

## Reported evidence

{evidence["result"]}

| Control | Recorded value |
|---|---|
| Same model | {evidence["same_model"]} |
| Same budget | {evidence["same_budget"]} |
| Evidence strength | {evidence["strength"]} |
| Claim type | {evidence["claim_type"]} |
| Comparison scope | {evidence["comparison_scope"]} |
| Source location | {escape_cell(evidence["source_location"])} |

## Caveat

{evidence["caveats"]}

## Primary links

- [Paper]({paper["paper_url"]})
{artifact_item}

---

Catalog ID: `{paper["id"]}` · Metadata last reviewed with catalog release.
"""


def render_paper_index(catalog: dict) -> str:
    rows = []
    for paper in sorted(catalog["papers"], key=lambda item: (-item["year"], item["system"])):
        rows.append(
            "| "
            + " | ".join(
                [
                    f"[{escape_cell(paper['system'])}]({paper['id']}.md)",
                    escape_cell(paper["title"]),
                    f"{paper['conference']} · {paper['venue']} {paper['year']}",
                    "<br>".join(DOMAIN_LABELS[domain] for domain in paper["domains"]),
                    CLASS_LABELS[paper["classification"]],
                    format_products(paper),
                    artifact_label(paper),
                ]
            )
            + " |"
        )
    return f"""{GENERATED_NOTICE}

[← Home](../README.md) · [Browse by product](../views/by-product.md)

# Paper dossiers

Every catalog entry has a generated evidence dossier. The YAML catalog remains the source of truth.

| System | Paper | Conference / venue | Domains | Evidence class | Product | Artifact |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""


def view_paper_link(paper: dict) -> str:
    return f"[{escape_cell(paper['system'])}](../papers/{paper['id']}.md)"


def render_views_index() -> str:
    return f"""{GENERATED_NOTICE}

[← Home](../README.md)

# Research views

- [By product](by-product.md) — Claude Code and Codex CLI separately.
- [By domain](by-domain.md) — software engineering, security, systems, formal methods, and more.
- [By conference](by-conference.md) — standardized 2026 conference series.
- [By method](by-method.md) — repository graphs, retrieval, verification, orchestration, and more.
- [Comparison fairness](fair-comparisons.md) — same-model and same-budget controls.
- [By exact venue](by-venue.md) — tracks, workshops, and proceedings labels as reported.
- [All paper dossiers](../papers/README.md) — one evidence page per paper.
"""


def render_by_product(catalog: dict) -> str:
    sections = []
    for product_id in ["claude-code", "codex-cli"]:
        papers = [
            paper
            for paper in catalog["papers"]
            if any(item["product"] == product_id for item in paper["products"])
        ]
        rows = []
        for paper in sorted(papers, key=lambda item: (-item["year"], item["system"])):
            rows.append(
                f"| {view_paper_link(paper)} | {paper['venue']} {paper['year']} | "
                f"{CLASS_LABELS[paper['classification']]} | "
                f"{escape_cell(paper['task']['summary'])} | {paper['evidence']['strength']} |"
            )
        sections.append(
            f"## {PRODUCT_LABELS[product_id]} ({len(papers)})\n\n"
            "| System | Venue | Evidence class | Task | Strength |\n"
            "|---|---|---|---|---|\n" + "\n".join(rows)
        )
    return f"""{GENERATED_NOTICE}

[← Research views](README.md) · [Home](../README.md)

# Papers by product

Product means the complete agent or harness evaluated by the paper,
not merely a model from the same vendor.

{chr(10).join(sections)}
"""


def render_by_method(catalog: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for paper in catalog["papers"]:
        for tag in paper["method"]["tags"]:
            grouped[tag].append(paper)

    sections = []
    for tag, papers in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        rows = []
        for paper in sorted(papers, key=lambda item: (-item["year"], item["system"])):
            rows.append(
                f"| {view_paper_link(paper)} | {paper['venue']} {paper['year']} | "
                f"{escape_cell(paper['method']['summary'])} |"
            )
        sections.append(
            f"## `{tag}` ({len(papers)})\n\n"
            "| System | Venue | Method |\n|---|---|---|\n" + "\n".join(rows)
        )
    return f"""{GENERATED_NOTICE}

[← Research views](README.md) · [Home](../README.md)

# Papers by method

Tags describe the intervention added around or instead of the production coding-agent baseline.

{chr(10).join(sections)}
"""


def render_by_domain(catalog: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for paper in catalog["papers"]:
        for domain in paper["domains"]:
            grouped[domain].append(paper)

    sections = []
    for domain in DOMAIN_LABELS:
        papers = grouped.get(domain, [])
        if not papers:
            continue
        rows = [
            f"| {view_paper_link(paper)} | {paper['conference']} | {paper['year']} | "
            f"{CLASS_LABELS[paper['classification']]} | {escape_cell(paper['task']['summary'])} |"
            for paper in sorted(papers, key=lambda item: (-item["year"], item["system"]))
        ]
        sections.append(
            f"## {DOMAIN_LABELS[domain]} ({len(papers)})\n\n"
            "| System | Conference | Year | Evidence class | Task |\n"
            "|---|---|---|---|---|\n" + "\n".join(rows)
        )
    return f"""{GENERATED_NOTICE}

[← Research views](README.md) · [Home](../README.md)

# Papers by domain

Domains describe the task or evidence area studied by each paper.
A paper may appear in more than one domain.

{chr(10).join(sections)}
"""


def render_by_conference(catalog: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for paper in catalog["papers"]:
        grouped[paper["conference"]].append(paper)

    sections = []
    for conference in CONFERENCE_ORDER:
        papers = grouped.get(conference, [])
        if not papers:
            continue
        rows = [
            f"| {view_paper_link(paper)} | {paper['venue']} | {paper['year']} | "
            f"{paper['publication_status']} | {CLASS_LABELS[paper['classification']]} |"
            for paper in sorted(papers, key=lambda item: (-item["year"], item["system"]))
        ]
        sections.append(
            f"## {conference} ({len(papers)})\n\n"
            "| System | Exact venue / track | Year | Status | Evidence class |\n"
            "|---|---|---|---|---|\n" + "\n".join(rows)
        )
    return f"""{GENERATED_NOTICE}

[← Research views](README.md) · [Home](../README.md)

# Papers by conference

Conference is a standardized series label used for filtering.
Exact tracks and proceedings names remain in the venue field.

{chr(10).join(sections)}
"""


def render_fair_comparisons(catalog: dict) -> str:
    direct = [paper for paper in catalog["papers"] if paper["classification"] == "direct"]
    groups = [
        (
            "Same model and same budget",
            [
                paper
                for paper in direct
                if paper["evidence"]["same_model"] == "yes"
                and paper["evidence"]["same_budget"] == "yes"
            ],
        ),
        (
            "Known model or budget mismatch",
            [
                paper
                for paper in direct
                if "no" in {paper["evidence"]["same_model"], paper["evidence"]["same_budget"]}
            ],
        ),
        (
            "Control parity not fully reported",
            [
                paper
                for paper in direct
                if "unknown" in {paper["evidence"]["same_model"], paper["evidence"]["same_budget"]}
                and "no" not in {paper["evidence"]["same_model"], paper["evidence"]["same_budget"]}
            ],
        ),
    ]
    sections = []
    for title, papers in groups:
        rows = []
        for paper in sorted(papers, key=lambda item: (-item["year"], item["system"])):
            evidence = paper["evidence"]
            rows.append(
                f"| {view_paper_link(paper)} | {evidence['same_model']} | "
                f"{evidence['same_budget']} | {evidence['strength']} | "
                f"{escape_cell(evidence['caveats'])} |"
            )
        table = "_No papers in this group._"
        if rows:
            table = (
                "| System | Same model | Same budget | Strength | Caveat |\n"
                "|---|---|---|---|---|\n" + "\n".join(rows)
            )
        sections.append(f"## {title} ({len(papers)})\n\n{table}")
    return f"""{GENERATED_NOTICE}

[← Research views](README.md) · [Home](../README.md)

# Comparison fairness

“Direct comparison” means a numeric head-to-head was reported.
It does not mean the model, budget, tools, or product policy were held fixed.

{chr(10).join(sections)}
"""


def render_by_venue(catalog: dict) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for paper in catalog["papers"]:
        grouped[paper["venue"]].append(paper)
    sections = []
    for venue, papers in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        rows = [
            f"| {view_paper_link(paper)} | {paper['year']} | "
            f"{paper['publication_status']} | {CLASS_LABELS[paper['classification']]} |"
            for paper in sorted(papers, key=lambda item: (-item["year"], item["system"]))
        ]
        sections.append(
            f"## {venue} ({len(papers)})\n\n"
            "| System | Year | Status | Evidence class |\n|---|---|---|---|\n" + "\n".join(rows)
        )
    return f"""{GENERATED_NOTICE}

[← Research views](README.md) · [Home](../README.md)

# Papers by venue

Main-conference, workshop, benchmark-track, and preprint status remain explicit.

{chr(10).join(sections)}
"""


def render_all() -> dict[Path, str]:
    catalog = load_catalog()
    catalog_json = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    pending_summary = json.loads(PENDING_SUMMARY_PATH.read_text(encoding="utf-8"))
    pending_summary_json = json.dumps(pending_summary, indent=2, ensure_ascii=False) + "\n"
    outputs = {
        README_PATH: render_marked_readme(README_PATH, catalog, "en"),
        README_ZH_PATH: render_marked_readme(README_ZH_PATH, catalog, "zh"),
        ROOT / "data" / "papers.json": catalog_json,
        ROOT / "website" / "data" / "catalog.json": catalog_json,
        ROOT / "website" / "data" / "pending-summary.json": pending_summary_json,
        ROOT / "papers" / "README.md": render_paper_index(catalog),
        ROOT / "views" / "README.md": render_views_index(),
        ROOT / "views" / "by-product.md": render_by_product(catalog),
        ROOT / "views" / "by-domain.md": render_by_domain(catalog),
        ROOT / "views" / "by-conference.md": render_by_conference(catalog),
        ROOT / "views" / "by-method.md": render_by_method(catalog),
        ROOT / "views" / "fair-comparisons.md": render_fair_comparisons(catalog),
        ROOT / "views" / "by-venue.md": render_by_venue(catalog),
    }
    for paper in catalog["papers"]:
        outputs[ROOT / "papers" / f"{paper['id']}.md"] = render_paper_page(paper)
    return {
        path: (content.rstrip() + "\n" if path.suffix == ".md" else content)
        for path, content in outputs.items()
    }


def generated_extras(expected: set[Path]) -> list[Path]:
    extras = []
    for directory in [ROOT / "papers", ROOT / "views"]:
        if not directory.exists():
            continue
        for path in directory.glob("*.md"):
            if path not in expected and path.read_text(encoding="utf-8").startswith(
                GENERATED_NOTICE
            ):
                extras.append(path)
    return extras


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when any generated catalog file is missing or stale.",
    )
    args = parser.parse_args()

    outputs = render_all()
    if args.check:
        stale = [
            path
            for path, content in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != content
        ]
        extras = generated_extras(set(outputs))
        if stale or extras:
            for path in stale:
                print(f"stale or missing: {path.relative_to(ROOT)}", file=sys.stderr)
            for path in extras:
                print(f"unexpected generated file: {path.relative_to(ROOT)}", file=sys.stderr)
            print("Run `python scripts/build_readme.py`.", file=sys.stderr)
            return 1
        print(f"All {len(outputs)} generated catalog files are current.")
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
    extras = generated_extras(set(outputs))
    if extras:
        print("Removing obsolete generated files:")
        for path in extras:
            path.unlink()
            print(f"- {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
