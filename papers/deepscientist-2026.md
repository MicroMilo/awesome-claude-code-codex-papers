<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# DeepScientist

## DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively

| Field | Value |
|---|---|
| Authors | Yixuan Weng, Minjun Zhu, Qiujie Xie, Qiyao Sun, Zhen Lin, Sifan Liu, Yue Zhang |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (conference) |
| Domains | Scientific Computing, Machine Learning |
| Evidence class | Related method |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/ResearAI/DeepScientist) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | host | Claude-4-opus | v1.0.53 |

## Task

**Task.** Long-horizon autonomous scientific discovery with code implementation, experiment validation, and analysis/report generation.

**Benchmark or scale.** Three frontier scientific tasks; five generated research papers and multi-week operational logs

## Method

A three-stage hypothesis, implementation/evaluation, and analysis loop backed by persistent Findings Memory and Bayesian exploration.

**Tags.** `structured-state` `memory` `performance-feedback` `verifier-loop` `parallelism`

## Reported evidence

Claude Code executes all code implementation and analysis tasks as a host component; the system reports 21 validated innovations and 60% simulated acceptance under the stated review protocol.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | component-level |
| Source location | Section F Implementation Details; Section 4.2 Experimental Setup; Figure 4 |

## Caveat

Claude Code is a host executor rather than the paper''s comparison baseline; the scientific reasoning backbone is Gemini-2.5-pro and product-level Claude Code ablations are not reported.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4f64494ecc3442f1c9261baa036378bc-Abstract-Conference.html)
- [Artifact](https://github.com/ResearAI/DeepScientist)

---

Catalog ID: `deepscientist-2026` · Metadata last reviewed with catalog release.
