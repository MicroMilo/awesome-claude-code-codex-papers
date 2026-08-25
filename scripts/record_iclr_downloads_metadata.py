#!/usr/bin/env python3
"""Record the official ICLR Downloads event totals alongside the paper census."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

if __package__:
    from .census_store import load_census, write_census
else:  # pragma: no cover - documented direct-script entry point
    from census_store import load_census, write_census

ROOT = Path(__file__).resolve().parents[1]
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
    census = load_census()
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
    write_census(census, only={"ICLR"})
    print(
        f"Recorded ICLR Downloads metadata: events={conference['downloads_event_count']}, "
        f"poster_links={conference['downloads_poster_link_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
