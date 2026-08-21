<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# CodeGrep

## CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents

| Field | Value |
|---|---|
| Authors | Wuya Chen, Yihao Yang, Yang Cao, Yue Lin |
| Venue | arXiv 2026 (preprint) |
| Evidence class | Related method |
| First published | 2026-08-06 |
| Identifiers | [arXiv:2608.05886](https://arxiv.org/abs/2608.05886) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | not-reported | Claude-Code-like agent |

## Task

**Task.** Repository retrieval for issue resolution

**Benchmark or scale.** SWE-bench Verified

## Method

GRPO-trained 14B retrieval agent that issues multi-turn parallel grep, glob, and read operations for a frozen downstream coding agent

**Tags.** `retrieval` `context-reduction` `parallelism`

## Reported evidence

Resolve rate 27.0% versus 25.8% without retrieval; resolved tasks use 15% fewer rounds and 19% fewer tokens.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | contextual |
| Claim type | mixed |
| Comparison scope | component-level |
| Source location | Abstract and frozen-agent retrieval comparison |

## Caveat

The clean numeric comparison is against a frozen no-retrieval downstream agent, not necessarily the released Claude Code CLI.

## Primary links

- [Paper](https://arxiv.org/abs/2608.05886)
- No official artifact was found during the latest review.

---

Catalog ID: `codegrep-2026` · Metadata last reviewed with catalog release.
