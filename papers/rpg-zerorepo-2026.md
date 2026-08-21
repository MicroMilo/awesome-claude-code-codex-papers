<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# ZeroRepo

## RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation

| Field | Value |
|---|---|
| Authors | Jane Luo, Xin Zhang, Steven Liu, Jie Wu, Jianfeng Liu, Yiming Huang, Yangyu Huang, Chengyu Yin, Ying Xin, Yuefeng Zhan, Hao Sun, Qi Chen, Scarlett Li, Mao Yang |
| Venue | ICLR 2026 (main) |
| Evidence class | Direct comparison |
| First published | 2025-09-19 |
| Identifiers | [arXiv:2509.16198](https://arxiv.org/abs/2509.16198) |
| Artifact | [Official artifact](https://github.com/microsoft/RPG-ZeroRepo) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Claude 4 Sonnet | not-reported |
| Codex CLI | baseline | o3-pro | not-reported |

## Task

**Task.** Repository-level codebase generation

**Benchmark or scale.** RepoCraft

## Method

Persistent graph over features, functions, files, interfaces, and data flow with graph-guided generation and validation

**Tags.** `structured-state` `repository-graph` `dependency-aware-planning` `test-feedback`

## Reported evidence

ZeroRepo coverage 81.5% versus Claude Code 54.2% and Codex 28.4%; pass rate 69.7% versus Claude Code 33.9%.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Section 4.3 and RepoCraft main-results table |

## Caveat

ZeroRepo uses o3-mini while the Claude Code baseline uses Claude 4 Sonnet, so model and harness effects are mixed.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/9482f45fdd89aba9130bb04c44f788a9-Paper-Conference.pdf)
- [Artifact](https://github.com/microsoft/RPG-ZeroRepo)

---

Catalog ID: `rpg-zerorepo-2026` · Metadata last reviewed with catalog release.
