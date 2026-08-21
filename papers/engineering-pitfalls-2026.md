<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Bug taxonomy

## Engineering Pitfalls in AI Coding Tools: An Empirical Study of Bugs in Claude Code, Codex, and Gemini CLI

| Field | Value |
|---|---|
| Authors | Ruixin Zhang, Wuyang Dai, Hung Viet Pham, Gias Uddin, Jinqiu Yang, Song Wang |
| Conference | FSE |
| Venue | FSE Industry Track 2026 (conference) |
| Domains | Software Engineering |
| Evidence class | Evaluation only |
| First published | 2026-03-21 |
| Identifiers | [arXiv:2603.20847](https://arxiv.org/abs/2603.20847) · [DOI:10.1145/3803437.3805213](https://doi.org/10.1145/3803437.3805213) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | not-applicable | multiple |
| Codex CLI | evaluated | not-applicable | multiple |

## Task

**Task.** Empirical analysis of product bug reports

**Benchmark or scale.** More than 3,800 reported bugs

## Method

Evaluation-only manual taxonomy of functionality, integration, invocation, and command-execution failures

**Tags.** `observability`

## Reported evidence

More than 67% of studied bugs concern functionality; API, integration, and configuration account for 36.9% of root causes.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Abstract and root-cause, symptom, and workflow-stage findings |

## Caveat

Failure-taxonomy study; it does not propose an agent that outperforms the products.

## Primary links

- [Paper](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/12/Engineering-Pitfalls-in-AI-Coding-Tools-An-Empirical-Study-of-Bugs-in-Claude-Code-C)
- No official artifact was found during the latest review.

---

Catalog ID: `engineering-pitfalls-2026` · Metadata last reviewed with catalog release.
