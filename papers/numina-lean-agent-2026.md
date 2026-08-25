<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Numina-Lean-Agent

## Numina-Lean-Agent: An Open and General Agentic Reasoning System for Formal Mathematics

| Field | Value |
|---|---|
| Authors | Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Yunzhou Xie, Junqiao Zhao, Qiufeng Wang, Lihong Zhi, Jia Li, Wenda Li |
| Conference | ICML |
| Venue | ICML Main Conference 2026 (main) |
| Domains | Formal Methods |
| Evidence class | Related method |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/project-numina/numina-lean-agent) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | host | Claude Opus 4.5 | not-reported |

## Task

**Task.** Prove and formalize mathematics in Lean, including olympiad problems and a paper-scale Brascamp-Lieb development.

**Benchmark or scale.** Putnam 2025 (12 problems) plus an interactive formalization case study exceeding 8,000 lines of Lean

## Method

Claude Code is extended with MCP tools for Lean proof-state interaction, semantic theorem retrieval, iterative informal proving, external discussion, and subagent-based context decomposition.

**Tags.** `verifier-loop` `retrieval` `multi-agent` `context-reduction` `structured-state`

## Reported evidence

Numina-Lean-Agent with Claude Opus 4.5 solves all 12 Putnam 2025 problems, matching AxiomProver and exceeding Aristotle by two problems; the paper also reports more than 8,000 lines of Lean produced during a sub-two-week human-agent formalization.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | component-level |
| Source location | Section 2 Numina-Lean-Agent; Section 3.1 Performance; Tables 1-4; Section 4 in arXiv v1 |

## Caveat

Claude Code is the host scaffold rather than an independently measured baseline. Product version, decoding settings, output-token cap, and total failed attempts are not reported; the very large A5/B6 budgets are approximate rather than exact accounting.

## Primary links

- [Paper](https://icml.cc/virtual/2026/poster/66755)
- [Artifact](https://github.com/project-numina/numina-lean-agent)
- [Identity-verified evidence copy](https://arxiv.org/abs/2601.14027v1) (submittedVersion; not the acceptance source)

---

Catalog ID: `numina-lean-agent-2026` · Metadata last reviewed with catalog release.
