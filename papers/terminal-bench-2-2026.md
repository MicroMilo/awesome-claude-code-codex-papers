<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Terminal-Bench 2.0

## Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces

| Field | Value |
|---|---|
| Authors | Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, Boxuan Li, Harsh Raj, Ivan Bercovich, Lin Shi, Jeong Yeon Shin, Thomas Walshe, E. Kelly Buchanan, Junhong Shen, Guanghao Ye, Haowei Lin, Jason Poulos, Maoyu Wang, Marianna Nezhurina, Jenia Jitsev, Di Lu, Orfeas Menis Mastromichalakis, Zhiwei Xu, Zizhao Chen, Yue Liu, Robert Zhang, Leon Liangyu Chen, Anurag Kashyap, Jan-Lucas Uslu, Jeffrey Li, Jianbo Wu, Minghao Yan, Song Bian, Vedang Sharma, Ke Sun, Steven Dillmann, Akshay Anand, Andrew Lanpouthakoun, Bardia Koopah, Changran Hu, Etash Guha, Gabriel H. S. Dreiman, Jiacheng Zhu, Karl Krauth, Li Zhong, Niklas Muennighoff, Robert Amanfu, Shangyin Tan, Shreyas Pimpalgaonkar, Tushar Aggarwal, Xiangning Lin, Xin Lan, Xuandong Zhao, Yiqing Liang, Yuanli Wang, Zilong Wang, Changzhi Zhou, David Heineman, Hange Liu, Harsh Trivedi, John Yang, Junhong Lin, Manish Shetty, Michael Yang, Nabil Omi, Negin Raoof, Shanda Li, Terry Yue Zhuo, Wuwei Lin, Yiwei Dai, Yuxin Wang, Wenhao Chai, Shang Zhou, Dariush Wahdany, Ziyu She, Jiaming Hu, Zhikang Dong, Yuxuan Zhu, Sasha Cui, Ahson Saiyed, Arinbjörn Kolbeinsson, Jesse Hu, Christopher Michael Rytting, Ryan Marten, Yixin Wang, Alex Dimakis, Andy Konwinski, Ludwig Schmidt |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (dataset-benchmark) |
| Domains | Software Engineering, Systems & Performance |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/harbor-framework/terminal-bench-2) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Opus 4.5; Claude Sonnet 4.5; Claude Opus 4.1; Claude Haiku 4.5 | not-reported |
| Codex CLI | evaluated | GPT-5.2; GPT-5; GPT-5-Mini; GPT-5-Nano | not-reported |

## Task

**Task.** Evaluate industrial and open-source agents on realistic command-line tasks with executable tests.

**Benchmark or scale.** Terminal-Bench 2.0: 89 hard tasks, Harbor harness, containerized environments

## Method

A benchmark design with realistic terminal environments, human-written solutions, executable tests, standardized Harbor tasks, and failure-mode analysis.

**Tags.** `benchmark-design` `verifier-loop` `observability` `adversarial-testing`

## Reported evidence

Codex CLI with GPT-5.2 reaches 62.9% resolution; Claude Code with Claude Opus 4.5 reaches 52.1%, with lower Claude Code rows for Sonnet 4.5, Opus 4.1, and Haiku 4.5 reported in Table 2.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | no |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 3.2 Agents; Section 3.3 Models; Table 2; Appendix B |

## Caveat

This paper evaluates products and models rather than proposing a method that beats them; token and cost budgets vary substantially across agent-model combinations.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html)
- [Artifact](https://github.com/harbor-framework/terminal-bench-2)

---

Catalog ID: `terminal-bench-2-2026` · Metadata last reviewed with catalog release.
