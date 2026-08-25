from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from scripts.build_conference_census import is_first_party_pdf
from scripts.enrich_official_metadata import (
    extract_aaai_abstract,
    extract_icml_abstract,
    extract_researchr_modal,
)
from scripts.enrich_official_pdf_urls import acm_pdf_url, discover_from_page
from scripts.fetch_iclr_sources import (
    build_download_payload,
    parse_proceedings_detail,
    parse_proceedings_index,
)
from scripts.metadata_relevance import SCREEN_VERSION, screen_metadata
from scripts.scan_conference_fulltext import scan_record, update_census
from scripts.source_fetcher import (
    FetchError,
    JsonlLedger,
    RetryPolicy,
    StableFetcher,
    parse_retry_after,
)
from scripts.update_pending_review import blocker_for, direct_product_signals


class FakeResponse:
    def __init__(
        self, status_code: int, body: bytes, headers: dict[str, str] | None = None
    ) -> None:
        self.status_code = status_code
        self._body = body
        self.headers = headers or {"content-type": "application/octet-stream"}
        self.closed = False

    @property
    def content(self) -> bytes:
        return self._body

    def iter_content(self, chunk_size: int = 1024) -> list[bytes]:
        del chunk_size
        return [self._body] if self._body else []

    def close(self) -> None:
        self.closed = True


class FakeSession:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = responses
        self.calls: list[dict[str, object]] = []
        self.headers: dict[str, str] = {}

    def request(self, method: str, url: str, **kwargs: object) -> FakeResponse:
        self.calls.append({"method": method, "url": url, **kwargs})
        return self.responses.pop(0)

    def get(self, url: str, **kwargs: object) -> FakeResponse:
        return self.request("GET", url, **kwargs)


def make_fetcher(session: FakeSession, sleeps: list[float] | None = None) -> StableFetcher:
    return StableFetcher(
        user_agent="test-source-fetcher/1.0",
        retry_policy=RetryPolicy(max_attempts=3, base_delay=0.1, jitter=0),
        per_host_concurrency=1,
        per_host_min_interval=0,
        session_factory=lambda: session,
        sleep=sleeps.append if sleeps is not None else lambda _delay: None,
        random_value=lambda: 0,
    )


def test_retryable_status_uses_bounded_retry_and_metadata() -> None:
    session = FakeSession(
        [
            FakeResponse(503, b"busy", {"retry-after": "0", "content-type": "text/plain"}),
            FakeResponse(200, b"ok", {"content-type": "text/plain", "etag": '"a"'}),
        ]
    )
    sleeps: list[float] = []
    result = make_fetcher(session, sleeps).request_bytes("GET", "https://example.test/data")

    assert result.body == b"ok"
    assert result.metadata.attempts == 2
    assert result.metadata.etag == '"a"'
    assert len(session.calls) == 2
    assert sleeps == [0.0]


def test_fetcher_decodes_gzip_when_content_encoding_header_is_missing() -> None:
    body = gzip.compress(b"<html><p>official metadata</p></html>")
    session = FakeSession([FakeResponse(200, body, {"content-type": "text/html"})])

    result = make_fetcher(session).request_bytes("GET", "https://example.test/page")

    assert result.body == b"<html><p>official metadata</p></html>"
    assert result.metadata.byte_size == len(result.body)


def test_challenge_is_not_retried_or_hidden() -> None:
    session = FakeSession(
        [
            FakeResponse(
                403,
                b'{"name":"ChallengeRequiredError"}',
                {"content-type": "application/json"},
            )
        ]
    )

    with pytest.raises(FetchError) as raised:
        make_fetcher(session).request_bytes("GET", "https://openreview.net/pdf?id=abc")

    assert raised.value.challenge is True
    assert raised.value.error_class == "challenge"
    assert len(session.calls) == 1


def test_pending_review_prioritizes_product_signal_without_promoting() -> None:
    paper = {
        "title": "A proof-engineering benchmark",
        "abstract": "We compare Claude Code with Codex CLI on identical tasks.",
        "pdf_url": "https://openreview.net/pdf?id=abc",
        "scan": {"challenge": True, "http_status": 403},
    }

    assert direct_product_signals(paper) == [
        {"product": "claude-code", "matched_text": "Claude Code"},
        {"product": "codex-cli", "matched_text": "Codex CLI"},
    ]
    assert blocker_for(paper)[0] == "official-source-challenge"


def test_acm_pdf_url_is_derived_only_from_an_official_acm_doi() -> None:
    assert (
        acm_pdf_url("https://doi.org/10.1145/3808347")
        == "https://dl.acm.org/doi/pdf/10.1145/3808347"
    )
    assert acm_pdf_url("https://doi.org/10.5555/example") is None
    assert acm_pdf_url("https://example.com/10.1145/3808347") is None


def test_researchr_pdf_policy_rejects_preprints_on_external_hosts() -> None:
    official = "https://conf.researchr.org/track/fse-2026/fse-2026-research-papers"

    assert not is_first_party_pdf("https://github.com/example/paper.pdf", official)
    assert not is_first_party_pdf("https://arxiv.org/pdf/2601.00001.pdf", official)
    assert is_first_party_pdf("https://dl.acm.org/doi/pdf/10.1145/3808103", official)


def test_official_page_acm_doi_is_promoted_to_first_party_pdf() -> None:
    result = discover_from_page(
        "FSE",
        "https://conf.researchr.org/details/fse-2026/paper",
        b'<div><label class="control-label">Link to Publication</label>'
        b'<a href="https://dl.acm.org/doi/10.1145/3808103">publication</a></div>',
    )

    assert result["pdf_url"] == "https://dl.acm.org/doi/pdf/10.1145/3808103"
    assert result["doi_url"] == "https://doi.org/10.1145/3808103"


def test_researchr_detail_ignores_doi_from_embedded_session_program() -> None:
    result = discover_from_page(
        "FSE",
        "https://conf.researchr.org/details/fse-2026/target",
        b'<table class="session-table"><a href="https://doi.org/10.1145/wrong">DOI</a></table>',
    )

    assert result["status"] == "pending"


def test_download_resumes_partial_file_and_replaces_atomically(tmp_path: Path) -> None:
    destination = tmp_path / "paper.pdf"
    partial = destination.with_suffix(".pdf.part")
    partial.write_bytes(b"%PDF")
    session = FakeSession(
        [
            FakeResponse(
                206,
                b"-1.7\n",
                {"content-type": "application/pdf", "etag": '"pdf"'},
            )
        ]
    )

    metadata = make_fetcher(session).download(
        "https://proceedings.example/paper.pdf",
        destination,
        expected_prefix=b"%PDF",
    )

    assert destination.read_bytes() == b"%PDF-1.7\n"
    assert not partial.exists()
    assert metadata.content_type == "application/pdf"
    assert session.calls[0]["headers"] == {"Range": "bytes=4-"}


def test_jsonl_ledger_ignores_an_incomplete_final_line(tmp_path: Path) -> None:
    path = tmp_path / "manifest.jsonl"
    ledger = JsonlLedger(path)
    ledger.append({"source_key": "one", "status": "success"})
    with path.open("a", encoding="utf-8") as handle:
        handle.write('{"source_key":"broken"')

    latest = ledger.latest()

    assert latest["one"]["status"] == "success"
    assert "broken" not in latest


def test_iclr_official_parsers_keep_proceedings_identity() -> None:
    index = b"""
    <html><body>
      <a href="/paper_files/paper/2026/hash/abc123-Abstract-Conference.html"> A Paper </a>
      <a href="/paper_files/paper/2026/hash/abc123-Abstract-Conference.html"> A Paper </a>
      <a href="/paper_files/paper/2026/hash/def456-Abstract-Conference.html">Second Paper</a>
    </body></html>
    """
    records = parse_proceedings_index(index)
    detail = parse_proceedings_detail(
        b"""
        <html><body><h1>A Paper</h1>
          <a href="/paper_files/paper/2026/file/abc123-Paper-Conference.pdf">Paper</a>
          <a href="/paper_files/paper/2026/file/abc123-Supplemental.pdf">Supplemental</a>
        </body></html>
        """,
        records[0]["official_url"],
    )

    assert [record["paper_id"] for record in records] == ["abc123", "def456"]
    assert detail["abstract"] == ""
    assert detail["pdf_url"].endswith("abc123-Paper-Conference.pdf")
    assert detail["supplementary_url"].endswith("abc123-Supplemental.pdf")


def test_iclr_detail_parser_extracts_official_abstract() -> None:
    detail = parse_proceedings_detail(
        b"""
        <html><body><h1>Coding agents</h1>
          <section class="paper-section"><h2>Abstract</h2>
            <p class="paper-abstract"><p>We evaluate coding agents on repository-level issues.</p></p>
          </section>
        </body></html>
        """,
        "https://proceedings.example/paper",
    )

    assert detail["abstract"] == "We evaluate coding agents on repository-level issues."


def test_researchr_event_modal_parser_extracts_official_abstract() -> None:
    payload = json.dumps(
        [
            {
                "action": "append",
                "id": "event-modals",
                "value": """
                <div class="event-description">
                  <p>This is the official event abstract.</p>
                  <p></p>
                  <div class="row">authors</div>
                </div>
                <a href="/details/fse-2026/fse-2026-research-papers/1/Paper">All Details</a>
                """,
            }
        ]
    ).encode()

    result = extract_researchr_modal(payload, "https://conf.researchr.org/track/fse-2026/papers")

    assert result["abstract"] == "This is the official event abstract."
    assert result["details_url"].endswith("/details/fse-2026/fse-2026-research-papers/1/Paper")


def test_icml_official_poster_parser_extracts_abstract() -> None:
    result = extract_icml_abstract(
        b"""
        <div class="abstract-section">
          <h3 class="abstract-header">Abstract</h3>
          <div class="abstract-text-inner"><p>Official ICML abstract.</p></div>
        </div>
        <div class="abstract-section">
          <h3 class="abstract-header">Lay Summary</h3>
          <div class="abstract-text-inner"><p>Lay summary.</p></div>
        </div>
        """,
        "https://icml.cc/virtual/2026/poster/1",
    )

    assert result["abstract"] == "Official ICML abstract."


def test_aaai_ojs_parser_extracts_abstract_without_label() -> None:
    result = extract_aaai_abstract(
        b"""
        <section class="item abstract">
          <h2 class="label">Abstract</h2>
          The official AAAI abstract is here.
        </section>
        """,
        "https://ojs.aaai.org/index.php/AAAI/article/view/1",
    )

    assert result["abstract"] == "The official AAAI abstract is here."


def test_metadata_screen_retains_high_recall_code_agent_candidates() -> None:
    result = screen_metadata(
        "An autonomous software engineering system",
        "We evaluate a large language model coding agent on repository-level bug fixing.",
    )

    assert result["screen_version"] == SCREEN_VERSION
    assert result["screen_status"] == "candidate"
    assert result["screen_decision"] == "candidate"
    assert result["matched_signals"]["agent"]
    assert result["matched_signals"]["language-model"]


def test_metadata_screen_filters_unrelated_abstract_without_pdf() -> None:
    result = screen_metadata(
        "Masked Guidance for Video Generation",
        "We introduce a framework for controllable and high-fidelity video synthesis.",
    )

    assert result["screen_status"] == "filtered"
    assert result["screen_decision"] == "excluded"
    assert result["abstract_chars"] > 0


def test_metadata_screen_keeps_missing_abstract_pending() -> None:
    result = screen_metadata("A paper with an unavailable abstract", None)

    assert result["screen_status"] == "pending"
    assert result["screen_decision"] == "pending"


def test_metadata_screen_keeps_direct_product_title_without_abstract() -> None:
    result = screen_metadata("Evaluating Claude Code", None)

    assert result["screen_status"] == "candidate"
    assert result["abstract_chars"] == 0


def test_download_payload_uses_explicit_track_flags() -> None:
    payload = build_download_payload("csrf", ["posters", "workshops"])

    assert payload["format"] == "5"
    assert payload["posters"] == "on"
    assert payload["workshops"] == "on"
    assert "tutorials" not in payload


def test_retry_after_supports_seconds_and_http_date() -> None:
    assert parse_retry_after("2") == 2.0
    assert parse_retry_after("not-a-delay") is None


def test_fulltext_scanner_uses_shared_fetcher(monkeypatch: pytest.MonkeyPatch) -> None:
    session = FakeSession([FakeResponse(200, b"%PDF-1.7", {"content-type": "application/pdf"})])
    fetcher = make_fetcher(session)
    monkeypatch.setattr(
        "scripts.scan_conference_fulltext.extract_pdf_text",
        lambda _payload: ("Section 5.1\nNo target product.", "test"),
    )

    result = scan_record(
        "ICLR",
        {
            "title": "A paper",
            "official_url": "https://proceedings.example/paper",
            "pdf_url": "https://proceedings.example/paper.pdf",
        },
        30,
        fetcher,
        pdf_scope="all",
    )

    assert result["status"] == "scanned"
    assert result["disposition"] == "excluded"
    assert result["fetch"]["sha256"]


def test_fulltext_scanner_skips_unrelated_iclr_pdf_after_abstract_screen() -> None:
    detail_html = b"""
    <html><body>
      <section class="paper-section"><h2>Abstract</h2>
        <p class="paper-abstract"><p>We study image generation and visual fidelity.</p></p>
      </section>
    </body></html>
    """
    session = FakeSession([FakeResponse(200, detail_html, {"content-type": "text/html"})])
    fetcher = make_fetcher(session)

    result = scan_record(
        "ICLR",
        {
            "title": "A vision paper",
            "official_url": "https://proceedings.iclr.cc/paper_files/paper/2026/hash/"
            "a4c17d9b88eaefc9bdf7c656ffc8ce55-Abstract-Conference.html",
            "pdf_url": "https://proceedings.iclr.cc/paper_files/paper/2026/file/"
            "a4c17d9b88eaefc9bdf7c656ffc8ce55-Paper-Conference.pdf",
        },
        30,
        fetcher,
    )

    assert result["status"] == "metadata-filtered"
    assert result["disposition"] == "excluded"
    assert result["metadata_screen_status"] == "filtered"
    assert len(session.calls) == 1


def test_fulltext_scanner_keeps_missing_non_iclr_metadata_pending() -> None:
    session = FakeSession([])
    fetcher = make_fetcher(session)

    result = scan_record(
        "FSE",
        {
            "title": "A paper without an official abstract",
            "official_url": "https://conf.researchr.org/track/fse-2026/fse-2026-research-papers",
            "pdf_url": "https://example.test/paper.pdf",
        },
        30,
        fetcher,
    )

    assert result["status"] == "pending"
    assert "metadata" in result["reason"]
    assert session.calls == []


def test_scan_checkpoint_does_not_undo_context_review() -> None:
    census = {
        "conferences": [
            {
                "conference": "ICLR",
                "papers": [
                    {
                        "title": "Reviewed product hit",
                        "disposition": "excluded",
                        "product_review": {"status": "excluded-after-context-review"},
                    },
                    {"title": "Promoted catalog paper", "disposition": "included"},
                ],
            }
        ]
    }

    update_census(
        census,
        [
            {
                "conference": "ICLR",
                "title": "Reviewed product hit",
                "status": "scanned",
                "disposition": "pending",
                "reason": "stale",
            },
            {
                "conference": "ICLR",
                "title": "Promoted catalog paper",
                "status": "scanned",
                "disposition": "pending",
                "reason": "stale",
            },
        ],
    )

    papers = census["conferences"][0]["papers"]
    assert papers[0]["disposition"] == "excluded"
    assert papers[1]["disposition"] == "included"
