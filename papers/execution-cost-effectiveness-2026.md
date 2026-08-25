<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Execution-aware repair policies

## To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair

| Field | Value |
|---|---|
| Authors | Zhihao Lin, Junhua Zhu, Mingyi Zhou, Xin Wang, Zhensu Sun, Renyu Yang, David Lo, Li Li |
| Conference | ISSTA |
| Venue | ISSTA Research Papers 2026 (main) |
| Domains | Software Engineering, Systems & Performance |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/mathieu0905/To_Run_Or_Not_To_Run) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Anthropic claude-sonnet-4-5 | v1.0.16 |
| Codex CLI | baseline | OpenAI gpt-5.2 | v0.1.2025062301 |

## Task

**Task.** Repair SWE-bench issues while varying whether and how often the industrial coding agent can run project tests or scripts.

**Benchmark or scale.** First 100 SWE-bench Lite and first 100 SWE-bench Verified instances; 3,000 controlled attempts plus 7,745 public trace analyses

## Method

Five execution policies isolate test execution as a controlled resource, combining paired outcome tests, token/time accounting, hard tool denial, and trajectory-level analysis of localization and validation feedback.

**Tags.** `test-feedback` `performance-feedback` `observability`

## Reported evidence

Prohibiting execution changes commercial-agent resolve rate by only 1.25 points on average and is not significant. For Claude Code it saves 56–62% tokens and 48–54% wall time for only 1–3 points lower resolve rate; for Codex, Quota-1 saves 21–25% tokens. Most failures persist because 81.2% of Claude Code and 100% of Codex fail-to-fail cases pass at least one agent-selected validation but fail official tests.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | no |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | configuration-ablation |
| Source location | Section 3.3 Models and Agents footnote 1; Section 3.5; Tables 2-7; Sections 4.2-4.3; Tables 8-13 in arXiv v1 |

## Caveat

Execution access is intentionally unequal across configurations, and most restrictions are prompt-level; the paper separately verifies zero-execution subsets and a 100-task hard-denial Claude Code run. Results cover Python-heavy SWE-bench subsets and one fixed product/model version per commercial agent.

## Primary links

- [Paper](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/22/To-Run-or-Not-to-Run-Analyzing-the-Cost-Effectiveness-of-Code-Execution-in-LLM-Based)
- [Artifact](https://github.com/mathieu0905/To_Run_Or_Not_To_Run)
- [Identity-verified evidence copy](https://arxiv.org/abs/2606.26978v1) (submittedVersion; not the acceptance source)

---

Catalog ID: `execution-cost-effectiveness-2026` · Metadata last reviewed with catalog release.
