<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# RepoOMP

## RepoOMP: Repository-Aware Hotspot OpenMP Parallelization via Dependency-Aware Context Reduction

| Field | Value |
|---|---|
| Authors | Yongjie Qian, Ke Gao, Zhibin Zhang, Shaohui Peng, Ling Li |
| Venue | arXiv 2026 (preprint) |
| Evidence class | Direct comparison |
| First published | 2026-08-06 |
| Identifiers | [arXiv:2608.05855](https://arxiv.org/abs/2608.05855) |
| Artifact | [Official artifact](https://github.com/Qlalq/RepoOMP_Simplified) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |

## Task

**Task.** Repository-aware OpenMP hotspot parallelization

**Benchmark or scale.** 951 hotspots including 330 accepted real-world hotspots

## Method

Multi-granularity dependency graph, rule-or-LLM hotspot routing, reduced transformation context, and compile/workload/speedup validation

**Tags.** `repository-graph` `context-reduction` `deterministic-search` `performance-feedback` `verifier-loop`

## Reported evidence

Across nine detailed kernels, speedup improves 18% to 28% and token cost falls 47% to 68% relative to unstructured Claude Code.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Abstract and nine-kernel cross-backbone comparison |

## Caveat

Domain-specific high-performance-computing task and preprint status.

## Primary links

- [Paper](https://arxiv.org/abs/2608.05855)
- [Artifact](https://github.com/Qlalq/RepoOMP_Simplified)

---

Catalog ID: `repoomp-2026` · Metadata last reviewed with catalog release.
