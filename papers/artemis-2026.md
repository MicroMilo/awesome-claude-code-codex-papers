<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# ARTEMIS

## Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing

| Field | Value |
|---|---|
| Authors | Justin W. Lin, Eliot Krzysztof Jones, Donovan Julian Jasper, Ethan Jun-shen Ho, Anna Wu, Arnold Tianyi Yang, Neil Perry, Andy Zou, Matt Fredrikson, J. Zico Kolter, Percy Liang, Dan Boneh, Daniel E. Ho |
| Conference | ICLR |
| Venue | ICLR 2026 (main) |
| Domains | Security |
| Evidence class | Direct comparison |
| First published | 2025-12-10 |
| Identifiers | [arXiv:2512.09882](https://arxiv.org/abs/2512.09882) |
| Artifact | [Official artifact](https://github.com/Stanford-Trinity/ARTEMIS) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude Sonnet 4 | not-reported |
| Codex CLI | baseline | GPT-5 | not-reported |

## Task

**Task.** Long-horizon penetration testing in a live enterprise network

**Benchmark or scale.** Approximately 8,000 hosts across 12 subnets

## Method

Supervisor with dynamic expert agents, recursive task decomposition, parallel exploration, context management, triage, and reporting

**Tags.** `multi-agent` `dynamic-specialization` `parallelism` `memory` `verifier-loop`

## Reported evidence

ARTEMIS found 9 valid vulnerabilities with an 82% valid-submission rate, ranked second overall, and outperformed 9 of 10 human participants.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | no |
| Evidence strength | medium |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Abstract and main penetration-testing results |

## Caveat

Runtime limits, model combinations, safety refusals, and product policies differ across systems.

## Primary links

- [Paper](https://arxiv.org/abs/2512.09882)
- [Artifact](https://github.com/Stanford-Trinity/ARTEMIS)

---

Catalog ID: `artemis-2026` · Metadata last reviewed with catalog release.
