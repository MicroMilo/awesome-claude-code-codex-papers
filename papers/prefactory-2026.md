<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Prefactory

## Prefactory: Automated Discovery and Application of Library-Adoption Refactorings

| Field | Value |
|---|---|
| Authors | Islem Bouzenia, Michael Pradel |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Direct comparison |
| First published | 2026-07-19 |
| Identifiers | [arXiv:2607.17211](https://arxiv.org/abs/2607.17211) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | baseline | not-reported | not-reported |

## Task

**Task.** Discovery and application of library-adoption refactorings

**Benchmark or scale.** PrefactoryBench

## Method

LLM-synthesized lexical and structural search heuristics, deterministic candidate ranking, targeted refactoring, and differential tests

**Tags.** `deterministic-search` `static-analysis` `test-feedback` `verifier-loop`

## Reported evidence

File-level detection 75 versus Codex 35; function-level detection 56 versus 32; 40 of 56 candidates yield test-validated refactorings.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Abstract and PrefactoryBench detection and validation results |

## Caveat

The strongest comparison concerns candidate detection, not universal end-to-end task success.

## Primary links

- [Paper](https://arxiv.org/abs/2607.17211)
- No official artifact was found during the latest review.

---

Catalog ID: `prefactory-2026` · Metadata last reviewed with catalog release.
