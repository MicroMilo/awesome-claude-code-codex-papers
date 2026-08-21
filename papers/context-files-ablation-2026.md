<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Context-file ablation

## Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories

| Field | Value |
|---|---|
| Authors | Prakhar Khatri |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Software Engineering |
| Evidence class | Related method |
| First published | 2026-07-28 |
| Identifiers | [arXiv:2607.27250](https://arxiv.org/abs/2607.27250) |
| Artifact | [Official artifact](https://github.com/codeprakhar25/context-files-coding-agents) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Sonnet 4.6 | not-reported |
| Codex CLI | evaluated | GPT-5.5 | not-reported |

## Task

**Task.** Repository repair under different persistent-context strategies

**Benchmark or scale.** 17 real tasks from three Python repositories; 288 evaluated runs

## Method

Within-task comparison of no context, always-on AGENTS.md, and selectively retrieved repository wiki context with gold tests and equivalence testing

**Tags.** `repository-instructions` `retrieval`

## Reported evidence

Claude Code pass rates are 53.3%, 55.6%, and 55.6%; Codex rates are 58.8%, 56.9%, and 52.9%, with no detectable strategy effect and bounded null effects of 10 to 15 points.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | configuration-ablation |
| Source location | Table 1 and Sections 3.4 to 4.4 |

## Caveat

Only three Python repositories are studied; Claude and Codex receive injected context through different channels, and two selective-context corpora are larger than AGENTS.md.

## Primary links

- [Paper](https://arxiv.org/abs/2607.27250)
- [Artifact](https://github.com/codeprakhar25/context-files-coding-agents)

---

Catalog ID: `context-files-ablation-2026` · Metadata last reviewed with catalog release.
