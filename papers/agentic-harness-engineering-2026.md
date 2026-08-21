<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Agentic Harness Engineering

## Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses

| Field | Value |
|---|---|
| Authors | Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Huang, Hang Yan, Zhenhua Han, Tao Gui, Yu-Gang Jiang |
| Venue | arXiv 2026 (preprint) |
| Evidence class | Direct comparison |
| First published | 2026-04-28 |
| Identifiers | [arXiv:2604.25850](https://arxiv.org/abs/2604.25850) |
| Artifact | [Official artifact](https://github.com/china-qijizhifeng/agentic-harness-engineering) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | baseline | not-reported | not-reported |

## Task

**Task.** Automatic evolution of coding-agent harnesses

**Benchmark or scale.** Terminal-Bench 2 and SWE-bench Verified

## Method

Closed-loop harness evolution using component, trajectory, and decision observability with evidence-backed edits and rollback

**Tags.** `harness-evolution` `observability` `memory` `verifier-loop`

## Reported evidence

Terminal-Bench 2 pass@1 improves from 69.7 to 77.0, above a human-designed Codex-CLI harness at 71.9; transfer uses 12% fewer tokens on SWE-bench Verified.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Abstract and Terminal-Bench 2 transfer and ablation results |

## Caveat

Preprint; model, harness, and evaluation-budget effects require careful separation.

## Primary links

- [Paper](https://arxiv.org/abs/2604.25850)
- [Artifact](https://github.com/china-qijizhifeng/agentic-harness-engineering)

---

Catalog ID: `agentic-harness-engineering-2026` · Metadata last reviewed with catalog release.
