<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SWE-bench Science

## SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science?

| Field | Value |
|---|---|
| Authors | Zhipeng Xu, Jiahao Lu, Yining Zheng, Yuxin Wang, Xipeng Qiu |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering, Scientific Computing |
| Evidence class | Evaluation only |
| First published | 2026-08-20 |
| Identifiers | [arXiv:2608.19799](https://arxiv.org/abs/2608.19799) |
| Artifact | [Official artifact](https://github.com/OpenMOSS/SWE-bench-Science) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Opus 5 and DeepSeek V4 variants | not-reported |
| Codex CLI | evaluated | GPT-5.6, GLM 5.2, Nex N2, and Qwen 3.5 variants | not-reported |

## Task

**Task.** Repository repair in scientific software

**Benchmark or scale.** 119 tasks, 98 repositories, and 20 scientific domains

## Method

Three-paradigm benchmark with private tests, a scientific failure taxonomy, and paired ablations of explicit scientific guidance

**Tags.** `benchmark-design` `observability`

## Reported evidence

The best configuration, Claude Code with Opus 5 at max effort, reaches 47.90% Pass@1; no evaluated agent crosses 50%, and scientific guidance helps some models but hurts others.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Tables 2 to 3 and Figures 5 to 7 |

## Caveat

Results span different models, harnesses, and reasoning settings; the paper is a benchmark and failure analysis, not a method that beats the products.

## Primary links

- [Paper](https://arxiv.org/abs/2608.19799)
- [Artifact](https://github.com/OpenMOSS/SWE-bench-Science)

---

Catalog ID: `swe-bench-science-2026` · Metadata last reviewed with catalog release.
