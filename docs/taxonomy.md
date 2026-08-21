# Catalog Taxonomy

## Products

- `claude-code`: Anthropic's Claude Code product or CLI used as an end-to-end agent harness.
- `codex-cli`: OpenAI Codex CLI used as an end-to-end agent harness.
- `openai-codex-model`: the historical OpenAI Codex model, without the modern Codex CLI harness.

The product field describes the evaluated harness, not merely the model provider. A paper using a Claude API model inside a custom scaffold is not automatically a Claude Code paper.

## Domains

Domains describe the task or evidence area studied by a paper. They are multi-valued: a mobile-agent benchmark can be both `software-engineering` and `web-ui`.

- `software-engineering`: repository understanding, code generation, repair, testing, maintenance, and development workflows.
- `security`: vulnerability discovery, exploitation, red teaming, secure repair, or agent security.
- `systems-performance`: systems work, runtime behavior, resource efficiency, or performance engineering.
- `machine-learning`: model training, architecture search, or ML research automation.
- `scientific-computing`: scientific software, simulation, numerical computing, or research code.
- `formal-methods`: theorem proving, proof assistants, program verification, or formal reasoning.
- `web-ui`: web, mobile, frontend, visual fidelity, or interaction implementation.
- `documents`: document generation, conversion, layout, or structured office artifacts.

## Conference and venue

`conference` is the standardized series used by filters: `AAAI`, `ASE`, `FSE`, `ICLR`, `ICML`, `ICSE`, `ISSTA`, `NeurIPS`, `arXiv`, or `Other`. `venue` preserves the exact proceedings, track, workshop, or preprint label reported by the source. A paper that has not been accepted by a listed conference remains `arXiv`, even when its subject fits that community.

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
- `coordination`: explicit communication, synchronization, delegation, or handoff between agents.
- `adversarial-testing`: attacks, red-team probes, or hostile inputs are used to expose failures.
- `benchmark-design`: dataset construction, executable oracles, contamination controls, or evaluation protocol design is the central contribution.

## Comparison controls

`same_model` and `same_budget` use `yes`, `no`, or `unknown`.

- `yes`: the paper explicitly holds the variable fixed.
- `no`: the paper explicitly uses different models or budgets.
- `unknown`: the source does not establish parity clearly enough.

These fields describe experimental controls, not paper quality.

## Claim types

- `quality`: correctness, pass rate, coverage, ranking, or another outcome-quality measure.
- `efficiency`: latency, token use, monetary cost, throughput, or another resource measure.
- `mixed`: the central evidence includes both quality and efficiency.
- `diagnostic`: the paper measures behavior or failures rather than claiming an improvement.

## Comparison scope

- `product-level`: the proposed system and production product are compared end to end.
- `component-level`: the main evidence isolates retrieval, planning, testing, or another component.
- `configuration-ablation`: the product is compared under changed instructions or configuration.
- `benchmark-only`: the product is measured without an improvement intervention.
- `historical-model`: the result concerns the pre-CLI OpenAI Codex model.

## Evidence strength

- `high`: the central claim is clearly reported in a primary paper table, figure, or section.
- `medium`: useful product-level evidence is reported, but controls or reporting are incomplete.
- `contextual`: the product appears in a partial, secondary, or non-central comparison.

Strength records how directly the catalog claim is supported. It is not a paper-quality score.

## Artifact status

- `official`: maintained by the paper authors or publishing organization.
- `community`: a useful third-party implementation or reproduction.
- `not-found`: no qualifying artifact was found during the latest catalog review.
