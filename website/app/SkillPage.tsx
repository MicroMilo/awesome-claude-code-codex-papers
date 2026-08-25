import { useEffect, useState } from "react";
import { copyText } from "./ShareButton";

type Language = "en" | "zh";

const REPOSITORY_URL =
  "https://github.com/MicroMilo/awesome-claude-code-codex-papers";
const SKILL_URL = `${REPOSITORY_URL}/tree/main/skills/official-conference-paper-census`;
const PROMPT =
  "Use $official-conference-paper-census to build an official acceptance census, resolve identity-verified abstracts and full text, apply metadata-first triage, and retain explicit included/excluded/pending/duplicate evidence.";

const copy = {
  en: {
    catalog: "Paper catalog",
    methods: "Methods",
    insights: "Insights",
    star: "Star on GitHub ↗",
    eyebrow: "Reusable research infrastructure",
    heroLead: "A conference crawler that knows when",
    heroAccent: "not to download the PDF.",
    heroDeck:
      "The repository ships the exact skill behind its 2026 census: official acceptance records, DOI-bound metadata, identity-verified open content, bounded candidate scanning, and an auditable decision for every paper.",
    openSkill: "Open the skill on GitHub ↗",
    copyPrompt: "Copy starter prompt",
    copied: "Prompt copied ✓",
    why: "Why use it",
    whyTitle: "The crawler is a protocol, not a pile of scraping scripts.",
    whyDeck:
      "It separates acceptance authority from content bytes, then keeps recall, download cost, and failure state explicit. A DOI-bound abstract can exclude an unrelated paper without a PDF request; a product name never becomes product evidence by itself.",
    source: "Official acceptance first",
    sourceDeck: "Conference pages, proceedings, publishers, and official OpenReview records define venue identity and the primary paper URL.",
    metadata: "Metadata before PDFs",
    metadataDeck: "Every title and identity-bound abstract is screened before candidates enter the bounded content queue.",
    audit: "Every record accounted for",
    auditDeck: "Included, excluded, pending, and duplicate decisions keep the missing papers visible.",
    workflow: "Five-stage workflow",
    stages: [
      ["01", "Freeze the official list", "Capture track scope, source URL, count, timestamp, and response hashes."],
      ["02", "Resolve and screen metadata", "Prefer first-party abstracts; otherwise bind OpenAlex metadata to the official DOI."],
      ["03", "Scan candidates only", "Fetch official or identity-verified open copies with bounded retries, checkpoints, versions, and hashes."],
      ["04", "Review product context", "Separate Claude Code/Codex CLI use from APIs, citations, acknowledgements, and model-only use."],
      ["05", "Promote with evidence", "Preserve exact model strings, budgets, tools, source locations, caveats, and census disposition."],
    ],
    support: "Current venue support",
    supportTitle: "Stable census paths for 12 venues; one accepted list still pending.",
    stable: "Stable end to end",
    gated: "Stable census/metadata; candidate content availability gated",
    pending: "Registered / pending adapter or list",
    availability:
      "“Stable” means official acceptance identity plus a bounded, resumable content path. Open copies may provide bytes, never venue status.",
    start: "Start from the protocol",
    startDeck:
      "Clone the repository, open the skill directory in your coding-agent workspace, and use this prompt. The skill links every adapter, audit invariant, and recovery path it expects the agent to follow.",
    clone: "Clone repository",
    viewSource: "Inspect scripts and support matrix →",
    footerLead: "Building another conference census?",
    footerCopy:
      "Reuse the skill, improve an adapter, and send the evidence trail back to the project.",
    footerButton: "Star the repository ★",
    footerNote: "Official sources · resumable scans · no silent drops",
  },
  zh: {
    catalog: "论文目录",
    methods: "方法",
    insights: "洞察",
    star: "去 GitHub 点 Star ↗",
    eyebrow: "可复用研究基础设施",
    heroLead: "一个知道什么时候",
    heroAccent: "不该下载 PDF 的会议爬虫。",
    heroDeck:
      "仓库直接提供生成 2026 census 的会议采集 Skill：官方接收记录、DOI 绑定 metadata、身份验证过的开放全文、限速候选扫描，以及每篇论文都可审计的处理结果。",
    openSkill: "在 GitHub 打开 Skill ↗",
    copyPrompt: "复制启动 Prompt",
    copied: "Prompt 已复制 ✓",
    why: "为什么值得复用",
    whyTitle: "它是一套采集协议，不是一堆临时爬虫脚本。",
    whyDeck:
      "它把会议身份与内容字节分开，再把召回率、下载成本和失败状态显式记录。DOI 绑定摘要可以先排除无关论文；只出现产品名不会被误判成产品级证据。",
    source: "官方接收来源优先",
    sourceDeck: "会议官网、正式 proceedings、出版平台和官方 OpenReview 记录定义会议身份与主论文 URL。",
    metadata: "先 metadata，后 PDF",
    metadataDeck: "先筛每篇标题与身份绑定摘要，再把候选送进有并发上限的全文队列。",
    audit: "每条记录都有去向",
    auditDeck: "included、excluded、pending、duplicate 都会保留，不能静默丢论文。",
    workflow: "五阶段工作流",
    stages: [
      ["01", "冻结官方清单", "记录 track 范围、来源 URL、数量、时间戳和响应哈希。"],
      ["02", "解析并筛选 metadata", "优先官方摘要；缺失时通过官方 DOI 绑定 OpenAlex metadata。"],
      ["03", "只扫描候选全文", "限速获取官方或身份验证过的开放副本，并保存断点、版本和哈希。"],
      ["04", "审核产品上下文", "区分 Claude Code/Codex CLI 产品使用与 API、引用、致谢和模型名命中。"],
      ["05", "携证据导入", "保留准确模型、预算、工具、证据位置、限制条件和 census disposition。"],
    ],
    support: "当前会议支持",
    supportTitle: "12 个会议已有稳定 census 路径，另 1 个仍等待接收清单。",
    stable: "端到端稳定",
    gated: "census/metadata 稳定；候选全文受可用性限制",
    pending: "已注册 / 等待 adapter 或官方清单",
    availability:
      "“稳定”表示官方会议身份与限速、可恢复的内容路径都明确；开放副本只能提供内容，不能证明接收。",
    start: "从协议开始",
    startDeck:
      "克隆仓库，在 coding agent 工作区打开 Skill 目录，再使用下面的 Prompt。Skill 已链接所需 adapter、审计不变量和失败恢复路径。",
    clone: "克隆仓库",
    viewSource: "查看脚本与支持矩阵 →",
    footerLead: "准备构建另一个会议全集吗？",
    footerCopy: "复用这套 Skill、改进 adapter，再把证据链贡献回项目。",
    footerButton: "去仓库点个 Star ★",
    footerNote: "一手来源 · 可恢复扫描 · 不静默丢弃",
  },
};

export function SkillPage() {
  const [language, setLanguage] = useState<Language>("en");
  const [copied, setCopied] = useState(false);
  const t = copy[language];

  useEffect(() => {
    document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  }, [language]);

  const copyPrompt = async () => {
    await copyText(PROMPT);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <main className="skill-page">
      <header className="site-header">
        <a className="brand" href="../" aria-label={t.catalog}>
          <span className="brand-mark">&gt;_</span>
          <span>Agent Papers</span>
        </a>
        <nav aria-label="Skill navigation">
          <a href="../#catalog">{t.catalog}</a>
          <a href="../methods/">{t.methods}</a>
          <a href="../insights/">{t.insights}</a>
          <button className="language-toggle" type="button" onClick={() => setLanguage((current) => current === "en" ? "zh" : "en")}>
            {language === "en" ? "中文" : "EN"}
          </button>
          <a className="star-link" href={REPOSITORY_URL} target="_blank" rel="noreferrer">{t.star}</a>
        </nav>
      </header>

      <section className="skill-hero">
        <div>
          <p className="eyebrow">{t.eyebrow}</p>
          <h1>{t.heroLead}<span> {t.heroAccent}</span></h1>
          <p className="hero-deck">{t.heroDeck}</p>
          <div className="hero-actions">
            <a className="primary-action" href={SKILL_URL} target="_blank" rel="noreferrer">{t.openSkill}</a>
            <button className="secondary-action prompt-copy" type="button" onClick={copyPrompt}>{copied ? t.copied : t.copyPrompt}</button>
          </div>
        </div>
        <aside className="skill-state-machine" aria-label="Metadata-first decision rule">
          <span>official title + identity-bound abstract</span>
          <div><strong>no signal</strong><small>excluded · no PDF</small></div>
          <div><strong>relevant signal</strong><small>candidate · scan PDF</small></div>
          <div><strong>missing / failed</strong><small>pending · no inference</small></div>
        </aside>
      </section>

      <section className="skill-principles">
        <header>
          <p className="eyebrow">{t.why}</p>
          <h2>{t.whyTitle}</h2>
          <p>{t.whyDeck}</p>
        </header>
        <div>
          <article><span>01</span><h3>{t.source}</h3><p>{t.sourceDeck}</p></article>
          <article><span>02</span><h3>{t.metadata}</h3><p>{t.metadataDeck}</p></article>
          <article><span>03</span><h3>{t.audit}</h3><p>{t.auditDeck}</p></article>
        </div>
      </section>

      <section className="skill-workflow">
        <p className="eyebrow">{t.workflow}</p>
        <ol>
          {t.stages.map(([number, title, description]) => (
            <li key={number}><span>{number}</span><h3>{title}</h3><p>{description}</p></li>
          ))}
        </ol>
      </section>

      <section className="skill-support">
        <header>
          <p className="eyebrow">{t.support}</p>
          <h2>{t.supportTitle}</h2>
        </header>
        <div className="support-ledger">
          <article data-status="stable"><span>{t.stable}</span><strong>ICLR · AAAI · IJCAI</strong></article>
          <article data-status="gated"><span>{t.gated}</span><strong>ASE · FSE · ISSTA · ICSE · ICML · KDD · PLDI · POPL · OOPSLA</strong></article>
          <article data-status="pending"><span>{t.pending}</span><strong>NeurIPS</strong></article>
        </div>
        <p className="support-note">{t.availability}</p>
      </section>

      <section className="skill-start">
        <div>
          <p className="eyebrow">{t.start}</p>
          <h2>{t.startDeck}</h2>
        </div>
        <div className="skill-code">
          <span>{t.clone}</span>
          <code>git clone {REPOSITORY_URL}.git</code>
          <span>Prompt</span>
          <code>{PROMPT}</code>
          <a href={SKILL_URL} target="_blank" rel="noreferrer">{t.viewSource}</a>
        </div>
      </section>

      <footer>
        <div className="footer-pitch"><span className="brand-mark">&gt;_</span><div><h2>{t.footerLead}</h2><p>{t.footerCopy}</p></div></div>
        <div className="footer-action"><a href={REPOSITORY_URL} target="_blank" rel="noreferrer">{t.footerButton}</a><span>{t.footerNote}</span></div>
      </footer>
    </main>
  );
}
