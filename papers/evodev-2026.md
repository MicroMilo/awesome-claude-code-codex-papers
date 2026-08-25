<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# EvoDev

## Towards Iterative End-to-End Software Development: A Feature-Driven Multi-Agent Framework

| Field | Value |
|---|---|
| Authors | Junwei Liu, Chen Xu, Chong Wang, Tong Bai, Weitong Chen, Kaseng Wong, Yiling Lou, Xin Peng |
| Conference | ISSTA |
| Venue | ISSTA Research Papers 2026 (main) |
| Domains | Software Engineering, Web & UI |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | claude-sonnet-4-20250514 | not-reported |

## Task

**Task.** Build complete Kotlin Android applications from detailed natural-language requirements and an Android Studio scaffold project.

**Benchmark or scale.** APPDev, 15 applications with 8-26 functional requirements each, blinded four-person manual evaluation, and standardized Android devices

## Method

EvoDev replaces a linear to-do list with global design, a dependency-aware Feature Map, predecessor context propagation, chief-programmer planning, iterative build-and-fix loops, and a compact current-file memory.

**Tags.** `dependency-aware-planning` `structured-state` `memory` `multi-agent` `verifier-loop` `context-reduction`

## Reported evidence

With the same claude-sonnet-4-20250514 model and task time limits, Claude Code reaches 73.3% build success and 2.27/4 function completeness; EvoDev reaches 100% and 3.57/4, a 57.3% relative completeness improvement. Ablations show that predecessor context reverses an iterative-only regression from 2.80 to 3.57.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Sections 4.3.2-4.3.4; Section 5.1 and Table 3; Section 5.3 and Table 6; Section 5.5 and Figure 7 in arXiv v3 |

## Caveat

APPDev contains only 15 Kotlin Android applications and relies on blinded manual scoring. Product CLI version, temperature, output-token cap, exact permissions, and repeated-run variance are not reported; average Claude Code cost is higher than EvoDev but EvoDev takes longer.

## Primary links

- [Paper](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/207/Towards-Iterative-End-to-End-Software-Development-A-Feature-Driven-Multi-Agent-Frame)
- No official artifact was found during the latest review.
- [Identity-verified evidence copy](https://arxiv.org/abs/2511.02399v3) (submittedVersion; not the acceptance source)

---

Catalog ID: `evodev-2026` · Metadata last reviewed with catalog release.
