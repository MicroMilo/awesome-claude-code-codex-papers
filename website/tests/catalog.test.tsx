import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { renderToStaticMarkup } from "react-dom/server";
import { CatalogExplorer, type Paper } from "../app/CatalogExplorer";
import catalog from "../data/catalog.json";

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
  assert.match(html, /Research domains/);
  assert.match(html, /Software Engineering/);
  assert.match(html, /ISSTA/);
  assert.match(html, /AgentRadio/);
  assert.match(html, /Models used/);
  assert.match(html, /Claude Sonnet 4/);
  assert.match(html, /GPT-5/);
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

test("ships filterable domain and conference metadata for every paper", () => {
  const papers = catalog.papers as Paper[];

  assert.equal(papers.length, 32);
  assert.equal(
    papers.filter((paper) => paper.year === 2026).length,
    29,
  );
  assert.ok(papers.every((paper) => paper.conference.length > 0));
  assert.ok(papers.every((paper) => paper.domains.length > 0));
});

test("ships GitHub Pages metadata without OpenAI hosting references", async () => {
  const html = await readFile(new URL("../dist/index.html", import.meta.url), "utf8");

  assert.match(html, /<title>Awesome Claude Code &amp; Codex Papers<\/title>/i);
  assert.match(
    html,
    /https:\/\/micromilo\.github\.io\/awesome-claude-code-codex-papers\/og\.png/,
  );
  assert.doesNotMatch(html, /chatgpt\.site|openai|vinext|wrangler/i);
});

test("site catalog mirrors the repository JSON export", async () => {
  const repositoryCatalog = JSON.parse(
    await readFile(new URL("../../data/papers.json", import.meta.url), "utf8"),
  );

  assert.deepEqual(catalog, repositoryCatalog);
});
