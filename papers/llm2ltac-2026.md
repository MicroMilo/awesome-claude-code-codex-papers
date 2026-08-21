<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# LLM2Ltac

## Mining Tactics for Automated Theorem Proving

| Field | Value |
|---|---|
| Authors | Jian Fang, Yixun Yao, Yingfei Xiong |
| Conference | ASE |
| Venue | ASE 2026 (main) |
| Domains | Formal Methods |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Not recorded |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |

## Task

**Task.** Automated theorem proving in Rocq projects

**Benchmark or scale.** 6,199 theorems across CompCert, Coq-Art, Ext-Lib, and VFA

## Method

LLM-mined reusable symbolic tactics, validity and generalization checks, and integration into CoqHammer

**Tags.** `deterministic-search` `verifier-loop` `static-analysis`

## Reported evidence

Mined tactics let CoqHammer prove 23.87% more theorems; integrating the improved prover with Claude Code increases the overall number proved by 9.90%.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | configuration-ablation |
| Source location | ASE 2026 official abstract |

## Caveat

The public conference record does not report the Claude Code version, backbone model, absolute theorem counts for the product ablation, or budget parity.

## Primary links

- [Paper](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/232/Mining-Tactics-for-Automated-Theorem-Proving)
- No official artifact was found during the latest review.

---

Catalog ID: `llm2ltac-2026` · Metadata last reviewed with catalog release.
