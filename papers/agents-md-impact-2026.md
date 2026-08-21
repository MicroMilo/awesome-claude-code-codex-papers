<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# AGENTS.md

## On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents

| Field | Value |
|---|---|
| Authors | Jai Lal Lulla, Seyedmoein Mohsenimofidi, Matthias Galster, Jie M. Zhang, Sebastian Baltes, Christoph Treude |
| Venue | ICSE JAWs 2026 (workshop) |
| Evidence class | Direct comparison |
| First published | 2026-01-28 |
| Identifiers | [arXiv:2601.20404](https://arxiv.org/abs/2601.20404) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | not-reported | not-reported |
| Codex CLI | baseline | not-reported | not-reported |

## Task

**Task.** Real pull-request tasks with and without repository instructions

**Benchmark or scale.** 10 repositories and 124 pull requests

## Method

Persistent repository-level build, test, style, and directory guidance in AGENTS.md

**Tags.** `repository-instructions` `structured-state` `context-reduction`

## Reported evidence

Median runtime falls 28.64% and output tokens fall 16.58% with comparable completion behavior.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | efficiency |
| Comparison scope | configuration-ablation |
| Source location | Abstract and with-versus-without AGENTS.md results |

## Caveat

Workshop study and configuration intervention rather than a standalone agent.

## Primary links

- [Paper](https://conf.researchr.org/details/icse-2026/jaws-2026-papers/31/On-the-Impact-of-AGENTS-md-Files-on-the-Efficiency-of-AI-Coding-Agents)
- No official artifact was found during the latest review.

---

Catalog ID: `agents-md-impact-2026` · Metadata last reviewed with catalog release.
