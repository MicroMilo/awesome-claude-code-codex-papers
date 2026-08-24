<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# AppForge

## From Assistant to Independent Developer — Are GPTs Ready for Software Development?

| Field | Value |
|---|---|
| Authors | Dezhi Ran, Yuan Cao, Mengzhou Wu, Simin Chen, Yuzhe Guo, Jun Ren, Zihe Song, Hao Yu, Jialei Wei, Linyi Li, Wei Yang, Baishakhi Ray, Tao Xie |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Software Engineering, Web & UI |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/TongmingLAIC/AppForge) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Qwen3-Coder | not-reported |

## Task

**Task.** Build complete Android applications from natural-language specifications and pass functional/runtime tests.

**Benchmark or scale.** AppForge, 101 software-development problems from real-world Android apps

## Method

Formal task specifications, expert-verified UI interaction traces, automated compilation/testing, and runtime fuzz testing create a full-app benchmark.

**Tags.** `benchmark-design` `visual-review` `test-feedback` `verifier-loop`

## Reported evidence

Claude Code with Qwen3-Coder reaches 6.93% functional success; the paper reports that coding-agent gains are marginal and that multi-file integration and lifecycle behavior remain bottlenecks.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 4.3 Table 2; Appendix C.1 Setup; Appendix C.2 detailed statistics |

## Caveat

The paper reports Claude Code as CC with Qwen3-Coder; it does not report a product version or a separate CLI iteration budget.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a421e88bb7db67cd0401475a0ed4a17d-Abstract-Conference.html)
- [Artifact](https://github.com/TongmingLAIC/AppForge)

---

Catalog ID: `appforge-2026` · Metadata last reviewed with catalog release.
