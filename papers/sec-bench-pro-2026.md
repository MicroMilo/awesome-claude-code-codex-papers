<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SEC-bench Pro

## SEC-bench Pro: Can Language Models Solve Long-Horizon Software Security Tasks?

| Field | Value |
|---|---|
| Authors | Hwiwon Lee, Jiawei Liu, Dongjun Kim, Wubing Xia, Ziqi Zhang, Chunqiu Steven Xia, Lingming Zhang |
| Conference | arXiv |
| Venue | arXiv 2026 (preprint) |
| Domains | Security |
| Evidence class | Evaluation only |
| First published | 2026-05-26 |
| Identifiers | [arXiv:2605.26548](https://arxiv.org/abs/2605.26548) |
| Artifact | [Official artifact](https://github.com/SEC-bench/SEC-bench-Pro) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Opus 4.6 | not-reported |
| Codex CLI | evaluated | GPT-5.4 and GPT-5.5 | not-reported |

## Task

**Task.** Long-horizon proof-of-concept synthesis for disclosed vulnerabilities

**Benchmark or scale.** 344 validated V8, SpiderMonkey, and Linux kernel vulnerabilities

## Method

Self-evolving reconstruction pipeline, three-image execution oracle, and LLM judge for vulnerability-specific PoC attribution

**Tags.** `benchmark-design` `verifier-loop`

## Reported evidence

Codex with GPT-5.5 solves 58% of all instances; Claude Code with Opus 4.6 times out often but solves most completed attempts, while GLM-5 solves 13 of 344.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Abstract and main agent-results tables |

## Caveat

The configurations use different models and completion behavior; this is comparative capability measurement rather than a proposed system beating a product baseline.

## Primary links

- [Paper](https://arxiv.org/abs/2605.26548)
- [Artifact](https://github.com/SEC-bench/SEC-bench-Pro)

---

Catalog ID: `sec-bench-pro-2026` · Metadata last reviewed with catalog release.
