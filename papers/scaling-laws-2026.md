<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SLDAgent

## Can Language Models Discover Scaling Laws?

| Field | Value |
|---|---|
| Authors | Haowei Lin, Haotian Ye, Wenzheng Feng, Quzhe Huang, Yujun Li, Hubert Lim, Zhengrui Li, Xiangyu Wang, Jianzhu Ma, Yitao Liang, James Zou |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Machine Learning, Scientific Computing |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude-Haiku-4.5; Claude-Sonnet-4.5 | 1.0.102 |
| Codex CLI | baseline | o4-mini; GPT-5 | 0.29.0 |

## Task

**Task.** Discover symbolic scaling laws from experimental data with executable code agents.

**Benchmark or scale.** SLDBench, eight scaling-law discovery tasks

## Method

Evolution-based program search jointly optimizes symbolic expressions and fitting procedures, with execution feedback and MAP-Elites selection.

**Tags.** `benchmark-design` `deterministic-search` `performance-feedback` `test-feedback`

## Reported evidence

SLDAgent reaches average R2 0.748 with GPT-5 versus 0.550 for Codex GPT-5, and improves over Claude Code rows for both Claude-Haiku-4.5 and Claude-Sonnet-4.5.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | benchmark-only |
| Source location | Section 4.1 Agent baselines; Table 3; Appendix B.5; Appendix D |

## Caveat

Provider-specific rows compare SLDAgent with native agents under different harnesses; the paper reports product versions but not exact token or temperature settings.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/636d57c09a5baacd83722639265802f6-Abstract-Conference.html)
- No official artifact was found during the latest review.

---

Catalog ID: `scaling-laws-2026` · Metadata last reviewed with catalog release.
