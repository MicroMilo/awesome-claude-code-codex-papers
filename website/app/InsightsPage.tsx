import { useEffect, useMemo, useState } from "react";
import type { Paper } from "./CatalogExplorer";
import { ShareButton } from "./ShareButton";
import {
  INSIGHT_DEFINITIONS,
  MECHANISM_DEFINITIONS,
  type InsightLanguage,
} from "../data/insights";

const REPOSITORY_URL =
  "https://github.com/MicroMilo/awesome-claude-code-codex-papers";

export type PendingSummary = {
  reviewed_at: string;
  pending_record_count: number;
  high_priority_product_candidate_count: number;
  blocker_counts: Record<string, number>;
  high_priority_product_candidates: Array<{
    conference: string;
    title: string;
    official_url: string;
    signals: Array<{ product: string; matched_text: string }>;
    blocker: string;
    blocker_reason: string;
  }>;
  conference_level_pending: Array<{
    conference: string;
    list_url: string;
    reason: string;
  }>;
};

type Props = {
  papers: Paper[];
  reviewedAt: string;
  pendingSummary: PendingSummary;
};

const PRODUCT_LABELS: Record<Paper["products"][number]["product"], string> = {
  "claude-code": "Claude Code",
  "codex-cli": "Codex CLI",
};

const copy = {
  en: {
    pageTitle: "Insights",
    catalog: "Paper catalog",
    methods: "Methods",
    skill: "Census skill",
    weaknesses: "Weakness map",
    mechanisms: "What works",
    evidenceRules: "Evidence limits",
    pending: "Open evidence",
    star: "Star on GitHub ↗",
    eyebrow: "Evidence synthesis · 2026 catalog",
    heroLead: "Where coding agents",
    heroAccent: "actually break.",
    heroDeck:
      "A paper-by-paper diagnosis of Claude Code and Codex: what fails, what repeatedly helps, and how far the evidence really lets us go.",
    reviewed: "Last reviewed",
    included: "included papers",
    mapped: "mapped into this synthesis",
    sameModel: "same-model comparisons",
    sameBudget: "same-budget comparisons",
    thesisLabel: "Working thesis",
    thesis:
      "These products are already capable local executors. Their recurring weakness is control: preserving state, composing stages, grounding decisions in domain evidence, and independently verifying that a long task is actually complete.",
    thesisCaveat:
      "This is a synthesis of the current catalog, not a universal capability claim. Every inference below links back to its paper evidence and carries its own confounders.",
    contents: "Six evidence-backed findings",
    finding: "Finding",
    share: "Copy finding link",
    shared: "Link copied ✓",
    diagnosis: "Diagnosis",
    whatWorks: "What appears to work",
    evidenceTrail: "Paper evidence trail",
    evidenceRecords: "records",
    diagnostic: "diagnostic evidence",
    context: "context only",
    supports: "Why it supports the inference",
    reported: "Paper-reported evidence",
    products: "Product / model",
    evidenceRecord: "Evidence record →",
    verify: "Verify in official paper ↗",
    source: "Evidence location",
    caveat: "Comparison limit",
    mechanismsEyebrow: "Cross-paper synthesis",
    mechanismsTitle: "The winning pattern is structure around the model.",
    mechanismsDeck:
      "These mechanisms are counted from the reviewed method tags. Open a paper to inspect the exact task, model, result, and caveat behind each occurrence.",
    papers: "papers",
    limitationsEyebrow: "Evidence discipline",
    limitationsTitle: "Do not turn this page into a vendor leaderboard.",
    limitationsDeck:
      "Only a minority of records hold the underlying model constant or report comparable task caps. Model snapshot, product harness, tool permissions, policy, and observed compute or API cost are often still entangled.",
    ruleOne: "A product baseline is diagnostic only when the product actually runs the task.",
    ruleTwo: "Host and judge uses inform workflow design, but do not show that the product was beaten.",
    ruleThree: "Cross-paper scores are never compared as if they came from one benchmark.",
    hostTitle: "Host-only evidence kept out of product claims",
    hostDeck:
      "These records remain in the synthesis as context, with their role made explicit.",
    pendingEyebrow: "Unresolved evidence queue",
    pendingTitle: "Pending means blocked—not silently rejected.",
    pendingDeck:
      "These records stay outside the six findings until official or identity-verified full text can be checked. A product name in an abstract prioritizes review; it never proves product-level use by itself.",
    pendingRecords: "pending paper records",
    priorityCandidates: "direct-product candidates",
    sourceChallenges: "publisher challenges without open copy",
    missingPdfs: "full-text copies not resolved",
    priorityTitle: "Highest-priority paper queue",
    priorityEmpty:
      "No abstract-level Claude Code or Codex candidate is currently blocked on full-text review.",
    prioritySignal: "Abstract signal",
    blocker: "Current blocker",
    officialRecord: "Official record ↗",
    conferencePending: "Conference-level sources still pending",
    backToCatalog: "Inspect all paper records →",
    footerLead: "Useful enough to change what you build next?",
    footerCopy:
      "Star the repository so more researchers can find—and challenge—the evidence trail.",
    footerButton: "Star the repository ★",
    footerNote: "Primary sources · traceable inference · explicit uncertainty",
  },
  zh: {
    pageTitle: "洞察",
    catalog: "论文目录",
    methods: "方法",
    skill: "会议采集 Skill",
    weaknesses: "薄弱能力",
    mechanisms: "有效方法",
    evidenceRules: "证据边界",
    pending: "待审证据",
    star: "去 GitHub 点 Star ↗",
    eyebrow: "证据综合 · 2026 论文目录",
    heroLead: "Coding agent 到底",
    heroAccent: "差在哪里。",
    heroDeck:
      "逐篇映射 Claude Code 与 Codex 的失败点、反复有效的方法，以及现有证据到底允许我们下多强的结论。",
    reviewed: "最近审计",
    included: "篇已收录论文",
    mapped: "篇进入本页证据映射",
    sameModel: "篇同模型对比",
    sameBudget: "篇同预算对比",
    thesisLabel: "当前核心判断",
    thesis:
      "这些产品已经是很强的局部执行器。它们反复暴露的短板是控制能力：如何保留状态、组合多个阶段、用领域证据约束决策，并独立验证一项长任务是否真的完成。",
    thesisCaveat:
      "这是基于当前目录的综合判断，不是普遍能力定论。下面每条推理都映射到具体论文，并单独写明混杂因素。",
    contents: "六条有论文证据的结论",
    finding: "结论",
    share: "复制结论链接",
    shared: "链接已复制 ✓",
    diagnosis: "问题判断",
    whatWorks: "看起来有效的方法",
    evidenceTrail: "论文证据链",
    evidenceRecords: "条记录",
    diagnostic: "诊断性证据",
    context: "仅作上下文",
    supports: "它为什么支持这条推理",
    reported: "论文报告的原始结果",
    products: "产品 / 模型",
    evidenceRecord: "查看证据记录 →",
    verify: "打开官方论文核验 ↗",
    source: "证据位置",
    caveat: "对比限制",
    mechanismsEyebrow: "跨论文综合",
    mechanismsTitle: "反复胜出的，是模型周围的结构。",
    mechanismsDeck:
      "这里的次数来自已审计论文的方法标签。每篇论文都可继续查看准确任务、模型、结果和限制。",
    papers: "篇论文",
    limitationsEyebrow: "证据纪律",
    limitationsTitle: "不要把这一页读成厂商排行榜。",
    limitationsDeck:
      "只有少数论文固定了底层模型或给出可比较的任务上限。模型 snapshot、产品 harness、工具权限、策略，以及实际计算/API 成本仍经常纠缠在一起。",
    ruleOne: "只有产品真的运行了目标任务，产品 baseline 才能用于诊断。",
    ruleTwo: "宿主或裁判用途能启发工作流，但不能证明该产品被超越。",
    ruleThree: "不同论文的分数绝不被当作来自同一个 benchmark 横向比较。",
    hostTitle: "没有用于产品结论的 host-only 证据",
    hostDeck: "这些论文仍作为上下文保留，但会明确标出产品只是宿主。",
    pendingEyebrow: "尚未解决的证据队列",
    pendingTitle: "Pending 是证据受阻，不是被静默排除。",
    pendingDeck:
      "在官方或身份验证过的全文完成核验前，这些记录不会参与上面的六条结论。摘要出现产品名只会提高审核优先级，不能单独证明论文真正运行了该产品。",
    pendingRecords: "篇 pending 论文记录",
    priorityCandidates: "篇产品名直接命中候选",
    sourceChallenges: "个出版平台受阻且无开放副本",
    missingPdfs: "篇尚未解析到同一论文全文",
    priorityTitle: "最高优先级论文队列",
    priorityEmpty: "当前没有因全文审核受阻的 Claude Code 或 Codex 摘要级候选。",
    prioritySignal: "摘要信号",
    blocker: "当前阻塞",
    officialRecord: "打开官方记录 ↗",
    conferencePending: "会议级数据源仍待公开",
    backToCatalog: "查看全部论文记录 →",
    footerLead: "这些结论足以改变你下一步做什么吗？",
    footerCopy: "点一个 Star，让更多研究者找到这条证据链，也来一起质疑它。",
    footerButton: "去仓库点个 Star ★",
    footerNote: "一手来源 · 推理可追溯 · 不确定性明确",
  },
};

function productLine(paper: Paper) {
  return paper.products
    .map((product) => `${PRODUCT_LABELS[product.product]} · ${product.model}`)
    .join(" / ");
}

export function InsightsPage({ papers, reviewedAt, pendingSummary }: Props) {
  const [language, setLanguage] = useState<InsightLanguage>("en");
  const t = copy[language];
  const paperById = useMemo(
    () => new Map(papers.map((paper) => [paper.id, paper])),
    [papers],
  );
  const mappedPaperIds = useMemo(
    () =>
      new Set(
        INSIGHT_DEFINITIONS.flatMap((insight) =>
          insight.evidence.map((evidence) => evidence.paperId),
        ),
      ),
    [],
  );
  const sameModelCount = papers.filter(
    (paper) => paper.evidence.same_model === "yes",
  ).length;
  const sameBudgetCount = papers.filter(
    (paper) => paper.evidence.same_budget === "yes",
  ).length;
  const hostOnlyPapers = papers.filter(
    (paper) =>
      paper.products.length > 0 &&
      paper.products.every((product) => product.role === "host"),
  );

  useEffect(() => {
    document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  }, [language]);

  return (
    <main className="insights-page">
      <header className="site-header">
        <a className="brand" href="../" aria-label={t.catalog}>
          <span className="brand-mark">&gt;_</span>
          <span>Agent Papers</span>
        </a>
        <nav aria-label="Insights navigation">
          <a href="#weakness-map">{t.weaknesses}</a>
          <a href="#mechanisms">{t.mechanisms}</a>
          <a href="#pending-evidence">{t.pending}</a>
          <a href="#evidence-limits">{t.evidenceRules}</a>
          <a href="../#catalog">{t.catalog}</a>
          <a href="../methods/">{t.methods}</a>
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

      <section className="insights-hero" id="top">
        <div className="insights-hero-copy">
          <p className="eyebrow">{t.eyebrow}</p>
          <h1>
            {t.heroLead}
            <span> {t.heroAccent}</span>
          </h1>
          <p className="hero-deck">{t.heroDeck}</p>
          <div className="hero-actions">
            <a className="primary-action" href="#weakness-map">
              {t.weaknesses} ↓
            </a>
            <span>
              {t.reviewed} {reviewedAt}
            </span>
          </div>
        </div>

        <aside className="synthesis-card" aria-label="Synthesis coverage">
          <div className="synthesis-card-heading">
            <span>Evidence ledger</span>
            <strong>2026</strong>
          </div>
          <dl>
            <div>
              <dt>{t.included}</dt>
              <dd>{papers.length}</dd>
            </div>
            <div>
              <dt>{t.mapped}</dt>
              <dd>{mappedPaperIds.size}</dd>
            </div>
            <div>
              <dt>{t.sameModel}</dt>
              <dd>{sameModelCount}</dd>
            </div>
            <div>
              <dt>{t.sameBudget}</dt>
              <dd>{sameBudgetCount}</dd>
            </div>
          </dl>
          <p>{t.thesisCaveat}</p>
        </aside>
      </section>

      <section className="working-thesis" aria-labelledby="working-thesis-title">
        <p className="eyebrow">{t.thesisLabel}</p>
        <p id="working-thesis-title">{t.thesis}</p>
      </section>

      <section className="insight-report" id="weakness-map">
        <aside className="insight-toc">
          <p>{t.contents}</p>
          <ol>
            {INSIGHT_DEFINITIONS.map((insight) => (
              <li key={insight.id}>
                <a href={`#${insight.id}`}>
                  <span>{insight.number}</span>
                  {insight.domain[language]}
                </a>
              </li>
            ))}
          </ol>
        </aside>

        <div className="insight-stories">
          {INSIGHT_DEFINITIONS.map((insight) => {
            const evidenceRows = insight.evidence.flatMap((evidence) => {
              const paper = paperById.get(evidence.paperId);
              return paper ? [{ evidence, paper }] : [];
            });
            return (
              <article className="insight-story" id={insight.id} key={insight.id}>
                <header className="insight-story-header">
                  <div>
                    <span>{insight.number}</span>
                    <p>{insight.domain[language]}</p>
                  </div>
                  <div className="insight-share-action">
                    <p>{t.finding}</p>
                    <ShareButton
                      path={`insights/${insight.id}/`}
                      label={t.share}
                      copiedLabel={t.shared}
                    />
                  </div>
                </header>
                <h2>{insight.title[language]}</h2>
                <div className="insight-diagnosis">
                  <div>
                    <p className="eyebrow">{t.diagnosis}</p>
                    <p>{insight.thesis[language]}</p>
                  </div>
                  <div className="works-callout">
                    <p className="eyebrow">{t.whatWorks}</p>
                    <p>{insight.whatWorks[language]}</p>
                  </div>
                </div>

                <div className="evidence-ledger">
                  <div className="evidence-ledger-heading">
                    <h3>{t.evidenceTrail}</h3>
                    <span>
                      {evidenceRows.length} {t.evidenceRecords}
                    </span>
                  </div>
                  {evidenceRows.map(({ evidence, paper }) => (
                    <article className="insight-evidence" key={paper.id}>
                      <div className="insight-evidence-meta">
                        <span className={`evidence-weight ${evidence.weight}`}>
                          {evidence.weight === "diagnostic" ? t.diagnostic : t.context}
                        </span>
                        <span>
                          {paper.conference} · {paper.year}
                        </span>
                      </div>
                      <div className="insight-evidence-title">
                        <div>
                          <h4>{paper.system}</h4>
                          <p>{paper.title}</p>
                        </div>
                        <a href={paper.paper_url} target="_blank" rel="noreferrer">
                          {t.verify}
                        </a>
                        <a className="local-record-link" href={`../papers/${paper.id}/`}>
                          {t.evidenceRecord}
                        </a>
                      </div>
                      <dl className="insight-evidence-body">
                        <div className="inference-row">
                          <dt>{t.supports}</dt>
                          <dd>{evidence.inference[language]}</dd>
                        </div>
                        <div>
                          <dt>{t.reported}</dt>
                          <dd>{paper.evidence.result}</dd>
                        </div>
                        <div>
                          <dt>{t.products}</dt>
                          <dd>{productLine(paper)}</dd>
                        </div>
                        <div>
                          <dt>{t.source}</dt>
                          <dd>{paper.evidence.source_location}</dd>
                        </div>
                        <div className="caveat-row">
                          <dt>{t.caveat}</dt>
                          <dd>{paper.evidence.caveats}</dd>
                        </div>
                      </dl>
                    </article>
                  ))}
                </div>

                <p className="story-caution">
                  <strong>{t.caveat}:</strong> {insight.caution[language]}
                </p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="mechanism-section" id="mechanisms">
        <div className="mechanism-heading">
          <div>
            <p className="eyebrow">{t.mechanismsEyebrow}</p>
            <h2>{t.mechanismsTitle}</h2>
          </div>
          <p>{t.mechanismsDeck}</p>
        </div>
        <div className="mechanism-grid">
          {MECHANISM_DEFINITIONS.map((mechanism, index) => {
            const matchingPapers = papers.filter((paper) =>
              mechanism.tags.some((tag) => paper.method.tags.includes(tag)),
            );
            return (
              <article key={mechanism.id}>
                <div className="mechanism-number">0{index + 1}</div>
                <h3>{mechanism.title[language]}</h3>
                <p>{mechanism.summary[language]}</p>
                <div className="mechanism-count">
                  <strong>{matchingPapers.length}</strong>
                  <span>{t.papers}</span>
                </div>
                <ul>
                  {matchingPapers.map((paper) => (
                    <li key={paper.id}>
                      <a href={`../papers/${paper.id}/`}>
                        {paper.system} →
                      </a>
                    </li>
                  ))}
                </ul>
              </article>
            );
          })}
        </div>
      </section>

      <section className="pending-evidence" id="pending-evidence">
        <div className="pending-heading">
          <div>
            <p className="eyebrow">{t.pendingEyebrow}</p>
            <h2>{t.pendingTitle}</h2>
          </div>
          <p>{t.pendingDeck}</p>
        </div>

        <div className="pending-stats" aria-label={t.pendingEyebrow}>
          <div>
            <strong>{pendingSummary.pending_record_count}</strong>
            <span>{t.pendingRecords}</span>
          </div>
          <div>
            <strong>{pendingSummary.high_priority_product_candidate_count}</strong>
            <span>{t.priorityCandidates}</span>
          </div>
          <div>
            <strong>{pendingSummary.blocker_counts["official-source-challenge"] ?? 0}</strong>
            <span>{t.sourceChallenges}</span>
          </div>
          <div>
            <strong>{pendingSummary.blocker_counts["full-text-not-resolved"] ?? 0}</strong>
            <span>{t.missingPdfs}</span>
          </div>
        </div>

        <div className="pending-ledger">
          <div className="pending-ledger-heading">
            <h3>{t.priorityTitle}</h3>
            <span>{pendingSummary.high_priority_product_candidates.length}</span>
          </div>
          {pendingSummary.high_priority_product_candidates.length === 0 ? (
            <p className="pending-empty">{t.priorityEmpty}</p>
          ) : null}
          {pendingSummary.high_priority_product_candidates.map((paper) => (
            <article key={`${paper.conference}-${paper.title}`}>
              <div className="pending-paper-title">
                <span>{paper.conference}</span>
                <h4>{paper.title}</h4>
              </div>
              <dl>
                <div>
                  <dt>{t.prioritySignal}</dt>
                  <dd>{paper.signals.map((signal) => signal.matched_text).join(" · ")}</dd>
                </div>
                <div>
                  <dt>{t.blocker}</dt>
                  <dd>{paper.blocker_reason}</dd>
                </div>
              </dl>
              <a href={paper.official_url} target="_blank" rel="noreferrer">
                {t.officialRecord}
              </a>
            </article>
          ))}
        </div>

        <aside className="conference-pending">
          <p className="eyebrow">{t.conferencePending}</p>
          {pendingSummary.conference_level_pending.map((conference) => (
            <a
              href={conference.list_url}
              target="_blank"
              rel="noreferrer"
              key={conference.conference}
            >
              <strong>{conference.conference}</strong>
              <span>{conference.reason}</span>
              <small>↗</small>
            </a>
          ))}
        </aside>
      </section>

      <section className="evidence-limits" id="evidence-limits">
        <div className="limits-copy">
          <p className="eyebrow">{t.limitationsEyebrow}</p>
          <h2>{t.limitationsTitle}</h2>
          <p>{t.limitationsDeck}</p>
          <ol>
            <li>{t.ruleOne}</li>
            <li>{t.ruleTwo}</li>
            <li>{t.ruleThree}</li>
          </ol>
          <a className="primary-action" href="../#catalog">
            {t.backToCatalog}
          </a>
        </div>
        <aside className="host-evidence">
          <p className="eyebrow">{t.hostTitle}</p>
          <p>{t.hostDeck}</p>
          {hostOnlyPapers.map((paper) => (
            <a href={paper.paper_url} target="_blank" rel="noreferrer" key={paper.id}>
              <span>{paper.system}</span>
              <small>{productLine(paper)}</small>
              <strong>host →</strong>
            </a>
          ))}
        </aside>
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
    </main>
  );
}
