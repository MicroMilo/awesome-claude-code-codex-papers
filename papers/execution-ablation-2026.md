<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Execution-policy ablation

## To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair

| Field | Value |
|---|---|
| Authors | Zhihao Lin, Junhua Zhu, Mingyi Zhou, Xin Wang, Zhensu Sun, Renyu Yang, David Lo, Li Li |
| Conference | ISSTA |
| Venue | ISSTA 2026 (main) |
| Domains | Software Engineering, Systems & Performance |
| Evidence class | Related method |
| First published | 2026-06-25 |
| Identifiers | [arXiv:2606.26978](https://arxiv.org/abs/2606.26978) |
| Artifact | [Official artifact](https://github.com/mathieu0905/To_Run_Or_Not_To_Run) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Sonnet 4.5 | 1.0.16 |
| Codex CLI | evaluated | GPT-5.2 xhigh | 0.1.2025062301 |

## Task

**Task.** Repository-level program repair with and without local code execution

**Benchmark or scale.** 200 SWE-bench Lite and Verified instances; 3,000 controlled runs

## Method

Paired five-arm execution-policy ablation spanning prohibited, quota-limited, budget-guided, and unrestricted execution

**Tags.** `test-feedback` `verifier-loop` `context-reduction`

## Reported evidence

Disabling execution changes resolve rate by only 1 to 3 points for Claude Code and Codex in the main cells, while saving 56 to 62% of tokens and 48 to 54% of wall-clock time for Claude Code.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | configuration-ablation |
| Source location | ISSTA 2026 paper, Tables 2 to 4 and Sections 4.2 to 4.3 |

## Caveat

The prompt-level prohibition was not perfectly obeyed by Claude Code, though the paper separately measures and hard-checks unintended execution.

## Primary links

- [Paper](https://arxiv.org/abs/2606.26978)
- [Artifact](https://github.com/mathieu0905/To_Run_Or_Not_To_Run)

---

Catalog ID: `execution-ablation-2026` · Metadata last reviewed with catalog release.
