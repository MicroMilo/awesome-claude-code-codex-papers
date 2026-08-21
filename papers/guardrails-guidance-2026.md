<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Guardrails Beat Guidance

## Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and Persistent Configuration for Coding Agents

| Field | Value |
|---|---|
| Authors | Xing Zhang, Guanghui Wang, Yanwei Cui, Wei Qiu, Ziyuan Li, Bing Zhu, Peiyang He |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Direct comparison |
| First published | 2026-04-13 |
| Identifiers | [arXiv:2604.11088](https://arxiv.org/abs/2604.11088) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Opus 4.6 | not-reported |

## Task

**Task.** Repository repair under persistent rule-file configurations

**Benchmark or scale.** SWE-bench Verified; more than 5,000 Claude Code runs

## Method

Paired rule-file experiments over source, count, polarity, type, and composition, backed by a corpus of 25,532 rules

**Tags.** `repository-instructions`

## Reported evidence

Random and expert-curated rule files both reach 63.8% pass rate versus 50.0% with no rules; only negative constraints are individually beneficial in the reported ablation.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | configuration-ablation |
| Source location | Figure 1 and Tables 1 to 5 |

## Caveat

Results are limited to Claude Code with Opus 4.6 on a discriminative Python subset; several headline pairwise differences do not reach conventional significance.

## Primary links

- [Paper](https://arxiv.org/abs/2604.11088)
- No official artifact was found during the latest review.

---

Catalog ID: `guardrails-guidance-2026` · Metadata last reviewed with catalog release.
