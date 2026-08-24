<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# ARTEMIS

## Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing

| Field | Value |
|---|---|
| Authors | Justin W. Lin, Eliot Krzysztof Jones, Donovan Julian Jasper, Ethan Jun-shen Ho, Anna Wu, Arnold Tianyi Yang, Neil Perry, Andy Zou, Matt Fredrikson, J. Zico Kolter, Percy Liang, Dan Boneh, Daniel E. Ho |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (main) |
| Domains | Security |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
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

ARTEMIS finds 9 valid vulnerabilities with an 82% valid-submission rate, ranks second overall, and outperforms 9 of 10 human participants in the reported penetration-testing study.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | no |
| Evidence strength | medium |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Section 4.2 Agent Results; Table 1; Appendix A and J |

## Caveat

This is live-network cybersecurity, not general coding; runtime limits, model mixtures, refusal behavior, and product policies differ.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0410c2ff9f872efe5a7c61a4323a5da3-Abstract-Conference.html)
- [Artifact](https://github.com/Stanford-Trinity/ARTEMIS)

---

Catalog ID: `artemis-2026` · Metadata last reviewed with catalog release.
