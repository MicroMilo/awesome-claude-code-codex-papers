<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Co-Coder

## When Parallelism Pays Off: Cohesion-Aware Task Partitioning for Multi-Agent Coding

| Field | Value |
|---|---|
| Authors | Xu Yang, Lunyiu Nie, Ethan Chandra, Stanislav Gannutin, Fangru Lin, Swarat Chaudhuri |
| Venue | arXiv 2026 (preprint) |
| Evidence class | Direct comparison |
| First published | 2026-05-31 |
| Identifiers | [arXiv:2606.00953](https://arxiv.org/abs/2606.00953) |
| Artifact | [Official artifact](https://github.com/Flitternie/CoCoder) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | Agent Teams |

## Task

**Task.** Parallel multi-agent coding

**Benchmark or scale.** 28 DevEval and CodeProjectEval tasks

## Method

Static dependency graph partitioning, structural hub isolation, community detection, and dependency-aware scheduling

**Tags.** `repository-graph` `dependency-aware-planning` `multi-agent` `parallelism`

## Reported evidence

Pass rate improves 14.0%, wall-clock speedup reaches 2.10x, and API cost falls 35% relative to Claude Code Agent Teams and simpler schedules.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Abstract and DevEval and CodeProjectEval comparisons |

## Caveat

Small 28-task evaluation and preprint status.

## Primary links

- [Paper](https://arxiv.org/abs/2606.00953)
- [Artifact](https://github.com/Flitternie/CoCoder)

---

Catalog ID: `co-coder-2026` · Metadata last reviewed with catalog release.
