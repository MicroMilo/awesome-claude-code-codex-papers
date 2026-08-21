# Contributing

Thank you for helping maintain an accurate, evidence-first catalog of research on production coding agents.

## Inclusion criteria

A paper belongs in the catalog when at least one of the following is true:

1. It directly executes Claude Code or Codex CLI in an experiment.
2. It proposes a method that wraps, configures, improves, or competes with one of those products.
3. It introduces a benchmark or empirical study with product-level Claude Code or Codex CLI results.
4. It studies the historical OpenAI Codex model and is clearly labeled `historical`.

A paper does not belong in the primary catalog merely because it uses a Claude or GPT-family model. The product agent or harness must be part of the study.

## Evidence standard

Every entry must link to a primary source: the official proceedings page, DOI landing page, OpenReview record, arXiv record, or authors' artifact repository.

Reported results must be paraphrased accurately and accompanied by comparison caveats. Do not infer that a comparison is same-model or same-budget unless the paper explicitly establishes it.

Use these values when the paper is unclear:

```yaml
same_model: unknown
same_budget: unknown
```

## Adding a paper

1. Add one entry to `data/papers.yaml`.
2. Use a stable identifier such as `short-title-year`.
3. Record authors, identifiers, system name, artifact status, and publication date from primary sources.
4. Choose the narrowest correct evidence class and comparison scope.
5. Record where the supporting result appears in the paper.
6. Run `make build` to regenerate READMEs, JSON, views, and paper dossiers.
7. Run `make check` before opening a pull request.

Do not manually edit content between `CATALOG:*:START` and `CATALOG:*:END` markers in either README. Files under `papers/` and `views/`, plus `data/papers.json`, are also generated.

## Required source checks

- Confirm the paper title and authors against an official paper page or PDF.
- Distinguish arXiv publication dates from final venue publication.
- Confirm that an artifact repository is author-maintained before marking it `official`.
- Record the exact CLI version and model when the paper or artifact reports them.
- Identify whether the result is product-level, component-level, a configuration ablation, benchmark-only, or historical-model evidence.
- Keep missing details as `not-reported`, `not-found`, or `unknown`; absence is useful data.

## Evidence classes

- `direct`: a numeric head-to-head comparison with Claude Code or Codex CLI.
- `related`: relevant product-level evidence, but not a clean numeric head-to-head.
- `evaluation`: product evaluation without a proposed improvement method.
- `historical`: pre-CLI OpenAI Codex model research.

## Product naming

Use canonical identifiers:

- `claude-code`
- `codex-cli`
- `openai-codex-model` for historical model-only work

Future products must be added to both `data/schema.json` and `docs/taxonomy.md` before use.

## Pull request checklist

- [ ] The paper satisfies the inclusion criteria.
- [ ] All quantitative claims match the cited primary source.
- [ ] Model, version, budget, and tool details are recorded or marked unknown.
- [ ] Author, identifier, publication, and artifact fields come from primary sources.
- [ ] The evidence location and comparison scope are recorded.
- [ ] Comparison caveats are explicit.
- [ ] `make check` passes.
- [ ] No copyrighted PDF has been committed.
