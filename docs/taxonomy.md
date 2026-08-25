# Catalog Taxonomy

## Products

- `claude-code`: Anthropic's Claude Code product or CLI used as an end-to-end agent harness.
- `codex-cli`: OpenAI Codex CLI used as an end-to-end agent harness.

The product field describes the evaluated harness, not merely the model provider. A paper using a Claude API model, a GPT-family model, or the historical OpenAI Codex model without the corresponding product harness is outside the main-catalog scope.

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

`conference` is the standardized series used by filters: `AAAI`, `ASE`, `FSE`, `ICLR`, `ICML`, `ICSE`, `ISSTA`, `NeurIPS`, `IJCAI`, `KDD`, `PLDI`, `POPL`, or `OOPSLA`. `venue` preserves the exact proceedings, track, or workshop label reported by the first-party source. The main catalog contains only 2026 records with an official conference/proceedings/OpenReview source; preprint-only records live in the audit report as excluded or pending records.

Each main-catalog record also carries `year_tag: 2026`, `conference_tag` (equal to `conference`), `source_type`, and `audit_status: included`. `source_type` makes the provenance machine-checkable; `audit_status` prevents an unreviewed census record from being silently promoted.

`paper_url` is always the official acceptance/proceedings/publisher record.
Optional `content_sources` identify auxiliary abstract or full-text copies and
must record provider, version, identity method, official DOI binding,
discovery time, and intended use. An arXiv URL may appear there as content
evidence, but never as the primary paper source.

## Evidence classes

### Direct comparison

The paper reports at least one numeric comparison between its proposed method and Claude Code or Codex CLI. Direct does not imply fair: `same_model`, `same_budget`, and caveats record comparability.

### Related method

The product is integrated, discussed, or used in a partial experiment, but the central result is not a clean product-level comparison.

### Evaluation only

The paper introduces a benchmark, dataset, measurement study, or failure analysis and reports product-level results without a method intended to outperform the product.

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

## Experiment configuration

`experiment` preserves the paper's reported settings as strings so that exact
snapshots and phrases such as `gpt-5.2-2025-12-11`, `minimal reasoning`, or
`not-reported` are not silently normalized away. It records reasoning mode,
temperature, output and time/turn/token/API budgets, run count, tool
permissions, and the baseline configuration. Product rows carry the exact
model and product/CLI version; a version is `not-reported` only after the
full text, appendix, and available artifact have been checked.

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

## Evidence strength

- `high`: the central claim is clearly reported in a primary paper table, figure, or section.
- `medium`: useful product-level evidence is reported, but controls or reporting are incomplete.
- `contextual`: the product appears in a partial, secondary, or non-central comparison.

Strength records how directly the catalog claim is supported. It is not a paper-quality score.

## Artifact status

- `official`: maintained by the paper authors or publishing organization.
- `community`: a useful third-party implementation or reproduction.
- `not-found`: no qualifying artifact was found during the latest catalog review.
