<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# MLZero

## MLZero: A Multi-Agent System for End-to-end Machine Learning Automation

| Field | Value |
|---|---|
| Authors | Haoyang Fang, Boran Han, Nick Erickson, Xiyuan Zhang, Su Zhou, Anirudh Dagar, Jiani Zhang, Ali Caner Turkmen, Cuixiong Hu, Huzefa Rangwala, Ying Nian Wu, Bernie Wang, George Karypis |
| Venue | NeurIPS 2025 (main) |
| Evidence class | Direct comparison |
| First published | 2025-05-20 |
| Identifiers | [arXiv:2505.13941](https://arxiv.org/abs/2505.13941) |
| Artifact | [Official artifact](https://github.com/autogluon/autogluon-assistant) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | baseline | GPT-4.1 and o4-mini | not-reported |

## Task

**Task.** End-to-end machine learning automation

**Benchmark or scale.** MLE-Bench Lite and Multimodal AutoML Agent Benchmark

## Method

Hierarchical agents with multimodal perception, semantic and episodic memory, and a planning-coding-evaluation loop

**Tags.** `multi-agent` `memory` `verifier-loop` `test-feedback`

## Reported evidence

MLZero led MLE-Bench Lite with six gold medals and achieved 0.92 success on its multimodal benchmark; one appendix setting reports 6.5% errors versus 26.9% for Codex CLI.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | medium |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Abstract, main benchmark results, and appendix error analysis |

## Caveat

Results concern machine-learning automation and should not be generalized to all software-engineering tasks.

## Primary links

- [Paper](https://papers.neurips.cc/paper_files/paper/2025/hash/63ed15a46a143ff57484b38cd6b85d91-Abstract-Conference.html)
- [Artifact](https://github.com/autogluon/autogluon-assistant)

---

Catalog ID: `mlzero-2025` · Metadata last reviewed with catalog release.
