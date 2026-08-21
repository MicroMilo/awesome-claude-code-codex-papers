<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# AgentRadio

## AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration

| Field | Value |
|---|---|
| Authors | Xinxing Ren, Qianbo Zang, Ziyan Wang, Caelum Forder, Suman Deb, Peter Carroll, Zekun Guo |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Direct comparison |
| First published | 2026-07-30 |
| Identifiers | [arXiv:2607.28430](https://arxiv.org/abs/2607.28430) |
| Artifact | [Official artifact](https://github.com/Coral-Protocol/AgentRadio) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Opus 4.6 | not-reported |

## Task

**Task.** Long-horizon repository question answering

**Benchmark or scale.** SWE-Atlas QnA, 124 tasks and 1,306 rubrics

## Method

Four Claude Code agents coordinated through asynchronous threads, messages, passive mention watching, and a five-phase negotiation protocol

**Tags.** `multi-agent` `coordination` `parallelism`

## Reported evidence

AgentRadio reaches 62.1% task accuracy versus 32.3% for single-agent Claude Code; a near-cost six-run baseline reaches 37.9%, and single-agent Opus 4.8 reaches 57.2%.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | no |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Figure 1 and Tables 1 to 2 |

## Caveat

The four-agent method costs about six times a single Opus 4.6 run, although the paper includes a near-cost resampling baseline.

## Primary links

- [Paper](https://arxiv.org/abs/2607.28430)
- [Artifact](https://github.com/Coral-Protocol/AgentRadio)

---

Catalog ID: `agentradio-2026` · Metadata last reviewed with catalog release.
