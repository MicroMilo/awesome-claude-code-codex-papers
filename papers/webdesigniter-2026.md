<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# WebDesignIter

## WebDesignIter: Co-Evolving Design Knowledge for Repository-Level Front-End Code Generation

| Field | Value |
|---|---|
| Authors | Zheng Pei, Mingwei Liu, Zhenxi Chen, Zihao Wang, Yanlin Wang |
| Venue | arXiv 2026 (preprint) |
| Evidence class | Direct comparison |
| First published | 2026-07-12 |
| Identifiers | [arXiv:2607.10621](https://arxiv.org/abs/2607.10621) |
| Artifact | [Official artifact](https://github.com/SYSUSELab/WebDesignIter) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |
| Codex CLI | baseline | not-reported | not-reported |

## Task

**Task.** Repository-level front-end code generation

**Benchmark or scale.** Web-Bench

## Method

Persistent architecture and design knowledge graph, design-informed planning, targeted patches, and sandbox repair

**Tags.** `structured-state` `repository-graph` `retrieval` `test-feedback`

## Reported evidence

Average Pass@2 improves by 9.55 percentage points over existing baselines; removing design knowledge reduces Pass@1 by 11.4 points.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Abstract, main Web-Bench comparison, and design-knowledge ablation |

## Caveat

Front-end-specific benchmark and preprint status.

## Primary links

- [Paper](https://arxiv.org/abs/2607.10621)
- [Artifact](https://github.com/SYSUSELab/WebDesignIter)

---

Catalog ID: `webdesigniter-2026` · Metadata last reviewed with catalog release.
