<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# QLCoder

## QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities

| Field | Value |
|---|---|
| Authors | Claire Wang, Ziyang Li, Saikat Dutta, Mayur Naik |
| Venue | ICLR 2026 (main) |
| Evidence class | Direct comparison |
| First published | 2025-11-11 |
| Identifiers | [arXiv:2511.08462](https://arxiv.org/abs/2511.08462) |
| Artifact | [Official artifact](https://github.com/neuralprogram/qlcoder) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Sonnet 4 | 1.0.120 |

## Task

**Task.** CodeQL query synthesis from CVE metadata

**Benchmark or scale.** 176 CVEs across 111 Java projects

## Method

CVE-grounded retrieval, AST guidance, CodeQL LSP tools, and iterative execution feedback

**Tags.** `retrieval` `verifier-loop` `static-analysis`

## Reported evidence

Correct-query rate 53.4% versus 10% for Claude Code-only; F1 0.70 versus 0.048 for IRIS and 0.073 for CodeQL suites.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Official abstract, main evaluation, and artifact paper environment |

## Caveat

Security-query synthesis is narrower than general software engineering.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html)
- [Artifact](https://github.com/neuralprogram/qlcoder)

---

Catalog ID: `qlcoder-2026` · Metadata last reviewed with catalog release.
