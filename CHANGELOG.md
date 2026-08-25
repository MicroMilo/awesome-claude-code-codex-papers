# Changelog

All notable catalog and schema changes are recorded here.

## [Unreleased]

### Planned

- Deeper audits of product versions, model snapshots, and execution budgets
- Additional official artifacts and evidence anchors

## [0.2.0] — 2026-08-25

### Added

- Auditable 2026 conference census covering 18,269 official-list records across 13 registered conference series
- Per-conference census files with checksums, explicit dispositions, exclusion reasons, and pending blockers
- Metadata-first screening and selective full-text analysis for ICLR, ICML, AAAI, Researchr, and proceedings sources
- Interactive bilingual catalog with conference, year, domain, product, evidence, model, venue, and method filters
- Evidence-backed insights page linking every synthesis claim to paper records and source locations
- Expandable evidence dossiers, pending-evidence queue, and recurring-method summaries
- GitHub Pages deployment, social-sharing metadata, community templates, and public contribution routes

### Changed

- Upgraded the catalog schema to version 3 and restricted the main catalog to formally accepted 2026 conference papers
- Made official conference, proceedings, OpenReview conference, or publisher records mandatory primary sources
- Split the 52 MB monolithic census into reviewable per-conference files
- Preserved exact model snapshots, experiment budgets, tool permissions, and comparison caveats when reported

### Removed

- arXiv-only papers from the main catalog
- Historical OpenAI Codex model-only records and filters from the product-level catalog

## [0.1.0] — 2026-08-21

### Added

- Initial Claude Code and Codex CLI scope
- Nineteen reviewed seed papers
- YAML catalog, JSON Schema, and generated JSON export
- Per-paper evidence dossiers and research views
- English and Simplified Chinese READMEs
- Automated generation, validation, tests, linting, and GitHub Actions
- Weekly arXiv candidate discovery with deduplication and bounded issue reports
- Contribution, citation, security, and community guidance

[Unreleased]: https://github.com/MicroMilo/awesome-claude-code-codex-papers/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/MicroMilo/awesome-claude-code-codex-papers/releases/tag/v0.2.0
[0.1.0]: https://github.com/MicroMilo/awesome-claude-code-codex-papers/releases/tag/v0.1.0
