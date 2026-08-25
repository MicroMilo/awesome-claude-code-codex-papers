import json
from pathlib import Path

from scripts.build_conference_census import parse_ijcai, parse_kdd


def test_parse_ijcai_preserves_track_abstract_and_official_pdf(tmp_path: Path) -> None:
    source = tmp_path / "ijcai.html"
    source.write_text(
        """
        <ol class="ij-list">
          <li class="ij-paper">
            <span class="ij-pid">#42</span>
            <h3 class="ij-ptitle">A Coding Agent Study</h3>
            <span class="ij-author">Ada Lovelace</span>
            <div class="ij-abstract">We evaluate coding agents.</div>
            <span class="ij-pdflink"><a href="https://ijcai-preprints.s3.us-west-1.amazonaws.com/2026/42.pdf">Preprint</a></span>
            <span class="ij-kw">Software Engineering</span>
          </li>
        </ol>
        """,
        encoding="utf-8",
    )
    records = parse_ijcai(
        source,
        {
            "list_url": "https://2026.ijcai.org/accepted-papers/?ijtrack=main-track",
            "track_name": "Main Track",
        },
    )
    assert records == [
        {
            "title": "A Coding Agent Study",
            "official_url": "https://2026.ijcai.org/accepted-papers/?ijtrack=main-track",
            "track": "Main Track",
            "official_record_id": "42",
            "authors": ["Ada Lovelace"],
            "abstract": "We evaluate coding agents.",
            "abstract_source_url": "https://2026.ijcai.org/accepted-papers/?ijtrack=main-track",
            "pdf_url": "https://ijcai-preprints.s3.us-west-1.amazonaws.com/2026/42.pdf",
            "keywords": ["Software Engineering"],
        }
    ]


def test_parse_kdd_reads_both_cycles_and_acm_dois(tmp_path: Path) -> None:
    source = tmp_path / "kdd.html"
    cycle1 = [
        {
            "track": "rtp",
            "title": "Agent &amp; Data",
            "url": "https://doi.org/10.1145/1.2",
            "authors": "Ada &amp; Bob",
        }
    ]
    cycle2 = [
        {
            "track": "dtb",
            "title": "Repository Benchmark",
            "url": "https://doi.org/10.1145/1.3",
            "authors": "Carol",
        }
    ]
    source.write_text(
        f"const cycle1Papers = {json.dumps(cycle1)}.map((paper, index) => ({{...paper}}));"
        f"const cycle2Papers = {json.dumps(cycle2)}.map((paper, index) => ({{...paper}}));",
        encoding="utf-8",
    )
    records = parse_kdd(source, {"list_url": "https://kdd2026.kdd.org/papers/"})
    assert len(records) == 2
    by_id = {record["official_record_id"]: record for record in records}
    assert by_id["cycle1:10.1145/1.2"]["title"] == "Agent & Data"
    assert by_id["cycle1:10.1145/1.2"]["authors"] == "Ada & Bob"
    assert by_id["cycle1:10.1145/1.2"]["track"] == "February Cycle · Research"
    assert by_id["cycle2:10.1145/1.3"]["track"] == "July Cycle · Datasets and Benchmarks"
    assert by_id["cycle2:10.1145/1.3"]["pdf_url"] == "https://dl.acm.org/doi/pdf/10.1145/1.3"
