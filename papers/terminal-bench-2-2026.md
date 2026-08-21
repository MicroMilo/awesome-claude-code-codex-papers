<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# Terminal-Bench 2.0

## Terminal-Bench 2.0: Advancing Agentic Terminal Intelligence through Better Evaluation and Verification

| Field | Value |
|---|---|
| Authors | Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, Boxuan Li, Harsh Raj, Ivan Bercovich, Lin Shi, Jeong Yeon Shin, Thomas Walshe, E. Kelly Buchanan, Junhong Shen, Guanghao Ye, Haowei Lin, Jason Poulos, Maoyu Wang, Marianna Nezhurina, Jenia Jitsev, Di Lu, Orfeas Menis Mastromichalakis, Zhiwei Xu, Zizhao Chen, Yue Liu, Robert Zhang, Leon Liangyu Chen, Anurag Kashyap, Jan-Lucas Uslu, Jeffrey Li, Jianbo Wu, Minghao Yan, Song Bian, Vedang Sharma, Ke Sun, Steven Dillmann, Akshay Anand, Andrew Lanpouthakoun, Bardia Koopah, Changran Hu, Etash Guha, Gabriel H. S. Dreiman, Jiacheng Zhu, Karl Krauth, Li Zhong, Niklas Muennighoff, Robert Amanfu, Shangyin Tan, Shreyas Pimpalgaonkar, Tushar Aggarwal, Xiangning Lin, Xin Lan, Xuandong Zhao, Yiqing Liang, Yuanli Wang, Zilong Wang, Changzhi Zhou, David Heineman, Hange Liu, Harsh Trivedi, John Yang, Junhong Lin, Manish Shetty, Michael Yang, Nabil Omi, Negin Raoof, Shanda Li, Terry Yue Zhuo, Wuwei Lin, Yiwei Dai, Yuxin Wang, Wenhao Chai, Shang Zhou, Dariush Wahdany, Ziyu She, Jiaming Hu, Zhikang Dong, Yuxuan Zhu, Sasha Cui, Ahson Saiyed, Arinbjörn Kolbeinsson, Jesse Hu, Christopher Michael Rytting, Ryan Marten, Yixin Wang, Alex Dimakis, Andy Konwinski, Ludwig Schmidt |
| Conference | ICLR |
| Venue | ICLR 2026 (main) |
| Domains | Software Engineering, Systems & Performance |
| Evidence class | Evaluation only |
| First published | 2026-01-17 |
| Identifiers | [arXiv:2601.11868](https://arxiv.org/abs/2601.11868) |
| Artifact | [Official artifact](https://github.com/harbor-framework/terminal-bench-2) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude Opus 4.5 | not-reported |
| Codex CLI | evaluated | GPT-5.2 | not-reported |

## Task

**Task.** General terminal-agent evaluation

**Benchmark or scale.** Terminal-Bench 2.0

## Method

Evaluation-only benchmark with stronger task verification and a neutral terminal scaffold

**Tags.** `verifier-loop`

## Reported evidence

GPT-5.2 with Codex CLI scores 62.9; Claude Opus 4.5 scores 57.8 with Terminus 2 and 52.1 with Claude Code.

| Control | Recorded value |
|---|---|
| Same model | unknown |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | benchmark-only |
| Source location | Main agent and model results table |

## Caveat

Benchmark result; differences can reflect both model and harness, and no new method is proposed to beat the products.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/444a3737adaee10d86ad2ef5f74468e6-Paper-Conference.pdf)
- [Artifact](https://github.com/harbor-framework/terminal-bench-2)

---

Catalog ID: `terminal-bench-2-2026` · Metadata last reviewed with catalog release.
