import { mkdir, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { Paper } from "../app/CatalogExplorer";
import catalogData from "../data/catalog.json";
import { INSIGHT_DEFINITIONS } from "../data/insights";

const SITE_URL =
  "https://micromilo.github.io/awesome-claude-code-codex-papers/";
const REPOSITORY_URL =
  "https://github.com/MicroMilo/awesome-claude-code-codex-papers";
const BASE_PATH = "/awesome-claude-code-codex-papers/";
const websiteRoot = fileURLToPath(new URL("..", import.meta.url));
const publicRoot = join(websiteRoot, "public");
const papers = catalogData.papers as Paper[];
const reviewedAt = catalogData.reviewed_at;

const PRODUCT_LABELS: Record<Paper["products"][number]["product"], string> = {
  "claude-code": "Claude Code",
  "codex-cli": "Codex CLI",
};

function escapeHtml(value: unknown) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function pageUrl(path = "") {
  return new URL(path, SITE_URL).toString();
}

function jsonLd(value: unknown) {
  return JSON.stringify(value).replaceAll("<", "\\u003c");
}

function htmlPage({
  title,
  description,
  canonical,
  type = "article",
  body,
  structuredData,
}: {
  title: string;
  description: string;
  canonical: string;
  type?: "article" | "website";
  body: string;
  structuredData: unknown;
}) {
  const safeTitle = escapeHtml(title);
  const safeDescription = escapeHtml(description);
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="${safeDescription}" />
    <meta name="robots" content="index,follow" />
    <meta name="theme-color" content="#0d1718" />
    <link rel="canonical" href="${escapeHtml(canonical)}" />
    <link rel="alternate" type="application/atom+xml" title="Agent Papers updates" href="${BASE_PATH}feed.xml" />
    <link rel="icon" href="${BASE_PATH}icon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="${BASE_PATH}record.css" />
    <meta property="og:type" content="${type}" />
    <meta property="og:site_name" content="Agent Papers" />
    <meta property="og:title" content="${safeTitle}" />
    <meta property="og:description" content="${safeDescription}" />
    <meta property="og:url" content="${escapeHtml(canonical)}" />
    <meta property="og:image" content="${SITE_URL}og.png" />
    <meta property="og:image:width" content="1280" />
    <meta property="og:image:height" content="640" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${safeTitle}" />
    <meta name="twitter:description" content="${safeDescription}" />
    <meta name="twitter:image" content="${SITE_URL}og.png" />
    <script type="application/ld+json">${jsonLd(structuredData)}</script>
    <title>${safeTitle}</title>
  </head>
  <body>
    ${body}
  </body>
</html>
`;
}

function productCards(paper: Paper) {
  return paper.products
    .map(
      (product) => `<article class="product-card" data-product="${product.product}">
        <span>${escapeHtml(PRODUCT_LABELS[product.product])} · ${escapeHtml(product.role)}</span>
        <strong>${escapeHtml(product.model)}</strong>
        <small>Version: ${escapeHtml(product.version)}</small>
        <small>Budget: ${escapeHtml(product.budget ?? "not-reported")}</small>
      </article>`,
    )
    .join("\n");
}

function renderPaperPage(paper: Paper) {
  const canonical = pageUrl(`papers/${paper.id}/`);
  const description = `${paper.system}: ${paper.method.summary} Evidence, exact product models, controls, source location, and caveats.`;
  const body = `<header class="record-header">
      <a class="brand" href="${BASE_PATH}"><span>&gt;_</span> Agent Papers</a>
      <nav><a href="${BASE_PATH}methods/">Methods</a><a href="${BASE_PATH}insights/">Insights</a><a href="${REPOSITORY_URL}">GitHub ↗</a></nav>
    </header>
    <main class="record-page">
      <nav class="breadcrumb"><a href="${BASE_PATH}">Catalog</a><span>/</span><span>${escapeHtml(paper.conference)} ${paper.year}</span><span>/</span><span>${escapeHtml(paper.system)}</span></nav>
      <header class="record-hero">
        <div class="record-kicker"><span>${escapeHtml(paper.classification)}</span><span>${escapeHtml(paper.conference)} · ${paper.year}</span><span>${escapeHtml(paper.evidence.strength)} evidence</span></div>
        <h1>${escapeHtml(paper.system)}</h1>
        <p class="paper-title">${escapeHtml(paper.title)}</p>
        <p class="authors">${escapeHtml(paper.authors.join(", "))}</p>
        <div class="tag-row">${paper.domains.map((domain) => `<span>${escapeHtml(domain)}</span>`).join("")}</div>
      </header>

      <section class="record-section">
        <p class="eyebrow">Product / exact model</p>
        <div class="product-grid">${productCards(paper)}</div>
      </section>

      <section class="two-column">
        <article><p class="eyebrow">Task</p><h2>${escapeHtml(paper.task.summary)}</h2><p>${escapeHtml(paper.task.benchmark)}</p></article>
        <article><p class="eyebrow">What changed</p><h2>${escapeHtml(paper.method.summary)}</h2><div class="tag-row">${paper.method.tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}</div></article>
      </section>

      <section class="result-panel"><p class="eyebrow">Paper-reported result</p><blockquote>${escapeHtml(paper.evidence.result)}</blockquote></section>

      <section class="control-strip">
        <div data-state="${paper.evidence.same_model}"><span>Same model</span><strong>${paper.evidence.same_model}</strong></div>
        <div data-state="${paper.evidence.same_budget}"><span>Same budget</span><strong>${paper.evidence.same_budget}</strong></div>
        <div data-state="${paper.evidence.strength}"><span>Evidence</span><strong>${paper.evidence.strength}</strong></div>
      </section>

      <section class="two-column evidence-notes">
        <article><p class="eyebrow">Where to verify</p><h2>${escapeHtml(paper.evidence.source_location)}</h2><p>${escapeHtml(paper.evidence.comparison_scope)}</p></article>
        <article class="caveat"><p class="eyebrow">Comparison limit</p><h2>${escapeHtml(paper.evidence.caveats)}</h2></article>
      </section>

      <div class="record-links">
        <a class="primary" href="${escapeHtml(paper.paper_url)}">Official paper ↗</a>
        ${paper.evidence.source_url && paper.evidence.source_url !== paper.paper_url ? `<a href="${escapeHtml(paper.evidence.source_url)}">Evidence copy (${escapeHtml(paper.evidence.source_version ?? "unknown version")}) ↗</a>` : ""}
        ${paper.artifact_url ? `<a href="${escapeHtml(paper.artifact_url)}">Artifact ↗</a>` : ""}
        <a href="${BASE_PATH}methods/#${escapeHtml(paper.id)}">Compare methods →</a>
      </div>
    </main>
    <footer class="record-footer"><div><strong>Did this evidence save you time?</strong><span>Share this exact page so the caveat travels with the result.</span></div><a href="${REPOSITORY_URL}/stargazers">Star the repository ★</a></footer>`;

  return htmlPage({
    title: `${paper.system}: Claude Code / Codex evidence`,
    description,
    canonical,
    body,
    structuredData: {
      "@context": "https://schema.org",
      "@type": "ScholarlyArticle",
      name: paper.title,
      headline: paper.system,
      author: paper.authors.map((name) => ({ "@type": "Person", name })),
      datePublished: paper.published_at ?? `${paper.year}-01-01`,
      isPartOf: { "@type": "PublicationEvent", name: paper.venue },
      url: canonical,
      sameAs: paper.paper_url,
      about: paper.products.map((product) => PRODUCT_LABELS[product.product]),
    },
  });
}

function renderInsightPage(insight: (typeof INSIGHT_DEFINITIONS)[number]) {
  const canonical = pageUrl(`insights/${insight.id}/`);
  const evidenceRows = insight.evidence.flatMap((evidence) => {
    const paper = papers.find((item) => item.id === evidence.paperId);
    return paper ? [{ evidence, paper }] : [];
  });
  const body = `<header class="record-header">
      <a class="brand" href="${BASE_PATH}"><span>&gt;_</span> Agent Papers</a>
      <nav><a href="${BASE_PATH}insights/">All insights</a><a href="${BASE_PATH}methods/">Methods</a><a href="${REPOSITORY_URL}">GitHub ↗</a></nav>
    </header>
    <main class="record-page insight-record">
      <nav class="breadcrumb"><a href="${BASE_PATH}insights/">Insights</a><span>/</span><span>${escapeHtml(insight.number)}</span><span>/</span><span>${escapeHtml(insight.domain.en)}</span></nav>
      <header class="record-hero">
        <div class="record-kicker"><span>Finding ${escapeHtml(insight.number)}</span><span>${escapeHtml(insight.domain.en)}</span><span>${evidenceRows.length} paper records</span></div>
        <h1>${escapeHtml(insight.title.en)}</h1>
        <p class="paper-title">${escapeHtml(insight.title.zh)}</p>
      </header>

      <section class="two-column diagnosis">
        <article><p class="eyebrow">Diagnosis</p><h2>${escapeHtml(insight.thesis.en)}</h2><p lang="zh-CN">${escapeHtml(insight.thesis.zh)}</p></article>
        <article class="works"><p class="eyebrow">What appears to work</p><h2>${escapeHtml(insight.whatWorks.en)}</h2><p lang="zh-CN">${escapeHtml(insight.whatWorks.zh)}</p></article>
      </section>

      <section class="insight-ledger">
        <div class="ledger-heading"><p class="eyebrow">Paper evidence trail</p><span>${evidenceRows.length} records</span></div>
        ${evidenceRows
          .map(
            ({ evidence, paper }) => `<article class="static-evidence">
              <header><span>${escapeHtml(evidence.weight)} evidence</span><span>${escapeHtml(paper.conference)} · ${paper.year}</span></header>
              <h2>${escapeHtml(paper.system)}</h2>
              <p>${escapeHtml(paper.title)}</p>
              <dl>
                <div><dt>Why it supports the inference</dt><dd>${escapeHtml(evidence.inference.en)}</dd></div>
                <div><dt>Paper-reported result</dt><dd>${escapeHtml(paper.evidence.result)}</dd></div>
                <div><dt>Product / model</dt><dd>${escapeHtml(paper.products.map((product) => `${PRODUCT_LABELS[product.product]} · ${product.model}`).join(" / "))}</dd></div>
                <div><dt>Evidence location</dt><dd>${escapeHtml(paper.evidence.source_location)}</dd></div>
                <div class="caveat"><dt>Comparison limit</dt><dd>${escapeHtml(paper.evidence.caveats)}</dd></div>
              </dl>
              <div class="record-links compact"><a href="${BASE_PATH}papers/${escapeHtml(paper.id)}/">Evidence record →</a><a href="${escapeHtml(paper.paper_url)}">Official paper ↗</a></div>
            </article>`,
          )
          .join("\n")}
      </section>

      <aside class="insight-caution"><p class="eyebrow">Inference limit</p><p>${escapeHtml(insight.caution.en)}</p><p lang="zh-CN">${escapeHtml(insight.caution.zh)}</p></aside>
      <div class="record-links"><a class="primary" href="${BASE_PATH}insights/#${escapeHtml(insight.id)}">Open full synthesis →</a><a href="${BASE_PATH}methods/">Compare methods →</a></div>
    </main>
    <footer class="record-footer"><div><strong>Useful enough to change what you build?</strong><span>Share the evidence page, then challenge the inference.</span></div><a href="${REPOSITORY_URL}/stargazers">Star the repository ★</a></footer>`;

  return htmlPage({
    title: insight.title.en,
    description: insight.thesis.en,
    canonical,
    body,
    structuredData: {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: insight.title.en,
      description: insight.thesis.en,
      dateModified: reviewedAt,
      url: canonical,
      citation: evidenceRows.map(({ paper }) => paper.paper_url),
      isPartOf: pageUrl("insights/"),
    },
  });
}

function renderSitemap() {
  const urls = [
    "",
    "insights/",
    "methods/",
    "skill/",
    ...papers.map((paper) => `papers/${paper.id}/`),
    ...INSIGHT_DEFINITIONS.map((insight) => `insights/${insight.id}/`),
  ];
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (path) => `  <url>
    <loc>${escapeHtml(pageUrl(path))}</loc>
    <lastmod>${reviewedAt}</lastmod>
    <changefreq>weekly</changefreq>
  </url>`,
  )
  .join("\n")}
</urlset>
`;
}

function renderFeed() {
  const updated = `${reviewedAt}T00:00:00Z`;
  const entries = papers
    .map(
      (paper) => `  <entry>
    <title>${escapeHtml(`${paper.system}: ${paper.title}`)}</title>
    <id>${escapeHtml(pageUrl(`papers/${paper.id}/`))}</id>
    <link href="${escapeHtml(pageUrl(`papers/${paper.id}/`))}" />
    <updated>${escapeHtml(paper.published_at ? `${paper.published_at}T00:00:00Z` : updated)}</updated>
    <summary>${escapeHtml(`${paper.method.summary} Reported evidence: ${paper.evidence.result}`)}</summary>
    <category term="${escapeHtml(paper.conference)}" />
  </entry>`,
    )
    .join("\n");
  return `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Awesome Claude Code &amp; Codex Papers</title>
  <subtitle>Audited product-level coding-agent research updates</subtitle>
  <id>${SITE_URL}</id>
  <link href="${SITE_URL}" />
  <link href="${SITE_URL}feed.xml" rel="self" type="application/atom+xml" />
  <updated>${updated}</updated>
  <author><name>MicroMilo</name><uri>https://github.com/MicroMilo</uri></author>
${entries}
</feed>
`;
}

async function writeText(path: string, value: string) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, value, "utf8");
}

async function main() {
  const paperOutput = join(publicRoot, "papers");
  const insightOutput = join(publicRoot, "insights");
  await rm(paperOutput, { recursive: true, force: true });
  await rm(insightOutput, { recursive: true, force: true });

  await Promise.all([
    ...papers.map((paper) =>
      writeText(join(paperOutput, paper.id, "index.html"), renderPaperPage(paper)),
    ),
    ...INSIGHT_DEFINITIONS.map((insight) =>
      writeText(join(insightOutput, insight.id, "index.html"), renderInsightPage(insight)),
    ),
    writeText(join(publicRoot, "sitemap.xml"), renderSitemap()),
    writeText(join(publicRoot, "feed.xml"), renderFeed()),
  ]);
}

await main();
