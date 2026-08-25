import { useEffect, useMemo, useState } from "react";
import type { Paper } from "./CatalogExplorer";
import { ShareButton } from "./ShareButton";

type Language = "en" | "zh";
type ProductId = Paper["products"][number]["product"];
type EvidenceStrength = Paper["evidence"]["strength"];

const REPOSITORY_URL =
  "https://github.com/MicroMilo/awesome-claude-code-codex-papers";

const PRODUCT_LABELS: Record<ProductId, string> = {
  "claude-code": "Claude Code",
  "codex-cli": "Codex CLI",
};

const copy = {
  en: {
    title: "Methods",
    catalog: "Paper catalog",
    insights: "Insights",
    skill: "Census skill",
    star: "Star on GitHub ↗",
    eyebrow: "Shareable evidence matrix · 2026",
    heroLead: "How researchers go beyond",
    heroAccent: "the product baseline.",
    heroDeck:
      "Each record keeps the industrial product, exact model, intervention, reported result, controls, source location, and caveat together—so a headline never travels without its evidence.",
    reviewed: "Last reviewed",
    records: "evidence records",
    patterns: "method patterns",
    sameModel: "same-model records",
    sameBudget: "same-budget records",
    filterTitle: "Choose the comparison you want to inspect.",
    product: "Product",
    strength: "Evidence strength",
    control: "Comparison control",
    method: "Method pattern",
    all: "All",
    sameModelOnly: "Same model only",
    directOnly: "Direct only",
    matching: "matching records",
    reset: "Clear filters",
    baseline: "Product / model",
    intervention: "What changed",
    result: "Paper-reported result",
    controls: "Controls",
    source: "Where to verify",
    caveat: "Comparison limit",
    sameModelLabel: "same model",
    sameBudgetLabel: "same budget",
    evidenceLabel: "evidence",
    record: "Open evidence record →",
    paper: "Official paper ↗",
    copy: "Copy link",
    copied: "Link copied ✓",
    empty: "No evidence record matches these filters.",
    noteTitle: "Read this as a method map, not a leaderboard.",
    note:
      "A reported improvement can mix changes in model, harness, permissions, policy, and budget. The control labels below are copied from the audited paper record; unknown stays unknown.",
    footerLead: "Found a method worth testing?",
    footerCopy:
      "Share the exact evidence record, then star the repository so the audit remains discoverable.",
    footerButton: "Star the repository ★",
    footerNote: "Exact models · primary sources · explicit controls",
  },
  zh: {
    title: "方法",
    catalog: "论文目录",
    insights: "洞察",
    skill: "会议采集 Skill",
    star: "去 GitHub 点 Star ↗",
    eyebrow: "可分享证据矩阵 · 2026",
    heroLead: "研究工作到底如何超越",
    heroAccent: "工业产品 baseline。",
    heroDeck:
      "每条记录把工业产品、准确模型、方法改动、论文结果、控制条件、证据位置和限制放在一起，避免结论脱离证据传播。",
    reviewed: "最近审计",
    records: "条证据记录",
    patterns: "种方法标签",
    sameModel: "条同模型记录",
    sameBudget: "条同预算记录",
    filterTitle: "先选择你真正想核验的对比。",
    product: "产品",
    strength: "证据强度",
    control: "对比控制",
    method: "方法标签",
    all: "全部",
    sameModelOnly: "只看同模型",
    directOnly: "只看直接对比",
    matching: "条匹配记录",
    reset: "清空筛选",
    baseline: "产品 / 模型",
    intervention: "新增了什么",
    result: "论文报告的结果",
    controls: "控制条件",
    source: "证据位置",
    caveat: "对比限制",
    sameModelLabel: "模型相同",
    sameBudgetLabel: "预算相同",
    evidenceLabel: "证据",
    record: "打开证据页 →",
    paper: "打开官方论文 ↗",
    copy: "复制链接",
    copied: "链接已复制 ✓",
    empty: "没有证据记录符合当前筛选。",
    noteTitle: "把这里看成方法地图，不是排行榜。",
    note:
      "论文报告的提升可能同时改变模型、harness、权限、策略和预算。下面的控制标签来自审计记录；无法确认的内容会继续保留为 unknown。",
    footerLead: "发现了值得验证的方法吗？",
    footerCopy: "先分享准确证据页，再点一个 Star，让这套审计更容易被找到。",
    footerButton: "去仓库点个 Star ★",
    footerNote: "准确模型 · 一手来源 · 明确控制条件",
  },
};

type Props = { papers: Paper[]; reviewedAt: string };

function controlValue(value: string) {
  return value === "yes" ? "yes" : value === "no" ? "no" : "unknown";
}

export function MethodsPage({ papers, reviewedAt }: Props) {
  const [language, setLanguage] = useState<Language>("en");
  const [product, setProduct] = useState<"all" | ProductId>("all");
  const [strength, setStrength] = useState<"all" | EvidenceStrength>("all");
  const [control, setControl] = useState<"all" | "same-model" | "direct">("all");
  const [method, setMethod] = useState("all");
  const t = copy[language];

  useEffect(() => {
    document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  }, [language]);

  const methodCounts = useMemo(() => {
    const counts = new Map<string, number>();
    papers.forEach((paper) =>
      paper.method.tags.forEach((tag) => counts.set(tag, (counts.get(tag) ?? 0) + 1)),
    );
    return [...counts.entries()].sort(
      ([tagA, countA], [tagB, countB]) =>
        countB - countA || tagA.localeCompare(tagB),
    );
  }, [papers]);

  const filtered = useMemo(
    () =>
      papers.filter((paper) => {
        const productMatch =
          product === "all" || paper.products.some((item) => item.product === product);
        const strengthMatch = strength === "all" || paper.evidence.strength === strength;
        const controlMatch =
          control === "all" ||
          (control === "same-model" && paper.evidence.same_model === "yes") ||
          (control === "direct" && paper.classification === "direct");
        const methodMatch = method === "all" || paper.method.tags.includes(method);
        return productMatch && strengthMatch && controlMatch && methodMatch;
      }),
    [control, method, papers, product, strength],
  );

  const clearFilters = () => {
    setProduct("all");
    setStrength("all");
    setControl("all");
    setMethod("all");
  };

  return (
    <main className="methods-page">
      <header className="site-header">
        <a className="brand" href="../" aria-label={t.catalog}>
          <span className="brand-mark">&gt;_</span>
          <span>Agent Papers</span>
        </a>
        <nav aria-label="Methods navigation">
          <a href="../#catalog">{t.catalog}</a>
          <a href="../insights/">{t.insights}</a>
          <a href="../skill/">{t.skill}</a>
          <button
            className="language-toggle"
            type="button"
            onClick={() => setLanguage((current) => (current === "en" ? "zh" : "en"))}
          >
            {language === "en" ? "中文" : "EN"}
          </button>
          <a className="star-link" href={REPOSITORY_URL} target="_blank" rel="noreferrer">
            {t.star}
          </a>
        </nav>
      </header>

      <section className="methods-hero" id="top">
        <div>
          <p className="eyebrow">{t.eyebrow}</p>
          <h1>
            {t.heroLead}
            <span> {t.heroAccent}</span>
          </h1>
          <p className="hero-deck">{t.heroDeck}</p>
          <p className="reviewed-line">
            {t.reviewed} {reviewedAt}
          </p>
        </div>
        <aside className="methods-note">
          <span>Read protocol</span>
          <h2>{t.noteTitle}</h2>
          <p>{t.note}</p>
        </aside>
      </section>

      <section className="stats methods-stats" aria-label="Method evidence summary">
        <div>
          <strong>{papers.length}</strong>
          <span>{t.records}</span>
        </div>
        <div>
          <strong>{methodCounts.length}</strong>
          <span>{t.patterns}</span>
        </div>
        <div>
          <strong>{papers.filter((paper) => paper.evidence.same_model === "yes").length}</strong>
          <span>{t.sameModel}</span>
        </div>
        <div>
          <strong>{papers.filter((paper) => paper.evidence.same_budget === "yes").length}</strong>
          <span>{t.sameBudget}</span>
        </div>
      </section>

      <section className="methods-catalog" id="evidence-matrix">
        <div className="methods-filter-heading">
          <div>
            <p className="eyebrow">Evidence controls</p>
            <h2>{t.filterTitle}</h2>
          </div>
          <button type="button" onClick={clearFilters}>{t.reset} ×</button>
        </div>

        <div className="method-filters">
          <label>
            <span>{t.product}</span>
            <select value={product} onChange={(event) => setProduct(event.target.value as "all" | ProductId)}>
              <option value="all">{t.all}</option>
              <option value="claude-code">Claude Code</option>
              <option value="codex-cli">Codex CLI</option>
            </select>
          </label>
          <label>
            <span>{t.strength}</span>
            <select value={strength} onChange={(event) => setStrength(event.target.value as "all" | EvidenceStrength)}>
              <option value="all">{t.all}</option>
              <option value="high">high</option>
              <option value="medium">medium</option>
              <option value="contextual">contextual</option>
            </select>
          </label>
          <label>
            <span>{t.control}</span>
            <select value={control} onChange={(event) => setControl(event.target.value as "all" | "same-model" | "direct")}>
              <option value="all">{t.all}</option>
              <option value="same-model">{t.sameModelOnly}</option>
              <option value="direct">{t.directOnly}</option>
            </select>
          </label>
          <label>
            <span>{t.method}</span>
            <select value={method} onChange={(event) => setMethod(event.target.value)}>
              <option value="all">{t.all}</option>
              {methodCounts.map(([tag, count]) => (
                <option value={tag} key={tag}>{tag} ({count})</option>
              ))}
            </select>
          </label>
        </div>

        <div className="method-result-count" aria-live="polite">
          {filtered.length} {t.matching}
        </div>

        <div className="method-records">
          {filtered.map((paper, index) => (
            <article className="method-record" id={paper.id} key={paper.id}>
              <header>
                <div>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <p>{paper.conference} · {paper.year} · {paper.classification}</p>
                </div>
                <strong data-strength={paper.evidence.strength}>{paper.evidence.strength}</strong>
              </header>
              <div className="method-record-title">
                <div>
                  <h2>{paper.system}</h2>
                  <p>{paper.title}</p>
                </div>
                <div className="record-actions">
                  <ShareButton
                    path={`papers/${paper.id}/`}
                    label={t.copy}
                    copiedLabel={t.copied}
                  />
                  <a href={`../papers/${paper.id}/`}>{t.record}</a>
                </div>
              </div>

              <div className="method-record-grid">
                <section className="method-baseline-cell">
                  <p className="eyebrow">{t.baseline}</p>
                  {paper.products.map((item) => (
                    <div data-product={item.product} key={`${item.product}-${item.model}`}>
                      <span>{PRODUCT_LABELS[item.product]}</span>
                      <strong>{item.model}</strong>
                      <small>{item.role} · {item.version}</small>
                    </div>
                  ))}
                </section>
                <section>
                  <p className="eyebrow">{t.intervention}</p>
                  <p>{paper.method.summary}</p>
                  <div className="tag-list">
                    {paper.method.tags.map((tag) => <span key={tag}>{tag}</span>)}
                  </div>
                </section>
                <section className="method-result-cell">
                  <p className="eyebrow">{t.result}</p>
                  <blockquote>{paper.evidence.result}</blockquote>
                </section>
                <section className="method-controls-cell">
                  <p className="eyebrow">{t.controls}</p>
                  <div>
                    <span data-state={controlValue(paper.evidence.same_model)}>
                      {t.sameModelLabel}: {paper.evidence.same_model}
                    </span>
                    <span data-state={controlValue(paper.evidence.same_budget)}>
                      {t.sameBudgetLabel}: {paper.evidence.same_budget}
                    </span>
                    <span data-state={paper.evidence.strength}>
                      {t.evidenceLabel}: {paper.evidence.strength}
                    </span>
                  </div>
                </section>
                <section>
                  <p className="eyebrow">{t.source}</p>
                  <p>{paper.evidence.source_location}</p>
                  <a href={paper.paper_url} target="_blank" rel="noreferrer">{t.paper}</a>
                </section>
                <section className="method-caveat-cell">
                  <p className="eyebrow">{t.caveat}</p>
                  <p>{paper.evidence.caveats}</p>
                </section>
              </div>
            </article>
          ))}
          {filtered.length === 0 && <p className="method-empty">{t.empty}</p>}
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
          <a href={REPOSITORY_URL} target="_blank" rel="noreferrer">{t.footerButton}</a>
          <span>{t.footerNote}</span>
        </div>
      </footer>
    </main>
  );
}
