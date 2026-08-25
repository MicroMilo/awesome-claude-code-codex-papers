---
name: official-conference-paper-census
description: Build or audit a reproducible official-conference census, then resolve identity-verified abstracts/full text for metadata-first screening, exact model/configuration evidence, and included/excluded/pending/duplicate dispositions. Use for conference-wide paper collection across ICLR, ASE, FSE, ISSTA, ICSE, ICML, AAAI, KDD, or another venue with an official paper list.
---

# Official Conference Paper Census

Use this skill to turn an official conference listing into an auditable dataset. Keep two authorities separate:

- **Acceptance authority:** the conference website, official proceedings, official publisher, or official OpenReview conference record. This determines venue identity and the primary `paper_url`.
- **Content evidence:** the official PDF when available, otherwise an OpenAlex-resolved repository copy or a reviewed arXiv/institutional copy that is identity-matched to the official record. This supplies abstract/full-text bytes only and never proves acceptance.

An arXiv-only paper is never eligible for the main catalog.

## Workflow

1. Freeze the current catalog and inspect the repository schema before changing data.
2. Capture the official conference entry point, fetched timestamp, track names, published count, and source URL.
3. Prefer an official machine-readable export. For ICLR, use `scripts/export_iclr_downloads.py`; the official [ICLR Downloads 2026](https://iclr.cc/Downloads/2026) form supports JSON/CSV/XLSX/YAML and independent track selection. Record the Downloads event total separately from the main-conference proceedings total because the page mixes posters, tutorials, invited talks, workshops, and demonstrations.
4. Check [references/conference-support.md](references/conference-support.md) before choosing an adapter. Use the venue adapter already present in `scripts/build_conference_census.py` or add a small official-source adapter. It must preserve the conference's own track labels and use a first-party page, proceedings record, official publisher page, or official OpenReview record as the source of truth. For Researchr venues (ASE/FSE/ISSTA/ICSE/PLDI/POPL/OOPSLA), the accepted-paper page is the census and the official event-details AJAX response is the abstract source. For ICML, use the official poster page; for AAAI, use the official OJS article page. Store source hashes, response metadata, raw snapshots where practical, and an append-only JSONL ledger. Per-host concurrency and pacing must be bounded; challenge pages are recorded as `pending` and are never bypassed.
   If a first-party host fails only because the local HTTP proxy cannot complete its TLS connection, retry through a direct connection for that exact host (for example with a narrowly scoped `NO_PROXY` entry); this is transport troubleshooting, not a challenge or CAPTCHA bypass. Keep the official URL and the transport outcome in the audit ledger.
5. Normalize every official record into the census with its title, venue, year, track, official URL, full-text URL when available, and a unique key. Give every record a disposition: `included`, `excluded`, `pending`, or `duplicate`. Every non-included record needs a concrete reason.
6. Refresh Researchr track pages before doing per-paper requests: `scripts/refresh_researchr_extensions.py` merges newly exposed DOI/PDF identifiers without resetting prior review state. Then run `scripts/enrich_official_pdf_urls.py` for unresolved AAAI/ICML/Researchr/SIGPLAN candidates. ACM DOI records may be mapped to the official `dl.acm.org` PDF endpoint, but never bypass publisher challenges or bulk-download against host policy. “No PDF exposed” means only that no usable first-party link was visible at the recorded fetch time.
7. Run `scripts/enrich_official_metadata.py` first. When the official host omits metadata or blocks content, run `scripts/enrich_scholarly_content.py --conference <ID>`. It batches official DOIs through OpenAlex, reconstructs abstracts, records open locations, applies reviewed overrides from `data/audit/content-source-overrides.yaml`, and checkpoints every result in `data/audit/2026-scholarly-content.jsonl`. A DOI mismatch is rejected. A non-DOI override must bind to the exact official detail URL and record reviewed identity evidence. Prefer exact title plus authors; when a submitted manuscript and accepted paper have different titles, require a complete author match plus materially identical abstract, method, datasets, and reported results, and preserve the title-change caveat explicitly.
8. Run `scripts/scan_conference_fulltext.py` in batches. The default is metadata-first: an identity-bound title/abstract filters clearly unrelated records before any PDF request, while candidates enter the PDF queue. For publisher-constrained venues, use `--verified-content-only` so only resolved open copies are requested. Use `--pdf-scope all` only for an explicitly documented full-PDF pass. Store source identity, version, retrieval hash, extraction status, page/snippet evidence, and model candidates in `data/audit/2026-fulltext-scan.jsonl`; do not commit PDFs. Resume from the JSONL checkpoint.
9. Review every product hit in context. Search the full text, appendix, tables, footnotes, supplementary material, and artifact documentation for `Claude Code`, `Claude-Code`, `Claude Code CLI`, `Codex CLI`, `Codex-CLI`, `Repo Codex`, `OpenAI Codex`, `Codex agent`, and `coding agent`. A paper using a Claude or GPT API is not automatically a paper about Claude Code or Codex CLI.
10. Extract the paper's original model string and configuration. Preserve snapshots such as `gpt-5.2-2025-12-11` verbatim; record `not-reported` only after the full text and available artifact have been checked. Save the section/page/table/appendix location for each claim.
11. Review recall-oriented product hits with `scripts/review_iclr_product_hits.py` or `scripts/review_other_product_hits.py` so references and ancillary author assistance become excluded records with reasons rather than silent omissions. If a venue has unreviewed product hits, stop promotion and add an explicit review mapping.
12. Before promotion, run `scripts/update_pending_review.py`. It identifies direct product signals in identity-bound titles/abstracts, records whether content is unresolved, challenged, or awaiting scanning, and writes `data/audit/2026-pending-summary.json`. A high-priority pending record is still pending; title/abstract evidence alone never qualifies it for the catalog.
13. Promote only records that have an exact official record and reviewed product-level evidence. Run `scripts/finalize_catalog_audit.py`, then generate `docs/2026-conference-census.md` with `scripts/build_audit_report.py`.

The census is stored under `data/audit/2026-conference-census/`: `index.yaml` contains ordered file references, counts, and SHA-256 checksums; each conference has its own YAML file. Always read and write it through `scripts/census_store.py` so index hashes remain synchronized.

## Metadata-first decision rule

Use the following state machine for each official record:

```text
official title + identity-bound abstract
        │
        ├─ no relevant signal ──> metadata-filtered / excluded; no PDF request
        ├─ relevant signal ─────> candidate; scan official or verified open PDF
        └─ missing or failed ──> pending; do not infer exclusion and do not bulk-download
```

The metadata screen is deliberately high recall, not the inclusion decision. A paper that only mentions a generic LLM, uses a vendor API, or cites Codex is excluded only after the relevant full-text/context rule is applied. A paper is imported only when the full text shows Claude Code/Codex CLI as a product, baseline, evaluated system, host, or product-level comparison target.

## ICLR export and failure handling

Run the official export with a bounded retry policy:

```bash
python scripts/export_iclr_downloads.py \
  --format json --track posters \
  --output tmp/census/iclr-2026-downloads.json
```

The exporter streams to `<output>.part`, validates JSON before replacement, and retries incomplete responses. If an export still fails, preserve the error and mark the affected export as `pending`; do not replace it with a search result or an arXiv list.

## Required audit invariants

- The census is complete relative to the stated official source and track scope.
- Each record has an explicit disposition and non-empty reason when excluded, pending, or duplicate.
- Included records have an official paper/proceedings/OpenReview/publisher URL and an evidence location.
- Auxiliary content has a verified identity method, source version, URL, discovery time, and retrieval hash in the scan ledger. It never becomes the primary paper URL.
- A renamed submitted manuscript is accepted as content evidence only when the audit records the old and accepted titles and multiple independent identity fields; fuzzy title similarity alone is insufficient.
- Exact model snapshots, product versions, effort/reasoning settings, budgets, runs, and tool permissions are copied from the paper; unknown values remain `not-reported`.
- A failed download or failed text extraction is `pending`, not `excluded`.
- A successful metadata screen can exclude an unrelated record without downloading its PDF; missing or failed metadata remains `pending`.
- The metadata-first policy applies to every conference. A venue-specific adapter must not silently fall back to downloading all PDFs when first-party metadata is unavailable; resolve DOI-bound metadata first.
- Main-catalog records are conference records, not arXiv-only records.
- Re-run validation and site generation after every data promotion.

## Repository entry points

- `scripts/build_conference_census.py`: collect official conference lists.
- `scripts/census_store.py`: atomically read/write the checksum-indexed per-conference census.
- `scripts/split_conference_census.py`: one-time migration from a legacy monolithic census.
- `scripts/refresh_researchr_extensions.py`: refresh and merge ASE, FSE, ISSTA, ICSE, PLDI, POPL, and OOPSLA official Researchr lists without resetting prior audit decisions.
- `scripts/refresh_official_list_extensions.py`: refresh and merge IJCAI and KDD official lists, and recheck whether NeurIPS has released public accepted submissions, without resetting prior audit decisions.
- `scripts/export_iclr_downloads.py`: stream the official ICLR event export.
- `scripts/fetch_iclr_sources.py`: acquire proceedings, track exports, and OpenReview enrichment with a resumable source ledger.
- `scripts/source_fetcher.py`: shared per-host limiter, retry policy, resumable download, hashing, and JSONL ledger primitives.
- `scripts/enrich_official_metadata.py`: fetch official abstracts for Researchr, ICML, AAAI, and other registered venue adapters before PDF scanning.
- `scripts/enrich_scholarly_content.py`: batch official DOIs through OpenAlex and attach identity-verified metadata/open content without changing venue identity.
- `data/audit/content-source-overrides.yaml`: reviewed title/author mappings for candidate-only arXiv or institutional copies.
- `scripts/record_iclr_downloads_metadata.py`: record ICLR event totals and track metadata.
- `scripts/enrich_official_pdf_urls.py`: discover first-party PDF/OpenReview links.
- `scripts/scan_conference_fulltext.py`: extract PDF text and evidence snippets.
- `scripts/update_pending_review.py`: classify unresolved blockers and build the compact priority-pending queue.
- `scripts/review_iclr_product_hits.py`: record context-level decisions for recall-oriented ICLR product hits.
- `scripts/finalize_catalog_audit.py`: synchronize reviewed catalog records and dispositions.
- `scripts/build_audit_report.py`: write the human-readable census report.
