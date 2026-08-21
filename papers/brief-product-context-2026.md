<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Brief

## Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%

| Field | Value |
|---|---|
| Authors | Drew Dillon, Kasyap Varanasi |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Direct comparison |
| First published | 2026-04-27 |
| Identifiers | [arXiv:2605.08112](https://arxiv.org/abs/2605.08112) |
| Artifact | [Official artifact](https://github.com/brief-hq/dcbench) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Sonnet 4.6 | not-reported |

## Task

**Task.** Product-decision-compliant feature implementation

**Benchmark or scale.** DCBench, eight tasks with 41 weighted decision points and 48 runs

## Method

Retrieval over recorded product decisions, personas, customer signals, and competitive context during specification and implementation

**Tags.** `retrieval` `structured-state` `test-feedback`

## Reported evidence

Decision compliance rises from 19/41 (46%) for Claude Code to 39/41 (95%) with Brief; cost per merge-ready task falls 68% despite 28% higher total spend.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | no |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Tables 2 to 5 |

## Caveat

The augmented arm adds Opus planning, a longer timeout, generated specifications, tests, and retrieval, so the 49-point gain is not attributable to product context alone.

## Primary links

- [Paper](https://arxiv.org/abs/2605.08112)
- [Artifact](https://github.com/brief-hq/dcbench)

---

Catalog ID: `brief-product-context-2026` · Metadata last reviewed with catalog release.
