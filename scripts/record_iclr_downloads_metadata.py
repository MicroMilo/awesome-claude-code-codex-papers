#!/usr/bin/env python3
"""Record the official ICLR Downloads event totals alongside the paper census."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "data" / "audit" / "2026-conference-census.yaml"
URL = "https://iclr.cc/Downloads/2026"
EXPORT_PATH = ROOT / "tmp" / "census" / "iclr-2026-downloads.json"


def main() -> int:
    response = requests.get(
        URL,
        headers={"User-Agent": "awesome-coding-agent-papers-iclr-metadata/1.0"},
        timeout=90,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    match = re.search(r"Number of events:\s*(\d+)", text)
    if not match:
        raise RuntimeError("ICLR Downloads page did not expose the event count")
    poster_links = [
        link
        for link in soup.find_all("a", href=True)
        if "/virtual/2026/poster/" in str(link["href"])
    ]
    census = yaml.safe_load(CENSUS_PATH.read_text(encoding="utf-8"))
    conference = next(item for item in census["conferences"] if item["conference"] == "ICLR")
    conference["official_url"] = URL
    conference["downloads_url"] = URL
    conference["downloads_event_count"] = int(match.group(1))
    conference["downloads_poster_link_count"] = len(poster_links)
    conference["downloads_fetched_at"] = datetime.now(UTC).replace(microsecond=0).isoformat()
    if EXPORT_PATH.exists():
        export_bytes = EXPORT_PATH.read_bytes()
        export_data = json.loads(export_bytes)
        conference["downloads_export_record_count"] = len(export_data)
        conference["downloads_export_sha256"] = hashlib.sha256(export_bytes).hexdigest()
        conference["downloads_export_format"] = "json"
    CENSUS_PATH.write_text(
        yaml.safe_dump(census, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8"
    )
    print(
        f"Recorded ICLR Downloads metadata: events={conference['downloads_event_count']}, "
        f"poster_links={conference['downloads_poster_link_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
