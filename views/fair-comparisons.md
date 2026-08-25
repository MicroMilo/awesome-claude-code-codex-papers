<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Research views](README.md) · [Home](../README.md)

# Comparison fairness

“Direct comparison” means a numeric head-to-head was reported.
It does not mean the model, budget, tools, or product policy were held fixed.

## Same model and same budget (3)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [APE-Bench / APE-Harness / APE-Agent](../papers/ape-bench-2026.md) | yes | yes | high | The auxiliary manuscript is arXiv v3 and its author list differs from the official ICML poster. Product CLI versions, temperature, output-token caps, and independent repeat counts are not reported; the domain is Lean proof engineering rather than general-purpose software repair. |
| [EvoDev](../papers/evodev-2026.md) | yes | yes | high | APPDev contains only 15 Kotlin Android applications and relies on blinded manual scoring. Product CLI version, temperature, output-token cap, exact permissions, and repeated-run variance are not reported; average Claude Code cost is higher than EvoDev but EvoDev takes longer. |
| [LLM2Ltac](../papers/llm2ltac-2026.md) | yes | yes | high | The evidence copy predates the accepted-title change and still contains placeholder ACM venue text. The Claude Code CLI version, exact model snapshot, temperature, output-token cap, and independent repeat count are not reported; the result is specific to Rocq theorem proving. |
## Known model or budget mismatch (4)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [ARTEMIS](../papers/artemis-2026.md) | unknown | no | medium | This is live-network cybersecurity, not general coding; runtime limits, model mixtures, refusal behavior, and product policies differ. |
| [Execution-aware repair policies](../papers/execution-cost-effectiveness-2026.md) | yes | no | high | Execution access is intentionally unequal across configurations, and most restrictions are prompt-level; the paper separately verifies zero-execution subsets and a 100-task hard-denial Claude Code run. Results cover Python-heavy SWE-bench subsets and one fixed product/model version per commercial agent. |
| [Helmsman](../papers/helmsman-2026.md) | no | unknown | high | The paper compares a multi-agent federated-learning system synthesis framework against product code-synthesis baselines. CLI versions, temperature, tool permissions, and exact budget caps are not reported. Helmsman's main backbone uses Gemini-2.5-flash for planning and Claude-Sonnet-4.0 for coding and evaluation; additional experiments use Claude-Sonnet-4.5 and GPT-5.1. |
| [ZeroRepo / RPG](../papers/rpg-zerorepo-2026.md) | no | unknown | high | ZeroRepo uses a different backbone/configuration from each terminal-product baseline, so model and harness effects are mixed. |
## Control parity not fully reported (3)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [FormAct](../papers/formact-2026.md) | yes | unknown | high | The task is rich-format document editing rather than source-code repair; the paper does not report a CLI version or a matched multi-pass budget. |
| [Lean Refactor](../papers/lean-refactor-2026.md) | unknown | unknown | contextual | The IJCAI Early Career Spotlight paper reports only aggregate Lean Refactor results and the Claude Code comparison claim. It does not identify the Claude Code model or CLI version, task-level results, run count, tool permissions, or a common budget, so comparison fairness cannot be established from the official paper. |
| [QLCoder](../papers/qlcoder-2026.md) | unknown | unknown | high | The task is CodeQL security-query synthesis, not general repository-level software engineering; GPT-5 reasoning settings differ across Codex baseline rows. |
