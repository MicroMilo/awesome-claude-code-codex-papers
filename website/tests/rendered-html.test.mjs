import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render(url = "https://papers.example.test/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  const requestUrl = new URL(url);

  return worker.fetch(
    new Request(url, {
      headers: {
        accept: "text/html",
        host: requestUrl.host,
        "x-forwarded-host": requestUrl.host,
        "x-forwarded-proto": requestUrl.protocol.slice(0, -1),
      },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the finished research catalog", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Awesome Claude Code &amp; Codex Papers<\/title>/i);
  assert.match(html, /What actually beats/);
  assert.match(html, /Claude Code &amp; Codex\?/);
  assert.match(html, /QLCoder/);
  assert.match(html, /Star the repository/);
  assert.match(html, /https:\/\/github\.com\/MicroMilo\/awesome-claude-code-codex-papers/);
  assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Your site is taking shape/i);
});

test("emits host-aware social metadata", async () => {
  const response = await render("https://catalog.example.org/");
  const html = await response.text();

  assert.match(
    html,
    /<meta[^>]+property="og:image"[^>]+content="https:\/\/catalog\.example\.org\/og\.png"/i,
  );
  assert.match(html, /<meta[^>]+name="twitter:card"[^>]+content="summary_large_image"/i);
  assert.match(
    html,
    /<meta[^>]+name="twitter:image"[^>]+content="https:\/\/catalog\.example\.org\/og\.png"/i,
  );
});

test("site catalog mirrors the repository JSON export", async () => {
  const [siteCatalog, repositoryCatalog] = await Promise.all([
    readFile(new URL("../data/catalog.json", import.meta.url), "utf8"),
    readFile(new URL("../../data/papers.json", import.meta.url), "utf8"),
  ]);

  assert.deepEqual(JSON.parse(siteCatalog), JSON.parse(repositoryCatalog));
});
