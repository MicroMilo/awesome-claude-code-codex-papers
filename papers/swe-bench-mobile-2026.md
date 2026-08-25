<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SWE-Bench Mobile

## SWE-Bench Mobile: Can Large Language Model Agents Develop Industry-Level Mobile Applications?

| Field | Value |
|---|---|
| Authors | Muxin Tian, Zhe Wang, Blair Yang, Zhenwei Tang, Kunlun Zhu, Honghua Dong, Hanchen Li, Xinni Xie, Guangjing Wang, Jiaxuan You |
| Conference | KDD |
| Venue | KDD 2026 Applied Data Science Track (July Cycle) 2026 (dataset-benchmark) |
| Domains | Software Engineering, Web & UI |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | [DOI:10.1145/3770855.3818488](https://doi.org/10.1145/3770855.3818488) |
| Artifact | [Official artifact](https://swebenchmobile.com/) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | evaluated | GLM-4.6; Claude Sonnet 4.5; GPT-5; Claude Opus 4.5; GPT-5.1 | v0.77.0 |
| Claude Code | evaluated | GLM-4.6; Claude Sonnet 4.5; Claude Opus 4.5; Claude Haiku | v2.1.37 |

## Task

**Task.** Implement production iOS features from product requirements, Figma designs, and an existing Swift/Objective-C codebase.

**Benchmark or scale.** SWE-Bench Mobile; 50 proprietary tasks, 449 diff-based tests, about 500K lines of code, and 22 agent-model configurations

## Method

A hosted, contamination-resistant mobile software-engineering benchmark with real PRDs, multimodal design inputs, production code, and task-specific patch tests.

**Tags.** `benchmark-design`

## Reported evidence

Codex + GLM-4.6 reaches 12.0% task success and 19.6% test pass; Claude Code + GLM-4.6 reaches 10.0% and 26.7%. Across all 22 configurations, no system exceeds 12.0% task success, and success falls from 18% on 1-2-file tasks to 2% on tasks requiring 7 or more files.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 3.1-3.9; Appendix B Tables 5-6; Appendix E Reproducibility in arXiv v1 |

## Caveat

The official KDD DOI proves venue identity, while detailed evidence was checked in the identity-matched arXiv v1 because the ACM PDF endpoint was unavailable to the crawler. The benchmark uses a proprietary codebase and diff-based tests rather than compiling or running the iOS app; model snapshots, hard token limits, and common time or cost caps are not reported.

## Primary links

- [Paper](https://doi.org/10.1145/3770855.3818488)
- [Artifact](https://swebenchmobile.com/)
- [Identity-verified evidence copy](https://arxiv.org/abs/2602.09540v1) (submittedVersion; not the acceptance source)

---

Catalog ID: `swe-bench-mobile-2026` · Metadata last reviewed with catalog release.
