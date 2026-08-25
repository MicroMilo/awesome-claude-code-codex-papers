<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# LLM2Ltac

## Mining Tactics for Automated Theorem Proving

| Field | Value |
|---|---|
| Authors | Jian Fang, Yixun Yao, Yingfei Xiong |
| Conference | ASE |
| Venue | ASE Research Papers 2026 (main) |
| Domains | Formal Methods, Software Engineering |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://zenodo.org/records/19251765) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Sonnet 4.6 | not-reported |

## Task

**Task.** Prove Rocq theorems with Claude Code, optionally augmented by CoqHammer or tactics mined and verified by LLM2Ltac.

**Benchmark or scale.** 200 sampled theorems, 50 each from CompCert, Ext-Lib, Coq-Art, and VFA; tactic mining uses 11,725 standard-library theorems

## Method

LLM2Ltac mines reusable symbolic tactics with GPT-5.2 or DeepSeek-V3.2, compiler-checks and generalization-tests them, retrieves applicable tactics with BM25, and integrates them into CoqHammer for Claude Code.

**Tags.** `retrieval` `verifier-loop` `deterministic-search` `repository-instructions`

## Reported evidence

On the same 200 theorem tasks, Claude Code proves 71 alone, 101 with CoqHammer, and 111 with LLM2Ltac-enhanced CoqHammer. Relative to Claude Code + CoqHammer, LLM2Ltac improves proved theorems by 9.90% and reduces token use from 38,346,691 to 34,317,809 (10.51%).

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | configuration-ablation |
| Source location | Section 5 Evaluation; Section 5.3 RQ3; Table 4 in arXiv v1 |

## Caveat

The evidence copy predates the accepted-title change and still contains placeholder ACM venue text. The Claude Code CLI version, exact model snapshot, temperature, output-token cap, and independent repeat count are not reported; the result is specific to Rocq theorem proving.

## Primary links

- [Paper](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/232/Mining-Tactics-for-Automated-Theorem-Proving)
- [Artifact](https://zenodo.org/records/19251765)
- [Identity-verified evidence copy](https://arxiv.org/abs/2605.08694v1) (submittedVersion; not the acceptance source)

---

Catalog ID: `llm2ltac-2026` · Metadata last reviewed with catalog release.
