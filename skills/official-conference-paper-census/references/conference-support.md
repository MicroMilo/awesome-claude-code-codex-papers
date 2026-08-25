# Conference adapter support

Read this matrix when selecting a source adapter or explaining current coverage. “Stable” means the repository has a bounded, resumable path with official acceptance identity and audited content provenance; it does not promise that a venue has already published every artifact.

| Conference | Official census | Official abstract | Official PDF | Current adapter status |
|---|---|---|---|---|
| ICLR | Proceedings index + Downloads export | Proceedings/Downloads metadata | First-party proceedings PDF | Stable end to end |
| AAAI | Official AAAI OJS issues | OJS article page | OJS galley/PDF | Stable end to end |
| ASE | Researchr accepted list | Researchr event-details AJAX | ACM DOI/PDF when published; reviewed identity-bound open copy otherwise | Stable metadata and reviewed open-copy fallback; official PDF publication-gated |
| FSE | Researchr accepted list | Researchr event-details AJAX | PACMSE/ACM DOI/PDF | Stable through DOI discovery; publisher response may still challenge |
| ISSTA | Researchr accepted list | Researchr event-details AJAX | PACMSE/ACM DOI/PDF when published; reviewed identity-bound open copy otherwise | Stable metadata and reviewed open-copy fallback; official PDF publication-gated |
| ICSE | Researchr accepted/program list | Researchr event-details AJAX | ACM/IEEE official link when exposed | Stable through metadata; mixed publisher availability |
| PLDI | Researchr accepted list | Researchr event-details AJAX | PACMPL/ACM DOI/PDF | Stable through DOI discovery; publisher response may still challenge |
| POPL | Researchr accepted list | Researchr event-details AJAX | PACMPL/ACM DOI/PDF | Stable through DOI discovery; publisher response may still challenge |
| OOPSLA | Researchr accepted list | Researchr event-details AJAX | PACMPL/ACM DOI/PDF when published | Stable through metadata; publication-gated PDF |
| ICML | Official Downloads/poster list | Official poster page | Official OpenReview link | Stable through metadata; current PDF host may return a recorded 403 challenge |
| NeurIPS | Official OpenReview group status check | Not run until accepted list exists | Not run until accepted list exists | Stable release check; pending 2026 accepted-list release |
| IJCAI | Official accepted-paper track pages | Accepted-paper page | Conference-hosted preprint PDF | Stable end to end |
| KDD | Official two-cycle papers page + ACM DOI | OpenAlex abstract bound by exact DOI | Official ACM PDF when usable; otherwise DOI-bound or reviewed open copy | Stable census and metadata triage; candidate full text is availability-gated |

For Researchr venues, refresh the track page first. Publication links often appear after the accepted list and abstracts, so an older `official-pdf-not-exposed` result must be rechecked before reporting it as current.

Across all venues, the official column establishes acceptance. An OpenAlex, arXiv, or institutional URL belongs only in `content_sources`; it must carry an identity method and version and must never replace the official `paper_url`.
