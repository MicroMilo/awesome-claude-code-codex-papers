import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { renderToStaticMarkup } from "react-dom/server";
import { CatalogExplorer, type Paper } from "../app/CatalogExplorer";
import { InsightsPage } from "../app/InsightsPage";
import catalog from "../data/catalog.json";
import { INSIGHT_DEFINITIONS } from "../data/insights";
import pendingSummary from "../data/pending-summary.json";

test("renders the complete research catalog", () => {
  const html = renderToStaticMarkup(
    <CatalogExplorer
      papers={catalog.papers as Paper[]}
      reviewedAt={catalog.reviewed_at}
    />,
  );

  assert.match(html, /What actually beats/);
  assert.match(html, /Claude Code &amp; Codex\?/);
  assert.match(html, /QLCoder/);
  assert.match(html, /What the catalog covers/);
  assert.match(html, /Read the synthesis/);
  assert.match(html, /\.\/insights\//);
  assert.match(html, /Research domains/);
  assert.match(html, /Software Engineering/);
  assert.match(html, /ICLR/);
  assert.match(html, /Terminal-Bench/);
  assert.match(html, /Models used/);
  assert.match(html, /Claude Sonnet 4/);
  assert.match(html, /GPT-5/);
  assert.match(html, /gpt-5\.2-2025-12-11/);
  assert.doesNotMatch(html, /control-strip|fairness-section/);
  assert.doesNotMatch(
    html,
    /A direct comparison is not automatically a fair comparison/,
  );
  assert.match(html, /Star the repository/);
  assert.match(
    html,
    /https:\/\/github\.com\/MicroMilo\/awesome-claude-code-codex-papers/,
  );
});

test("maps every insight to real catalog evidence", () => {
  const catalogIds = new Set(catalog.papers.map((paper) => paper.id));
  const mappedIds = new Set(
    INSIGHT_DEFINITIONS.flatMap((insight) =>
      insight.evidence.map((evidence) => evidence.paperId),
    ),
  );

  assert.equal(INSIGHT_DEFINITIONS.length, 6);
  assert.ok(
    INSIGHT_DEFINITIONS.every(
      (insight) => insight.evidence.length > 0 && insight.caution.en.length > 0,
    ),
  );
  assert.deepEqual([...mappedIds].sort(), [...catalogIds].sort());
});

test("renders a paper-traceable insights report", () => {
  const html = renderToStaticMarkup(
    <InsightsPage
      papers={catalog.papers as Paper[]}
      reviewedAt={catalog.reviewed_at}
      pendingSummary={pendingSummary}
    />,
  );

  assert.match(html, /Where coding agents/);
  assert.match(html, /Long-horizon work breaks at interfaces/);
  assert.match(html, /Paper evidence trail/);
  assert.match(html, /FeatureBench/);
  assert.match(html, /11\.0% for Claude Code and 12\.5% for Codex/);
  assert.match(html, /gpt-5\.2-2025-12-11/);
  assert.match(html, /context only/);
  assert.match(html, /Do not turn this page into a vendor leaderboard/);
  assert.match(html, /same-budget comparisons/);
  assert.match(html, /Pending means blocked/);
  assert.match(html, />701</);
  assert.match(html, /APE-Bench/);
  assert.match(html, /first-party full-text endpoint returned an HTTP 403/);
  assert.match(html, /Star the repository/);
});

test("keeps the website pending queue synchronized and first-party only", () => {
  assert.equal(pendingSummary.pending_record_count, 701);
  assert.equal(pendingSummary.high_priority_product_candidate_count, 8);
  assert.equal(
    Object.values(pendingSummary.blocker_counts).reduce(
      (total, count) => total + count,
      0,
    ),
    pendingSummary.pending_record_count,
  );
  assert.ok(
    pendingSummary.high_priority_product_candidates.every(
      (paper) => !paper.official_url.includes("arxiv.org"),
    ),
  );
});

test("ships filterable domain and conference metadata for every paper", () => {
  const papers = catalog.papers as Paper[];

  assert.ok(papers.length > 0);
  assert.equal(
    papers.filter((paper) => paper.year === 2026).length,
    papers.length,
  );
  assert.ok(papers.every((paper) => paper.conference.length > 0));
  assert.ok(papers.every((paper) => paper.domains.length > 0));
  assert.ok(papers.every((paper) => !paper.paper_url.includes("arxiv.org")));
});

test("ships GitHub Pages metadata without OpenAI hosting references", async () => {
  const html = await readFile(new URL("../dist/index.html", import.meta.url), "utf8");
  const insightsHtml = await readFile(
    new URL("../dist/insights/index.html", import.meta.url),
    "utf8",
  );

  assert.match(html, /<title>Awesome Claude Code &amp; Codex Papers<\/title>/i);
  assert.match(
    html,
    /https:\/\/micromilo\.github\.io\/awesome-claude-code-codex-papers\/og\.png/,
  );
  assert.doesNotMatch(html, /chatgpt\.site|openai|vinext|wrangler/i);
  assert.match(
    insightsHtml,
    /<title>Insights: Where Claude Code &amp; Codex Break<\/title>/i,
  );
  assert.match(
    insightsHtml,
    /awesome-claude-code-codex-papers\/insights\//,
  );
  assert.doesNotMatch(insightsHtml, /chatgpt\.site|vinext|wrangler/i);
});

test("site catalog mirrors the repository JSON export", async () => {
  const repositoryCatalog = JSON.parse(
    await readFile(new URL("../../data/papers.json", import.meta.url), "utf8"),
  );

  assert.deepEqual(catalog, repositoryCatalog);
});
