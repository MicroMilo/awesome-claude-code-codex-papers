<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Lean Refactor

## Verifiable PDE Reasoning and Modeling with Neurosymbolics

| Field | Value |
|---|---|
| Authors | Wuyang Chen |
| Conference | IJCAI |
| Venue | IJCAI-ECAI 2026 Early Career Spotlight 2026 (conference) |
| Domains | Formal Methods, Scientific Computing |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |

## Task

**Task.** Refactor Lean 4 proofs to reduce proof length and compilation cost while preserving correctness across library versions.

**Benchmark or scale.** Competition proof benchmarks and research Lean repositories; exact benchmark composition is not reported in the IJCAI spotlight paper.

## Method

A version-filtered strategy bank and multi-objective retrieve-and-rerank pipeline steer a frozen planner-refactorer-debugger agent without retraining.

**Tags.** `retrieval` `verifier-loop` `context-reduction`

## Reported evidence

Lean Refactor reports over 70% token-level compression on competition benchmarks, over 20% on research repositories, and up to 60% compilation-time reduction, while stating that it outperforms Claude Code.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | contextual |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Section 2.3 Formalizing Maintainable PDE Proofs in Lean; PDF page 3 |

## Caveat

The IJCAI Early Career Spotlight paper reports only aggregate Lean Refactor results and the Claude Code comparison claim. It does not identify the Claude Code model or CLI version, task-level results, run count, tool permissions, or a common budget, so comparison fairness cannot be established from the official paper.

## Primary links

- [Paper](https://2026.ijcai.org/accepted-papers/?ijtrack=early-career-spotlight)
- No official artifact was found during the latest review.

---

Catalog ID: `lean-refactor-2026` · Metadata last reviewed with catalog release.
