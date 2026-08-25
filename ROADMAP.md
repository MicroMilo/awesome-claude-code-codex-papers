# Roadmap

The catalog optimizes for evidence quality before paper count. Checked items describe shipped, reproducible repository behavior—not aspirations.

## v0.1 — Product-level foundation

- [x] Strict product-versus-model distinction for Claude Code and Codex CLI
- [x] Machine-readable YAML, JSON Schema, and generated JSON exports
- [x] Direct, related, and evaluation evidence classes
- [x] Same-model and same-budget controls
- [x] Per-paper evidence dossiers and research views
- [x] Interactive bilingual catalog generated from the same data
- [x] Schema validation, tests, linting, and CI
- [x] Structured paper-suggestion and correction workflows

## v0.2 — Official 2026 conference census

- [x] First-party paper-list adapters for ICLR, ICML, AAAI, Researchr, and proceedings sources
- [x] Metadata-first filtering before selective full-text retrieval
- [x] Explicit `included`, `excluded`, `pending`, and `duplicate` disposition for every indexed record
- [x] Per-conference census files with checksums and a compact index
- [x] Full-text product/model extraction with evidence locations
- [x] Conference, year, domain, product, classification, evidence, and model filters
- [x] Evidence-backed insights page with paper-level provenance
- [x] Public community health files, Discussions routing, and release notes

## v0.3 — Close the evidence gaps

- [ ] Resolve first-party full-text blocks as proceedings become available
- [ ] Audit every included paper for exact CLI version, model snapshot, reasoning mode, and execution date
- [ ] Record wall-clock, turn, token, concurrency, and monetary budgets whenever reported
- [ ] Add table, figure, section, or artifact anchors for every quantitative claim
- [ ] Link official evaluation traces and datasets when available
- [ ] Add reproducibility grades separate from evidence strength
- [ ] Add a non-blocking link-health monitor

## v0.4 — Broader conference coverage

- [ ] Add stable official-list adapters for NeurIPS, IJCAI, and KDD when complete 2026 sources are released
- [ ] Add additional software-engineering and code-intelligence CCF-A venues with first-party sources
- [ ] Detect duplicate OpenReview, DOI, and final-proceedings records automatically
- [ ] Publish a small release for every audited catalog update

## Future product expansion

Expansion requires enough product-level conference research to justify a maintained category. Candidates include Kimi Code, Zed, Cursor, Gemini CLI, GitHub Copilot CLI, and OpenCode.

Model-only papers remain out of scope unless they evaluate the corresponding industrial product harness directly.

## Long-term

- Reproduction packs for a small set of high-impact claims
- Community-maintained venue watchlists and artifact-status audits
- Stable dataset releases suitable for citation and downstream analysis
