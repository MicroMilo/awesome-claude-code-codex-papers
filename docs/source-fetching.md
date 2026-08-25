# Official source fetching

The repository separates source acquisition from catalog promotion. A fetch
failure is a `pending` source record, never an exclusion.

It also separates two kinds of provenance. The official conference,
proceedings, OpenReview, or publisher record establishes acceptance and stays
in `paper_url`. Abstract/full-text bytes may come from that source or from an
OpenAlex-resolved or manually reviewed open copy. Auxiliary copies are usable
only after an explicit DOI or reviewed bibliographic identity match; their
URL, version, identity method, and retrieval hash remain in the audit ledger.
For a renamed accepted paper, the mapping must preserve both titles and match
the complete author list plus the abstract, method, datasets, and exact results.
Title similarity by itself is never sufficient.

## ICLR 2026

The main-paper authority is the official proceedings book. The Downloads page
is used for track-aware event exports, and OpenReview API v2 is optional
enrichment for metadata, reviews, and attachments.

Run a safe metadata-only smoke test:

```bash
python scripts/fetch_iclr_sources.py \
  --source proceedings \
  --metadata-only \
  --limit 3
```

Fetch the proceedings index and the first three official paper pages:

```bash
python scripts/fetch_iclr_sources.py \
  --source proceedings \
  --limit 3
```

The paper pages expose the official abstracts. When `--fetch-pdfs` is used,
the default `--pdf-scope metadata` checks the title and abstract first and
downloads only high-recall candidates. The screen is intentionally broad and
transparent; it is a cost-saving triage step, not the final product-level
evidence decision. A missing abstract is `pending`, never an exclusion.

Download the first three official PDFs as well:

```bash
python scripts/fetch_iclr_sources.py \
  --source proceedings \
  --limit 3 \
  --fetch-pdfs
```

Force a full-PDF acquisition when an audit explicitly requires it:

```bash
python scripts/fetch_iclr_sources.py \
  --source proceedings \
  --fetch-pdfs \
  --pdf-scope all
```

The full-text scanner applies the same gate to ICLR records. Use
`--pdf-scope all` there too for a deliberate PDF-first pass.

If a first-party host is already returning explicit browser-verification
challenges, finish only records that have not yet been attempted:

```bash
python scripts/scan_conference_fulltext.py \
  --conference ICML \
  --pdf-only \
  --skip-known-challenges
```

This option reuses the append-only scan ledger; it does not turn a challenge
into an exclusion and does not bypass the challenge.

For a resumable batch run, combine `--offset` and `--limit`; the output
inventory still contains all 5,351 official records, while only the selected
slice makes network requests:

```bash
python scripts/fetch_iclr_sources.py \
  --source proceedings \
  --offset 1000 \
  --limit 250 \
  --fetch-pdfs
```

Fetch a machine-readable official track export:

```bash
python scripts/fetch_iclr_sources.py \
  --source downloads \
  --track posters
```

The durable manifest is `data/audit/2026-source-fetch.jsonl`. Raw HTML,
exports, partial files, and PDFs live under `tmp/crawl/` and are ignored by
Git. Each source record contains the official URL, status, HTTP metadata,
SHA256, byte count, attempts, and local snapshot path.

## Researchr / SIGPLAN extensions

PLDI, POPL, and OOPSLA use their official Researchr/SIGPLAN accepted-paper
pages. Refresh those lists without rebuilding or discarding the existing audit:

```bash
python scripts/refresh_researchr_extensions.py
```

Then fetch official abstracts and apply the metadata-first screen. Only
candidates proceed to first-party PDF discovery:

```bash
python scripts/enrich_official_metadata.py \
  --conference PLDI --conference POPL --conference OOPSLA
python scripts/scan_conference_fulltext.py \
  --conference PLDI --conference POPL --conference OOPSLA
```

For unresolved candidates, the PDF enricher inspects only pending records. An
ACM DOI is deterministically mapped to its `dl.acm.org` PDF endpoint; the
scanner still verifies the response before any exclusion is made:

```bash
python scripts/enrich_official_pdf_urls.py \
  --conference PLDI --conference POPL --conference OOPSLA \
  --pending-only
```

An ACM browser-verification response remains an explicit
`official-source-challenge`. It is not retried through challenge-bypass tools
and never triggers bulk scraping. A separately identity-verified open copy may
still provide content while the ACM DOI remains the acceptance authority.

## IJCAI, KDD, and NeurIPS

Refresh the official IJCAI track pages, both KDD paper cycles, and the NeurIPS
OpenReview publication flag without resetting earlier review decisions:

```bash
python scripts/refresh_official_list_extensions.py
```

IJCAI's official accepted-paper pages expose abstracts and conference-hosted
PDFs, so the normal metadata-first scanner can complete the high-recall pass.
KDD's official paper page exposes titles, authors, tracks, and ACM DOIs but no
abstracts. Resolve those official DOIs in batches before requesting any PDF:

```bash
python scripts/enrich_scholarly_content.py --conference KDD
python scripts/scan_conference_fulltext.py \
  --conference KDD --verified-content-only
```

The first command checkpoints OpenAlex results in
`data/audit/2026-scholarly-content.jsonl`, reconstructs DOI-bound abstracts,
and applies reviewed candidate overrides from
`data/audit/content-source-overrides.yaml`. The second command downloads only
metadata-selected candidates with verified open content. It does not crawl ACM
systematically. Missing abstracts or unresolved candidate full text remain
pending.

NeurIPS remains conference-level pending until its official OpenReview group
releases a public accepted-paper list.

## Failure policy

- 408, 425, 429, 5xx, and transport failures use bounded exponential backoff.
- `Retry-After` is honored when provided.
- Downloads resume from `.part` files and replace the final file atomically.
- First-party challenge/CAPTCHA responses (including OpenReview and ACM) are
  recorded as `pending`.
- Proxy rotation and CAPTCHA bypass are not part of the acquisition layer.
- An open copy can supply content only after identity verification; it can
  never substitute for an official acceptance record.

The shared implementation is in `scripts/source_fetcher.py`; venue-specific
logic is in `scripts/fetch_iclr_sources.py`, DOI-bound open-content enrichment
is in `scripts/enrich_scholarly_content.py`, and the deterministic
title/abstract policy is in `scripts/metadata_relevance.py`. Run
`scripts/update_pending_review.py` after a retry pass to update the compact
blocker summary and high-priority direct-product queue.
