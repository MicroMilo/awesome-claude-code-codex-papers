# Repository instructions

## Source of truth

- Edit `data/papers.yaml`; do not hand-edit generated README stats, `data/papers.json`, `website/data/catalog.json`, `papers/*.md`, or `views/*.md`.
- Update `data/schema.json` and `docs/taxonomy.md` together when adding fields, products, statuses, or method tags.
- A product mention means the complete agent or harness, not merely a model from the same vendor.

## Evidence rules

- Prefer official proceedings, DOI, OpenReview, arXiv, and author-maintained artifacts.
- Record paper claims as claims; do not silently convert them into universal conclusions.
- Use `unknown` when model or budget parity is not established.
- Keep direct, related, evaluation-only, and historical entries separate.
- Never commit paper PDFs.

## Commands

```bash
python -m pip install -r requirements-dev.txt
make build
make check
npm --prefix website install
make site-check
```

Run `make build` after catalog edits and include all generated changes in the same commit.
The website reads the generated `website/data/catalog.json`; never maintain a second paper list in the frontend.
