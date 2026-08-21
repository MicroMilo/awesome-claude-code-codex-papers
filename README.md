# Awesome Claude Code & Codex Papers

> Research papers that evaluate, analyze, or improve **Claude Code** and **Codex CLI**.

This is an evidence-first catalog of research on production coding agents. It records not only which papers mention an agent, but also the exact baseline role, task, method, reported result, experimental controls, and reproducibility artifacts.

The initial scope is intentionally narrow: **Claude Code** and **Codex CLI**. The schema is product-agnostic so future releases can add Kimi Code, Zed, Cursor, Gemini CLI, and other industrial coding agents without changing the data model.

## Why this catalog exists

Broad agent-paper lists answer “what has been published?” This catalog focuses on a more operational question:

> When researchers evaluate or outperform a production coding agent, what did they add, what exactly improved, and was the comparison fair?

Each entry is reviewed for:

- the product and model used as the baseline;
- the task, benchmark, and resource budget;
- the method added around or instead of the baseline;
- the reported metric and result;
- same-model and same-budget comparability;
- paper, code, data, and reproduction links.

## Scope

Included:

- papers that directly run Claude Code or Codex CLI;
- papers that improve, wrap, configure, or compare their agent harnesses;
- benchmarks and empirical studies that report product-level results;
- older OpenAI Codex model papers, clearly separated from Codex CLI.

Not included in the primary catalog:

- papers that only use a Claude or GPT model without the corresponding product agent;
- blog posts or product comparisons without a research artifact;
- claims that cannot be traced to a paper or official artifact.

## Evidence classes

- **Direct comparison** — the proposed method is numerically compared with Claude Code or Codex CLI.
- **Related method** — the product is discussed or partially used, but the key numeric comparison is not a clean product-level head-to-head.
- **Evaluation only** — the paper evaluates the product without proposing a method intended to beat it.
- **Historical model** — the paper studies the pre-CLI OpenAI Codex model.

## Direct comparisons

<!-- CATALOG:DIRECT:START -->
| Paper | Venue | Product baseline | Task / benchmark | Method | Reported result | Controls |
|---|---|---|---|---|---|---|
| [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](https://arxiv.org/abs/2604.25850) | arXiv 2026<br>preprint | Codex CLI | Automatic evolution of coding-agent harnesses<br>Terminal-Bench 2 and SWE-bench Verified | Closed-loop harness evolution using component, trajectory, and decision observability with evidence-backed edits and rollback<br>`harness-evolution` `observability` `memory` `verifier-loop` | Terminal-Bench 2 pass@1 improves from 69.7 to 77.0, above a human-designed Codex-CLI harness at 71.9; transfer uses 12% fewer tokens on SWE-bench Verified. | model: unknown<br>budget: unknown<br>evidence: medium |
| [Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing](https://arxiv.org/abs/2512.09882)<br>[artifact](https://github.com/Stanford-Trinity/ARTEMIS) | ICLR 2026<br>main | Claude Code (Claude Sonnet 4)<br>Codex CLI (GPT-5) | Long-horizon penetration testing in a live enterprise network<br>Approximately 8,000 hosts across 12 subnets | Supervisor with dynamic expert agents, recursive task decomposition, parallel exploration, context management, triage, and reporting<br>`multi-agent` `dynamic-specialization` `parallelism` `memory` `verifier-loop` | ARTEMIS found 9 valid vulnerabilities with an 82% valid-submission rate, ranked second overall, and outperformed 9 of 10 human participants. | model: unknown<br>budget: different<br>evidence: medium |
| [FormAct: Agentic Source Editing for Rich-Format Document Generation](https://openreview.net/forum?id=n7Ta0YEcgw) | ICML 2026<br>main | Codex CLI | Rich-format document generation and editing<br>RichDocBench and RichDocFuzz | HTML source editor, template retrieval, rendered-page review agent, iterative refinement, and edit-triggered context compression<br>`retrieval` `context-reduction` `verifier-loop` `visual-review` | Render correctness 4.81 versus 4.39 for multi-pass Codex; human rank-1 rate 0.760 versus 0.140. | model: unknown<br>budget: unknown<br>evidence: high |
| [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://conf.researchr.org/details/icse-2026/jaws-2026-papers/31/On-the-Impact-of-AGENTS-md-Files-on-the-Efficiency-of-AI-Coding-Agents) | ICSE JAWs 2026<br>workshop | Claude Code<br>Codex CLI | Real pull-request tasks with and without repository instructions<br>10 repositories and 124 pull requests | Persistent repository-level build, test, style, and directory guidance in AGENTS.md<br>`repository-instructions` `structured-state` `context-reduction` | Median runtime falls 28.64% and output tokens fall 16.58% with comparable completion behavior. | model: same<br>budget: same<br>evidence: high |
| [Prefactory: Automated Discovery and Application of Library-Adoption Refactorings](https://arxiv.org/abs/2607.17211) | arXiv 2026<br>preprint | Codex CLI | Discovery and application of library-adoption refactorings<br>PrefactoryBench | LLM-synthesized lexical and structural search heuristics, deterministic candidate ranking, targeted refactoring, and differential tests<br>`deterministic-search` `static-analysis` `test-feedback` `verifier-loop` | File-level detection 75 versus Codex 35; function-level detection 56 versus 32; 40 of 56 candidates yield test-validated refactorings. | model: unknown<br>budget: unknown<br>evidence: medium |
| [QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html) | ICLR 2026<br>main | Claude Code | CodeQL query synthesis from CVE metadata<br>176 CVEs across 111 Java projects | CVE-grounded retrieval, AST guidance, CodeQL LSP tools, and iterative execution feedback<br>`retrieval` `verifier-loop` `static-analysis` | Correct-query rate 53.4% versus 10% for Claude Code-only; F1 0.70 versus 0.048 for IRIS and 0.073 for CodeQL suites. | model: unknown<br>budget: unknown<br>evidence: high |
| [RepoOMP: Repository-Aware Hotspot OpenMP Parallelization via Dependency-Aware Context Reduction](https://arxiv.org/abs/2608.05855)<br>[artifact](https://github.com/Qlalq/RepoOMP_Simplified) | arXiv 2026<br>preprint | Claude Code | Repository-aware OpenMP hotspot parallelization<br>951 hotspots including 330 accepted real-world hotspots | Multi-granularity dependency graph, rule-or-LLM hotspot routing, reduced transformation context, and compile/workload/speedup validation<br>`repository-graph` `context-reduction` `deterministic-search` `performance-feedback` `verifier-loop` | Across nine detailed kernels, speedup improves 18% to 28% and token cost falls 47% to 68% relative to unstructured Claude Code. | model: unknown<br>budget: unknown<br>evidence: medium |
| [RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation](https://proceedings.iclr.cc/paper_files/paper/2026/file/9482f45fdd89aba9130bb04c44f788a9-Paper-Conference.pdf)<br>[artifact](https://github.com/microsoft/RPG-ZeroRepo) | ICLR 2026<br>main | Claude Code (Claude 4 Sonnet)<br>Codex CLI (o3-pro) | Repository-level codebase generation<br>RepoCraft | Persistent graph over features, functions, files, interfaces, and data flow with graph-guided generation and validation<br>`structured-state` `repository-graph` `dependency-aware-planning` `test-feedback` | ZeroRepo coverage 81.5% versus Claude Code 54.2% and Codex 28.4%; pass rate 69.7% versus Claude Code 33.9%. | model: different<br>budget: unknown<br>evidence: high |
| [RustPrint: Documentation-Guided Agentic Codebase Migration from C to Rust](https://arxiv.org/abs/2605.14634) | arXiv 2026<br>preprint | Claude Code | Whole-codebase migration from C to Rust<br>Eight real C repositories from 11K to 84K lines of code | Architecture documentation blueprint, module and data-flow planning, compile feedback, documentation mismatch repair, and source-test translation<br>`structured-state` `dependency-aware-planning` `verifier-loop` `test-feedback` | In the reported Kimi-K2-Instruct setting, feature preservation is 93.26% versus 52.52% for agentic Claude Code; cross-evaluation test pass is 95.17% versus 79.85%. | model: different<br>budget: unknown<br>evidence: medium |
| [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](https://arxiv.org/abs/2606.25514) | arXiv 2026<br>preprint | Claude Code | Repository issue resolution<br>SWE-bench Verified and SWE-bench Pro | Event-based agent communication, issue-quality routing, parallel patching and validation, and exploratory fallback<br>`multi-agent` `dynamic-specialization` `parallelism` `test-feedback` | SWE-bench Verified improves 3.6 to 8.4 percentage points and SWE-bench Pro 6.3 to 18.5 points; average cost is $1.18 lower than multi-agent Claude Code. | model: unknown<br>budget: unknown<br>evidence: medium |
| [WebDesignIter: Co-Evolving Design Knowledge for Repository-Level Front-End Code Generation](https://arxiv.org/abs/2607.10621) | arXiv 2026<br>preprint | Claude Code<br>Codex CLI | Repository-level front-end code generation<br>Web-Bench | Persistent architecture and design knowledge graph, design-informed planning, targeted patches, and sandbox repair<br>`structured-state` `repository-graph` `retrieval` `test-feedback` | Average Pass@2 improves by 9.55 percentage points over existing baselines; removing design knowledge reduces Pass@1 by 11.4 points. | model: unknown<br>budget: unknown<br>evidence: medium |
| [When Parallelism Pays Off: Cohesion-Aware Task Partitioning for Multi-Agent Coding](https://arxiv.org/abs/2606.00953) | arXiv 2026<br>preprint | Claude Code (Agent Teams) | Parallel multi-agent coding<br>28 DevEval and CodeProjectEval tasks | Static dependency graph partitioning, structural hub isolation, community detection, and dependency-aware scheduling<br>`repository-graph` `dependency-aware-planning` `multi-agent` `parallelism` | Pass rate improves 14.0%, wall-clock speedup reaches 2.10x, and API cost falls 35% relative to Claude Code Agent Teams and simpler schedules. | model: unknown<br>budget: unknown<br>evidence: medium |
| [MLZero: A Multi-Agent System for End-to-end Machine Learning Automation](https://papers.neurips.cc/paper_files/paper/2025/hash/63ed15a46a143ff57484b38cd6b85d91-Abstract-Conference.html)<br>[artifact](https://github.com/autogluon/autogluon-assistant) | NeurIPS 2025<br>main | Codex CLI (GPT-4.1 and o4-mini) | End-to-end machine learning automation<br>MLE-Bench Lite and Multimodal AutoML Agent Benchmark | Hierarchical agents with multimodal perception, semantic and episodic memory, and a planning-coding-evaluation loop<br>`multi-agent` `memory` `verifier-loop` `test-feedback` | MLZero led MLE-Bench Lite with six gold medals and achieved 0.92 success on its multimodal benchmark; one appendix setting reports 6.5% errors versus 26.9% for Codex CLI. | model: unknown<br>budget: unknown<br>evidence: medium |
<!-- CATALOG:DIRECT:END -->

## Related methods

<!-- CATALOG:RELATED:START -->
| Paper | Venue | Product baseline | Task / benchmark | Method | Reported result | Controls |
|---|---|---|---|---|---|---|
| [CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents](https://arxiv.org/abs/2608.05886) | arXiv 2026<br>preprint | Claude Code (Claude-Code-like agent) | Repository retrieval for issue resolution<br>SWE-bench Verified | GRPO-trained 14B retrieval agent that issues multi-turn parallel grep, glob, and read operations for a frozen downstream coding agent<br>`retrieval` `context-reduction` `parallelism` | Resolve rate 27.0% versus 25.8% without retrieval; resolved tasks use 15% fewer rounds and 19% fewer tokens. | model: same<br>budget: unknown<br>evidence: contextual |
| [SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation](https://arxiv.org/abs/2607.08983) | arXiv 2026<br>preprint | Claude Code | Automated test generation<br>Repository-level test-generation benchmark | Contextual-bandit supervisor that selects testing actions from current coverage and testability state<br>`test-feedback` `verifier-loop` | Line coverage improves 32.3% and branch coverage 30.9% over agent-only Gemini CLI; adaptation is also evaluated with Claude Code. | model: unknown<br>budget: unknown<br>evidence: contextual |
<!-- CATALOG:RELATED:END -->

## Evaluation-only papers

<!-- CATALOG:EVALUATION:START -->
| Paper | Venue | Product baseline | Task / benchmark | Method | Reported result | Controls |
|---|---|---|---|---|---|---|
| [Engineering Pitfalls in AI Coding Tools: An Empirical Study of Bugs in Claude Code, Codex, and Gemini CLI](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/12/Engineering-Pitfalls-in-AI-Coding-Tools-An-Empirical-Study-of-Bugs-in-Claude-Code-C) | FSE Industry Track 2026<br>conference | Claude Code<br>Codex CLI | Empirical analysis of product bug reports<br>More than 3,800 reported bugs | Evaluation-only manual taxonomy of functionality, integration, invocation, and command-execution failures<br>`observability` | More than 67% of studied bugs concern functionality; API, integration, and configuration account for 36.9% of root causes. | model: unknown<br>budget: unknown<br>evidence: high |
| [Terminal-Bench 2.0: Advancing Agentic Terminal Intelligence through Better Evaluation and Verification](https://proceedings.iclr.cc/paper_files/paper/2026/file/444a3737adaee10d86ad2ef5f74468e6-Paper-Conference.pdf) | ICLR 2026<br>main | Claude Code (Claude Opus 4.5)<br>Codex CLI (GPT-5.2) | General terminal-agent evaluation<br>Terminal-Bench 2.0 | Evaluation-only benchmark with stronger task verification and a neutral terminal scaffold<br>`verifier-loop` | GPT-5.2 with Codex CLI scores 62.9; Claude Opus 4.5 scores 57.8 with Terminus 2 and 52.1 with Claude Code. | model: unknown<br>budget: unknown<br>evidence: high |
| [BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems](https://proceedings.neurips.cc/paper_files/paper/2025/hash/faed4276b52ef762879db4142655c699-Abstract-Datasets_and_Benchmarks_Track.html) | NeurIPS 2025<br>dataset benchmark | Claude Code<br>Codex CLI (o3-high and o4-mini) | Vulnerability detection, exploitation, and patching<br>BountyBench | Evaluation-only benchmark of offensive and defensive cybersecurity agents<br>`verifier-loop` | Codex o3-high detects 12.5% and patches 90%; Claude Code patches 87.5% and exploits 57.5% in the reported settings. | model: unknown<br>budget: unknown<br>evidence: high |
<!-- CATALOG:EVALUATION:END -->

## Historical OpenAI Codex model papers

<!-- CATALOG:HISTORICAL:START -->
| Paper | Venue | Product baseline | Task / benchmark | Method | Reported result | Controls |
|---|---|---|---|---|---|---|
| [Interactive Code Generation via Test-Driven User-Intent Formalization](https://arxiv.org/abs/2208.05950)<br>[artifact](https://github.com/microsoft/TiCoder) | AST at ICSE 2022<br>workshop | OpenAI Codex model (OpenAI Codex) | Interactive function-level code generation<br>MBPP and HumanEval | Generate tests to formalize user intent, collect lightweight feedback, and rank or prune candidate programs<br>`test-feedback` `verifier-loop` | With one to five simulated user queries, Codex pass@1 gains 22.49 to 37.71 points on MBPP and 24.79 to 53.98 points on HumanEval. | model: same<br>budget: different<br>evidence: high |
<!-- CATALOG:HISTORICAL:END -->

## Method taxonomy

The catalog currently tracks these recurring ways of improving coding agents:

- persistent structured state and repository graphs;
- retrieval and context reduction;
- executable verification and feedback loops;
- dependency-aware planning and parallelism;
- multi-agent coordination and specialization;
- harness observability and self-improvement;
- repository-level instructions and configuration;
- deterministic search or analysis before LLM invocation.

See [docs/taxonomy.md](docs/taxonomy.md) for definitions.

## Data and validation

`data/papers.yaml` is the source of truth. The JSON Schema and project checks validate required metadata, unique identifiers, supported products, evidence classes, and comparison fields.

```bash
python -m pip install -r requirements-dev.txt
make check
```

To regenerate the tables after editing the catalog:

```bash
make build
```

## Contributing

Paper suggestions and corrections are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), then open the paper-submission issue template or submit a pull request that updates `data/papers.yaml`.

Please link to official paper and artifact pages. Do not upload or redistribute paper PDFs in this repository.

## Related collections

- [PurCL/ASE](https://github.com/PurCL/ASE) — a broad Agentic Software Engineering literature database.
- [EuniAI/awesome-code-agents](https://github.com/EuniAI/awesome-code-agents) — a research map of code agents.
- [Awesome Agent Harnesses](https://github.com/NeuraLiying/Awesome-Agent-Harnesses) — papers and engineering resources about agent harnesses.

## License

Code and catalog metadata are available under the [MIT License](LICENSE). Copyright remains with the original paper authors and publishers.
