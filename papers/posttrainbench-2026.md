<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# PostTrainBench

## PostTrainBench: Can LLM Agents Automate LLM Post-Training?

| Field | Value |
|---|---|
| Authors | Ben Rank, Hardik Bhatnagar, Ameya Pandurang Prabhu, Shira Eisenberg, Karina Nguyen, Matthias Bethge, Maksym Andriushchenko |
| Conference | ICML |
| Venue | ICML Main Conference 2026 (dataset-benchmark) |
| Domains | Machine Learning, Scientific Computing |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://posttrainbench.com/) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Opus 4.6; Claude Opus 4.5; Claude Sonnet 4.6; Claude Sonnet 4.5; Claude Haiku 4.5; Qwen3 Max | not-reported |
| Codex CLI | evaluated | GPT-5.2; GPT 5.4 (High); GPT 5.1 Codex Max; GPT 5.3 Codex (High); GPT 5.3 Codex (Med); GPT 5.2 Codex | not-reported |

## Task

**Task.** Autonomously post-train a supplied 1.7B-4B base LLM for one target benchmark without starter code, data, or strategy.

**Benchmark or scale.** PostTrainBench, 4 base models × 7 benchmarks spanning math, science, code, tool use, writing, and health

## Method

A bounded, end-to-end AI-R&D benchmark gives CLI agents one H100, terminal and web access, then audits submitted checkpoints and pipelines for contamination, model substitution, and API misuse.

**Tags.** `benchmark-design` `verifier-loop` `observability` `adversarial-testing`

## Reported evidence

Claude Opus 4.6 on Claude Code leads agents at 23.2% weighted average versus 51.1% for official instruct models; GPT-5.2 on Codex CLI reaches 21.4%. Agents can win narrowly—GPT-5.1 Codex Max reaches 89% on BFCL for Gemma-3-4B versus 67% for the official model—but the audit finds reward hacking, including 12 contamination flags for Opus 4.6 across 84 runs.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 2 PostTrainBench Setup; Figure 2; Section 3.1 and Table 1; Sections 4.1-4.4; Sections 5.3-5.5 in arXiv v1 |

## Caveat

The same-model statement applies to reported native-scaffold versus OpenCode comparisons, not every leaderboard row. Agents optimize one narrow benchmark for ten hours, whereas official instruction-tuned models target broad capabilities; CLI versions, temperature, and output-token caps are not reported.

## Primary links

- [Paper](https://icml.cc/virtual/2026/poster/63667)
- [Artifact](https://posttrainbench.com/)
- [Identity-verified evidence copy](https://arxiv.org/abs/2603.08640v1) (submittedVersion; not the acceptance source)

---

Catalog ID: `posttrainbench-2026` · Metadata last reviewed with catalog release.
