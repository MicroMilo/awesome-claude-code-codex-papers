# Catalog Taxonomy

## Products

- `claude-code`: Anthropic's Claude Code product or CLI used as an end-to-end agent harness.
- `codex-cli`: OpenAI Codex CLI used as an end-to-end agent harness.
- `openai-codex-model`: the historical OpenAI Codex model, without the modern Codex CLI harness.

The product field describes the evaluated harness, not merely the model provider. A paper using a Claude API model inside a custom scaffold is not automatically a Claude Code paper.

## Evidence classes

### Direct comparison

The paper reports at least one numeric comparison between its proposed method and Claude Code or Codex CLI. Direct does not imply fair: `same_model`, `same_budget`, and caveats record comparability.

### Related method

The product is integrated, discussed, or used in a partial experiment, but the central result is not a clean product-level comparison.

### Evaluation only

The paper introduces a benchmark, dataset, measurement study, or failure analysis and reports product-level results without a method intended to outperform the product.

### Historical model

The paper studies the pre-CLI OpenAI Codex model. These entries are retained for research continuity but never mixed with modern Codex CLI results.

## Method tags

- `structured-state`: externalized plans, repository graphs, architecture descriptions, or durable state.
- `repository-graph`: graph representation of files, symbols, features, dependencies, or data flow.
- `retrieval`: learned or engineered selection of relevant code and evidence.
- `context-reduction`: removal or compression of irrelevant context.
- `verifier-loop`: an external executable judge provides iterative repair signals.
- `static-analysis`: static-analysis queries, ASTs, LSP services, or program-analysis tools.
- `test-feedback`: tests or coverage guide the next action.
- `performance-feedback`: measured runtime or speedup guides acceptance and repair.
- `multi-agent`: more than one active reasoning agent.
- `dynamic-specialization`: roles or experts are created based on task state.
- `dependency-aware-planning`: ordering or partitioning follows program dependencies.
- `parallelism`: concurrent agent execution is a core mechanism.
- `memory`: durable semantic, episodic, or task memory.
- `harness-evolution`: automatic modification of tools, prompts, memory, middleware, or runtime policy.
- `observability`: structured trajectory, component, or decision-level evidence.
- `repository-instructions`: repository-scoped instruction files such as AGENTS.md.
- `deterministic-search`: non-LLM rules or analyses narrow candidates before generation.
- `visual-review`: rendered output is inspected and used as feedback.

## Comparison controls

`same_model` and `same_budget` use `yes`, `no`, or `unknown`.

- `yes`: the paper explicitly holds the variable fixed.
- `no`: the paper explicitly uses different models or budgets.
- `unknown`: the source does not establish parity clearly enough.

These fields describe experimental controls, not paper quality.
