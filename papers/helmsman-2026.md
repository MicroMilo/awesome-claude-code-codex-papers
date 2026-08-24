<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Helmsman

## Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents

| Field | Value |
|---|---|
| Authors | Haoyuan Li, Mathias Funk, Aaqib Saeed |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (main) |
| Domains | Software Engineering, Machine Learning |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/haoyuan-l/Helmsman) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Sonnet 4.5 | not-reported |
| Codex CLI | baseline | GPT-5.1-Codex | not-reported |

## Task

**Task.** End-to-end synthesis of federated learning systems from high-level specifications.

**Benchmark or scale.** AgentFL-Bench, 16 tasks across five federated-learning research areas; cross-silo (5 clients) and cross-device (10 clients) settings

## Method

Human-in-the-loop planning, modular code generation by collaborative agent teams, and closed-loop sandboxed evaluation and refinement with hierarchical runtime and semantic verification.

**Tags.** `multi-agent` `coordination` `verifier-loop` `test-feedback` `benchmark-design`

## Reported evidence

Claude Code with Claude Sonnet 4.5 reports 43.75% success and Codex with GPT-5.1-Codex reports 37.50%; Helmsman with Claude Sonnet 4.5 and GPT-5.1 reports 100% success in the paper's 16-task comparison.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Section 4.2 Implementation Details; Appendix A.1 Tables 8-12; Appendix A.2 Table 12; PDF p. 15 |

## Caveat

The paper compares a multi-agent federated-learning system synthesis framework against product code-synthesis baselines. CLI versions, temperature, tool permissions, and exact budget caps are not reported. Helmsman's main backbone uses Gemini-2.5-flash for planning and Claude-Sonnet-4.0 for coding and evaluation; additional experiments use Claude-Sonnet-4.5 and GPT-5.1.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1c364d98a5cdc426fd8c76fbb2c10e34-Abstract-Conference.html)
- [Artifact](https://github.com/haoyuan-l/Helmsman)

---

Catalog ID: `helmsman-2026` · Metadata last reviewed with catalog release.
