from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from scripts.census_store import load_census, write_census


def sample_census() -> dict:
    return {
        "report_version": 1,
        "scope_year": 2026,
        "conferences": [
            {"conference": "ICLR", "paper_count": 1, "papers": [{"title": "One"}]},
            {"conference": "FSE", "paper_count": 0, "papers": []},
        ],
    }


def test_split_census_round_trip_preserves_order(tmp_path: Path) -> None:
    index = write_census(sample_census(), tmp_path)

    assert index == tmp_path / "index.yaml"
    assert [item["conference"] for item in load_census(index)["conferences"]] == ["ICLR", "FSE"]
    metadata = yaml.safe_load(index.read_text(encoding="utf-8"))
    assert metadata["storage_format"] == "per-conference-v1"
    assert [item["path"] for item in metadata["conference_files"]] == ["iclr.yaml", "fse.yaml"]
    assert metadata["conference_files"][0]["record_count"] == 1


def test_split_census_detects_tampering(tmp_path: Path) -> None:
    index = write_census(sample_census(), tmp_path)
    (tmp_path / "iclr.yaml").write_text("conference: ICLR\npapers: []\n", encoding="utf-8")

    with pytest.raises(ValueError, match="checksum mismatch"):
        load_census(index)


def test_load_census_accepts_legacy_monolith(tmp_path: Path) -> None:
    source = tmp_path / "legacy.yaml"
    source.write_text(yaml.safe_dump(sample_census(), sort_keys=False), encoding="utf-8")

    assert load_census(source) == sample_census()


def test_index_hash_matches_conference_file(tmp_path: Path) -> None:
    index = write_census(sample_census(), tmp_path)
    metadata = yaml.safe_load(index.read_text(encoding="utf-8"))
    entry = metadata["conference_files"][0]

    assert entry["sha256"] == hashlib.sha256((tmp_path / entry["path"]).read_bytes()).hexdigest()


def test_partial_write_reuses_unselected_conference_file(tmp_path: Path) -> None:
    census = sample_census()
    write_census(census, tmp_path)
    fse_before = (tmp_path / "fse.yaml").read_bytes()
    census["conferences"][0]["papers"].append({"title": "Two"})
    census["generated_at"] = "later"

    write_census(census, tmp_path, only={"ICLR"})

    assert (tmp_path / "fse.yaml").read_bytes() == fse_before
    reloaded = load_census(tmp_path)
    assert reloaded["generated_at"] == "later"
    assert len(reloaded["conferences"][0]["papers"]) == 2
