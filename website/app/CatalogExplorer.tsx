import { useEffect, useMemo, useRef, useState } from "react";

type ProductId = "claude-code" | "codex-cli" | "openai-codex-model";
type Classification = "direct" | "related" | "evaluation" | "historical";
type Language = "en" | "zh";
type FairnessFilter = "all" | "controlled" | "unknown" | "mismatch";

export type Paper = {
  id: string;
  title: string;
  authors: string[];
  year: number;
  venue: string;
  publication_status: string;
  classification: Classification;
  system: string;
  paper_url: string;
  artifact_url?: string;
  artifact_status: "official" | "community" | "not-found";
  arxiv_id?: string;
  doi?: string;
  published_at?: string;
  products: Array<{
    product: ProductId;
    role: string;
    model: string;
    version: string;
  }>;
  task: { summary: string; benchmark: string };
  method: { summary: string; tags: string[] };
  evidence: {
    result: string;
    strength: "high" | "medium" | "contextual";
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
  "openai-codex-model": "Codex model",
};

const copy = {
  en: {
    papers: "Papers",
    methods: "Patterns",
    fairness: "Fairness",
    star: "Star on GitHub ↗",
    eyebrow: "Evidence, not leaderboard hype",
    heroLead: "What actually beats",
    heroAccent: "Claude Code & Codex?",
    heroDeck:
      "A readable research index for the methods, controls, and caveats behind production coding-agent comparisons.",
    explore: "Explore the evidence ↓",
    reviewed: "Last reviewed",
    reviewedPapers: "reviewed papers",
    directComparisons: "direct comparisons",
    officialArtifacts: "official artifacts",
    productionAgents: "production agents",
    catalogEyebrow: "Research catalog",
    catalogTitle: "Start with the result. Open the controls only when needed.",
    search: "Search systems, tasks, methods…",
    product: "Product",
    evidenceClass: "Evidence class",
    comparison: "Comparison",
    venue: "Venue",
    method: "Method",
    all: "All",
    direct: "Direct",
    related: "Related",
    evaluation: "Evaluation",
    historical: "Historical",
    controlled: "Same model + budget",
    unknown: "Controls unclear",
    mismatch: "Known mismatch",
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
    fairnessEyebrow: "Comparison sanity check",
    fairnessTitle: "A direct comparison is not automatically a fair comparison.",
    fairControlled: "Controlled",
    fairUnknown: "Unclear",
    fairMismatch: "Mismatch",
    fairControlledText: "The paper explicitly holds model and budget fixed.",
    fairUnknownText: "At least one important control is not reported clearly.",
    fairMismatchText: "The paper explicitly changes the model or budget.",
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
    methods: "方法",
    fairness: "公平性",
    star: "去 GitHub 点 Star ↗",
    eyebrow: "看证据，不看榜单气氛",
    heroLead: "到底什么方法能超越",
    heroAccent: "Claude Code 与 Codex？",
    heroDeck:
      "把工业 coding agent 论文里的方法、实验控制和限制条件，整理成真正读得下去的研究索引。",
    explore: "开始看证据 ↓",
    reviewed: "最近审计",
    reviewedPapers: "篇已审论文",
    directComparisons: "篇直接对比",
    officialArtifacts: "个官方 Artifact",
    productionAgents: "个工业 Agent",
    catalogEyebrow: "论文目录",
    catalogTitle: "先看结果；需要时，再展开实验控制和限制。",
    search: "搜索系统、任务或方法…",
    product: "产品",
    evidenceClass: "证据类型",
    comparison: "实验控制",
    venue: "会议",
    method: "方法",
    all: "全部",
    direct: "直接对比",
    related: "相关方法",
    evaluation: "仅评测",
    historical: "历史模型",
    controlled: "相同模型与预算",
    unknown: "控制不明确",
    mismatch: "已知不一致",
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
    fairnessEyebrow: "先检查可比性",
    fairnessTitle: "有直接对比，不等于做了公平对比。",
    fairControlled: "严格控制",
    fairUnknown: "信息不明",
    fairMismatch: "条件不同",
    fairControlledText: "论文明确保持模型和预算一致。",
    fairUnknownText: "至少一个关键实验控制没有写清楚。",
    fairMismatchText: "论文明确使用了不同模型或预算。",
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
    historical: "Historical",
  },
  zh: {
    direct: "直接对比",
    related: "相关方法",
    evaluation: "仅评测",
    historical: "历史模型",
  },
};

function fairnessGroup(paper: Paper): Exclude<FairnessFilter, "all"> {
  if (
    paper.evidence.same_model === "yes" &&
    paper.evidence.same_budget === "yes"
  ) {
    return "controlled";
  }
  if (
    paper.evidence.same_model === "no" ||
    paper.evidence.same_budget === "no"
  ) {
    return "mismatch";
  }
  return "unknown";
}

function readableValue(value: string, fallback: string) {
  return value === "not-reported" || value === "not-applicable"
    ? fallback
    : value;
}

type Props = { papers: Paper[]; reviewedAt: string };

export function CatalogExplorer({ papers, reviewedAt }: Props) {
  const [language, setLanguage] = useState<Language>("en");
  const [query, setQuery] = useState("");
  const [product, setProduct] = useState<"all" | ProductId>("all");
  const [classification, setClassification] = useState<
    "all" | Classification
  >("all");
  const [fairness, setFairness] = useState<FairnessFilter>("all");
  const [venue, setVenue] = useState("all");
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

  const venues = useMemo(
    () => [...new Set(papers.map((paper) => paper.venue))].sort(),
    [papers],
  );

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

  const fairnessCounts = useMemo(
    () => ({
      controlled: papers.filter((paper) => fairnessGroup(paper) === "controlled")
        .length,
      unknown: papers.filter((paper) => fairnessGroup(paper) === "unknown")
        .length,
      mismatch: papers.filter((paper) => fairnessGroup(paper) === "mismatch")
        .length,
    }),
    [papers],
  );

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const rank: Record<Classification, number> = {
      direct: 0,
      evaluation: 1,
      related: 2,
      historical: 3,
    };
    return papers
      .filter((paper) => {
        const matchesQuery =
          !needle ||
          [
            paper.system,
            paper.title,
            paper.venue,
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
        const matchesFairness =
          fairness === "all" || fairnessGroup(paper) === fairness;
        const matchesVenue = venue === "all" || paper.venue === venue;
        const matchesMethod =
          method === "all" || paper.method.tags.includes(method);
        return (
          matchesQuery &&
          matchesProduct &&
          matchesClass &&
          matchesFairness &&
          matchesVenue &&
          matchesMethod
        );
      })
      .sort(
        (paperA, paperB) =>
          rank[paperA.classification] - rank[paperB.classification] ||
          paperB.year - paperA.year ||
          paperA.system.localeCompare(paperB.system),
      );
  }, [classification, fairness, method, papers, product, query, venue]);

  const filtersActive =
    query !== "" ||
    product !== "all" ||
    classification !== "all" ||
    fairness !== "all" ||
    venue !== "all" ||
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
    setFairness("all");
    setVenue("all");
    setMethod("all");
  };

  const chooseMethod = (tag: string) => {
    setMethod(tag);
    document.getElementById("catalog")?.scrollIntoView({ behavior: "smooth" });
  };

  const chooseFairness = (value: Exclude<FairnessFilter, "all">) => {
    setFairness(value);
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
          <a href="#catalog">{t.papers}</a>
          <a href="#method-patterns">{t.methods}</a>
          <a href="#fairness">{t.fairness}</a>
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
          <strong>2</strong>
          <span>{t.productionAgents}</span>
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
              <option value="historical">{t.historical}</option>
            </select>
          </label>

          <label>
            <span>{t.comparison}</span>
            <select
              value={fairness}
              onChange={(event) => setFairness(event.target.value as FairnessFilter)}
            >
              <option value="all">{t.all}</option>
              <option value="controlled">{t.controlled}</option>
              <option value="unknown">{t.unknown}</option>
              <option value="mismatch">{t.mismatch}</option>
            </select>
          </label>

          <label>
            <span>{t.venue}</span>
            <select value={venue} onChange={(event) => setVenue(event.target.value)}>
              <option value="all">{t.all}</option>
              {venues.map((item) => (
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
                    {paper.venue} · {paper.year}
                  </span>
                </div>
                <h3>{paper.system}</h3>
                <p className="paper-title">{paper.title}</p>
                <div className="product-list">
                  {paper.products.map((item) => (
                    <span key={item.product}>{PRODUCT_LABELS[item.product]}</span>
                  ))}
                </div>
                <div className="method-summary">
                  <span>{t.intervention}</span>
                  <p>{paper.method.summary}</p>
                </div>
                <blockquote>{paper.evidence.result}</blockquote>
                <div className="control-strip">
                  <span data-state={paper.evidence.same_model}>
                    M · {paper.evidence.same_model}
                  </span>
                  <span data-state={paper.evidence.same_budget}>
                    B · {paper.evidence.same_budget}
                  </span>
                  <span data-state={paper.evidence.strength}>
                    E · {paper.evidence.strength}
                  </span>
                </div>
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

      <section className="fairness-section" id="fairness">
        <div className="fairness-heading">
          <p className="eyebrow">{t.fairnessEyebrow}</p>
          <h2>{t.fairnessTitle}</h2>
        </div>
        <div className="fairness-grid">
          <button type="button" onClick={() => chooseFairness("controlled")}>
            <span className="fairness-number controlled">{fairnessCounts.controlled}</span>
            <strong>{t.fairControlled}</strong>
            <p>{t.fairControlledText}</p>
          </button>
          <button type="button" onClick={() => chooseFairness("unknown")}>
            <span className="fairness-number unknown">{fairnessCounts.unknown}</span>
            <strong>{t.fairUnknown}</strong>
            <p>{t.fairUnknownText}</p>
          </button>
          <button type="button" onClick={() => chooseFairness("mismatch")}>
            <span className="fairness-number mismatch">{fairnessCounts.mismatch}</span>
            <strong>{t.fairMismatch}</strong>
            <p>{t.fairMismatchText}</p>
          </button>
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
                {activePaper.venue} · {activePaper.year} · {activePaper.publication_status}
              </p>
              <h2 id="dialog-title">{activePaper.system}</h2>
              <h3>{activePaper.title}</h3>
              <p className="author-line">{activePaper.authors.join(", ")}</p>
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
