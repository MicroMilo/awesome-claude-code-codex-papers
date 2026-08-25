"""Read and write the conference census as one audited file per venue."""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CENSUS_DIR = ROOT / "data" / "audit" / "2026-conference-census"
CENSUS_INDEX_PATH = CENSUS_DIR / "index.yaml"
LEGACY_CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"


def _slug(value: object) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(value).casefold()).strip("-")
    if not slug:
        raise ValueError("conference name cannot be empty")
    return slug


def _yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120).encode("utf-8")


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
        temporary.chmod(0o644)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _resolve_index(path: Path | None) -> Path:
    if path is None:
        return CENSUS_INDEX_PATH
    path = Path(path)
    if path.is_dir() or not path.suffix:
        return path / "index.yaml"
    return path


def load_census(path: Path | None = None) -> dict[str, Any]:
    """Load either the split index or a legacy monolithic census."""

    source = _resolve_index(path)
    if path is None and not source.exists() and LEGACY_CENSUS_PATH.exists():
        source = LEGACY_CENSUS_PATH
    payload = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"census root must be a mapping: {source}")
    if "conferences" in payload:
        return payload

    entries = payload.get("conference_files")
    if not isinstance(entries, list):
        raise ValueError(f"split census index lacks conference_files: {source}")
    conferences: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(f"invalid conference_files entry in {source}")
        name = str(entry.get("conference", ""))
        relative_path = Path(str(entry.get("path", "")))
        if not name or relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"unsafe or incomplete conference file entry: {entry}")
        conference_path = source.parent / relative_path
        raw = conference_path.read_bytes()
        expected_hash = str(entry.get("sha256", ""))
        actual_hash = hashlib.sha256(raw).hexdigest()
        if expected_hash and expected_hash != actual_hash:
            raise ValueError(f"checksum mismatch for {conference_path}")
        conference = yaml.safe_load(raw)
        if not isinstance(conference, dict) or conference.get("conference") != name:
            raise ValueError(f"conference identity mismatch in {conference_path}")
        if name in seen:
            raise ValueError(f"duplicate conference in split census: {name}")
        seen.add(name)
        conferences.append(conference)

    result = {key: value for key, value in payload.items() if key != "conference_files"}
    result["conferences"] = conferences
    return result


def write_census(
    census: dict[str, Any],
    path: Path | None = None,
    *,
    only: set[str] | None = None,
) -> Path:
    """Atomically persist a split census and return its index path."""

    index_path = _resolve_index(path)
    if index_path.name != "index.yaml":
        raise ValueError("split census destination must be a directory or an index.yaml path")
    conferences = census.get("conferences")
    if not isinstance(conferences, list):
        raise ValueError("census conferences must be a list")

    existing_entries: dict[str, dict[str, Any]] = {}
    if only is not None and index_path.exists():
        existing_index = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
        existing_entries = {
            str(entry.get("conference")): entry
            for entry in existing_index.get("conference_files", [])
            if isinstance(entry, dict)
        }

    entries: list[dict[str, Any]] = []
    seen_files: set[str] = set()
    serialized: list[tuple[Path, bytes]] = []
    for conference in conferences:
        if not isinstance(conference, dict) or not conference.get("conference"):
            raise ValueError("every census conference must be a named mapping")
        name = str(conference["conference"])
        filename = f"{_slug(name)}.yaml"
        if filename in seen_files:
            raise ValueError(f"conference filename collision: {name}")
        seen_files.add(filename)
        existing = existing_entries.get(name)
        if only is not None and name not in only and existing:
            existing_path = index_path.parent / str(existing.get("path", ""))
            if existing_path.exists():
                entries.append(existing)
                continue
        raw = _yaml_bytes(conference)
        entries.append(
            {
                "conference": name,
                "path": filename,
                "record_count": len(conference.get("papers", [])),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
        serialized.append((index_path.parent / filename, raw))

    index = {key: value for key, value in census.items() if key != "conferences"}
    index["storage_format"] = "per-conference-v1"
    index["conference_files"] = entries
    for destination, raw in serialized:
        _atomic_write(destination, raw)
    _atomic_write(index_path, _yaml_bytes(index))
    return index_path
