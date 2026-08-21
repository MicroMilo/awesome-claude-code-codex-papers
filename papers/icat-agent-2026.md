<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# icat-agent

## Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution

| Field | Value |
|---|---|
| Authors | Yang Chen, Aliya Ahmad, Yiheng Zhou, Reyhaneh Jabbarvand |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Direct comparison |
| First published | 2026-06-24 |
| Identifiers | [arXiv:2606.25514](https://arxiv.org/abs/2606.25514) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |

## Task

**Task.** Repository issue resolution

**Benchmark or scale.** SWE-bench Verified and SWE-bench Pro

## Method

Event-based agent communication, issue-quality routing, parallel patching and validation, and exploratory fallback

**Tags.** `multi-agent` `dynamic-specialization` `parallelism` `test-feedback`

## Reported evidence

SWE-bench Verified improves 3.6 to 8.4 percentage points and SWE-bench Pro 6.3 to 18.5 points; average cost is $1.18 lower than multi-agent Claude Code.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Abstract and SWE-bench Verified and Pro comparisons |

## Caveat

Exact model parity varies by reported configuration; preprint.

## Primary links

- [Paper](https://arxiv.org/abs/2606.25514)
- No official artifact was found during the latest review.

---

Catalog ID: `icat-agent-2026` · Metadata last reviewed with catalog release.
