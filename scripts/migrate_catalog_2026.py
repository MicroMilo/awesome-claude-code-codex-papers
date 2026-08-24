#!/usr/bin/env python3
"""Create the 2026 official-source main catalog from the audited seed data."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "papers.yaml"

OVERRIDES = {
    "qlcoder-2026": {
        "title": "QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities",
        "conference": "ICLR",
        "venue": "ICLR Conference",
        "paper_url": "https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html",
        "publication_status": "main",
        "classification": "direct",
        "system": "QLCoder",
        "products": [
            {
                "product": "claude-code",
                "role": "baseline",
                "model": "Claude Sonnet 4",
                "version": "not-reported",
                "reasoning_mode": "not-reported",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "maximum 10 iterations per CVE and agent baseline",
                "runs": "not-reported",
                "tool_permissions": "Claude Code framework with CodeQL MCP/LSP and execution feedback",
            },
            {
                "product": "codex-cli",
                "role": "baseline",
                "model": "GPT-5",
                "version": "not-reported",
                "reasoning_mode": "minimal and medium",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "maximum 10 iterations per CVE and agent baseline",
                "runs": "not-reported",
                "tool_permissions": "Codex CLI official tools; exact permissions not reported",
            },
        ],
        "experiment": {
            "reasoning_mode": "Codex GPT-5 minimal and medium; Claude Sonnet 4 not-reported",
            "temperature": "not-reported",
            "max_output_tokens": "not-reported",
            "time_budget": "not-reported",
            "turn_budget": "maximum 10 iterations per CVE and agent baseline",
            "token_budget": "not-reported",
            "api_budget": "not-reported",
            "runs": "not-reported",
            "tool_permissions": "QLCoder MCP interface exposes CodeQL LSP, retrieval, and execution feedback; baseline permissions are product defaults",
            "baseline_config": "Claude Code-only; Codex with GPT-5 minimal/medium; Gemini CLI; static-analysis baselines IRIS and CodeQL suites",
        },
        "evidence": {
            "result": "QLCoder synthesizes correct queries for 53.4% of CVEs versus 10% for Claude Code-only; its query F1 is 0.70, versus 0.048 for IRIS and 0.073 for CodeQL suites.",
            "same_model": "unknown",
            "same_budget": "unknown",
            "strength": "high",
            "claim_type": "quality",
            "comparison_scope": "product-level",
            "source_location": "Section 4.1 Experimental Setup; Table 2; Table 5; Appendix A",
            "caveats": "The task is CodeQL security-query synthesis, not general repository-level software engineering; GPT-5 reasoning settings differ across Codex baseline rows.",
        },
        "method": {
            "summary": "CVE-grounded retrieval, AST/LSP guidance, an MCP interface, and an executable CodeQL validator that feeds back into iterative query repair.",
            "tags": ["retrieval", "verifier-loop", "static-analysis"],
        },
        "task": {
            "summary": "CodeQL query synthesis from CVE metadata",
            "benchmark": "176 CVEs across 111 Java projects",
        },
    },
    "rpg-zerorepo-2026": {
        "conference": "ICLR",
        "venue": "ICLR Conference",
        "paper_url": "https://proceedings.iclr.cc/paper_files/paper/2026/hash/9482f45fdd89aba9130bb04c44f788a9-Abstract-Conference.html",
        "publication_status": "main",
        "classification": "direct",
        "system": "ZeroRepo / RPG",
        "products": [
            {
                "product": "claude-code",
                "role": "baseline",
                "model": "claude 4 sonnet",
                "version": "not-reported",
                "reasoning_mode": "official strongest model; exact effort not reported",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "averaged across 30 rounds",
                "runs": "30 rounds",
                "tool_permissions": "terminal agent with web search enabled",
            },
            {
                "product": "codex-cli",
                "role": "baseline",
                "model": "o3 pro",
                "version": "not-reported",
                "reasoning_mode": "official strongest model; exact effort not reported",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "averaged across 30 rounds",
                "runs": "30 rounds",
                "tool_permissions": "terminal agent with web search enabled",
            },
        ],
        "experiment": {
            "reasoning_mode": "Codex CLI o3 pro; Claude Code CLI claude 4 sonnet; exact effort not reported",
            "temperature": "not-reported",
            "max_output_tokens": "not-reported",
            "time_budget": "not-reported",
            "turn_budget": "not-reported",
            "token_budget": "not-reported",
            "api_budget": "not-reported",
            "runs": "30 rounds for strong baselines and ZeroRepo",
            "tool_permissions": "Terminal agents can retrieve real-world knowledge via web search",
            "baseline_config": "Claude Code CLI, Codex CLI, Gemini CLI, OpenHands, and workflow baselines compared with ZeroRepo/RPG",
        },
        "evidence": {
            "result": "ZeroRepo reaches 81.5% functional coverage and 69.7% test accuracy, improving over Claude Code by 27.3 and 35.8 points; it produces about 36K lines and 445K code tokens.",
            "same_model": "no",
            "same_budget": "unknown",
            "strength": "high",
            "claim_type": "quality",
            "comparison_scope": "product-level",
            "source_location": "Section 3.3 Baselines; Section 4.3; RepoCraft main-results table",
            "caveats": "ZeroRepo uses a different backbone/configuration from each terminal-product baseline, so model and harness effects are mixed.",
        },
        "method": {
            "summary": "A persistent repository planning graph over features, functions, files, interfaces, and data flow guides staged generation, dependency-aware planning, and validation.",
            "tags": [
                "structured-state",
                "repository-graph",
                "dependency-aware-planning",
                "test-feedback",
            ],
        },
    },
    "artemis-2026": {
        "conference": "ICLR",
        "venue": "ICLR Conference",
        "paper_url": "https://proceedings.iclr.cc/paper_files/paper/2026/hash/0410c2ff9f872efe5a7c61a4323a5da3-Abstract-Conference.html",
        "publication_status": "main",
        "classification": "direct",
        "system": "ARTEMIS",
        "products": [
            {
                "product": "claude-code",
                "role": "baseline",
                "model": "Claude Sonnet 4",
                "version": "not-reported",
                "reasoning_mode": "not-reported",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "runs to completion; human-comparison window is 10 hours",
                "runs": "not-reported",
                "tool_permissions": "live enterprise-network penetration-testing environment",
            },
            {
                "product": "codex-cli",
                "role": "baseline",
                "model": "GPT-5",
                "version": "not-reported",
                "reasoning_mode": "not-reported",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "runs to completion; human-comparison window is 10 hours",
                "runs": "not-reported",
                "tool_permissions": "live enterprise-network penetration-testing environment",
            },
        ],
        "experiment": {
            "reasoning_mode": "ARTEMIS A1 uses GPT-5; A2 uses a multi-model supervisor ensemble with Claude Sonnet 4 sub-agents",
            "temperature": "not-reported",
            "max_output_tokens": "not-reported",
            "time_budget": "ARTEMIS configurations execute for 16 hours; first 10 hours evaluated for human comparability",
            "turn_budget": "not-reported",
            "token_budget": "not-reported",
            "api_budget": "not-reported",
            "runs": "not-reported",
            "tool_permissions": "same VM/live network setting for agents; scaffold-specific capabilities differ",
            "baseline_config": "OpenAI Codex with GPT-5, Claude Code with Claude Sonnet 4, CyAgent, Incalmo, MAPTA, and human professionals",
        },
        "evidence": {
            "result": "ARTEMIS finds 9 valid vulnerabilities with an 82% valid-submission rate, ranks second overall, and outperforms 9 of 10 human participants in the reported penetration-testing study.",
            "same_model": "unknown",
            "same_budget": "no",
            "strength": "medium",
            "claim_type": "mixed",
            "comparison_scope": "product-level",
            "source_location": "Section 4.2 Agent Results; Table 1; Appendix A and J",
            "caveats": "This is live-network cybersecurity, not general coding; runtime limits, model mixtures, refusal behavior, and product policies differ.",
        },
    },
    "formact-2026": {
        "conference": "ICML",
        "venue": "ICML Main Conference",
        "paper_url": "https://openreview.net/forum?id=n7Ta0YEcgw",
        "source_type": "openreview-conference",
        "publication_status": "main",
        "classification": "direct",
        "system": "FormAct",
        "products": [
            {
                "product": "codex-cli",
                "role": "baseline",
                "model": "gpt-5.2-2025-12-11",
                "version": "not-reported",
                "reasoning_mode": "not-reported",
                "temperature": "1.0",
                "max_output_tokens": "32768",
                "budget": "multi-pass; exact budget not reported",
                "runs": "not-reported",
                "tool_permissions": "not-reported",
            }
        ],
        "experiment": {
            "reasoning_mode": "not-reported",
            "temperature": "1.0",
            "max_output_tokens": "32768",
            "time_budget": "not-reported",
            "turn_budget": "multi-pass baseline; exact turn budget not reported",
            "token_budget": "not-reported",
            "api_budget": "not-reported",
            "runs": "not-reported",
            "tool_permissions": "not-reported",
            "baseline_config": "Repo Codex (OpenAI, 2025), multi-pass; all methods and evaluation use gpt-5.2-2025-12-11",
        },
        "evidence": {
            "result": "Render correctness is 4.81 versus 4.39 for multi-pass Codex; human rank-1 rate is 0.760 versus 0.140. Content alignment is the caveat where Codex is slightly higher.",
            "same_model": "yes",
            "same_budget": "unknown",
            "strength": "high",
            "claim_type": "mixed",
            "comparison_scope": "product-level",
            "source_location": "Section 5.1 Experimental Setup; Section 5.2; main comparison table; review-refinement ablation",
            "caveats": "The task is rich-format document editing rather than source-code repair; the paper does not report a CLI version or a matched multi-pass budget.",
        },
    },
    "terminal-bench-2-2026": {
        "title": "Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces",
        "conference": "ICLR",
        "venue": "ICLR Conference",
        "paper_url": "https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html",
        "source_type": "official-proceedings",
        "publication_status": "dataset-benchmark",
        "classification": "evaluation",
        "system": "Terminal-Bench 2.0",
        "products": [
            {
                "product": "claude-code",
                "role": "evaluated",
                "model": "Claude Opus 4.5; Claude Sonnet 4.5; Claude Opus 4.1; Claude Haiku 4.5",
                "version": "not-reported",
                "reasoning_mode": "provider default medium",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "89 tasks; token totals vary by agent-model combination",
                "runs": "not-reported",
                "tool_permissions": "Claude Code tool scaffold in Harbor",
            },
            {
                "product": "codex-cli",
                "role": "evaluated",
                "model": "GPT-5.2; GPT-5; GPT-5-Mini; GPT-5-Nano",
                "version": "not-reported",
                "reasoning_mode": "provider default medium",
                "temperature": "not-reported",
                "max_output_tokens": "not-reported",
                "budget": "89 tasks; token totals vary by agent-model combination",
                "runs": "not-reported",
                "tool_permissions": "Codex CLI tool scaffold in Harbor",
            },
        ],
        "experiment": {
            "reasoning_mode": "provider default medium for configurable Anthropic/OpenAI models",
            "temperature": "not-reported",
            "max_output_tokens": "not-reported",
            "time_budget": "most attempts under 20 minutes; some up to 2 hours",
            "turn_budget": "not-reported",
            "token_budget": "Table 2 reports aggregate input/output tokens per 74 tasks; per-task budgets vary",
            "api_budget": "approximately $1–$100 per run depending on model",
            "runs": "not-reported",
            "tool_permissions": "Harbor containerized terminal tasks; Claude Code and Codex CLI use their product scaffolds",
            "baseline_config": "Claude Code, Codex CLI, Gemini CLI, OpenHands, Mini-SWE-Agent, and Terminus 2 across 89 Terminal-Bench 2.0 tasks",
        },
        "evidence": {
            "result": "Codex CLI with GPT-5.2 reaches 62.9% resolution; Claude Code with Claude Opus 4.5 reaches 52.1%, with lower Claude Code rows for Sonnet 4.5, Opus 4.1, and Haiku 4.5 reported in Table 2.",
            "same_model": "no",
            "same_budget": "no",
            "strength": "high",
            "claim_type": "diagnostic",
            "comparison_scope": "benchmark-only",
            "source_location": "Section 3.2 Agents; Section 3.3 Models; Table 2; Appendix B",
            "caveats": "This paper evaluates products and models rather than proposing a method that beats them; token and cost budgets vary substantially across agent-model combinations.",
        },
        "task": {
            "summary": "Evaluate industrial and open-source agents on realistic command-line tasks with executable tests.",
            "benchmark": "Terminal-Bench 2.0: 89 hard tasks, Harbor harness, containerized environments",
        },
        "method": {
            "summary": "A benchmark design with realistic terminal environments, human-written solutions, executable tests, standardized Harbor tasks, and failure-mode analysis.",
            "tags": ["benchmark-design", "verifier-loop", "observability", "adversarial-testing"],
        },
    },
}


def migrate(catalog: dict) -> dict:
    source_by_id = {paper["id"]: paper for paper in catalog.get("papers", [])}
    papers = []
    for paper_id, override in OVERRIDES.items():
        if paper_id not in source_by_id:
            raise KeyError(f"Missing audited seed paper: {paper_id}")
        paper = {
            key: value
            for key, value in source_by_id[paper_id].items()
            if key not in {"arxiv_id", "published_at"}
        }
        paper.update(override)
        paper.setdefault("source_type", "official-proceedings")
        paper["year"] = 2026
        paper["year_tag"] = 2026
        paper["conference_tag"] = paper["conference"]
        paper["audit_status"] = "included"
        papers.append(paper)
    return {"catalog_version": 2, "reviewed_at": "2026-08-21", "papers": papers}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=SOURCE)
    args = parser.parse_args()
    catalog = yaml.safe_load(args.source.read_text(encoding="utf-8"))
    migrated = migrate(catalog)
    args.output.write_text(
        yaml.safe_dump(migrated, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8"
    )
    print(
        f"Wrote {args.output.relative_to(ROOT)} with {len(migrated['papers'])} official 2026 papers."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
