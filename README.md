<p align="center">
  <img src="assets/hero.png" alt="Coding-agent experiments flowing through an evidence graph into research papers" width="100%">
</p>

<h1 align="center">Awesome Claude Code & Codex Papers</h1>

<p align="center">
  <strong>Research that measures, analyzes, or beats real production coding agents.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml"><img alt="Validate catalog" src="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-22c55e"></a>
  <a href="CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen"></a>
  <a href="data/papers.yaml"><img alt="Data YAML" src="https://img.shields.io/badge/catalog-YAML%20%2B%20JSON-2563eb"></a>
</p>

<!-- CATALOG:STATS:START -->
<p align="center">
  <img alt="papers: 19" src="https://img.shields.io/badge/papers-19-0f766e">
  <img alt="direct comparisons: 13" src="https://img.shields.io/badge/direct%20comparisons-13-dc6b46">
  <img alt="official artifacts: 11" src="https://img.shields.io/badge/official%20artifacts-11-2563eb">
  <img alt="venues: 7" src="https://img.shields.io/badge/venues-7-7c3aed">
  <img alt="reviewed: 2026-08-21" src="https://img.shields.io/badge/reviewed-2026--08--21-475569">
</p>
<!-- CATALOG:STATS:END -->

This repository is an evidence-first catalog of papers that study **Claude Code** and **Codex CLI** as complete products—not merely Claude or GPT-family models. It records the baseline configuration, task, intervention, reported result, comparison controls, caveats, and official artifacts.

> [!IMPORTANT]
> This is not a leaderboard. Product versions, backbone models, budgets, tools, and task domains often differ. Every direct result links to a paper dossier that makes those differences explicit.

## Start here

| View | Best for |
|---|---|
| [All paper dossiers](papers/README.md) | Inspecting authors, products, models, versions, evidence locations, and caveats |
| [By product](views/by-product.md) | Finding Claude Code or Codex CLI papers |
| [By method](views/by-method.md) | Studying retrieval, repository graphs, verification, multi-agent coordination, and harness evolution |
| [Comparison fairness](views/fair-comparisons.md) | Separating controlled comparisons from model or budget confounds |
| [By venue](views/by-venue.md) | Browsing main conferences, workshops, benchmark tracks, and preprints |
| [Machine-readable catalog](data/papers.json) | Building tools, visualizations, or downstream surveys |

## The question this catalog answers

Broad agent-paper lists answer **“What has been published?”** This catalog asks:

> **When researchers evaluate or outperform Claude Code or Codex CLI, what did they add, what improved, and was the comparison fair?**

Each reviewed entry captures:

- product, CLI version, model, and role in the experiment;
- task, benchmark, and evaluation scale;
- the method added around or instead of the product baseline;
- reported quality, efficiency, or diagnostic evidence;
- same-model and same-budget controls;
- evidence location, caveats, and artifact availability.

## Scope

The initial scope is deliberately narrow: **Claude Code** and **Codex CLI**. The schema is already product-agnostic, so later releases can add Kimi Code, Zed, Cursor, Gemini CLI, and other industrial coding agents without redesigning the catalog.

Included:

- direct product-level comparisons;
- harness, configuration, retrieval, planning, and verification improvements;
- benchmarks and empirical studies with product-level results;
- historical OpenAI Codex model papers, isolated from modern Codex CLI results.

Excluded from the primary catalog:

- papers that use a vendor model but never run the corresponding product agent;
- blog-only or marketing comparisons without a research artifact;
- claims that cannot be traced to a primary paper or official artifact.

## Direct comparisons

These papers numerically compare a proposed method with Claude Code or Codex CLI. “Direct” does not imply same-model or same-budget parity—check the controls column and linked dossier.

<details>
<summary><strong>Open the raw direct-comparison table</strong></summary>

<!-- CATALOG:DIRECT:START -->
| System / paper | Venue | Product baseline | Task | What changed | Reported evidence | Controls |
|---|---|---|---|---|---|---|
| **[Agentic Harness Engineering](papers/agentic-harness-engineering-2026.md)**<br>[paper](https://arxiv.org/abs/2604.25850) · [artifact](https://github.com/china-qijizhifeng/agentic-harness-engineering) | arXiv 2026<br>preprint | Codex CLI | Automatic evolution of coding-agent harnesses | Closed-loop harness evolution using component, trajectory, and decision observability with evidence-backed edits and rollback<br>`harness-evolution` `observability` `memory` `verifier-loop` | Terminal-Bench 2 pass@1 improves from 69.7 to 77.0, above a human-designed Codex-CLI harness at 71.9; transfer uses 12% fewer tokens on SWE-bench Verified. | model: unknown<br>budget: unknown<br>evidence: medium |
| **[AGENTS.md](papers/agents-md-impact-2026.md)**<br>[paper](https://conf.researchr.org/details/icse-2026/jaws-2026-papers/31/On-the-Impact-of-AGENTS-md-Files-on-the-Efficiency-of-AI-Coding-Agents) | ICSE JAWs 2026<br>workshop | Claude Code<br>Codex CLI | Real pull-request tasks with and without repository instructions | Persistent repository-level build, test, style, and directory guidance in AGENTS.md<br>`repository-instructions` `structured-state` `context-reduction` | Median runtime falls 28.64% and output tokens fall 16.58% with comparable completion behavior. | model: same<br>budget: same<br>evidence: high |
| **[ARTEMIS](papers/artemis-2026.md)**<br>[paper](https://arxiv.org/abs/2512.09882) · [artifact](https://github.com/Stanford-Trinity/ARTEMIS) | ICLR 2026<br>main | Claude Code (Claude Sonnet 4)<br>Codex CLI (GPT-5) | Long-horizon penetration testing in a live enterprise network | Supervisor with dynamic expert agents, recursive task decomposition, parallel exploration, context management, triage, and reporting<br>`multi-agent` `dynamic-specialization` `parallelism` `memory` `verifier-loop` | ARTEMIS found 9 valid vulnerabilities with an 82% valid-submission rate, ranked second overall, and outperformed 9 of 10 human participants. | model: unknown<br>budget: different<br>evidence: medium |
| **[Co-Coder](papers/co-coder-2026.md)**<br>[paper](https://arxiv.org/abs/2606.00953) · [artifact](https://github.com/Flitternie/CoCoder) | arXiv 2026<br>preprint | Claude Code (Agent Teams) | Parallel multi-agent coding | Static dependency graph partitioning, structural hub isolation, community detection, and dependency-aware scheduling<br>`repository-graph` `dependency-aware-planning` `multi-agent` `parallelism` | Pass rate improves 14.0%, wall-clock speedup reaches 2.10x, and API cost falls 35% relative to Claude Code Agent Teams and simpler schedules. | model: unknown<br>budget: unknown<br>evidence: medium |
| **[FormAct](papers/formact-2026.md)**<br>[paper](https://openreview.net/forum?id=n7Ta0YEcgw) | ICML 2026<br>main | Codex CLI | Rich-format document generation and editing | HTML source editor, template retrieval, rendered-page review agent, iterative refinement, and edit-triggered context compression<br>`retrieval` `context-reduction` `verifier-loop` `visual-review` | Render correctness 4.81 versus 4.39 for multi-pass Codex; human rank-1 rate 0.760 versus 0.140. | model: unknown<br>budget: unknown<br>evidence: high |
| **[icat-agent](papers/icat-agent-2026.md)**<br>[paper](https://arxiv.org/abs/2606.25514) | arXiv 2026<br>preprint | Claude Code | Repository issue resolution | Event-based agent communication, issue-quality routing, parallel patching and validation, and exploratory fallback<br>`multi-agent` `dynamic-specialization` `parallelism` `test-feedback` | SWE-bench Verified improves 3.6 to 8.4 percentage points and SWE-bench Pro 6.3 to 18.5 points; average cost is $1.18 lower than multi-agent Claude Code. | model: unknown<br>budget: unknown<br>evidence: medium |
| **[Prefactory](papers/prefactory-2026.md)**<br>[paper](https://arxiv.org/abs/2607.17211) | arXiv 2026<br>preprint | Codex CLI | Discovery and application of library-adoption refactorings | LLM-synthesized lexical and structural search heuristics, deterministic candidate ranking, targeted refactoring, and differential tests<br>`deterministic-search` `static-analysis` `test-feedback` `verifier-loop` | File-level detection 75 versus Codex 35; function-level detection 56 versus 32; 40 of 56 candidates yield test-validated refactorings. | model: unknown<br>budget: unknown<br>evidence: medium |
| **[QLCoder](papers/qlcoder-2026.md)**<br>[paper](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html) · [artifact](https://github.com/neuralprogram/qlcoder) | ICLR 2026<br>main | Claude Code (Claude Sonnet 4, 1.0.120) | CodeQL query synthesis from CVE metadata | CVE-grounded retrieval, AST guidance, CodeQL LSP tools, and iterative execution feedback<br>`retrieval` `verifier-loop` `static-analysis` | Correct-query rate 53.4% versus 10% for Claude Code-only; F1 0.70 versus 0.048 for IRIS and 0.073 for CodeQL suites. | model: unknown<br>budget: unknown<br>evidence: high |
| **[RepoOMP](papers/repoomp-2026.md)**<br>[paper](https://arxiv.org/abs/2608.05855) · [artifact](https://github.com/Qlalq/RepoOMP_Simplified) | arXiv 2026<br>preprint | Claude Code | Repository-aware OpenMP hotspot parallelization | Multi-granularity dependency graph, rule-or-LLM hotspot routing, reduced transformation context, and compile/workload/speedup validation<br>`repository-graph` `context-reduction` `deterministic-search` `performance-feedback` `verifier-loop` | Across nine detailed kernels, speedup improves 18% to 28% and token cost falls 47% to 68% relative to unstructured Claude Code. | model: unknown<br>budget: unknown<br>evidence: medium |
| **[RustPrint](papers/rustprint-2026.md)**<br>[paper](https://arxiv.org/abs/2605.14634) | arXiv 2026<br>preprint | Claude Code | Whole-codebase migration from C to Rust | Architecture documentation blueprint, module and data-flow planning, compile feedback, documentation mismatch repair, and source-test translation<br>`structured-state` `dependency-aware-planning` `verifier-loop` `test-feedback` | In the reported Kimi-K2-Instruct setting, feature preservation is 93.26% versus 52.52% for agentic Claude Code; cross-evaluation test pass is 95.17% versus 79.85%. | model: different<br>budget: unknown<br>evidence: medium |
| **[WebDesignIter](papers/webdesigniter-2026.md)**<br>[paper](https://arxiv.org/abs/2607.10621) · [artifact](https://github.com/SYSUSELab/WebDesignIter) | arXiv 2026<br>preprint | Claude Code<br>Codex CLI | Repository-level front-end code generation | Persistent architecture and design knowledge graph, design-informed planning, targeted patches, and sandbox repair<br>`structured-state` `repository-graph` `retrieval` `test-feedback` | Average Pass@2 improves by 9.55 percentage points over existing baselines; removing design knowledge reduces Pass@1 by 11.4 points. | model: unknown<br>budget: unknown<br>evidence: medium |
| **[ZeroRepo](papers/rpg-zerorepo-2026.md)**<br>[paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/9482f45fdd89aba9130bb04c44f788a9-Paper-Conference.pdf) · [artifact](https://github.com/microsoft/RPG-ZeroRepo) | ICLR 2026<br>main | Claude Code (Claude 4 Sonnet)<br>Codex CLI (o3-pro) | Repository-level codebase generation | Persistent graph over features, functions, files, interfaces, and data flow with graph-guided generation and validation<br>`structured-state` `repository-graph` `dependency-aware-planning` `test-feedback` | ZeroRepo coverage 81.5% versus Claude Code 54.2% and Codex 28.4%; pass rate 69.7% versus Claude Code 33.9%. | model: different<br>budget: unknown<br>evidence: high |
| **[MLZero](papers/mlzero-2025.md)**<br>[paper](https://papers.neurips.cc/paper_files/paper/2025/hash/63ed15a46a143ff57484b38cd6b85d91-Abstract-Conference.html) · [artifact](https://github.com/autogluon/autogluon-assistant) | NeurIPS 2025<br>main | Codex CLI (GPT-4.1 and o4-mini) | End-to-end machine learning automation | Hierarchical agents with multimodal perception, semantic and episodic memory, and a planning-coding-evaluation loop<br>`multi-agent` `memory` `verifier-loop` `test-feedback` | MLZero led MLE-Bench Lite with six gold medals and achieved 0.92 success on its multimodal benchmark; one appendix setting reports 6.5% errors versus 26.9% for Codex CLI. | model: unknown<br>budget: unknown<br>evidence: medium |
<!-- CATALOG:DIRECT:END -->

</details>

## What repeatedly works

Across the current catalog, successful methods repeatedly add structure around the model:

1. **Persistent repository state** — plans, architecture, dependencies, and design knowledge survive beyond one context window.
2. **Executable feedback** — tests, compilers, static analyzers, renderers, or performance measurements decide what is correct.
3. **Targeted retrieval** — specialized search and context reduction replace indiscriminate long-context loading.
4. **Dependency-aware orchestration** — task graphs determine what can run in parallel and what must remain serial.
5. **Harness observability** — trajectories, components, and decisions become inspectable and reversible.
6. **Low-cost repository guidance** — focused project instructions reduce wasted actions and tokens.

See the generated [method view](views/by-method.md) and [taxonomy](docs/taxonomy.md).

## Related methods

These papers contain useful product-level evidence, but their central numeric result is a component comparison or another agent's result rather than a clean Claude Code/Codex CLI head-to-head.

<details>
<summary><strong>Open the raw related-method table</strong></summary>

<!-- CATALOG:RELATED:START -->
| System / paper | Venue | Product baseline | Task | What changed | Reported evidence | Controls |
|---|---|---|---|---|---|---|
| **[CodeGrep](papers/codegrep-2026.md)**<br>[paper](https://arxiv.org/abs/2608.05886) | arXiv 2026<br>preprint | Claude Code (Claude-Code-like agent) | Repository retrieval for issue resolution | GRPO-trained 14B retrieval agent that issues multi-turn parallel grep, glob, and read operations for a frozen downstream coding agent<br>`retrieval` `context-reduction` `parallelism` | Resolve rate 27.0% versus 25.8% without retrieval; resolved tasks use 15% fewer rounds and 19% fewer tokens. | model: same<br>budget: unknown<br>evidence: contextual |
| **[SCATE](papers/scate-2026.md)**<br>[paper](https://arxiv.org/abs/2607.08983) | arXiv 2026<br>preprint | Claude Code | Automated test generation | Contextual-bandit supervisor that selects testing actions from current coverage and testability state<br>`test-feedback` `verifier-loop` | Line coverage improves 32.3% and branch coverage 30.9% over agent-only Gemini CLI; adaptation is also evaluated with Claude Code. | model: unknown<br>budget: unknown<br>evidence: contextual |
<!-- CATALOG:RELATED:END -->

</details>

## Evaluation-only papers

These papers benchmark or diagnose the products without proposing a method intended to outperform them.

<details>
<summary><strong>Open the raw evaluation table</strong></summary>

<!-- CATALOG:EVALUATION:START -->
| System / paper | Venue | Product baseline | Task | What changed | Reported evidence | Controls |
|---|---|---|---|---|---|---|
| **[Bug taxonomy](papers/engineering-pitfalls-2026.md)**<br>[paper](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/12/Engineering-Pitfalls-in-AI-Coding-Tools-An-Empirical-Study-of-Bugs-in-Claude-Code-C) | FSE Industry Track 2026<br>conference | Claude Code<br>Codex CLI | Empirical analysis of product bug reports | Evaluation-only manual taxonomy of functionality, integration, invocation, and command-execution failures<br>`observability` | More than 67% of studied bugs concern functionality; API, integration, and configuration account for 36.9% of root causes. | model: unknown<br>budget: unknown<br>evidence: high |
| **[Terminal-Bench 2.0](papers/terminal-bench-2-2026.md)**<br>[paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/444a3737adaee10d86ad2ef5f74468e6-Paper-Conference.pdf) · [artifact](https://github.com/harbor-framework/terminal-bench-2) | ICLR 2026<br>main | Claude Code (Claude Opus 4.5)<br>Codex CLI (GPT-5.2) | General terminal-agent evaluation | Evaluation-only benchmark with stronger task verification and a neutral terminal scaffold<br>`verifier-loop` | GPT-5.2 with Codex CLI scores 62.9; Claude Opus 4.5 scores 57.8 with Terminus 2 and 52.1 with Claude Code. | model: unknown<br>budget: unknown<br>evidence: high |
| **[BountyBench](papers/bountybench-2025.md)**<br>[paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/faed4276b52ef762879db4142655c699-Abstract-Datasets_and_Benchmarks_Track.html) · [artifact](https://github.com/bountybench/bountybench) | NeurIPS 2025<br>dataset benchmark | Claude Code<br>Codex CLI (o3-high and o4-mini) | Vulnerability detection, exploitation, and patching | Evaluation-only benchmark of offensive and defensive cybersecurity agents<br>`verifier-loop` | Codex o3-high detects 12.5% and patches 90%; Claude Code patches 87.5% and exploits 57.5% in the reported settings. | model: unknown<br>budget: unknown<br>evidence: high |
<!-- CATALOG:EVALUATION:END -->

</details>

## Historical OpenAI Codex model papers

These entries study the pre-CLI OpenAI Codex model and are never mixed with modern Codex CLI results.

<details>
<summary><strong>Open the raw historical-model table</strong></summary>

<!-- CATALOG:HISTORICAL:START -->
| System / paper | Venue | Product baseline | Task | What changed | Reported evidence | Controls |
|---|---|---|---|---|---|---|
| **[TiCoder](papers/ticoder-2022.md)**<br>[paper](https://arxiv.org/abs/2208.05950) · [artifact](https://github.com/microsoft/TiCoder) | AST at ICSE 2022<br>workshop | OpenAI Codex model (OpenAI Codex) | Interactive function-level code generation | Generate tests to formalize user intent, collect lightweight feedback, and rank or prune candidate programs<br>`test-feedback` `verifier-loop` | With one to five simulated user queries, Codex pass@1 gains 22.49 to 37.71 points on MBPP and 24.79 to 53.98 points on HumanEval. | model: same<br>budget: different<br>evidence: high |
<!-- CATALOG:HISTORICAL:END -->

</details>

## Evidence classes

- **Direct comparison** — numeric comparison with the production product.
- **Related method** — product-relevant evidence without a clean product-level head-to-head.
- **Evaluation only** — benchmark, dataset, measurement, or failure analysis.
- **Historical model** — pre-CLI OpenAI Codex research.

Evidence strength and comparison controls are separate fields. A paper can report a strong result while still using a different backbone or budget.

## Reproducible data pipeline

`data/papers.yaml` is the source of truth. One command validates the schema, regenerates both READMEs, exports JSON, builds paper dossiers and research views, checks internal links, runs tests, and lints the scripts:

```bash
python -m pip install -r requirements-dev.txt
make build
make check
```

Generated sections and pages are checked in CI. Hand edits to generated catalog tables fail the build.

## Contributing

The fastest way to help is to [suggest a paper](https://github.com/MicroMilo/awesome-claude-code-codex-papers/issues/new?template=paper.yml) or correct an existing evidence record.

Before submitting a PR, read [CONTRIBUTING.md](CONTRIBUTING.md). Quantitative claims must point to a primary source, and missing model or budget information must stay explicitly `unknown` rather than being guessed.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term priorities are deeper baseline-version audits, weekly candidate discovery, richer artifact coverage, and carefully scoped expansion to additional industrial coding agents.

## Related collections

- [PurCL/ASE](https://github.com/PurCL/ASE) — broad Agentic Software Engineering literature database.
- [EuniAI/awesome-code-agents](https://github.com/EuniAI/awesome-code-agents) — research map of code agents.
- [Awesome Agent Harnesses](https://github.com/NeuraLiying/Awesome-Agent-Harnesses) — harness research and engineering resources.

## Citation and license

If this catalog supports academic work, use [CITATION.cff](CITATION.cff). Code and catalog metadata are available under the [MIT License](LICENSE); paper copyright remains with the original authors and publishers.
