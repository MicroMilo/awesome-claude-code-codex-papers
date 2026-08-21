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
</p>

<p align="center">
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml"><img alt="Validate catalog" src="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-22c55e"></a>
  <a href="CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen"></a>
  <a href="data/papers.yaml"><img alt="Data YAML" src="https://img.shields.io/badge/catalog-YAML%20%2B%20JSON-2563eb"></a>
</p>

<!-- CATALOG:STATS:START -->
<p align="center">
  <img alt="papers: 19" src="https://img.shields.io/badge/papers-19-0f766e">
  <img alt="direct comparisons: 13" src="https://img.shields.io/badge/direct%20comparisons-13-dc6b46">
  <img alt="official artifacts: 11" src="https://img.shields.io/badge/official%20artifacts-11-2563eb">
  <img alt="venues: 7" src="https://img.shields.io/badge/venues-7-7c3aed">
  <img alt="reviewed: 2026-08-21" src="https://img.shields.io/badge/reviewed-2026--08--21-475569">
</p>
<!-- CATALOG:STATS:END -->

This repository is the open data and maintenance layer behind the **web-first research catalog**. It covers papers that evaluate, analyze, or outperform **Claude Code** and **Codex CLI** as complete products—not papers that merely use a Claude or GPT-family model.

## Start with the website

The [interactive catalog](https://micromilo.github.io/awesome-claude-code-codex-papers/) is the fastest way to:

- search systems, tasks, methods, authors, and reported results;
- filter by product, evidence class, venue, method, and comparison fairness;
- inspect baseline models, versions, budgets, evidence locations, and caveats;
- switch between English and Chinese without reading giant Markdown tables.

## Evidence standard

This is not a leaderboard. Product versions, backbone models, budgets, tools, and task domains often differ. Every entry separates the paper's reported result from our comparison controls and caveats. Missing details stay explicitly `unknown`.

For raw or generated research material, use the [paper dossiers](papers/README.md), [method view](views/by-method.md), [fair-comparison view](views/fair-comparisons.md), or [machine-readable JSON](data/papers.json).

## Contributing

[Suggest a paper](https://github.com/MicroMilo/awesome-claude-code-codex-papers/issues/new?template=paper.yml), correct an evidence record, or read [CONTRIBUTING.md](CONTRIBUTING.md). The catalog is generated from `data/papers.yaml` and validated in CI.

---

<p align="center">
  <strong>Did this save you a paper-reading session?</strong><br>
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers">Star the repository ★</a> — it helps more researchers find the evidence.
</p>
