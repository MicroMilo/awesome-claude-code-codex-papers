import { useEffect, useMemo, useRef, useState } from "react";

type ProductId = "claude-code" | "codex-cli";
type Classification = "direct" | "related" | "evaluation";
type EvidenceStrength = "high" | "medium" | "contextual";
type Language = "en" | "zh";
type ConferenceId =
  | "AAAI"
  | "ASE"
  | "FSE"
  | "ICLR"
  | "ICML"
  | "ICSE"
  | "ISSTA"
  | "NeurIPS"
  | "IJCAI"
  | "KDD"
  | "PLDI"
  | "POPL"
  | "OOPSLA";
type DomainId =
  | "software-engineering"
  | "security"
  | "systems-performance"
  | "machine-learning"
  | "scientific-computing"
  | "formal-methods"
  | "web-ui"
  | "documents";

export type Paper = {
  id: string;
  title: string;
  authors: string[];
  year: number;
  year_tag: 2026;
  conference: ConferenceId;
  conference_tag: ConferenceId;
  venue: string;
  domains: DomainId[];
  publication_status: string;
  classification: Classification;
  system: string;
  paper_url: string;
  source_type: string;
  audit_status: "included";
  artifact_url?: string;
  artifact_status: "official" | "community" | "not-found";
  doi?: string;
  published_at?: string;
  products: Array<{
    product: ProductId;
    role: string;
    model: string;
    version: string;
    reasoning_mode?: string;
    temperature?: string;
    max_output_tokens?: string;
    budget?: string;
    runs?: string;
    tool_permissions?: string;
  }>;
  task: { summary: string; benchmark: string };
  experiment: {
    reasoning_mode: string;
    temperature: string;
    max_output_tokens: string;
    time_budget: string;
    turn_budget: string;
    token_budget: string;
    api_budget: string;
    runs: string;
    tool_permissions: string;
    baseline_config: string;
  };
  method: { summary: string; tags: string[] };
  evidence: {
    result: string;
    strength: EvidenceStrength;
    same_model: "yes" | "no" | "unknown";
    same_budget: "yes" | "no" | "unknown";
    claim_type: string;
    comparison_scope: string;
    source_location: string;
    caveats: string;
  };
};

const REPOSITORY_URL =
  "https://github.com/MicroMilo/awesome-claude-code-codex-papers";

const PRODUCT_LABELS: Record<ProductId, string> = {
  "claude-code": "Claude Code",
  "codex-cli": "Codex CLI",
};

const DOMAIN_LABELS: Record<Language, Record<DomainId, string>> = {
  en: {
    "software-engineering": "Software Engineering",
    security: "Security",
    "systems-performance": "Systems & Performance",
    "machine-learning": "Machine Learning",
    "scientific-computing": "Scientific Computing",
    "formal-methods": "Formal Methods",
    "web-ui": "Web & UI",
    documents: "Documents",
  },
  zh: {
    "software-engineering": "软件工程",
    security: "安全",
    "systems-performance": "系统与性能",
    "machine-learning": "机器学习",
    "scientific-computing": "科学计算",
    "formal-methods": "形式化方法",
    "web-ui": "Web 与 UI",
    documents: "文档",
  },
};

const CONFERENCE_ORDER: ConferenceId[] = [
  "AAAI",
  "ASE",
  "FSE",
  "ICLR",
  "ICML",
  "ICSE",
  "ISSTA",
  "NeurIPS",
  "IJCAI",
  "KDD",
  "PLDI",
  "POPL",
  "OOPSLA",
];

const DOMAIN_ORDER = Object.keys(DOMAIN_LABELS.en) as DomainId[];

const copy = {
  en: {
    papers: "Papers",
    coverage: "Coverage",
    methods: "Patterns",
    insights: "Insights",
    star: "Star on GitHub ↗",
    eyebrow: "Evidence, not leaderboard hype",
    heroLead: "What actually beats",
    heroAccent: "Claude Code & Codex?",
    heroDeck:
      "A readable research index for the models, methods, results, and caveats behind production coding-agent comparisons.",
    explore: "Explore the evidence ↓",
    readInsights: "Read the synthesis →",
    reviewed: "Last reviewed",
    reviewedPapers: "reviewed papers",
    directComparisons: "direct comparisons",
    officialArtifacts: "official artifacts",
    researchDomains: "research domains",
    coverageEyebrow: "What the catalog covers",
    coverageTitle: "Choose a domain or conference before opening a paper.",
    coverageDeck:
      "Every entry uses a standardized domain and conference label, while preserving the exact venue in its evidence record.",
    domains: "Research domains",
    conferences: "Conferences / sources",
    catalogEyebrow: "Research catalog",
    catalogTitle: "See the model and result before opening the details.",
    search: "Search systems, tasks, methods…",
    product: "Product",
    modelsUsed: "Models used",
    evidenceClass: "Evidence class",
    evidenceStrength: "Evidence strength",
    conference: "Conference / source",
    year: "Year",
    modelFilter: "Model",
    exactVenue: "Exact venue",
    method: "Method",
    all: "All",
    direct: "Direct",
    related: "Related",
    evaluation: "Evaluation",
    clear: "Clear filters",
    results: "matching papers",
    noResults: "No paper matches these filters.",
    reset: "Reset the catalog",
    inspect: "Inspect evidence",
    paper: "Paper ↗",
    artifact: "Artifact ↗",
    methodPattern: "Recurring method patterns",
    methodTitle: "Structure around the model keeps winning.",
    methodDeck:
      "Select a pattern to see the papers behind it. Counts are generated from the same reviewed catalog.",
    task: "Task",
    benchmark: "Benchmark / scale",
    intervention: "What changed",
    reportedEvidence: "Reported evidence",
    controls: "Comparison controls",
    sameModel: "Same model",
    sameBudget: "Same budget",
    strength: "Evidence strength",
    source: "Where to verify",
    caveat: "Read this caveat",
    productConfig: "Product configuration",
    model: "Model",
    version: "Version",
    notReported: "Not reported",
    close: "Close",
    footerLead: "Did this save you a paper-reading session?",
    footerCopy:
      "A star helps more researchers find the evidence—and tells us to keep auditing it.",
    footerButton: "Star the repository ★",
    footerNote: "Open data · primary sources · explicit caveats",
  },
  zh: {
    papers: "论文",
    coverage: "收录范围",
    methods: "方法",
    insights: "洞察",
    star: "去 GitHub 点 Star ↗",
    eyebrow: "看证据，不看榜单气氛",
    heroLead: "到底什么方法能超越",
    heroAccent: "Claude Code 与 Codex？",
    heroDeck:
      "把工业 coding agent 论文里的模型、方法、结果和限制条件，整理成真正读得下去的研究索引。",
    explore: "开始看证据 ↓",
    readInsights: "阅读综合结论 →",
    reviewed: "最近审计",
    reviewedPapers: "篇已审论文",
    directComparisons: "篇直接对比",
    officialArtifacts: "个官方 Artifact",
    researchDomains: "个研究领域",
    coverageEyebrow: "目录收录什么",
    coverageTitle: "先选研究领域或会议，再打开论文。",
    coverageDeck:
      "每篇论文都使用统一的领域与会议标签，同时在证据记录中保留准确的 venue / track。",
    domains: "研究领域",
    conferences: "会议 / 来源",
    catalogEyebrow: "论文目录",
    catalogTitle: "打开详情之前，先看清模型和结果。",
    search: "搜索系统、任务或方法…",
    product: "产品",
    modelsUsed: "使用的模型",
    evidenceClass: "证据类型",
    evidenceStrength: "证据强度",
    conference: "会议 / 来源",
    year: "年份",
    modelFilter: "模型",
    exactVenue: "准确 venue / track",
    method: "方法",
    all: "全部",
    direct: "直接对比",
    related: "相关方法",
    evaluation: "仅评测",
    clear: "清空筛选",
    results: "篇匹配论文",
    noResults: "没有论文符合当前筛选。",
    reset: "重置目录",
    inspect: "查看证据",
    paper: "打开论文 ↗",
    artifact: "打开 Artifact ↗",
    methodPattern: "反复出现的方法",
    methodTitle: "真正有效的，往往是模型周围的结构。",
    methodDeck: "点击方法即可筛选对应论文；数量直接来自审计后的目录。",
    task: "任务",
    benchmark: "Benchmark / 规模",
    intervention: "新增了什么",
    reportedEvidence: "论文报告的结果",
    controls: "实验控制",
    sameModel: "模型相同",
    sameBudget: "预算相同",
    strength: "证据强度",
    source: "证据位置",
    caveat: "需要注意",
    productConfig: "产品配置",
    model: "模型",
    version: "版本",
    notReported: "未报告",
    close: "关闭",
    footerLead: "这个目录帮你省下了一轮翻论文的时间吗？",
    footerCopy: "点一个 Star，让更多研究者找到这些证据，也让我们知道值得继续审计。",
    footerButton: "去仓库点个 Star ★",
    footerNote: "开放数据 · 一手来源 · 明确限制",
  },
};

const CLASS_LABELS: Record<Language, Record<Classification, string>> = {
  en: {
    direct: "Direct comparison",
    related: "Related method",
    evaluation: "Evaluation",
  },
  zh: {
    direct: "直接对比",
    related: "相关方法",
    evaluation: "仅评测",
  },
};

function readableValue(value: string, fallback: string) {
  return value === "not-reported" || value === "not-applicable"
    ? fallback
    : value;
}

function modelNames(value: string) {
  return value
    .split(";")
    .map((item) => item.trim())
    .filter((item) => item && item !== "not-reported" && item !== "not-applicable");
}

type Props = { papers: Paper[]; reviewedAt: string };

export function CatalogExplorer({ papers, reviewedAt }: Props) {
  const [language, setLanguage] = useState<Language>("en");
  const [query, setQuery] = useState("");
  const [product, setProduct] = useState<"all" | ProductId>("all");
  const [classification, setClassification] = useState<
    "all" | Classification
  >("all");
  const [conference, setConference] = useState<"all" | ConferenceId>("all");
  const [year, setYear] = useState<"all" | number>("all");
  const [domain, setDomain] = useState<"all" | DomainId>("all");
  const [evidenceStrength, setEvidenceStrength] = useState<
    "all" | EvidenceStrength
  >("all");
  const [model, setModel] = useState("all");
  const [method, setMethod] = useState("all");
  const [activePaper, setActivePaper] = useState<Paper | null>(null);
  const dialogCloseButton = useRef<HTMLButtonElement>(null);

  const t = copy[language];
  const directCount = papers.filter(
    (paper) => paper.classification === "direct",
  ).length;
  const artifactCount = papers.filter(
    (paper) => paper.artifact_status === "official",
  ).length;

  const conferenceCounts = useMemo(() => {
    const counts = new Map<ConferenceId, number>();
    papers.forEach((paper) => {
      counts.set(paper.conference, (counts.get(paper.conference) ?? 0) + 1);
    });
    return CONFERENCE_ORDER.flatMap((item) => {
      const count = counts.get(item);
      return count ? ([[item, count]] as Array<[ConferenceId, number]>) : [];
    });
  }, [papers]);

  const domainCounts = useMemo(() => {
    const counts = new Map<DomainId, number>();
    papers.forEach((paper) => {
      paper.domains.forEach((item) => {
        counts.set(item, (counts.get(item) ?? 0) + 1);
      });
    });
    return DOMAIN_ORDER.flatMap((item) => {
      const count = counts.get(item);
      return count ? ([[item, count]] as Array<[DomainId, number]>) : [];
    });
  }, [papers]);

  const yearCounts = useMemo(() => {
    const counts = new Map<number, number>();
    papers.forEach((paper) => counts.set(paper.year, (counts.get(paper.year) ?? 0) + 1));
    return [...counts.entries()].sort(([yearA], [yearB]) => yearB - yearA);
  }, [papers]);

  const evidenceStrengthCounts = useMemo(() => {
    const counts = new Map<EvidenceStrength, number>();
    papers.forEach((paper) => {
      const value = paper.evidence.strength;
      counts.set(value, (counts.get(value) ?? 0) + 1);
    });
    return (["high", "medium", "contextual"] as EvidenceStrength[]).flatMap(
      (item) => {
        const count = counts.get(item);
        return count ? ([[item, count]] as Array<[EvidenceStrength, number]>) : [];
      },
    );
  }, [papers]);

  const modelOptions = useMemo(() => {
    const values = new Set<string>();
    papers.forEach((paper) =>
      paper.products.forEach((item) => modelNames(item.model).forEach((name) => values.add(name))),
    );
    return [...values].sort((modelA, modelB) => modelA.localeCompare(modelB));
  }, [papers]);

  const methodCounts = useMemo(() => {
    const counts = new Map<string, number>();
    papers.forEach((paper) => {
      paper.method.tags.forEach((tag) => {
        counts.set(tag, (counts.get(tag) ?? 0) + 1);
      });
    });
    return [...counts.entries()].sort(
      ([tagA, countA], [tagB, countB]) =>
        countB - countA || tagA.localeCompare(tagB),
    );
  }, [papers]);

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const rank: Record<Classification, number> = {
      direct: 0,
      evaluation: 1,
      related: 2,
    };
    return papers
      .filter((paper) => {
        const matchesQuery =
          !needle ||
          [
            paper.system,
            paper.title,
            paper.conference,
            paper.venue,
            ...paper.domains,
            ...paper.domains.map((item) => DOMAIN_LABELS[language][item]),
            paper.task.summary,
            paper.task.benchmark,
            paper.method.summary,
            paper.evidence.result,
            ...paper.authors,
            ...paper.method.tags,
          ]
            .join(" ")
            .toLowerCase()
            .includes(needle);
        const matchesProduct =
          product === "all" ||
          paper.products.some((item) => item.product === product);
        const matchesClass =
          classification === "all" || paper.classification === classification;
        const matchesConference =
          conference === "all" || paper.conference === conference;
        const matchesYear = year === "all" || paper.year === year;
        const matchesDomain = domain === "all" || paper.domains.includes(domain);
        const matchesStrength =
          evidenceStrength === "all" || paper.evidence.strength === evidenceStrength;
        const matchesModel =
          model === "all" || paper.products.some((item) => modelNames(item.model).includes(model));
        const matchesMethod =
          method === "all" || paper.method.tags.includes(method);
        return (
          matchesQuery &&
          matchesProduct &&
          matchesClass &&
          matchesConference &&
          matchesYear &&
          matchesDomain &&
          matchesStrength &&
          matchesModel &&
          matchesMethod
        );
      })
      .sort(
        (paperA, paperB) =>
          rank[paperA.classification] - rank[paperB.classification] ||
          paperB.year - paperA.year ||
          paperA.system.localeCompare(paperB.system),
      );
  }, [
    classification,
    conference,
    domain,
    evidenceStrength,
    language,
    method,
    model,
    papers,
    product,
    query,
    year,
  ]);

  const filtersActive =
    query !== "" ||
    product !== "all" ||
    classification !== "all" ||
    conference !== "all" ||
    year !== "all" ||
    domain !== "all" ||
    evidenceStrength !== "all" ||
    model !== "all" ||
    method !== "all";

  useEffect(() => {
    document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  }, [language]);

  useEffect(() => {
    if (!activePaper) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    dialogCloseButton.current?.focus();
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setActivePaper(null);
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", closeOnEscape);
    };
  }, [activePaper]);

  const clearFilters = () => {
    setQuery("");
    setProduct("all");
    setClassification("all");
    setConference("all");
    setYear("all");
    setDomain("all");
    setEvidenceStrength("all");
    setModel("all");
    setMethod("all");
  };

  const chooseDomain = (value: DomainId) => {
    setDomain(value);
    document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
  };

  const chooseConference = (value: ConferenceId) => {
    setConference(value);
    document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
  };

  const chooseMethod = (tag: string) => {
    setMethod(tag);
    document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
  };

  const toggleLanguage = () => {
    setLanguage((current) => (current === "en" ? "zh" : "en"));
  };

  return (
    <main>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="Go to the top">
          <span className="brand-mark">&gt;_</span>
          <span>Agent Papers</span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="./insights/">{t.insights}</a>
          <a href="#coverage">{t.coverage}</a>
          <a href="#catalog">{t.papers}</a>
          <a href="#method-patterns">{t.methods}</a>
          <button className="language-toggle" type="button" onClick={toggleLanguage}>
            {language === "en" ? "中文" : "EN"}
          </button>
          <a className="star-link" href={REPOSITORY_URL} target="_blank" rel="noreferrer">
            {t.star}
          </a>
        </nav>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">{t.eyebrow}</p>
          <h1>
            {t.heroLead}
            <span> {t.heroAccent}</span>
          </h1>
          <p className="hero-deck">{t.heroDeck}</p>
          <div className="hero-actions">
            <a className="primary-action" href="#catalog">
              {t.explore}
            </a>
            <a className="secondary-action" href="./insights/">
              {t.readInsights}
            </a>
            <span>
              {t.reviewed} {reviewedAt}
            </span>
          </div>
        </div>

        <div className="signal-map" aria-label="Evidence pipeline illustration">
          <div className="signal-source coral">
            <span>&gt;_</span>
            <small>Claude Code</small>
          </div>
          <div className="signal-source cyan">
            <span>&gt;_</span>
            <small>Codex CLI</small>
          </div>
          <div className="signal-lines" aria-hidden="true">
            <i />
            <i />
            <i />
          </div>
          <div className="signal-proof">
            <strong>✓</strong>
            <span>method</span>
            <span>budget</span>
            <span>result</span>
          </div>
        </div>
      </section>

      <section className="stats" aria-label="Catalog summary">
        <div>
          <strong>{papers.length}</strong>
          <span>{t.reviewedPapers}</span>
        </div>
        <div>
          <strong>{directCount}</strong>
          <span>{t.directComparisons}</span>
        </div>
        <div>
          <strong>{artifactCount}</strong>
          <span>{t.officialArtifacts}</span>
        </div>
        <div>
          <strong>{domainCounts.length}</strong>
          <span>{t.researchDomains}</span>
        </div>
      </section>

      <section className="coverage-section" id="coverage">
        <div className="coverage-heading">
          <p className="eyebrow">{t.coverageEyebrow}</p>
          <h2>{t.coverageTitle}</h2>
          <p>{t.coverageDeck}</p>
        </div>
        <div className="coverage-groups">
          <div className="coverage-group">
            <h3>{t.domains}</h3>
            <div className="coverage-options">
              {domainCounts.map(([item, count]) => (
                <button
                  aria-pressed={domain === item}
                  className={domain === item ? "active" : ""}
                  key={item}
                  type="button"
                  onClick={() => chooseDomain(item)}
                >
                  <span>{DOMAIN_LABELS[language][item]}</span>
                  <strong>{count.toString().padStart(2, "0")}</strong>
                </button>
              ))}
            </div>
          </div>
          <div className="coverage-group conference-group">
            <h3>{t.conferences}</h3>
            <div className="coverage-options conference-options">
              {conferenceCounts.map(([item, count]) => (
                <button
                  aria-pressed={conference === item}
                  className={conference === item ? "active" : ""}
                  key={item}
                  type="button"
                  onClick={() => chooseConference(item)}
                >
                  <span>{item}</span>
                  <strong>{count.toString().padStart(2, "0")}</strong>
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="catalog-section" id="catalog">
        <div className="section-heading">
          <div>
            <p className="eyebrow">{t.catalogEyebrow}</p>
            <h2>{t.catalogTitle}</h2>
          </div>
          <label className="search-box">
            <span aria-hidden="true">⌕</span>
            <span className="sr-only">{t.search}</span>
            <input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder={t.search}
            />
          </label>
        </div>

        <div className="filters" aria-label="Catalog filters">
          <fieldset>
            <legend>{t.product}</legend>
            <div className="segmented-control">
              {[
                ["all", t.all],
                ["claude-code", "Claude Code"],
                ["codex-cli", "Codex CLI"],
              ].map(([value, label]) => (
                <button
                  className={product === value ? "active" : ""}
                  key={value}
                  type="button"
                  onClick={() => setProduct(value as "all" | ProductId)}
                >
                  {label}
                </button>
              ))}
            </div>
          </fieldset>

          <label>
            <span>{t.evidenceClass}</span>
            <select
              value={classification}
              onChange={(event) =>
                setClassification(event.target.value as "all" | Classification)
              }
            >
              <option value="all">{t.all}</option>
              <option value="direct">{t.direct}</option>
              <option value="evaluation">{t.evaluation}</option>
              <option value="related">{t.related}</option>
            </select>
          </label>

          <label>
            <span>{t.conference}</span>
            <select
              value={conference}
              onChange={(event) =>
                setConference(event.target.value as "all" | ConferenceId)
              }
            >
              <option value="all">{t.all}</option>
              {conferenceCounts.map(([item, count]) => (
                <option value={item} key={item}>
                  {item} ({count})
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>{t.year}</span>
            <select
              value={year}
              onChange={(event) =>
                setYear(event.target.value === "all" ? "all" : Number(event.target.value))
              }
            >
              <option value="all">{t.all}</option>
              {yearCounts.map(([item, count]) => (
                <option value={item} key={item}>
                  {item} ({count})
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>{t.domains}</span>
            <select
              value={domain}
              onChange={(event) =>
                setDomain(event.target.value as "all" | DomainId)
              }
            >
              <option value="all">{t.all}</option>
              {domainCounts.map(([item, count]) => (
                <option value={item} key={item}>
                  {DOMAIN_LABELS[language][item]} ({count})
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>{t.evidenceStrength}</span>
            <select
              value={evidenceStrength}
              onChange={(event) =>
                setEvidenceStrength(event.target.value as "all" | EvidenceStrength)
              }
            >
              <option value="all">{t.all}</option>
              {evidenceStrengthCounts.map(([item, count]) => (
                <option value={item} key={item}>
                  {item} ({count})
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>{t.modelFilter}</span>
            <select value={model} onChange={(event) => setModel(event.target.value)}>
              <option value="all">{t.all}</option>
              {modelOptions.map((item) => (
                <option value={item} key={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>{t.method}</span>
            <select value={method} onChange={(event) => setMethod(event.target.value)}>
              <option value="all">{t.all}</option>
              {methodCounts.map(([tag]) => (
                <option value={tag} key={tag}>
                  {tag}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="result-line" aria-live="polite">
          <span>
            {filtered.length} {t.results}
          </span>
          {filtersActive && (
            <button type="button" onClick={clearFilters}>
              {t.clear} ×
            </button>
          )}
        </div>

        {filtered.length > 0 ? (
          <div className="paper-grid">
            {filtered.map((paper) => (
              <article className="paper-card" key={paper.id}>
                <div className="card-topline">
                  <span className={`class-pill ${paper.classification}`}>
                    {CLASS_LABELS[language][paper.classification]}
                  </span>
                  <span>
                    {paper.conference} · {paper.year}
                  </span>
                </div>
                <h3>{paper.system}</h3>
                <p className="paper-title">{paper.title}</p>
                <div className="model-list" aria-label={t.modelsUsed}>
                  <p>{t.modelsUsed}</p>
                  {paper.products.map((item) => (
                    <div data-product={item.product} key={`${item.product}-${item.model}`}>
                      <span>{PRODUCT_LABELS[item.product]}</span>
                      <strong>{readableValue(item.model, t.notReported)}</strong>
                    </div>
                  ))}
                </div>
                <div className="domain-list" aria-label={t.domains}>
                  {paper.domains.map((item) => (
                    <span key={item}>{DOMAIN_LABELS[language][item]}</span>
                  ))}
                </div>
                <div className="method-summary">
                  <span>{t.intervention}</span>
                  <p>{paper.method.summary}</p>
                </div>
                <blockquote>{paper.evidence.result}</blockquote>
                <div className="card-footer">
                  <span>{paper.method.tags.slice(0, 2).join(" · ")}</span>
                  <button type="button" onClick={() => setActivePaper(paper)}>
                    {t.inspect} →
                  </button>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <strong>0</strong>
            <p>{t.noResults}</p>
            <button type="button" onClick={clearFilters}>
              {t.reset}
            </button>
          </div>
        )}
      </section>

      <section className="method-note" id="method-patterns">
        <div className="method-intro">
          <div>
            <p className="eyebrow">{t.methodPattern}</p>
            <h2>{t.methodTitle}</h2>
          </div>
          <p>{t.methodDeck}</p>
        </div>
        <div className="method-cloud">
          {methodCounts.slice(0, 12).map(([tag, count], index) => (
            <button
              className={index < 3 ? "featured" : ""}
              key={tag}
              type="button"
              onClick={() => chooseMethod(tag)}
            >
              <span>{tag}</span>
              <strong>{count.toString().padStart(2, "0")}</strong>
            </button>
          ))}
        </div>
      </section>

      <footer>
        <div className="footer-pitch">
          <span className="brand-mark">&gt;_</span>
          <div>
            <h2>{t.footerLead}</h2>
            <p>{t.footerCopy}</p>
          </div>
        </div>
        <div className="footer-action">
          <a href={REPOSITORY_URL} target="_blank" rel="noreferrer">
            {t.footerButton}
          </a>
          <span>{t.footerNote}</span>
        </div>
      </footer>

      {activePaper && (
        <div
          className="dialog-backdrop"
          role="presentation"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setActivePaper(null);
          }}
        >
          <div
            className="paper-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="dialog-title"
          >
            <button
              ref={dialogCloseButton}
              className="dialog-close"
              type="button"
              aria-label={t.close}
              onClick={() => setActivePaper(null)}
            >
              {t.close} ×
            </button>
            <div className="dialog-header">
              <span className={`class-pill ${activePaper.classification}`}>
                {CLASS_LABELS[language][activePaper.classification]}
              </span>
              <p>
                {activePaper.conference} · {activePaper.year} ·{" "}
                {activePaper.publication_status}
              </p>
              <h2 id="dialog-title">{activePaper.system}</h2>
              <h3>{activePaper.title}</h3>
              <p className="author-line">{activePaper.authors.join(", ")}</p>
              <div className="dialog-metadata">
                <span>
                  {t.exactVenue}: {activePaper.venue}
                </span>
                {activePaper.domains.map((item) => (
                  <span key={item}>{DOMAIN_LABELS[language][item]}</span>
                ))}
              </div>
            </div>

            <div className="dialog-section product-config">
              <p className="eyebrow">{t.productConfig}</p>
              {activePaper.products.map((item) => (
                <div key={item.product}>
                  <strong>{PRODUCT_LABELS[item.product]}</strong>
                  <span>
                    {t.model}: {readableValue(item.model, t.notReported)}
                  </span>
                  <span>
                    {t.version}: {readableValue(item.version, t.notReported)}
                  </span>
                </div>
              ))}
            </div>

            <div className="dialog-grid">
              <section>
                <p className="eyebrow">{t.task}</p>
                <p>{activePaper.task.summary}</p>
                <small>
                  {t.benchmark}: {activePaper.task.benchmark}
                </small>
              </section>
              <section>
                <p className="eyebrow">{t.intervention}</p>
                <p>{activePaper.method.summary}</p>
                <div className="tag-list">
                  {activePaper.method.tags.map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
              </section>
            </div>

            <section className="evidence-callout">
              <p className="eyebrow">{t.reportedEvidence}</p>
              <blockquote>{activePaper.evidence.result}</blockquote>
            </section>

            <section className="dialog-section">
              <p className="eyebrow">{t.controls}</p>
              <div className="control-grid">
                <div data-state={activePaper.evidence.same_model}>
                  <span>{t.sameModel}</span>
                  <strong>{activePaper.evidence.same_model}</strong>
                </div>
                <div data-state={activePaper.evidence.same_budget}>
                  <span>{t.sameBudget}</span>
                  <strong>{activePaper.evidence.same_budget}</strong>
                </div>
                <div data-state={activePaper.evidence.strength}>
                  <span>{t.strength}</span>
                  <strong>{activePaper.evidence.strength}</strong>
                </div>
              </div>
            </section>

            <div className="dialog-grid evidence-notes">
              <section>
                <p className="eyebrow">{t.source}</p>
                <p>{activePaper.evidence.source_location}</p>
              </section>
              <section className="caveat-box">
                <p className="eyebrow">{t.caveat}</p>
                <p>{activePaper.evidence.caveats}</p>
              </section>
            </div>

            <div className="dialog-actions">
              <a href={activePaper.paper_url} target="_blank" rel="noreferrer">
                {t.paper}
              </a>
              {activePaper.artifact_url && (
                <a href={activePaper.artifact_url} target="_blank" rel="noreferrer">
                  {t.artifact}
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
