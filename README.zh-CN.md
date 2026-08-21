<p align="center">
  <img src="assets/hero.png" alt="Coding agent 实验经过证据图谱汇入研究论文" width="100%">
</p>

<h1 align="center">Claude Code 与 Codex 研究论文精选</h1>

<p align="center">
  <strong>专门收录评测、分析或超越真实工业 coding agent 的研究。</strong>
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

这是一个以证据为核心的论文库，研究对象是完整的 **Claude Code** 与 **Codex CLI** 产品，而不只是 Claude 或 GPT 系列模型。每篇论文都记录 baseline 配置、任务、新增方法、论文结果、实验控制、风险说明和官方 artifact。

> [!IMPORTANT]
> 这不是排行榜。产品版本、底层模型、预算、工具权限和任务领域经常不同。每项直接结果都链接到独立证据页，明确展示这些差异。

## 从这里开始

| 入口 | 适合查看什么 |
|---|---|
| [全部论文证据页](papers/README.md) | 作者、产品、模型、版本、证据位置和风险说明 |
| [按产品浏览](views/by-product.md) | Claude Code 或 Codex CLI 相关论文 |
| [按方法浏览](views/by-method.md) | 检索、仓库图、验证闭环、多 agent 和 harness 演化 |
| [实验公平性](views/fair-comparisons.md) | 区分严格控制、模型不同和预算不明的实验 |
| [按会议浏览](views/by-venue.md) | 主会、workshop、benchmark track 和预印本 |
| [机器可读数据](data/papers.json) | 二次开发、可视化和下游综述 |

## 这个仓库回答的问题

普通论文列表回答“有哪些论文”，这个仓库重点回答：

> **研究者用 Claude Code 或 Codex CLI 做 baseline 时，增加了什么、提升了什么，以及比较是否公平？**

每个条目都会记录：

- 产品、CLI 版本、底层模型及其在实验中的角色；
- 任务、benchmark 和实验规模；
- 围绕产品 baseline 增加或替换的方法；
- 质量、效率或故障分析结果；
- 是否保持相同模型和相同预算；
- 证据位置、限制条件和 artifact 状态。

## 收录范围

第一阶段只做 **Claude Code** 和 **Codex CLI**。数据结构已经与产品解耦，未来可以自然加入 Kimi Code、Zed、Cursor、Gemini CLI 等工业 coding agent。

收录：

- 产品级直接对比；
- harness、配置、检索、规划和验证方法；
- 包含产品级结果的 benchmark 与实证研究；
- 单独隔离的旧 OpenAI Codex 模型论文。

主列表不收录：

- 只使用厂商模型、没有运行对应产品 agent 的论文；
- 没有研究材料的博客或营销对比；
- 无法追溯到原论文或官方 artifact 的说法。

## 直接对比

这些论文把提出的方法与 Claude Code 或 Codex CLI 做了数值比较。“直接”不代表模型和预算相同，请同时查看可比性字段和论文证据页。

<!-- CATALOG:DIRECT:START -->
| 系统 / 论文 | 会议 | 产品 baseline | 任务 | 新增方法 | 论文结果 | 可比性 |
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

## 反复出现的有效方法

1. **持久化仓库状态**：把计划、架构、依赖和设计知识放到上下文窗口之外。
2. **可执行反馈**：让测试、编译器、静态分析器、渲染器或性能测量判断正确性。
3. **定向检索**：使用专门检索和上下文压缩，减少无关信息。
4. **依赖感知调度**：根据任务图判断哪些步骤可以并行、哪些必须串行。
5. **Harness 可观测性**：让轨迹、组件和决策可检查、可归因、可回滚。
6. **低成本仓库指令**：用精炼的项目级说明减少无效操作和 token。

详见[按方法浏览](views/by-method.md)和[方法分类](docs/taxonomy.md)。

## 相关方法

这些论文包含有用的产品证据，但主要数值可能来自组件实验或其他 agent，不构成严格的 Claude Code/Codex CLI 正面对比。

<!-- CATALOG:RELATED:START -->
| 系统 / 论文 | 会议 | 产品 baseline | 任务 | 新增方法 | 论文结果 | 可比性 |
|---|---|---|---|---|---|---|
| **[CodeGrep](papers/codegrep-2026.md)**<br>[paper](https://arxiv.org/abs/2608.05886) | arXiv 2026<br>preprint | Claude Code (Claude-Code-like agent) | Repository retrieval for issue resolution | GRPO-trained 14B retrieval agent that issues multi-turn parallel grep, glob, and read operations for a frozen downstream coding agent<br>`retrieval` `context-reduction` `parallelism` | Resolve rate 27.0% versus 25.8% without retrieval; resolved tasks use 15% fewer rounds and 19% fewer tokens. | model: same<br>budget: unknown<br>evidence: contextual |
| **[SCATE](papers/scate-2026.md)**<br>[paper](https://arxiv.org/abs/2607.08983) | arXiv 2026<br>preprint | Claude Code | Automated test generation | Contextual-bandit supervisor that selects testing actions from current coverage and testability state<br>`test-feedback` `verifier-loop` | Line coverage improves 32.3% and branch coverage 30.9% over agent-only Gemini CLI; adaptation is also evaluated with Claude Code. | model: unknown<br>budget: unknown<br>evidence: contextual |
<!-- CATALOG:RELATED:END -->

## 仅评测论文

这些论文负责 benchmark、测量或故障分析，没有提出专门超越产品的新方法。

<!-- CATALOG:EVALUATION:START -->
| 系统 / 论文 | 会议 | 产品 baseline | 任务 | 新增方法 | 论文结果 | 可比性 |
|---|---|---|---|---|---|---|
| **[Bug taxonomy](papers/engineering-pitfalls-2026.md)**<br>[paper](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/12/Engineering-Pitfalls-in-AI-Coding-Tools-An-Empirical-Study-of-Bugs-in-Claude-Code-C) | FSE Industry Track 2026<br>conference | Claude Code<br>Codex CLI | Empirical analysis of product bug reports | Evaluation-only manual taxonomy of functionality, integration, invocation, and command-execution failures<br>`observability` | More than 67% of studied bugs concern functionality; API, integration, and configuration account for 36.9% of root causes. | model: unknown<br>budget: unknown<br>evidence: high |
| **[Terminal-Bench 2.0](papers/terminal-bench-2-2026.md)**<br>[paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/444a3737adaee10d86ad2ef5f74468e6-Paper-Conference.pdf) · [artifact](https://github.com/harbor-framework/terminal-bench-2) | ICLR 2026<br>main | Claude Code (Claude Opus 4.5)<br>Codex CLI (GPT-5.2) | General terminal-agent evaluation | Evaluation-only benchmark with stronger task verification and a neutral terminal scaffold<br>`verifier-loop` | GPT-5.2 with Codex CLI scores 62.9; Claude Opus 4.5 scores 57.8 with Terminus 2 and 52.1 with Claude Code. | model: unknown<br>budget: unknown<br>evidence: high |
| **[BountyBench](papers/bountybench-2025.md)**<br>[paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/faed4276b52ef762879db4142655c699-Abstract-Datasets_and_Benchmarks_Track.html) · [artifact](https://github.com/bountybench/bountybench) | NeurIPS 2025<br>dataset benchmark | Claude Code<br>Codex CLI (o3-high and o4-mini) | Vulnerability detection, exploitation, and patching | Evaluation-only benchmark of offensive and defensive cybersecurity agents<br>`verifier-loop` | Codex o3-high detects 12.5% and patches 90%; Claude Code patches 87.5% and exploits 57.5% in the reported settings. | model: unknown<br>budget: unknown<br>evidence: high |
<!-- CATALOG:EVALUATION:END -->

## 旧 OpenAI Codex 模型论文

这些论文研究的是 Codex CLI 出现前的 OpenAI Codex 模型，不与现代 Codex CLI 结果混合。

<!-- CATALOG:HISTORICAL:START -->
| 系统 / 论文 | 会议 | 产品 baseline | 任务 | 新增方法 | 论文结果 | 可比性 |
|---|---|---|---|---|---|---|
| **[TiCoder](papers/ticoder-2022.md)**<br>[paper](https://arxiv.org/abs/2208.05950) · [artifact](https://github.com/microsoft/TiCoder) | AST at ICSE 2022<br>workshop | OpenAI Codex model (OpenAI Codex) | Interactive function-level code generation | Generate tests to formalize user intent, collect lightweight feedback, and rank or prune candidate programs<br>`test-feedback` `verifier-loop` | With one to five simulated user queries, Codex pass@1 gains 22.49 to 37.71 points on MBPP and 24.79 to 53.98 points on HumanEval. | model: same<br>budget: different<br>evidence: high |
<!-- CATALOG:HISTORICAL:END -->

## 数据与自动校验

`data/papers.yaml` 是唯一数据源。构建流程会校验 Schema、生成中英文 README、导出 JSON、生成每篇论文的证据页和研究视图，并检查内部链接、执行测试与 lint：

```bash
python -m pip install -r requirements-dev.txt
make build
make check
```

## 参与贡献

可以直接[推荐论文](https://github.com/MicroMilo/awesome-claude-code-codex-papers/issues/new?template=paper.yml)，也可以修正现有证据记录。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。定量结果必须指向一手来源；论文没写清模型或预算时，应保留为 `unknown`，不能自行猜测。

## 路线图、引用与许可

- 后续计划见 [ROADMAP.md](ROADMAP.md)。
- 学术引用信息见 [CITATION.cff](CITATION.cff)。
- 代码和目录元数据使用 [MIT License](LICENSE)，论文版权属于原作者与出版方。
