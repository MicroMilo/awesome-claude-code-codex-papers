<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# InnoGym

## InnoGym: Benchmarking the Innovation Potential of AI Agents

| Field | Value |
|---|---|
| Authors | Jintian Zhang, Kewei Xu, Jingsheng Zheng, Zhuoyun Yu, Yuqi Zhu, Yujie Luo, Lanning Wei, Shuofei Qiao, Lun Du, Da Zheng, Shumin Deng, Huajun Chen, Ningyu Zhang |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Machine Learning, Scientific Computing |
| Evidence class | Related method |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/zjunlp/igym) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | host | GPT-5 | not-reported |

## Task

**Task.** Evaluate whether ML/scientific agents improve solution performance while producing methodologically novel solutions.

**Benchmark or scale.** InnoGym/iBench, 18 tasks with a 10-task main evaluation subset

## Method

Agent-as-judge extraction and comparison turns complete solution repositories into summaries/pseudocode and scores novelty against known solutions.

**Tags.** `benchmark-design` `structured-state` `performance-feedback` `deterministic-search`

## Reported evidence

Codex with GPT-5 is actually used as the extraction and novelty-evaluation host; the benchmark compares MLAB, CodeAct, and AIDE rather than using Codex as a primary agent baseline.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | component-level |
| Source location | Section 3.2 Novelty Evaluation; Section 4.1; Appendix F.1 |

## Caveat

The paper calls the host product Codex rather than Codex CLI and does not report its product version or exact decoding settings; it is included as a related host use, not a direct product comparison.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/743514dfa1ef705f378424bd1effb57b-Abstract-Conference.html)
- [Artifact](https://github.com/zjunlp/igym)

---

Catalog ID: `innogym-2026` · Metadata last reviewed with catalog release.
