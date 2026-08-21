<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# BountyBench

## BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems

| Field | Value |
|---|---|
| Authors | Andy K. Zhang, Joey Ji, Celeste Menders, Riya Dulepet, Thomas Qin, Ron Y. Wang, Junrong Wu, Kyleen Liao, Jiliang Li, Jinghan Hu, Sara Hong, Nardos Demilew, Shivatmica Murgai, Jason Tran, Nishka Kacheria, Ethan Ho, Denis Liu, Lauren McLane, Olivia Bruvik, Dai-Rong Han, Seungwoo Kim, Akhil Vyas, Cuiyuanxiu Chen, Ryan Li, Weiran Xu, Jonathan Z. Ye, Prerit Choudhary, Siddharth M. Bhatia, Vikram Sivashankar, Yuxuan Bao, Dawn Song, Dan Boneh, Daniel E. Ho, Percy Liang |
| Conference | NeurIPS |
| Venue | NeurIPS 2025 (dataset-benchmark) |
| Domains | Security |
| Evidence class | Evaluation only |
| First published | 2025-05-21 |
| Identifiers | [arXiv:2505.15216](https://arxiv.org/abs/2505.15216) |
| Artifact | [Official artifact](https://github.com/bountybench/bountybench) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | not-reported | not-reported |
| Codex CLI | evaluated | o3-high and o4-mini | not-reported |

## Task

**Task.** Vulnerability detection, exploitation, and patching

**Benchmark or scale.** BountyBench

## Method

Evaluation-only benchmark of offensive and defensive cybersecurity agents

**Tags.** `verifier-loop`

## Reported evidence

Codex o3-high detects 12.5% and patches 90%; Claude Code patches 87.5% and exploits 57.5% in the reported settings.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | benchmark-only |
| Source location | Official abstract and agent task-results tables |

## Caveat

Benchmark-only evidence across different tasks and model configurations.

## Primary links

- [Paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/faed4276b52ef762879db4142655c699-Abstract-Datasets_and_Benchmarks_Track.html)
- [Artifact](https://github.com/bountybench/bountybench)

---

Catalog ID: `bountybench-2025` · Metadata last reviewed with catalog release.
