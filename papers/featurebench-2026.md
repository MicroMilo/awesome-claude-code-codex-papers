<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# FeatureBench

## FeatureBench: Benchmarking Agentic Coding for Complex Feature Development

| Field | Value |
|---|---|
| Authors | Qixing Zhou, Jiacheng Zhang, Haiyang Wang, Rui Hao, Jiahe Wang, Minghao Han, Yuxue Yang, Shuzhe Wu, Feiyang Pan, Lue Fan, Dandan Tu, Zhaoxiang Zhang |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Software Engineering |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/LiberCoders/FeatureBench) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Opus 4.5 | not-reported |
| Codex CLI | evaluated | GPT-5.1-Codex | not-reported |

## Task

**Task.** Implement large, cross-file features in existing repositories and pass comprehensive tests.

**Benchmark or scale.** FeatureBench, 210 complex feature tasks across 24 repositories; Lite set has 30 tasks

## Method

Execution-traced feature extraction removes target functionality while preserving interfaces, producing realistic feature-completion tasks with visible tests and anti-cheating controls.

**Tags.** `benchmark-design` `test-feedback` `verifier-loop` `repository-instructions`

## Reported evidence

Claude Code with Claude Opus 4.5 resolves 11.0% of Full tasks and Codex with GPT-5.1-Codex resolves 12.5%; the paper reports passed rates, token I/O, and failure modes.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 4.1.1 Baseline; Table 2; Table 8; Appendix C Table 16 |

## Caveat

The two products use different provider models; Claude Code's routing configuration and exact CLI version are not reported.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/25203d1cc8c58381eab578f4fcf9c4f8-Abstract-Conference.html)
- [Artifact](https://github.com/LiberCoders/FeatureBench)

---

Catalog ID: `featurebench-2026` · Metadata last reviewed with catalog release.
