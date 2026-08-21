<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# EvoDev

## Towards Iterative End-to-End Software Development: A Feature-Driven Multi-Agent Framework

| Field | Value |
|---|---|
| Authors | Junwei Liu, Chen Xu, Chong Wang, Tong Bai, Weitong Chen, Kaseng Wong, Yiling Lou, Xin Peng |
| Conference | ISSTA |
| Venue | ISSTA 2026 (main) |
| Domains | Software Engineering, Web & UI |
| Evidence class | Direct comparison |
| First published | 2025-11-04 |
| Identifiers | [arXiv:2511.02399](https://arxiv.org/abs/2511.02399) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude 4 Sonnet | not-reported |

## Task

**Task.** Iterative end-to-end Android application development

**Benchmark or scale.** APPDev, 15 Android applications with 8 to 26 functional requirements

## Method

Feature-driven multi-agent development with a dependency DAG, layered business/design/code context, iterative implementation, and build repair

**Tags.** `structured-state` `dependency-aware-planning` `multi-agent` `memory` `test-feedback`

## Reported evidence

With Claude 4 Sonnet, EvoDev reaches 100% build success and 3.57 function completeness versus 73.3% and 2.27 for Claude Code, a 57.3% relative completeness gain.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | no |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | ISSTA 2026 official abstract; Tables 3 and 7 |

## Caveat

APPDev contains 15 Android apps and uses manual quality scoring; EvoDev takes about twice Claude Code's wall-clock time in the Claude 4 Sonnet comparison.

## Primary links

- [Paper](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/207/Towards-Iterative-End-to-End-Software-Development-A-Feature-Driven-Multi-Agent-Frame)
- No official artifact was found during the latest review.

---

Catalog ID: `evodev-2026` · Metadata last reviewed with catalog release.
