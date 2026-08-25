<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# SWE-Compass

## SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities for Large Language Models

| Field | Value |
|---|---|
| Authors | Jingxuan Xu, Ken Deng, Weihao Li, Songwei Yu, Haoyang Huang, Xinping Lei, Yifan Yao, Huaixi Tang, Zhiyi Lai, Kepeng Lei, Zizheng Zhan, Yanan Wu, Chenchen Zhang, Wenqiang Zhu, Wen Xiang, Zongxian Feng, Han Li, Junqi Xiong, Dailin Li, Zuchen Gao, Kun Wu, Yuanxing Zhang, Wuxuan Gong, Ziyuan Gao, Guanxiang Wang, Yirong Xue, Mengfei Xie, Xiaojiang Zhang, Jinghui Wang, Wenhao Zhuang, Zheng Lin, Huiming Wang, Zhaoxiang Zhang, Yuqun Zhang, Haotian Zhang, Ming Sun, Chen Bin, Jiaheng Liu |
| Conference | ICML |
| Venue | ICML Main Conference 2026 (dataset-benchmark) |
| Domains | Software Engineering |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://huggingface.co/datasets/Kwaipilot/SWE-Compass) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude-Sonnet-4-20250514; Qwen3-Coder-480B-A35B-Instruct; Qwen3-Coder-30B-A3B-Instruct; Qwen3-235B-A22B-Instruct-2507; DeepSeek-V3-0324 | not-reported |

## Task

**Task.** Solve real pull-request tasks across feature work, repair, refactoring, performance, tests, understanding, and deployment in ten languages.

**Benchmark or scale.** SWE-Compass, 2,000 verified GitHub PR instances across 8 task types, 8 scenarios, and 10 programming languages

## Method

A broad execution-grounded benchmark pairs real PR tasks with reproducible containers and controlled agent budgets, then analyzes task, language, scenario, interaction, and failure-mode differences.

**Tags.** `benchmark-design` `test-feedback` `observability`

## Reported evidence

Claude-Sonnet-4-20250514 reaches 32.9% macro-average with Claude Code versus 31.8% with SWE-Agent. Across five shared models only two score higher with Claude Code; Claude Code favors deterministic deployment, understanding, and test-generation tasks, while failures are dominated by requirement misinterpretation and incomplete solutions rather than basic technical knowledge.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 4.1 Evaluated LLMs and Frameworks; Table 2; Sections 4.2.1-4.2.2; Figure 7; Appendix A.2 and A.4 in arXiv v3 |

## Caveat

The arXiv v3 author list differs from the official ICML poster and is retained only as a versioned evidence copy. Only five of ten models are run under Claude Code; the CLI version, temperature, output-token cap, and global job timeout are not reported.

## Primary links

- [Paper](https://icml.cc/virtual/2026/poster/64552)
- [Artifact](https://huggingface.co/datasets/Kwaipilot/SWE-Compass)
- [Identity-verified evidence copy](https://arxiv.org/abs/2511.05459v3) (submittedVersion; not the acceptance source)

---

Catalog ID: `swe-compass-2026` · Metadata last reviewed with catalog release.
