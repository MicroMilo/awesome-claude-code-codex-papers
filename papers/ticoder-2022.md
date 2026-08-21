<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Paper index](README.md) · [Home](../README.md)

# TiCoder

## Interactive Code Generation via Test-Driven User-Intent Formalization

| Field | Value |
|---|---|
| Authors | Shuvendu K. Lahiri, Sarah Fakhoury, Aaditya Naik, Georgios Sakkas, Saikat Chakraborty, Madanlal Musuvathi, Piali Choudhury, Curtis von Veh, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao |
| Conference | ICSE |
| Venue | AST at ICSE 2022 (workshop) |
| Domains | Software Engineering |
| Evidence class | Historical model |
| First published | 2022-08-11 |
| Identifiers | [arXiv:2208.05950](https://arxiv.org/abs/2208.05950) |
| Artifact | [Official artifact](https://github.com/microsoft/TiCoder) |

## Product configuration

| Product | Role | Model | Product version |
|---|---|---|---|
| OpenAI Codex model | historical-baseline | OpenAI Codex | not-reported |

## Task

**Task.** Interactive function-level code generation

**Benchmark or scale.** MBPP and HumanEval

## Method

Generate tests to formalize user intent, collect lightweight feedback, and rank or prune candidate programs

**Tags.** `test-feedback` `verifier-loop`

## Reported evidence

With one to five simulated user queries, Codex pass@1 gains 22.49 to 37.71 points on MBPP and 24.79 to 53.98 points on HumanEval.

| Control | Recorded value |
|---|---|
| Same model | yes |
| Same budget | no |
| Evidence strength | high |
| Claim type | quality |
| Comparison scope | historical-model |
| Source location | MBPP and HumanEval evaluation section |

## Caveat

This is the historical OpenAI Codex model, not the modern Codex CLI product.

## Primary links

- [Paper](https://arxiv.org/abs/2208.05950)
- [Artifact](https://github.com/microsoft/TiCoder)

---

Catalog ID: `ticoder-2022` · Metadata last reviewed with catalog release.
