# Research catalog website

Static Vite front end for the evidence catalog in `../data/papers.yaml`,
published with GitHub Pages.

The site provides full-text search, product and evidence filters, method views,
expandable paper dossiers, English/Chinese UI, and a dedicated `/insights/`
report that maps every synthesis claim back to paper-level results, source
locations, and caveats.

`../scripts/build_readme.py` generates `data/catalog.json`; do not edit that
file by hand.

```bash
npm install
npm run dev
npm test
```
