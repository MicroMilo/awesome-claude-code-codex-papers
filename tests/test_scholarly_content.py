from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from scripts.census_store import load_conference, write_conference
from scripts.enrich_scholarly_content import (
    apply_enrichment,
    merge_sources,
    normalize_doi,
    official_identity_value,
    openalex_content_sources,
    preferred_full_text_source,
    reconstruct_abstract,
    source_key,
    validate_override,
)


def test_reconstructs_openalex_abstract_in_token_order() -> None:
    inverted = {"agents": [2], "Coding": [0], "help": [1, 3]}

    assert reconstruct_abstract(inverted) == "Coding help agents help"


def test_openalex_locations_inherit_an_exact_doi_identity_match() -> None:
    work = {
        "id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1145/1234.5678",
        "locations": [
            {
                "is_oa": True,
                "pdf_url": "https://arxiv.org/pdf/2601.00001",
                "landing_page_url": "https://arxiv.org/abs/2601.00001",
                "version": "submittedVersion",
                "license": "cc-by",
            },
            {
                "is_oa": False,
                "pdf_url": "https://example.test/closed.pdf",
            },
        ],
    }

    sources = openalex_content_sources(work, "10.1145/1234.5678", "2026-08-25T00:00:00Z")

    assert sources[0]["source_role"] == "metadata"
    assert sources[1]["provider"] == "arxiv"
    assert sources[1]["identity_status"] == "verified"
    assert sources[1]["identity_method"] == "openalex-location-for-exact-doi"
    assert all(source["url"] != "https://example.test/closed.pdf" for source in sources)


def test_rejects_an_openalex_work_with_the_wrong_doi() -> None:
    with pytest.raises(ValueError, match="DOI mismatch"):
        openalex_content_sources(
            {"doi": "https://doi.org/10.1145/wrong", "locations": []},
            "10.1145/right",
            "2026-08-25T00:00:00Z",
        )


def test_preferred_full_text_requires_verified_identity() -> None:
    sources = [
        {
            "url": "https://example.test/unverified.pdf",
            "source_role": "full-text",
            "version": "publishedVersion",
            "identity_status": "pending",
        },
        {
            "url": "https://arxiv.org/pdf/2601.00001",
            "source_role": "full-text",
            "version": "submittedVersion",
            "identity_status": "verified",
        },
    ]

    assert preferred_full_text_source(sources)["url"] == "https://arxiv.org/pdf/2601.00001"


def test_new_versioned_arxiv_override_replaces_a_mutable_arxiv_url() -> None:
    current = [
        {
            "provider": "arxiv",
            "url": "https://arxiv.org/pdf/2601.00001",
            "source_role": "full-text",
        }
    ]
    versioned = {
        "provider": "arxiv",
        "url": "https://arxiv.org/pdf/2601.00001v3",
        "source_role": "full-text",
    }

    assert [source["url"] for source in merge_sources(current, [versioned])] == [
        "https://arxiv.org/pdf/2601.00001v3"
    ]


def test_override_must_match_official_doi_and_exact_title() -> None:
    paper = {
        "title": "A Coding Agent Paper",
        "official_url": "https://doi.org/10.1145/1234.5678",
    }
    override = {
        "doi": "10.1145/1234.5678",
        "title": "A Coding Agent Paper",
        "source": {
            "url": "https://arxiv.org/pdf/2601.00001",
            "source_role": "full-text",
            "identity_status": "verified",
            "identity_method": "exact-title-and-author-list",
            "identity_evidence": "The complete author lists match.",
        },
    }

    source = validate_override(override, paper)

    assert source["identity_value"] == "10.1145/1234.5678"
    assert source["version"] == "unknown"


def test_override_can_bind_to_an_official_record_without_a_doi() -> None:
    official_url = "https://icml.cc/virtual/2026/poster/12345"
    paper = {
        "title": "A Coding Agent Paper",
        "official_url": official_url,
        "official_record_id": "12345",
    }
    override = {
        "official_url": official_url,
        "title": "A Coding Agent Paper",
        "source": {
            "url": "https://arxiv.org/pdf/2601.00001",
            "source_role": "full-text",
            "identity_status": "verified",
            "identity_method": "exact-title-and-complete-author-list",
            "identity_evidence": "The title and complete author lists match.",
        },
    }

    source = validate_override(override, paper)

    assert official_identity_value(paper) == official_url
    assert source["identity_value"] == official_url


def test_enrichment_applies_an_override_to_a_non_doi_record() -> None:
    official_url = "https://icml.cc/virtual/2026/poster/12345"
    paper = {
        "title": "A Coding Agent Paper",
        "official_url": official_url,
        "disposition": "pending",
        "full_text_scan": "pending",
    }
    conference = {"conference": "ICML", "papers": [paper]}
    override = {
        "conference": "ICML",
        "official_url": official_url,
        "title": "A Coding Agent Paper",
        "source": {
            "url": "https://arxiv.org/pdf/2601.00001",
            "source_role": "full-text",
            "identity_status": "verified",
            "identity_method": "exact-title-and-complete-author-list",
            "identity_evidence": "The title and complete author lists match.",
        },
    }

    stats = apply_enrichment(conference, {}, [override])

    assert stats["overrides_applied"] == 1
    assert stats["verified_full_text_sources"] == 1
    assert paper["resolved_pdf_url"] == "https://arxiv.org/pdf/2601.00001"


def test_enrichment_filters_unrelated_abstracts_without_requesting_pdf() -> None:
    paper = {
        "title": "A Study of Graph Clustering",
        "official_url": "https://doi.org/10.1145/1234.5678",
        "disposition": "pending",
        "disposition_reason": "not screened",
        "full_text_scan": "pending",
    }
    conference = {"conference": "KDD", "papers": [paper]}
    latest = {
        source_key("KDD", "10.1145/1234.5678"): {
            "status": "matched",
            "openalex_id": "https://openalex.org/W1",
            "abstract": "We study spectral graph clustering and community detection.",
            "content_sources": [],
        }
    }

    stats = apply_enrichment(conference, latest, [])

    assert paper["disposition"] == "excluded"
    assert paper["full_text_scan"] == "metadata-filtered"
    assert stats["metadata_excluded"] == 1


def test_enrichment_preserves_official_abstract_and_completed_fulltext_review() -> None:
    paper = {
        "title": "A Coding Agent Paper",
        "official_url": "https://doi.org/10.1145/1234.5678",
        "abstract": "Official abstract about a coding agent.",
        "abstract_source_type": "official-publisher",
        "disposition": "included",
        "disposition_reason": "reviewed",
        "full_text_scan": "scanned",
        "scan": {"status": "scanned", "fetch": {"sha256": "abc"}},
    }
    conference = {"conference": "KDD", "papers": [paper]}
    latest = {
        source_key("KDD", "10.1145/1234.5678"): {
            "status": "matched",
            "openalex_id": "https://openalex.org/W1",
            "abstract": "A different secondary abstract.",
            "content_sources": [],
        }
    }

    apply_enrichment(conference, latest, [])

    assert paper["abstract"] == "Official abstract about a coding agent."
    assert paper["scan"] == {"status": "scanned", "fetch": {"sha256": "abc"}}
    assert paper["full_text_scan"] == "scanned"
    assert paper["disposition"] == "included"


def test_normalizes_doi_from_an_official_url() -> None:
    assert normalize_doi("https://doi.org/10.1145/3770855.3818488") == ("10.1145/3770855.3818488")


def test_load_and_write_one_conference_shard_updates_its_checksum(tmp_path: Path) -> None:
    conference = {"conference": "KDD", "paper_count": 1, "papers": [{"title": "One"}]}
    raw = yaml.safe_dump(conference, sort_keys=False).encode()
    (tmp_path / "kdd.yaml").write_bytes(raw)
    index = {
        "conference_files": [
            {
                "conference": "KDD",
                "path": "kdd.yaml",
                "record_count": 1,
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        ]
    }
    (tmp_path / "index.yaml").write_text(yaml.safe_dump(index, sort_keys=False))

    loaded = load_conference("KDD", tmp_path)
    loaded["papers"].append({"title": "Two"})
    write_conference(loaded, tmp_path)

    updated_index = yaml.safe_load((tmp_path / "index.yaml").read_text())
    updated_raw = (tmp_path / "kdd.yaml").read_bytes()
    assert updated_index["conference_files"][0]["record_count"] == 2
    assert updated_index["conference_files"][0]["sha256"] == hashlib.sha256(updated_raw).hexdigest()
    assert len(load_conference("KDD", tmp_path)["papers"]) == 2
