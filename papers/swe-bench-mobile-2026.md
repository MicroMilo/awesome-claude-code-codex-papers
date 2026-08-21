<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SWE-Bench Mobile

## SWE-Bench Mobile: Can Large Language Model Agents Develop Industry-Level Mobile Applications?

| Field | Value |
|---|---|
| Authors | Muxin Tian, Zhe Wang, Blair Yang, Zhenwei Tang, Kunlun Zhu, Honghua Dong, Hanchen Li, Xinni Xie, Guangjing Wang, Jiaxuan You |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering, Web & UI |
| Evidence class | Evaluation only |
| First published | 2026-02-10 |
| Identifiers | [arXiv:2602.09540](https://arxiv.org/abs/2602.09540) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | multiple | 2.1.37 |
| Codex CLI | evaluated | multiple | 0.77.0 |

## Task

**Task.** Industry-scale iOS feature development from PRDs and Figma designs

**Benchmark or scale.** 50 tasks over a 500,000-line Swift and Objective-C production codebase

## Method

Multimodal mobile benchmark with private tests, cross-agent model controls, cost analysis, prompt ablations, and error taxonomy

**Tags.** `benchmark-design` `visual-review` `test-feedback`

## Reported evidence

Across 22 configurations, the best task success is 12%; the same Opus 4.5 model varies by up to 6x across agents, and a defensive-programming prompt raises Claude Code test pass from 19.3% to 26.7%.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Figures 4 to 7 and Tables 3 to 6 |

## Caveat

The public artifact URL reported in the PDF was unavailable during review; product results vary across models and include MCP-assisted visual access.

## Primary links

- [Paper](https://arxiv.org/abs/2602.09540)
- No official artifact was found during the latest review.

---

Catalog ID: `swe-bench-mobile-2026` · Metadata last reviewed with catalog release.
