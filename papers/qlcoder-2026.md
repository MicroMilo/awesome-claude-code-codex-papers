<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# QLCoder

## QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities

| Field | Value |
|---|---|
| Authors | Claire Wang, Ziyang Li, Saikat Dutta, Mayur Naik |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (main) |
| Domains | Security |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/neuralprogram/qlcoder) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Sonnet 4 | not-reported |
| Codex CLI | baseline | GPT-5 | not-reported |

## Task

**Task.** CodeQL query synthesis from CVE metadata

**Benchmark or scale.** 176 CVEs across 111 Java projects

## Method

CVE-grounded retrieval, AST/LSP guidance, an MCP interface, and an executable CodeQL validator that feeds back into iterative query repair.

**Tags.** `retrieval` `verifier-loop` `static-analysis`

## Reported evidence

QLCoder synthesizes correct queries for 53.4% of CVEs versus 10% for Claude Code-only; its query F1 is 0.70, versus 0.048 for IRIS and 0.073 for CodeQL suites.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Section 4.1 Experimental Setup; Table 2; Table 5; Appendix A |

## Caveat

The task is CodeQL security-query synthesis, not general repository-level software engineering; GPT-5 reasoning settings differ across Codex baseline rows.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html)
- [Artifact](https://github.com/neuralprogram/qlcoder)

---

Catalog ID: `qlcoder-2026` · Metadata last reviewed with catalog release.
