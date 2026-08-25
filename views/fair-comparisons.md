<!-- Generated from data/papers.yaml; do not edit by hand. -->

[← Research views](README.md) · [Home](../README.md)

# Comparison fairness

“Direct comparison” means a numeric head-to-head was reported.
It does not mean the model, budget, tools, or product policy were held fixed.

## Same model and same budget (0)

_No papers in this group._
## Known model or budget mismatch (3)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [ARTEMIS](../papers/artemis-2026.md) | unknown | no | medium | This is live-network cybersecurity, not general coding; runtime limits, model mixtures, refusal behavior, and product policies differ. |
| [Helmsman](../papers/helmsman-2026.md) | no | unknown | high | The paper compares a multi-agent federated-learning system synthesis framework against product code-synthesis baselines. CLI versions, temperature, tool permissions, and exact budget caps are not reported. Helmsman's main backbone uses Gemini-2.5-flash for planning and Claude-Sonnet-4.0 for coding and evaluation; additional experiments use Claude-Sonnet-4.5 and GPT-5.1. |
| [ZeroRepo / RPG](../papers/rpg-zerorepo-2026.md) | no | unknown | high | ZeroRepo uses a different backbone/configuration from each terminal-product baseline, so model and harness effects are mixed. |
## Control parity not fully reported (3)

| System | Same model | Same budget | Strength | Caveat |
|---|---|---|---|---|
| [FormAct](../papers/formact-2026.md) | yes | unknown | high | The task is rich-format document editing rather than source-code repair; the paper does not report a CLI version or a matched multi-pass budget. |
| [Lean Refactor](../papers/lean-refactor-2026.md) | unknown | unknown | contextual | The IJCAI Early Career Spotlight paper reports only aggregate Lean Refactor results and the Claude Code comparison claim. It does not identify the Claude Code model or CLI version, task-level results, run count, tool permissions, or a common budget, so comparison fairness cannot be established from the official paper. |
| [QLCoder](../papers/qlcoder-2026.md) | unknown | unknown | high | The task is CodeQL security-query synthesis, not general repository-level software engineering; GPT-5 reasoning settings differ across Codex baseline rows. |
