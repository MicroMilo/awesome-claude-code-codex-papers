<p align="center">
  <img src="assets/hero.png" alt="Coding agent 实验经过证据图谱汇入研究论文" width="100%">
</p>

<h1 align="center">Claude Code 与 Codex 研究论文精选</h1>

<p align="center">
  <strong>专门收录评测、分析或超越真实工业 coding agent 的研究。</strong>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://micromilo.github.io/awesome-claude-code-codex-papers/"><img alt="打开网站" src="https://img.shields.io/badge/打开-可交互论文网站-f16f51?style=for-the-badge"></a>
  <a href="https://micromilo.github.io/awesome-claude-code-codex-papers/insights/"><img alt="阅读洞察" src="https://img.shields.io/badge/阅读-证据洞察-4bcbd5?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml"><img alt="目录校验" src="https://github.com/MicroMilo/awesome-claude-code-codex-papers/actions/workflows/validate.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-4bcbd5"></a>
  <a href="CONTRIBUTING.md"><img alt="欢迎 PR" src="https://img.shields.io/badge/PRs-welcome-f16f51"></a>
  <a href="data/papers.yaml"><img alt="YAML 数据" src="https://img.shields.io/badge/catalog-YAML%20%2B%20JSON-2563eb"></a>
</p>

<!-- CATALOG:STATS:START -->
<p align="center">
  <img alt="papers: 13" src="https://img.shields.io/badge/papers-13-16616a">
  <img alt="direct comparisons: 5" src="https://img.shields.io/badge/direct%20comparisons-5-dc6b46">
  <img alt="official artifacts: 10" src="https://img.shields.io/badge/official%20artifacts-10-2563eb">
  <img alt="domains: 7" src="https://img.shields.io/badge/domains-7-4bcbd5">
  <img alt="conference groups: 2" src="https://img.shields.io/badge/conference%20groups-2-7c3aed">
  <img alt="reviewed: 2026-08-24" src="https://img.shields.io/badge/reviewed-2026--08--24-475569">
</p>
<!-- CATALOG:STATS:END -->

## 收录范围一览

<!-- CATALOG:COVERAGE:START -->
<p align="center">
  <a href="views/by-domain.md"><strong>研究领域</strong></a><br>
  <code>软件工程 · 7</code> · <code>安全 · 3</code> · <code>系统与性能 · 1</code> · <code>机器学习 · 4</code> · <code>科学计算 · 3</code> · <code>Web 与 UI · 1</code> · <code>文档 · 1</code><br><br>
  <a href="views/by-conference.md"><strong>会议 / 来源</strong></a><br>
  <code>ICLR · 12</code> · <code>ICML · 1</code>
</p>
<!-- CATALOG:COVERAGE:END -->

这个仓库是**网页优先论文目录**背后的开放数据与维护层。主目录只收录**2026 年、拥有正式会议 / proceedings / OpenReview 会议记录**，并且把 **Claude Code** 或 **Codex CLI** 当作完整产品进行评测、分析或超越的论文；只使用 Claude 或 GPT 系列模型的论文不会混入主目录。

## 先看网站

[可交互论文目录](https://micromilo.github.io/awesome-claude-code-codex-papers/)适合直接：

- 搜索系统、任务、方法、作者和论文结果；
- 按研究领域、会议、年份、产品、证据强度、精确模型和方法筛选；
- 查看 baseline 模型、版本、预算、证据位置和限制；
- 在中英文之间切换，不再阅读超长 Markdown 表格。

独立的[证据洞察页](https://micromilo.github.io/awesome-claude-code-codex-papers/insights/)会综合这些产品的薄弱能力，并把每条推理直接映射到支撑论文、原始结果、证据位置与对比限制。

## 证据标准

这不是排行榜。产品版本、底层模型、预算、工具权限和任务领域经常不同。每条记录都会分开呈现论文报告的结果、实验控制和限制；论文没写清的内容会保留为 `unknown`。

需要原始或生成资料时，可以查看[论文证据页](papers/README.md)、[按领域浏览](views/by-domain.md)、[按会议浏览](views/by-conference.md)、[机器可读 JSON](data/papers.json)或[2026 会议全量审计报告](docs/2026-conference-census.md)。

## 参与贡献

可以直接[推荐论文](https://github.com/MicroMilo/awesome-claude-code-codex-papers/issues/new?template=paper.yml)、修正证据记录，或阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。目录由 `data/papers.yaml` 自动生成并通过 CI 校验。

---

<p align="center">
  <strong>这个目录帮你省下了一轮翻论文的时间吗？</strong><br>
  <a href="https://github.com/MicroMilo/awesome-claude-code-codex-papers">去仓库点个 Star ★</a>，让更多研究者找到这些证据。
</p>
