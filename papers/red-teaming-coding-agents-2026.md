<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# ToolLeak / RCE-2

## Red-Teaming Coding Agents from a Tool-Invocation Perspective: An Empirical Security Assessment

| Field | Value |
|---|---|
| Authors | Yuchong Xie, Mingyu Luo, Zesen Liu, Zhixiang Zhang, Kaikai Zhang, Yu Liu, Ci Tao, Changhui Wang, Zongjie Li, Ping Chen, Shuai Wang, Dongdong She |
| Conference | ISSTA |
| Venue | ISSTA Research Papers 2026 (main) |
| Domains | Security, Software Engineering |
| Evidence class | Evaluation only |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://anonymous.4open.science/r/issta_2026-B18F) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | evaluated | Claude-Sonnet 4; Claude-Sonnet 4.5; Claude-Sonnet 4.6; Claude-Opus-4.7 | v2.0.37 (Old); v2.1.138 (New) |

## Task

**Task.** Exfiltrate hidden coding-agent prompts and hijack MCP tool invocation to trigger attacker-selected command execution.

**Benchmark or scale.** Six real-world coding agents across 25 old/new agent-model pairs, plus emulated agents conditioned on recovered prompts

## Method

ToolLeak exploits weaker guardrails during schema-driven argument filling; RCE-2 chains a malicious tool description with a high-salience tool-return instruction tailored from leaked prompt details.

**Tags.** `adversarial-testing` `observability`

## Reported evidence

On old Claude Code v2.0.37, ToolLeak reaches 1.00 pseudo-recall for both Sonnet 4 and Sonnet 4.5, while RCE-2 reaches 0.6 and 0.7 attack success. On v2.1.138, progressive disclosure of tool names plus newer Sonnet 4.6/Opus 4.7 reduces RCE-2 to 0.0, demonstrating that agent-side tool-description isolation is an effective defense.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | diagnostic |
| Comparison scope | benchmark-only |
| Source location | Section 6.1 and Table 2; Sections 6.2-6.4; Tables 3-5; Section 7.2 in arXiv v6 |

## Caveat

The evidence copy predates an official camera-ready PDF and has two fewer authors than the official ISSTA record. Pseudo-recall uses the union of all methods rather than ground truth, real-world leakage selects best-of-10, and attack outcomes depend on exact product generation and MCP exposure.

## Primary links

- [Paper](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/176/Red-Teaming-Coding-Agents-from-a-Tool-Invocation-Perspective-An-Empirical-Security-A)
- [Artifact](https://anonymous.4open.science/r/issta_2026-B18F)
- [Identity-verified evidence copy](https://arxiv.org/abs/2509.05755v6) (submittedVersion; not the acceptance source)

---

Catalog ID: `red-teaming-coding-agents-2026` · Metadata last reviewed with catalog release.
