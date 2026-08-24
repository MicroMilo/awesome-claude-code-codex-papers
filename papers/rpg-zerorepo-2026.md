<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# ZeroRepo / RPG

## RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation

| Field | Value |
|---|---|
| Authors | Jane Luo, Xin Zhang, Steven Liu, Jie Wu, Jianfeng Liu, Yiming Huang, Yangyu Huang, Chengyu Yin, Ying Xin, Yuefeng Zhan, Hao Sun, Qi Chen, Scarlett Li, Mao Yang |
| Conference | ICLR |
| Venue | ICLR Conference 2026 (main) |
| Domains | Software Engineering |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/microsoft/RPG-ZeroRepo) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | claude 4 sonnet | not-reported |
| Codex CLI | baseline | o3 pro | not-reported |

## Task

**Task.** Repository-level codebase generation

**Benchmark or scale.** RepoCraft

## Method

A persistent repository planning graph over features, functions, files, interfaces, and data flow guides staged generation, dependency-aware planning, and validation.

**Tags.** `structured-state` `repository-graph` `dependency-aware-planning` `test-feedback`

## Reported evidence

ZeroRepo reaches 81.5% functional coverage and 69.7% test accuracy, improving over Claude Code by 27.3 and 35.8 points; it produces about 36K lines and 445K code tokens.

| Control | Recorded value |
|---|---|
| Same model | no |
| Same budget | unknown |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | product-level |
| Source location | Section 3.3 Baselines; Section 4.3; RepoCraft main-results table |

## Caveat

ZeroRepo uses a different backbone/configuration from each terminal-product baseline, so model and harness effects are mixed.

## Primary links

- [Paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9482f45fdd89aba9130bb04c44f788a9-Abstract-Conference.html)
- [Artifact](https://github.com/microsoft/RPG-ZeroRepo)

---

Catalog ID: `rpg-zerorepo-2026` · Metadata last reviewed with catalog release.
