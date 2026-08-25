<p align="center">
  <img src="assets/hero.png" alt="Coding-agent experiments flowing through an evidence graph into research papers" width="100%">
</p>

<h1 align="center">Awesome Claude Code & Codex Papers</h1>

<p align="center">
  <strong>Research that measures, analyzes, or beats real production coding agents.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://micromilo.github.io/awesome-claude-code-codex-papers/"><img alt="Open website" src="https://img.shields.io/badge/open-interactive%20website-f16f51?style=for-the-badge"></a>
  <a href="https://micromilo.github.io/awesome-claude-code-codex-papers/methods/"><img alt="Compare methods" src="https://img.shields.io/badge/compare-methods%20%2B%20evidence-4bcbd5?style=for-the-badge"></a>
  <a href="https://micromilo.github.io/awesome-claude-code-codex-papers/insights/"><img alt="Read insights" src="https://img.shields.io/badge/read-evidence%20insights-4bcbd5?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml"><img alt="Validate catalog" src="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml/badge.svg"></a>
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MicroMilo/awesome-claude-code-codex-papers?style=flat&logo=github&color=f16f51"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-4bcbd5"></a>
  <a href="CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-f16f51"></a>
  <a href="data/papers.yaml"><img alt="Data YAML" src="https://img.shields.io/badge/catalog-YAML%20%2B%20JSON-2563eb"></a>
</p>

<!-- CATALOG:STATS:START -->
<p align="center">
  <img alt="papers: 13" src="https://img.shields.io/badge/papers-13-16616a">
  <img alt="official records indexed: 18,269" src="https://img.shields.io/badge/official%20records%20indexed-18%2C269-0f766e">
  <img alt="direct comparisons: 5" src="https://img.shields.io/badge/direct%20comparisons-5-dc6b46">
  <img alt="official artifacts: 10" src="https://img.shields.io/badge/official%20artifacts-10-2563eb">
  <img alt="domains: 7" src="https://img.shields.io/badge/domains-7-4bcbd5">
  <img alt="conference series tracked: 13" src="https://img.shields.io/badge/conference%20series%20tracked-13-7c3aed">
  <img alt="reviewed: 2026-08-25" src="https://img.shields.io/badge/reviewed-2026--08--25-475569">
</p>
<!-- CATALOG:STATS:END -->

## Coverage at a glance

<!-- CATALOG:COVERAGE:START -->
<p align="center">
  <a href="views/by-domain.md"><strong>Research domains</strong></a><br>
  <code>Software Engineering · 7</code> · <code>Security · 3</code> · <code>Systems & Performance · 1</code> · <code>Machine Learning · 4</code> · <code>Scientific Computing · 3</code> · <code>Web & UI · 1</code> · <code>Documents · 1</code><br><br>
  <a href="views/by-conference.md"><strong>Conferences / sources</strong></a><br>
  <code>ICLR · 12</code> · <code>ICML · 1</code>
</p>
<!-- CATALOG:COVERAGE:END -->

This repository is the open data and maintenance layer behind the **web-first research catalog**. The main catalog is restricted to **2026 papers with an official conference, proceedings, or OpenReview conference record** that evaluate, analyze, or outperform **Claude Code** and **Codex CLI** as complete products—not papers that merely use a Claude or GPT-family model. Every official-list record remains auditable as `included`, `excluded`, `pending`, or `duplicate`, so a compact catalog reflects strict scope rather than silent filtering.

## Start with the website

The [interactive catalog](https://micromilo.github.io/awesome-claude-code-codex-papers/) is the fastest way to:

- search systems, tasks, methods, authors, and reported results;
- choose a research domain, conference, year, product, evidence strength, exact model, or method;
- inspect baseline models, versions, budgets, evidence locations, and caveats;
- switch between English and Chinese without reading giant Markdown tables.

The separate [evidence insights page](https://micromilo.github.io/awesome-claude-code-codex-papers/insights/) synthesizes where the products struggle and maps every inference back to the supporting papers, reported results, source locations, and comparison caveats.

Use the [methods matrix](https://micromilo.github.io/awesome-claude-code-codex-papers/methods/) to compare interventions without separating results from their controls, or reuse the [official-conference census skill](https://micromilo.github.io/awesome-claude-code-codex-papers/skill/) to build another auditable venue-wide scan.

## Evidence standard

This is not a leaderboard. Product versions, backbone models, budgets, tools, and task domains often differ. Every entry separates the paper's reported result from our comparison controls and caveats. Missing details stay explicitly `unknown`.

For raw or generated research material, use the [paper dossiers](papers/README.md), [domain view](views/by-domain.md), [conference view](views/by-conference.md), [machine-readable JSON](data/papers.json), or the [full 2026 conference census](docs/2026-conference-census.md).

## Contributing

[Suggest a paper](https://github.com/MicroMilo/awesome-claude-code-codex-papers/issues/new?template=paper.yml), correct an evidence record, join a [research discussion](https://github.com/MicroMilo/awesome-claude-code-codex-papers/discussions), or read [CONTRIBUTING.md](CONTRIBUTING.md). The catalog is generated from `data/papers.yaml` and validated in CI.

---

<p align="center">
  <strong>Did this save you a paper-reading session?</strong><br>
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers/stargazers">Star the repository ★</a> — it helps more researchers find the evidence.
</p>
