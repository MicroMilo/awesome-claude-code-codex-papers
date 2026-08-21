# Roadmap

The catalog optimizes for evidence quality before paper count.

## v0.1 — Claude Code and Codex foundation

- [x] Strict product-versus-model distinction
- [x] Machine-readable YAML and JSON catalog
- [x] Direct, related, evaluation-only, and historical evidence classes
- [x] Same-model and same-budget controls
- [x] Per-paper evidence dossiers
- [x] Product, method, venue, and fairness views
- [x] English and Simplified Chinese entry points
- [x] Schema, tests, linting, and CI
- [x] Structured paper-suggestion workflow

## v0.2 — Evidence depth

- [ ] Audit every paper for exact CLI version, model snapshot, reasoning mode, and execution date
- [ ] Record wall-clock, turn, token, concurrency, and monetary budgets when reported
- [ ] Add table, figure, or section anchors for every quantitative claim
- [ ] Link official evaluation traces and datasets when available
- [ ] Add reproducibility grades separate from evidence strength
- [ ] Add a non-blocking link-health monitor

## v0.3 — Discovery and maintenance

- [x] Weekly arXiv candidate discovery for exact product mentions
- [ ] Venue-proceedings ingestion for ICSE, FSE, ASE, ISSTA, ICLR, ICML, NeurIPS, AAAI, and security venues
- [ ] Duplicate detection across arXiv, OpenReview, DOI, and final proceedings versions
- [ ] Release notes for every catalog update

## v0.4 — Additional industrial products

Expansion requires enough product-level research to justify a maintained category. Candidate products include:

- Kimi Code
- Zed
- Cursor
- Gemini CLI
- GitHub Copilot CLI
- OpenCode

Model-only papers remain out of scope unless they study a product harness directly.

## Long-term

- Interactive static site generated from the same catalog
- Comparison matrices with matched-model and matched-budget filters
- Reproduction packs for a small set of high-impact claims
- Community-maintained venue watchlist and artifact-status audits
