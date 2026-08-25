# Contributing

Thank you for helping maintain an accurate, evidence-first catalog of research on production coding agents.

## Scope gate

A paper belongs in the main catalog only when all of these conditions hold:

1. It is a formally accepted 2026 paper in one of the conference series listed in `docs/taxonomy.md`.
2. Its primary URL is an official conference page, proceedings page, conference OpenReview record, or publisher record.
3. It actually runs or evaluates Claude Code or Codex CLI as a product-level agent harness.
4. The full text, appendix, and available artifact have been checked for the claimed product, model, configuration, and evidence location.

Qualifying uses include a product baseline, product-level evaluation, benchmark, empirical analysis, or a method that wraps, configures, improves, or competes with the product.

The following do **not** qualify by themselves:

- an arXiv-only preprint;
- a title or abstract that merely mentions a product;
- use of a Claude or GPT-family API model inside a custom scaffold;
- use of the historical OpenAI Codex model without Codex CLI;
- a citation, related-work mention, authoring acknowledgement, or artifact instruction.

If formal acceptance, first-party full text, or product-level context cannot be verified, keep the record `pending` in the conference census and record the blocker. Do not promote it to `data/papers.yaml`.

## Primary-source policy

Use sources in this order:

1. official conference or proceedings record;
2. official conference OpenReview record;
3. formal publisher or DOI landing page;
4. author-maintained artifact for implementation details.

An arXiv link may be preserved only as an auxiliary link. It never satisfies the main catalog's conference-source requirement. Blogs, search results, personal publication lists, and model cards are discovery aids, not evidence for acceptance or experimental claims.

## Adding or correcting a paper

1. Search `data/audit/2026-conference-census/` for the official-list record before creating a new one.
2. Confirm the title, authors, conference, track, acceptance status, and primary URL against a first-party source.
3. Check the paper body, tables, footnotes, appendix, supplement, and available artifact.
4. Record exact product model strings and snapshots without shortening them.
5. Record product/CLI version, reasoning mode, budgets, run count, tool permissions, and baseline configuration. Use `not-reported` or `unknown` only after checking all available primary material.
6. Give a section, table, figure, appendix, or artifact path in `evidence.source_location`.
7. Update the census disposition and reason. Add the paper to `data/papers.yaml` only after it passes the scope gate.
8. Run `make build`, `make check`, and `make site-check`.

Do not manually edit content between the `CATALOG:STATS` or `CATALOG:COVERAGE` markers in either README. Files under `papers/` and `views/`, plus `data/papers.json` and `website/data/catalog.json`, are generated from `data/papers.yaml`.

## Evidence classes

- `direct`: a numeric head-to-head comparison with Claude Code or Codex CLI.
- `related`: relevant product-level or component evidence without a clean numeric head-to-head.
- `evaluation`: a benchmark or empirical evaluation of the product without a proposed improvement method.

`direct` means a comparison exists; it does not mean the comparison is fair. Never infer same-model or same-budget parity. Preserve `unknown` and explain confounders in `evidence.caveats`.

## Canonical product names

- `claude-code`
- `codex-cli`

Additional industrial products require an explicit scope decision plus coordinated updates to the schema, taxonomy, validators, website, and census workflow.

## Pull request checklist

- [ ] The paper passes every scope-gate condition.
- [ ] The primary paper URL is an official 2026 conference source, not arXiv.
- [ ] Product use is verified from full-text context rather than a name match.
- [ ] Quantitative claims match the cited source location.
- [ ] Exact model strings, version, budget, tools, and runs are recorded or explicitly unavailable.
- [ ] Conference, venue, domains, classification, and comparison scope follow the taxonomy.
- [ ] The conference census carries a matching disposition and reason.
- [ ] Comparison caveats are explicit.
- [ ] No copyrighted paper PDF has been committed.
- [ ] `make check` and `make site-check` pass.
