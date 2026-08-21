<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# ToolLeak

## Red-Teaming Coding Agents from a Tool-Invocation Perspective: An Empirical Security Assessment

| Field | Value |
|---|---|
| Authors | Yuchong Xie, Mingyu Luo, Zesen Liu, Zhixiang Zhang, Kaikai Zhang, Yu Liu, Ci Tao, Changhui Wang, Zongjie Li, Ping Chen, Shuai Wang, Dongdong She |
| Conference | ISSTA |
| Venue | ISSTA 2026 (main) |
| Domains | Security |
| Evidence class | Evaluation only |
| First published | 2025-09-06 |
| Identifiers | [arXiv:2509.05755](https://arxiv.org/abs/2509.05755) |
| Artifact | Not found during the latest review |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | multiple | multiple |

## Task

**Task.** Prompt exfiltration and tool-invocation hijacking in production coding agents

**Benchmark or scale.** Six real-world coding agents and 25 agent-model configurations

## Method

Tool-call schema pressure for prompt leakage followed by a two-channel injection through tool descriptions and returns

**Tags.** `adversarial-testing` `observability`

## Reported evidence

ToolLeak obtains the best pseudo-recall on 18 of 25 real agent-model pairs; the follow-on attack hijacks all six studied agents, including a Claude Code RCE case study.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | ISSTA 2026 official abstract; Tables 3 to 5 and Sections 6 to 7 |

## Caveat

Claude Code is an attack target rather than a baseline to beat; results depend on product and backend versions that may change quickly.

## Primary links

- [Paper](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/176/Red-Teaming-Coding-Agents-from-a-Tool-Invocation-Perspective-An-Empirical-Security-A)
- No official artifact was found during the latest review.

---

Catalog ID: `toolleak-2026` · Metadata last reviewed with catalog release.
