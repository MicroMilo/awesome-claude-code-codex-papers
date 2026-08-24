#!/usr/bin/env python3
"""Export the official ICLR Downloads table in a machine-readable format.

The ICLR Downloads page exposes a server-side export form.  Using that form
preserves the conference's own event filters and avoids treating a scraped
HTML view as the only source of truth.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from bs4 import BeautifulSoup

if __package__:
    from .source_fetcher import JsonlLedger, RetryPolicy, StableFetcher, atomic_write_bytes
else:  # pragma: no cover - exercised by the documented direct-script command
    from source_fetcher import JsonlLedger, RetryPolicy, StableFetcher, atomic_write_bytes

ROOT = Path(__file__).resolve().parents[1]
URL = "https://iclr.cc/Downloads/2026"
TRACK_FIELDS = {
    "posters": "posters",
    "tutorials": "tutorials",
    "invited-talks": "invited_talks",
    "workshops": "workshops",
    "demonstrations": "demonstrations",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format", choices=["json", "yaml", "csv", "xlsx", "tsv", "ods"], default="json"
    )
    parser.add_argument(
        "--track",
        action="append",
        choices=sorted(TRACK_FIELDS),
        default=None,
        help="Repeat to include more official event tracks; defaults to posters only.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tmp" / "census" / "iclr-2026-downloads.json",
    )
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--per-host-concurrency", type=int, default=2)
    parser.add_argument("--per-host-delay", type=float, default=0.35)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "data" / "audit" / "2026-source-fetch.jsonl",
    )
    args = parser.parse_args()

    tracks = args.track or ["posters"]
    fetcher = StableFetcher(
        user_agent="awesome-coding-agent-papers-iclr-export/2.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=max(1, args.retries)),
        per_host_concurrency=max(1, args.per_host_concurrency),
        per_host_min_interval=max(0.0, args.per_host_delay),
    )
    ledger_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    ledger = JsonlLedger(ledger_path)
    page = fetcher.request_bytes("GET", URL, timeout=(15, args.timeout))
    soup = BeautifulSoup(page.body, "html.parser")
    token = soup.select_one("input[name=csrfmiddlewaretoken]")
    if token is None or not token.get("value"):
        raise RuntimeError("ICLR export form did not expose a CSRF token")

    output_format = args.format
    format_id = {
        "csv": "0",
        "xls": "1",
        "xlsx": "2",
        "tsv": "3",
        "ods": "4",
        "json": "5",
        "yaml": "6",
    }[output_format]
    payload: dict[str, str] = {
        "csrfmiddlewaretoken": token["value"],
        "format": format_id,
        "resource": "0",
        "submitaction": "Download Data",
    }
    for track in tracks:
        payload[TRACK_FIELDS[track]] = "on"

    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    exported = fetcher.request_bytes(
        "POST",
        URL,
        data=payload,
        headers={"Referer": URL},
        timeout=(15, args.timeout),
    )
    content_type = exported.metadata.content_type.lower()
    if "text/html" in content_type and output_format not in {"xlsx", "ods"}:
        raise RuntimeError(
            "ICLR returned the HTML page instead of an export; inspect the form response before importing it"
        )
    if output_format == "json":
        try:
            json.loads(exported.body)
        except json.JSONDecodeError as error:
            raise RuntimeError("ICLR returned invalid JSON") from error
    atomic_write_bytes(output, exported.body)
    ledger.append(
        {
            "source_key": f"iclr:2026:downloads:{output_format}:{'-'.join(tracks)}",
            "source_kind": "official-downloads-export",
            "source_url": URL,
            "status": "success",
            "format": output_format,
            "tracks": tracks,
            "local_path": str(output.relative_to(ROOT)),
            "http_status": exported.metadata.status_code,
            "content_type": exported.metadata.content_type,
            "etag": exported.metadata.etag,
            "last_modified": exported.metadata.last_modified,
            "sha256": exported.metadata.sha256,
            "byte_size": exported.metadata.byte_size,
            "attempts": exported.metadata.attempts,
            "retrieved_at": exported.metadata.retrieved_at,
        }
    )
    print(
        f"Wrote {output.relative_to(ROOT)} ({len(exported.body)} bytes; tracks={','.join(tracks)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
