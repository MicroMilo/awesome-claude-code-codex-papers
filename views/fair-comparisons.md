<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Research views](README.md) · [Home](../README.md)

# Comparison fairness

“Direct comparison” means a numeric head-to-head was reported.
It does not mean the model, budget, tools, or product policy were held fixed.

## Same model and same budget (1)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [AGENTS.md](../papers/agents-md-impact-2026.md) | yes | yes | high | Workshop study and configuration intervention rather than a standalone agent. |
## Known model or budget mismatch (6)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [ARTEMIS](../papers/artemis-2026.md) | unknown | no | medium | Runtime limits, model combinations, safety refusals, and product policies differ across systems. |
| [AgentRadio](../papers/agentradio-2026.md) | yes | no | high | The four-agent method costs about six times a single Opus 4.6 run, although the paper includes a near-cost resampling baseline. |
| [Brief](../papers/brief-product-context-2026.md) | no | no | high | The augmented arm adds Opus planning, a longer timeout, generated specifications, tests, and retrieval, so the 49-point gain is not attributable to product context alone. |
| [EvoDev](../papers/evodev-2026.md) | yes | no | high | APPDev contains 15 Android apps and uses manual quality scoring; EvoDev takes about twice Claude Code's wall-clock time in the Claude 4 Sonnet comparison. |
| [RustPrint](../papers/rustprint-2026.md) | no | unknown | medium | The comparison mixes model and scaffold choices and is specific to C-to-Rust migration. |
| [ZeroRepo](../papers/rpg-zerorepo-2026.md) | no | unknown | high | ZeroRepo uses o3-mini while the Claude Code baseline uses Claude 4 Sonnet, so model and harness effects are mixed. |
## Control parity not fully reported (12)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [Agentic Harness Engineering](../papers/agentic-harness-engineering-2026.md) | unknown | unknown | medium | Preprint; model, harness, and evaluation-budget effects require careful separation. |
| [Co-Coder](../papers/co-coder-2026.md) | unknown | unknown | medium | Small 28-task evaluation and preprint status. |
| [FormAct](../papers/formact-2026.md) | unknown | unknown | high | Codex has slightly higher content alignment, and the task is document formatting rather than source-code repair. |
| [Guardrails Beat Guidance](../papers/guardrails-guidance-2026.md) | yes | unknown | high | Results are limited to Claude Code with Opus 4.6 on a discriminative Python subset; several headline pairwise differences do not reach conventional significance. |
| [LLM2Ltac](../papers/llm2ltac-2026.md) | unknown | unknown | high | The public conference record does not report the Claude Code version, backbone model, absolute theorem counts for the product ablation, or budget parity. |
| [Prefactory](../papers/prefactory-2026.md) | unknown | unknown | medium | The strongest comparison concerns candidate detection, not universal end-to-end task success. |
| [QLCoder](../papers/qlcoder-2026.md) | unknown | unknown | high | Security-query synthesis is narrower than general software engineering. |
| [RepoOMP](../papers/repoomp-2026.md) | unknown | unknown | medium | Domain-specific high-performance-computing task and preprint status. |
| [Volt with LCM](../papers/lcm-2026.md) | yes | unknown | high | OOLONG may be contaminated in Opus 4.6, and the paper does not provide a matched end-to-end cost comparison for LCM's auxiliary calls. |
| [WebDesignIter](../papers/webdesigniter-2026.md) | unknown | unknown | medium | Front-end-specific benchmark and preprint status. |
| [icat-agent](../papers/icat-agent-2026.md) | unknown | unknown | medium | Exact model parity varies by reported configuration; preprint. |
| [MLZero](../papers/mlzero-2025.md) | unknown | unknown | medium | Results concern machine-learning automation and should not be generalized to all software-engineering tasks. |
