# Conference adapter support

Read this matrix when selecting a source adapter or explaining current coverage. “Stable” means the repository has a bounded, resumable first-party path for that stage; it does not promise that a venue has already published every 2026 artifact.

| Conference | Official census | Official abstract | Official PDF | Current adapter status |
|---|---|---|---|---|
| ICLR | Proceedings index + Downloads export | Proceedings/Downloads metadata | First-party proceedings PDF | Stable end to end |
| AAAI | Official AAAI OJS issues | OJS article page | OJS galley/PDF | Stable end to end |
| ASE | Researchr accepted list | Researchr event-details AJAX | ACM DOI/PDF when the venue publishes it | Stable through metadata; publication-gated PDF |
| FSE | Researchr accepted list | Researchr event-details AJAX | PACMSE/ACM DOI/PDF | Stable through DOI discovery; publisher response may still challenge |
| ISSTA | Researchr accepted list | Researchr event-details AJAX | PACMSE/ACM DOI/PDF when published | Stable through metadata; publication-gated PDF |
| ICSE | Researchr accepted/program list | Researchr event-details AJAX | ACM/IEEE official link when exposed | Stable through metadata; mixed publisher availability |
| PLDI | Researchr accepted list | Researchr event-details AJAX | PACMPL/ACM DOI/PDF | Stable through DOI discovery; publisher response may still challenge |
| POPL | Researchr accepted list | Researchr event-details AJAX | PACMPL/ACM DOI/PDF | Stable through DOI discovery; publisher response may still challenge |
| OOPSLA | Researchr accepted list | Researchr event-details AJAX | PACMPL/ACM DOI/PDF when published | Stable through metadata; publication-gated PDF |
| ICML | Official Downloads/poster list | Official poster page | Official OpenReview link | Stable through metadata; current PDF host may return a recorded 403 challenge |
| NeurIPS | Official OpenReview group status check | Not run until accepted list exists | Not run until accepted list exists | Stable release check; pending 2026 accepted-list release |
| IJCAI | Official accepted-paper track pages | Accepted-paper page | Conference-hosted preprint PDF | Stable end to end |
| KDD | Official two-cycle papers page + ACM DOI | Official page currently omits abstracts | ACM DOI/PDF, subject to publisher challenge | Stable census; metadata/PDF publication-gated |

For Researchr venues, refresh the track page first. Publication links often appear after the accepted list and abstracts, so an older `official-pdf-not-exposed` result must be rechecked before reporting it as current.
