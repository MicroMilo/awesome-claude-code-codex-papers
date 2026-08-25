<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# APE-Bench / APE-Harness / APE-Agent

## APE-Bench: Evaluating Automated Proof Engineering for Formal Math Libraries

| Field | Value |
|---|---|
| Authors | Huajian Xin, Zheng Yuan, Jacques Fleuriot, Wenda Li |
| Conference | ICML |
| Venue | ICML Main Conference 2026 (dataset-benchmark) |
| Domains | Formal Methods, Software Engineering |
| Evidence class | Direct comparison |
| First published | Not recorded |
| Identifiers | Official conference source |
| Artifact | [Official artifact](https://github.com/xinhjBrant/APE-Bench) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| Claude Code | baseline | Gemini 3 Flash; Gemini 3 Pro; GPT-5.2 | not-reported |
| Codex CLI | baseline | Gemini 3 Flash; Gemini 3 Pro; GPT-5.2 | not-reported |

## Task

**Task.** Modify pinned Mathlib repositories from natural-language proof-engineering requirements and satisfy compilation plus semantic constraints.

**Benchmark or scale.** APE-Bench, 100 tasks from 67 Mathlib commits dated 2026-01-06 through 2026-01-12; also miniCTX and miniF2F

## Method

Declarative task contracts bind repository versions, access controls, retrieval, compilation, and semantic verification while APE-Agent integrates editing with verification in a compact ReAct scaffold.

**Tags.** `benchmark-design` `verifier-loop` `retrieval` `deterministic-search`

## Reported evidence

On identical APE-Bench tasks and 3 USD/100-turn budgets, APE-Agent reaches 47%, 24%, and 27% with Gemini 3 Flash, Gemini 3 Pro, and GPT-5.2; Claude Code reaches 27%, 8%, and 10%, while Codex reaches 32%, 1%, and 11%. The paper attributes the 15–23 point gaps to integrated verification, shorter prompts, and lower redundant execution/retrieval overhead.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | yes |
| Evidence strength | high |
| Claim type | mixed |
| Comparison scope | product-level |
| Source location | Section 6.1 Experimental Setup; Figure 3; Section 6.4 Scaffold Interchangeability; Figure 4 in arXiv v3 |

## Caveat

The auxiliary manuscript is arXiv v3 and its author list differs from the official ICML poster. Product CLI versions, temperature, output-token caps, and independent repeat counts are not reported; the domain is Lean proof engineering rather than general-purpose software repair.

## Primary links

- [Paper](https://icml.cc/virtual/2026/poster/64323)
- [Artifact](https://github.com/xinhjBrant/APE-Bench)
- [Identity-verified evidence copy](https://arxiv.org/abs/2504.19110v3) (submittedVersion; not the acceptance source)

---

Catalog ID: `ape-bench-2026` · Metadata last reviewed with catalog release.
