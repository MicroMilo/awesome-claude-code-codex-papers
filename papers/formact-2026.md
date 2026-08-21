<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# FormAct

## FormAct: Agentic Source Editing for Rich-Format Document Generation

| Field | Value |
|---|---|
| Authors | Eugene J. Yu, Xingxing Zhang, Yuan Xia, Tao Ge, Xun Wang, FNU Kartik, Vishwas Suryanarayanan, Cheng Yang, Amanda Jiang, Jiayu Ding, Xiangyu Wong, Tengchao Lv, Lei Cui, Si-Qing Chen, Furu Wei, Sujian Li |
| Venue | ICML 2026 (main) |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Not recorded |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | baseline | not-reported | not-reported |

## Task

**Task.** Rich-format document generation and editing

**Benchmark or scale.** RichDocBench and RichDocFuzz

## Method

HTML source editor, template retrieval, rendered-page review agent, iterative refinement, and edit-triggered context compression

**Tags.** `retrieval` `context-reduction` `verifier-loop` `visual-review`

## Reported evidence

Render correctness 4.81 versus 4.39 for multi-pass Codex; human rank-1 rate 0.760 versus 0.140.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Main comparison table and review-refinement ablation |

## Caveat

Codex has slightly higher content alignment, and the task is document formatting rather than source-code repair.

## Primary links

- [Paper](https://openreview.net/forum?id=n7Ta0YEcgw)
- No official artifact was found during the latest review.

---

Catalog ID: `formact-2026` · Metadata last reviewed with catalog release.
