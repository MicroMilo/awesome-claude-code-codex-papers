<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# DevOps-Gym

## DevOps-Gym: Benchmarking AI Agents in Software DevOps Cycle

| Field | Value |
|---|---|
| Authors | Yuheng Tang, Kaijie Zhu, Bonan Ruan, Chuqi Zhang, Michael Yang, Hongwei Li, Suyue Guo, Tianneng Shi, Zekun Li, Christopher Kruegel, Giovanni Vigna, Dawn Song, William Yang Wang, Lun Wang, Yangruibo Ding, Zhenkai Liang, Wenbo Guo |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Software Engineering |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude-4-Sonnet | not-reported |

## Task

**Task.** Evaluate coding agents across build/configuration, monitoring, issue resolving, and test generation.

**Benchmark or scale.** DevOps-Gym, 704 tasks from 30+ Java/Go projects plus 14 end-to-end pipeline tasks

## Method

A realistic dynamic DevOps environment with standardized tool interfaces, multi-stage workflows, and stage-specific metrics.

**Tags.** `benchmark-design` `observability` `test-feedback` `coordination`

## Reported evidence

Claude Code with Claude-4-Sonnet reports 51.85% build/configuration, 20.56% monitoring, 23.87% issue resolving, and 13.87% test generation success.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 4.1 Experimental Setup; Table 1; Appendix D.3 Table 4 |

## Caveat

The paper evaluates Claude Code as one agent framework; exact product version and per-task token budget are not reported.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/15e35461247bbd05fa890d384060c847-Abstract-Conference.html)
- No official artifact was found during the latest review.

---

Catalog ID: `devops-gym-2026` · Metadata last reviewed with catalog release.
