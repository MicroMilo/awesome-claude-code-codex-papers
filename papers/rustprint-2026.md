<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# RustPrint

## RustPrint: Documentation-Guided Agentic Codebase Migration from C to Rust

| Field | Value |
|---|---|
| Authors | Minh Le-Anh, Anh Nguyen Hoang, Bach Le, Nghi D. Q. Bui |
| Venue | arXiv 2026 (preprint) |
| Evidence class | Direct comparison |
| First published | 2026-05-14 |
| Identifiers | [arXiv:2605.14634](https://arxiv.org/abs/2605.14634) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |

## Task

**Task.** Whole-codebase migration from C to Rust

**Benchmark or scale.** Eight real C repositories from 11K to 84K lines of code

## Method

Architecture documentation blueprint, module and data-flow planning, compile feedback, documentation mismatch repair, and source-test translation

**Tags.** `structured-state` `dependency-aware-planning` `verifier-loop` `test-feedback`

## Reported evidence

In the reported Kimi-K2-Instruct setting, feature preservation is 93.26% versus 52.52% for agentic Claude Code; cross-evaluation test pass is 95.17% versus 79.85%.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Abstract and feature-preservation and cross-evaluation results |

## Caveat

The comparison mixes model and scaffold choices and is specific to C-to-Rust migration.

## Primary links

- [Paper](https://arxiv.org/abs/2605.14634)
- No official artifact was found during the latest review.

---

Catalog ID: `rustprint-2026` · Metadata last reviewed with catalog release.
