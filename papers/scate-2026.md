<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SCATE

## SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation

| Field | Value |
|---|---|
| Authors | Sijia Gu, Noor Nashid, Ali Mesbah |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Related method |
| First published | 2026-07-09 |
| Identifiers | [arXiv:2607.08983](https://arxiv.org/abs/2607.08983) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | not-reported | not-reported |

## Task

**Task.** Automated test generation

**Benchmark or scale.** Repository-level test-generation benchmark

## Method

Contextual-bandit supervisor that selects testing actions from current coverage and testability state

**Tags.** `test-feedback` `verifier-loop`

## Reported evidence

Line coverage improves 32.3% and branch coverage 30.9% over agent-only Gemini CLI; adaptation is also evaluated with Claude Code.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | contextual |
| Claim type | quality |
| Comparison scope | component-level |
| Source location | Abstract and cross-agent adaptation experiment |

## Caveat

The abstract does not provide an equally complete numeric head-to-head against Claude Code.

## Primary links

- [Paper](https://arxiv.org/abs/2607.08983)
- No official artifact was found during the latest review.

---

Catalog ID: `scate-2026` · Metadata last reviewed with catalog release.
