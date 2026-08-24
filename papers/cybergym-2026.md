<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# CyberGym

## CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale

| Field | Value |
|---|---|
| Authors | Zhun Wang, Tianneng Shi, Jingxuan He, Matthew Cai, Jialin Zhang, Dawn Song |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Security, Software Engineering |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/sunblaze-ucb/cybergym) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Codex CLI | evaluated | GPT-4.1 | not-reported |

## Task

**Task.** Generate proof-of-concept tests that reproduce real vulnerabilities in source repositories.

**Benchmark or scale.** CyberGym, 1,507 vulnerabilities across 188 software projects

## Method

A scalable vulnerability-reproduction benchmark with difficulty levels, pre/post-patch execution validation, and zero-day discovery analysis.

**Tags.** `benchmark-design` `verifier-loop` `adversarial-testing` `observability`

## Reported evidence

Codex CLI with GPT-4.1 is directly compared with OpenHands, EnIGMA, and Cybench agent; the union of four agents reaches 18.4% Level-1 success, exposing complementary failure modes.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 4 experimental evaluation; Figure 5; Appendix C Detailed Agent Settings |

## Caveat

The Codex comparison uses a calibrated approximate cost budget and 100-iteration cap; the paper does not report a Codex CLI version or exact per-call token settings.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c876a2935a90aff21874e14c07dc3e33-Abstract-Conference.html)
- [Artifact](https://github.com/sunblaze-ucb/cybergym)

---

Catalog ID: `cybergym-2026` · Metadata last reviewed with catalog release.
