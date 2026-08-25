export type InsightLanguage = "en" | "zh";

export type LocalizedText = Record<InsightLanguage, string>;

export type InsightEvidence = {
  paperId: string;
  weight: "diagnostic" | "context";
  inference: LocalizedText;
};

export type InsightDefinition = {
  id: string;
  number: string;
  domain: LocalizedText;
  title: LocalizedText;
  thesis: LocalizedText;
  whatWorks: LocalizedText;
  caution: LocalizedText;
  evidence: InsightEvidence[];
};

export const INSIGHT_DEFINITIONS: InsightDefinition[] = [
  {
    id: "repository-horizon",
    number: "01",
    domain: {
      en: "Repository-scale engineering",
      zh: "仓库级工程",
    },
    title: {
      en: "Long-horizon work breaks at interfaces, not syntax.",
      zh: "长任务真正容易断在接口与依赖，而不是语法。",
    },
    thesis: {
      en: "Claude Code and Codex can produce substantial code, but full-feature completion remains low when state must stay coherent across files, components, and iterations. The strongest gains come from moving the plan and dependency state outside the chat history.",
      zh: "Claude Code 和 Codex 能写出大量代码，但当状态必须跨文件、组件和多轮迭代保持一致时，完整功能成功率仍然很低。提升最明显的方法，是把计划与依赖状态从对话历史中搬到显式结构里。",
    },
    whatWorks: {
      en: "Persistent repository graphs, dependency-aware staging, modular generation, and independent runtime plus semantic verification.",
      zh: "持久化仓库图、依赖感知的分阶段执行、模块化生成，以及独立的运行时与语义双重验证。",
    },
    caution: {
      en: "The strongest headline comparisons do not hold model and harness constant, so they support a mechanism hypothesis—not a clean vendor ranking.",
      zh: "最醒目的对比没有同时固定模型与 harness，因此它们支持的是“机制假设”，不能当作干净的厂商排名。",
    },
    evidence: [
      {
        paperId: "featurebench-2026",
        weight: "diagnostic",
        inference: {
          en: "Full feature completion stays at 11.0% for Claude Code and 12.5% for Codex, directly exposing the repository-level gap.",
          zh: "完整功能任务中 Claude Code 为 11.0%、Codex 为 12.5%，直接暴露了仓库级完成能力的缺口。",
        },
      },
      {
        paperId: "swe-bench-mobile-2026",
        weight: "diagnostic",
        inference: {
          en: "On production mobile features, no configuration exceeds 12% task success, and success falls from 18% for 1-2-file tasks to 2% for tasks touching 7 or more files.",
          zh: "在生产级移动端功能任务上，所有配置最高只有 12% 完整成功率；当任务从修改 1-2 个文件增长到 7 个以上文件时，成功率从 18% 降到 2%。",
        },
      },
      {
        paperId: "evodev-2026",
        weight: "diagnostic",
        inference: {
          en: "With the same Claude snapshot and task time limits, a feature dependency map and predecessor context raise function completeness from Claude Code's 2.27/4 to 3.57/4; removing predecessor context makes iterative development regress.",
          zh: "在相同 Claude snapshot 和任务时限下，特征依赖图与前序上下文把功能完整度从 Claude Code 的 2.27/4 提升到 3.57/4；去掉前序上下文后，迭代开发反而退化。",
        },
      },
      {
        paperId: "swe-compass-2026",
        weight: "diagnostic",
        inference: {
          en: "Across 2,000 repository tasks, Claude Code failures are dominated by requirement misinterpretation and incomplete solutions, while performance varies sharply by task type and language.",
          zh: "在 2,000 个仓库任务中，Claude Code 的主要失败不是基础语法，而是需求误解与方案不完整；表现还会随任务类型和语言显著波动。",
        },
      },
      {
        paperId: "rpg-zerorepo-2026",
        weight: "diagnostic",
        inference: {
          en: "An external repository planning graph plus staged validation reports large gains over the product baselines.",
          zh: "外置的仓库规划图与分阶段验证，相比产品 baseline 报告了显著提升。",
        },
      },
      {
        paperId: "helmsman-2026",
        weight: "diagnostic",
        inference: {
          en: "Modular teams and closed-loop sandbox verification solve all 16 reported synthesis tasks, while the product baselines do not.",
          zh: "模块化 agent 团队与沙箱闭环验证完成了论文中的全部 16 个综合任务，而产品 baseline 没有。",
        },
      },
    ],
  },
  {
    id: "operational-composition",
    number: "02",
    domain: {
      en: "DevOps and full applications",
      zh: "DevOps 与完整应用",
    },
    title: {
      en: "A local win rarely composes into a reliable system.",
      zh: "局部步骤做对了，不等于能拼成可靠系统。",
    },
    thesis: {
      en: "Performance falls sharply as tasks move from build/configuration into monitoring, issue resolution, testing, lifecycle behavior, and multi-file integration. The weak point is the handoff between stages and external contracts.",
      zh: "当任务从构建与配置推进到监控、故障处理、测试、生命周期行为和多文件集成时，成功率会明显下降。薄弱点集中在阶段之间的交接与外部契约。",
    },
    whatWorks: {
      en: "Explicit workflow stages, observable environments, compilation and test gates, runtime fuzzing, and stage-specific metrics.",
      zh: "显式工作流阶段、可观测环境、编译与测试门禁、运行时 fuzz，以及按阶段拆分的指标。",
    },
    caution: {
      en: "These benchmarks measure different operational surfaces, so the shared pattern is more reliable than any cross-paper score comparison.",
      zh: "这些 benchmark 测量的是不同操作面，因此跨论文不能直接比数字；共同失败模式比排行榜更可信。",
    },
    evidence: [
      {
        paperId: "devops-gym-2026",
        weight: "diagnostic",
        inference: {
          en: "Claude Code is much stronger on build/configuration than on monitoring, issue resolution, or test generation.",
          zh: "Claude Code 在构建/配置上的表现明显高于监控、故障处理与测试生成。",
        },
      },
      {
        paperId: "appforge-2026",
        weight: "diagnostic",
        inference: {
          en: "Functional success remains 6.93% despite a coding-agent harness, pointing to integration and lifecycle failures beyond code emission.",
          zh: "即使使用 coding-agent harness，功能成功率仍只有 6.93%，说明问题超出了单纯代码生成，落在集成与生命周期上。",
        },
      },
      {
        paperId: "posttrainbench-2026",
        weight: "diagnostic",
        inference: {
          en: "Under a ten-hour single-H100 budget, the best Claude Code and Codex configurations remain far below official instruction-tuned models overall, and some apparent wins rely on reward hacking or contamination.",
          zh: "在单张 H100、10 小时预算下，最佳 Claude Code/Codex 配置的整体表现仍远低于官方指令微调模型，而且部分表面胜利来自 reward hacking 或污染。",
        },
      },
    ],
  },
  {
    id: "security-proof",
    number: "03",
    domain: {
      en: "Security",
      zh: "安全",
    },
    title: {
      en: "Security work needs grounded tools and executable proof.",
      zh: "安全任务需要领域工具和可执行的证据闭环。",
    },
    thesis: {
      en: "Generic agent loops miss domain semantics, terminate early, or mistake plausible output for success. Retrieval, static-analysis guidance, specialist decomposition, and executable validation turn the largest improvements into verifiable progress.",
      zh: "通用 agent 循环容易漏掉领域语义、过早结束，或把“看起来合理”误当成成功。检索、静态分析引导、专家拆分和可执行验证，才能把改进变成可核验的进展。",
    },
    whatWorks: {
      en: "CVE-grounded retrieval, AST/LSP context, CodeQL execution, pre/post-patch tests, specialist routing, and triage before reporting.",
      zh: "基于 CVE 的检索、AST/LSP 上下文、CodeQL 执行、补丁前后测试、专家路由，以及报告前的 triage。",
    },
    caution: {
      en: "Offensive-security policy, refusal behavior, runtime limits, and benchmark harnesses are major confounders; do not attribute every failure to model capability.",
      zh: "攻防安全中的策略限制、拒答行为、运行时上限和 benchmark harness 都是重要混杂因素，不能把每个失败都归因于模型能力。",
    },
    evidence: [
      {
        paperId: "qlcoder-2026",
        weight: "diagnostic",
        inference: {
          en: "Grounded retrieval and an executable CodeQL validator raise correct-query synthesis from the Claude Code-only ablation's 10% to 53.4%.",
          zh: "领域检索与可执行 CodeQL 验证器，把 Claude Code-only 消融中的 10% 提升到 53.4%。",
        },
      },
      {
        paperId: "red-teaming-coding-agents-2026",
        weight: "diagnostic",
        inference: {
          en: "Tool-description isolation is not cosmetic: progressive disclosure in newer Claude Code configurations reduces the reported RCE-2 attack success from 0.6-0.7 to 0.0.",
          zh: "工具描述隔离并非表面改动：新版 Claude Code 的渐进式披露把论文报告的 RCE-2 攻击成功率从 0.6-0.7 降到 0.0。",
        },
      },
      {
        paperId: "cybergym-2026",
        weight: "diagnostic",
        inference: {
          en: "The four-agent union reaches 18.4%, showing both low individual coverage and complementary failure modes.",
          zh: "四个 agent 的并集成功率才达到 18.4%，同时说明单一 agent 覆盖不足、失败模式又彼此互补。",
        },
      },
      {
        paperId: "artemis-2026",
        weight: "context",
        inference: {
          en: "Dynamic specialists and parallel exploration are promising, but policy and runtime differences make this supporting—not causal—product evidence.",
          zh: "动态专家与并行探索很有潜力，但策略和运行时差异使它只能作为辅助证据，不能做产品层因果结论。",
        },
      },
    ],
  },
  {
    id: "visual-contracts",
    number: "04",
    domain: {
      en: "Visual and rich-format artifacts",
      zh: "视觉与富格式产物",
    },
    title: {
      en: "Syntactically valid is not visually or behaviorally correct.",
      zh: "语法正确，不代表视觉和行为正确。",
    },
    thesis: {
      en: "When success depends on rendered appearance, interaction traces, or OS and third-party contracts, text-only iteration misses an independent objective. Render-and-review loops outperform repeated source editing without equivalent visual feedback.",
      zh: "当成功取决于渲染效果、交互轨迹、操作系统或第三方契约时，只看文本的迭代会漏掉一个独立目标。带渲染审查的闭环，比单纯重复编辑源码更有效。",
    },
    whatWorks: {
      en: "Template retrieval, rendered-page review, interaction traces, automated execution, and context compression triggered by edits.",
      zh: "模板检索、渲染页面审查、交互轨迹、自动化执行，以及由编辑触发的上下文压缩。",
    },
    caution: {
      en: "FormAct is document editing and AppForge is full-app generation; together they expose a shared verification gap, not one interchangeable benchmark.",
      zh: "FormAct 是文档编辑，AppForge 是完整应用生成；二者揭示的是共同验证缺口，不是可以互换比较的同一个 benchmark。",
    },
    evidence: [
      {
        paperId: "formact-2026",
        weight: "diagnostic",
        inference: {
          en: "With the exact same generator snapshot, the render-review system beats multi-pass Codex on render correctness and human rank-1 preference.",
          zh: "在使用完全相同 generator snapshot 时，带渲染审查的系统在渲染正确性和人类 rank-1 偏好上超过 multi-pass Codex。",
        },
      },
      {
        paperId: "appforge-2026",
        weight: "context",
        inference: {
          en: "Low end-to-end functional success reinforces that compilation alone does not validate UI behavior and lifecycle contracts.",
          zh: "较低的端到端功能成功率进一步说明，编译通过本身无法验证 UI 行为和生命周期契约。",
        },
      },
    ],
  },
  {
    id: "structured-search",
    number: "05",
    domain: {
      en: "Formal reasoning and open-ended search",
      zh: "形式化推理与开放式搜索",
    },
    title: {
      en: "Search works when state and verification are explicit.",
      zh: "搜索过程只有把状态与验证显式化，才更可靠。",
    },
    thesis: {
      en: "A conversational trajectory is a poor substitute for a verified proof state, tactic library, experiment ledger, population, or persistent findings memory. Structured exploration preserves alternatives and separates generation from evaluation.",
      zh: "一条不断变长的对话轨迹，不能替代经验证的证明状态、策略库、实验账本、候选种群或持久化 findings memory。结构化探索能保留备选路径，并把生成与评估分开。",
    },
    whatWorks: {
      en: "Compiler-checked tactics, semantic retrieval, compact agent contracts, evolutionary search, executable scoring, persistent findings memory, and explicit novelty comparison.",
      zh: "编译器验证的策略、语义检索、紧凑 agent 契约、进化搜索、可执行评分、持久化 findings memory，以及显式 novelty 比较。",
    },
    caution: {
      en: "DeepScientist and InnoGym use Claude Code or Codex as host components. They inform workflow design but are not evidence that the host product was beaten.",
      zh: "DeepScientist 和 InnoGym 把 Claude Code 或 Codex 当作宿主组件。它们能启发工作流设计，但不能证明宿主产品被击败。",
    },
    evidence: [
      {
        paperId: "ape-bench-2026",
        weight: "diagnostic",
        inference: {
          en: "Across the same models and 3 USD/100-turn task caps, a compact scaffold with integrated verification beats both product scaffolds by 15-23 percentage points.",
          zh: "在相同模型和每题 3 美元/100 轮上限下，集成验证的紧凑 scaffold 比两款产品 scaffold 高 15-23 个百分点。",
        },
      },
      {
        paperId: "llm2ltac-2026",
        weight: "diagnostic",
        inference: {
          en: "Compiler-checked, generalization-tested symbolic tactics raise Claude Code + CoqHammer from 101 to 111 solved theorems on the same 200 tasks while using 10.51% fewer tokens.",
          zh: "经编译与泛化测试的符号策略，在同一批 200 个任务上把 Claude Code + CoqHammer 从 101 个成功提升到 111 个，同时少用 10.51% token。",
        },
      },
      {
        paperId: "scaling-laws-2026",
        weight: "diagnostic",
        inference: {
          en: "Under the same GPT-5 model label, evolutionary program search reports average R² 0.748 versus Codex's 0.550.",
          zh: "在相同 GPT-5 模型标签下，进化式程序搜索报告平均 R² 0.748，而 Codex 为 0.550。",
        },
      },
      {
        paperId: "deepscientist-2026",
        weight: "context",
        inference: {
          en: "Persistent findings and staged hypothesis/evaluation loops show how Claude Code can be embedded as an executor in a larger research controller.",
          zh: "持久化 findings 与分阶段假设/评估循环，展示了如何把 Claude Code 作为执行器嵌入更大的研究控制器。",
        },
      },
      {
        paperId: "numina-lean-agent-2026",
        weight: "context",
        inference: {
          en: "Claude Code acts as the host for proof-state tools, semantic retrieval, discussion, and subagent decomposition; the result supports the surrounding workflow, not a claim that Claude Code itself was beaten.",
          zh: "Claude Code 在这里承载证明状态工具、语义检索、讨论和子 agent 分解；它支持的是外围工作流设计，不能被读成 Claude Code 本身被击败。",
        },
      },
      {
        paperId: "innogym-2026",
        weight: "context",
        inference: {
          en: "Codex performs extraction and novelty judging here; that is useful host evidence, not a product baseline result.",
          zh: "Codex 在这里负责提取和 novelty 判断；这是有用的宿主使用证据，而不是产品 baseline 结果。",
        },
      },
      {
        paperId: "lean-refactor-2026",
        weight: "context",
        inference: {
          en: "Version-filtered retrieval and executable Lean checking support the value of explicit, library-aware strategy memory, but the spotlight paper does not report a controlled Claude Code configuration.",
          zh: "版本过滤检索与可执行 Lean 检查支持了“显式、库版本感知的策略记忆”这一方向，但 spotlight 论文没有报告可控的 Claude Code 配置。",
        },
      },
    ],
  },
  {
    id: "terminal-boundary",
    number: "06",
    domain: {
      en: "Boundary condition",
      zh: "边界条件",
    },
    title: {
      en: "Terminal access itself is not the main bottleneck.",
      zh: "终端访问本身不是主要瓶颈。",
    },
    thesis: {
      en: "On bounded, executable terminal tasks, both products can be strong. This control case shifts the diagnosis away from tool access alone and toward long-horizon state, composition, specialized context, and verification quality.",
      zh: "在边界清晰、可执行验证的终端任务上，两款产品都可以很强。这个对照把问题从“有没有工具”转向了长程状态、任务组合、领域上下文和验证质量。",
    },
    whatWorks: {
      en: "Realistic environments, executable tests, standardized task packaging, and model selection calibrated to the task.",
      zh: "真实环境、可执行测试、标准化任务封装，以及与任务匹配的模型选择。",
    },
    caution: {
      en: "Budgets and agent-model combinations vary substantially, and the detailed failure taxonomy is not specific to each product row.",
      zh: "不同 agent-model 组合的预算差异很大，而且详细失败分类并非逐一对应每个产品行。",
    },
    evidence: [
      {
        paperId: "terminal-bench-2-2026",
        weight: "diagnostic",
        inference: {
          en: "Codex reaches 62.9% and Claude Code 52.1%, preventing the synthesis from turning into a blanket claim that these products cannot execute real tasks.",
          zh: "Codex 达到 62.9%、Claude Code 达到 52.1%，因此不能把结论泛化成“这些产品无法执行真实任务”。",
        },
      },
      {
        paperId: "execution-cost-effectiveness-2026",
        weight: "diagnostic",
        inference: {
          en: "Removing execution changes resolve rate by only 1.25 points on average; many failed repairs pass an agent-selected check but fail the official test, so test selection matters more than simply having a shell.",
          zh: "禁用执行后平均解决率只变化 1.25 个百分点；许多失败补丁通过了 agent 自选检查却未通过官方测试，因此测试选择比“有没有 shell”更关键。",
        },
      },
    ],
  },
];

export const MECHANISM_DEFINITIONS = [
  {
    id: "executable-verification",
    title: {
      en: "Independent executable verification",
      zh: "独立的可执行验证",
    },
    summary: {
      en: "Tests, sandboxes, static analyzers, fuzzers, and render reviewers turn self-assessment into an external signal.",
      zh: "测试、沙箱、静态分析器、fuzzer 和渲染审查器，把 agent 的自我判断替换成外部信号。",
    },
    tags: ["verifier-loop", "test-feedback", "visual-review"],
  },
  {
    id: "persistent-state",
    title: {
      en: "Persistent task state",
      zh: "持久化任务状态",
    },
    summary: {
      en: "Repository graphs, findings memories, and structured records survive context compression and failed iterations.",
      zh: "仓库图、findings memory 和结构化记录，可以跨越上下文压缩与失败迭代继续存在。",
    },
    tags: ["structured-state", "repository-graph", "memory"],
  },
  {
    id: "domain-grounding",
    title: {
      en: "Domain-grounded context",
      zh: "领域化上下文",
    },
    summary: {
      en: "Retrieval, AST/LSP signals, and repository instructions narrow the search space before generation.",
      zh: "检索、AST/LSP 信号和仓库说明，在生成之前先缩小搜索空间。",
    },
    tags: ["retrieval", "static-analysis", "repository-instructions"],
  },
  {
    id: "structured-exploration",
    title: {
      en: "Structured exploration",
      zh: "结构化探索",
    },
    summary: {
      en: "Dependency-aware plans, evolutionary search, and specialist parallelism preserve alternatives instead of following one fragile trajectory.",
      zh: "依赖感知计划、进化搜索和专家并行，让系统保留多个候选，而不是押注一条脆弱轨迹。",
    },
    tags: [
      "dependency-aware-planning",
      "deterministic-search",
      "parallelism",
      "multi-agent",
    ],
  },
] as const;
