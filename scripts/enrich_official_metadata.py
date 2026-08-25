#!/usr/bin/env python3
"""Fetch official title/abstract metadata before queuing conference PDFs.

The adapters are deliberately first-party only:

* Researchr conference pages expose abstracts through their official event
  details AJAX endpoint.
* ICML poster pages expose the abstract in the official HTML page.
* AAAI OJS article pages are queried directly when the publisher is reachable.

The script writes a resumable JSONL metadata ledger and copies successful
abstracts into the audit census. A missing abstract is recorded explicitly and
is not treated as permission to download every PDF.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

if __package__:
    from .census_store import load_census, write_census
    from .source_fetcher import FetchError, RetryPolicy, StableFetcher, metadata_dict
else:  # pragma: no cover - exercised by the documented direct-script command
    from census_store import load_census, write_census
    from source_fetcher import FetchError, RetryPolicy, StableFetcher, metadata_dict

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "audit" / "2026-official-metadata.jsonl"
CACHE_DIR = ROOT / "tmp" / "census"

RESEARCHR_SNAPSHOTS = {
    "ASE": "ase-2026.html",
    "FSE": "fse-2026-research.html",
    "ISSTA": "issta-2026-research.html",
    "ICSE": "icse-2026-research.html",
    "PLDI": "pldi-2026-research.html",
    "POPL": "popl-2026-research.html",
    "OOPSLA": "oopsla-2026.html",
}


def normalize(value: str) -> str:
    return " ".join(str(value).split()).strip()


def key_for(conference: str, title: str) -> tuple[str, str]:
    return conference, normalize(title).casefold()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_latest_manifest() -> dict[tuple[str, str], dict[str, Any]]:
    if not MANIFEST_PATH.exists():
        return {}
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            records[key_for(str(item["conference"]), str(item["title"]))] = item
    return records


def append_manifest(results: list[dict[str, Any]]) -> None:
    if not results:
        return
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("a", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def researchr_form(snapshot: Path) -> dict[str, str]:
    soup = BeautifulSoup(snapshot.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    form = soup.select_one("#event-modal-loader form")
    if form is None:
        raise RuntimeError(f"Researchr event modal form missing from {snapshot}")
    action_url = str(form.get("action", ""))
    event_field_node = form.select_one("input.event-id-input")
    event_field = str(event_field_node.get("name", "")) if event_field_node else ""
    action_match = re.search(r'serverInvoke\("[^"]+","([^"]+)"', str(form))
    action_name = action_match.group(1) if action_match else ""
    values = {
        str(node["name"]): str(node.get("value", ""))
        for node in form.find_all("input", attrs={"name": True})
        if node.get("name") and node.get("name") != event_field
    }
    if not action_url or not event_field or not action_name:
        raise RuntimeError(f"Researchr event modal form is incomplete in {snapshot}")
    return {
        "action_url": action_url,
        "event_field": event_field,
        "action_name": action_name,
        "values": json.dumps(values, ensure_ascii=False),
    }


def extract_researchr_modal(payload: bytes, fallback_url: str) -> dict[str, Any]:
    try:
        actions = json.loads(payload.decode("utf-8", errors="replace"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Researchr AJAX response was not JSON: {error}") from error
    html = "".join(
        str(action.get("value", ""))
        for action in actions
        if isinstance(action, dict) and action.get("value")
    )
    soup = BeautifulSoup(html, "html.parser")
    description = soup.select_one(".event-description")
    details = soup.select_one('a[href*="/details/"]')
    details_url = urljoin(fallback_url, str(details.get("href"))) if details else fallback_url
    paragraphs: list[str] = []
    if description:
        for child in description.find_all("p", recursive=False):
            text = normalize(child.get_text(" ", strip=True))
            if text and text.casefold() != "no description available":
                paragraphs.append(text)
    abstract = normalize(" ".join(paragraphs))
    return {
        "abstract": abstract,
        "abstract_source_url": details_url,
        "details_url": details_url if details else None,
    }


def extract_icml_abstract(payload: bytes, official_url: str) -> dict[str, Any]:
    soup = BeautifulSoup(payload, "html.parser")
    for section in soup.select(".abstract-section"):
        header = section.select_one(".abstract-header")
        if not header or not normalize(header.get_text(" ", strip=True)).casefold().startswith(
            "abstract"
        ):
            continue
        node = section.select_one(".abstract-text-inner") or section.select_one(".abstract-text")
        abstract = normalize(node.get_text(" ", strip=True)) if node else ""
        return {"abstract": abstract, "abstract_source_url": official_url}
    return {"abstract": "", "abstract_source_url": official_url}


def extract_aaai_abstract(payload: bytes, official_url: str) -> dict[str, Any]:
    soup = BeautifulSoup(payload, "html.parser")
    candidates = [
        soup.select_one(".item.abstract .value"),
        soup.select_one(".item.abstract"),
        soup.select_one("section.abstract"),
        soup.select_one("div.abstract"),
        soup.select_one('meta[name="description"]'),
    ]
    for node in candidates:
        if node is None:
            continue
        if node.name == "meta":
            text = str(node.get("content", ""))
        else:
            label = node.select_one(".label")
            if label is not None:
                label.extract()
            text = node.get_text(" ", strip=True)
        text = normalize(text)
        if text and text.casefold() not in {"abstract", "no abstract available"}:
            return {"abstract": text, "abstract_source_url": official_url}
    return {"abstract": "", "abstract_source_url": official_url}


def fetch_record(
    conference: str,
    record: dict[str, Any],
    fetcher: StableFetcher,
    timeout: int,
    forms: dict[str, dict[str, str]],
) -> dict[str, Any]:
    title = str(record.get("title", ""))
    result: dict[str, Any] = {
        "conference": conference,
        "title": title,
        "official_url": record.get("official_url"),
    }
    try:
        if conference in forms:
            form = forms[conference]
            values = json.loads(form["values"])
            values[form["event_field"]] = str(record.get("official_record_id", ""))
            values[form["action_name"]] = "1"
            values["__ajax_runtime_request__"] = "event-modal-loader"
            fetched = fetcher.request_bytes(
                "POST",
                form["action_url"],
                data=values,
                headers={"X-Requested-With": "XMLHttpRequest"},
                timeout=(15, timeout),
            )
            extracted = extract_researchr_modal(fetched.body, str(record.get("official_url", "")))
        else:
            fetched = fetcher.request_bytes(
                "GET",
                str(record.get("official_url", "")),
                timeout=(15, timeout),
            )
            if conference == "ICML":
                extracted = extract_icml_abstract(fetched.body, str(record.get("official_url", "")))
            elif conference == "AAAI":
                extracted = extract_aaai_abstract(fetched.body, str(record.get("official_url", "")))
            elif conference == "ICLR":
                soup = BeautifulSoup(fetched.body, "html.parser")
                node = soup.select_one(".paper-abstract")
                extracted = {
                    "abstract": normalize(node.get_text(" ", strip=True)) if node else "",
                    "abstract_source_url": str(record.get("official_url", "")),
                }
            else:
                raise RuntimeError(f"No official metadata adapter for {conference}")
        abstract = str(extracted.get("abstract", ""))
        result.update(
            {
                "status": "fetched" if abstract else "no-abstract",
                "reason": "Official abstract fetched."
                if abstract
                else "Official page exposed no abstract.",
                "abstract": abstract,
                "abstract_source_url": extracted.get("abstract_source_url"),
                "details_url": extracted.get("details_url"),
                "abstract_sha256": sha256_text(abstract) if abstract else None,
                "fetch": metadata_dict(fetched.metadata),
            }
        )
        return result
    except (FetchError, RuntimeError, ValueError) as error:
        result.update(
            {
                "status": "pending",
                "reason": str(error),
                "error_class": getattr(error, "error_class", "metadata-error"),
                "challenge": getattr(error, "challenge", False),
                "attempts": getattr(error, "attempts", None),
                "http_status": getattr(error, "status_code", None),
            }
        )
        return result


def update_census(census: dict[str, Any], results: list[dict[str, Any]]) -> None:
    by_key = {key_for(str(item["conference"]), str(item["title"])): item for item in results}
    for conference in census.get("conferences", []):
        name = str(conference["conference"])
        for paper in conference.get("papers", []):
            result = by_key.get(key_for(name, str(paper["title"])))
            if not result:
                continue
            paper["abstract_status"] = result["status"]
            paper["abstract_reason"] = result["reason"]
            if result.get("abstract"):
                paper["abstract"] = result["abstract"]
                paper["abstract_source_url"] = result.get("abstract_source_url")
                paper["abstract_sha256"] = result.get("abstract_sha256")
            if result.get("details_url"):
                paper["details_url"] = result["details_url"]
            if result.get("fetch"):
                paper["abstract_fetch"] = result["fetch"]
    updated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    census["official_metadata_enrichment"] = {
        "updated_at": updated_at,
        "policy": "Only official conference, proceedings, publisher, or official OpenReview pages are queried; missing metadata remains pending.",
    }
    census["last_audited_at"] = updated_at


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conference", action="append", help="Only enrich these conference IDs.")
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--per-host-concurrency", type=int, default=4)
    parser.add_argument("--per-host-delay", type=float, default=0.25)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument(
        "--pending-only",
        action="store_true",
        help="Retry records whose official abstract is missing or previously pending.",
    )
    args = parser.parse_args()

    census = load_census()
    selected = set(args.conference or ["ASE", "FSE", "ISSTA", "ICSE", "ICML", "AAAI"])
    latest = load_latest_manifest()
    forms: dict[str, dict[str, str]] = {}
    for conference in selected & set(RESEARCHR_SNAPSHOTS):
        snapshot = CACHE_DIR / RESEARCHR_SNAPSHOTS[conference]
        if not snapshot.exists():
            print(f"missing official snapshot for {conference}: {snapshot}", file=sys.stderr)
            continue
        try:
            forms[conference] = researchr_form(snapshot)
        except RuntimeError as error:
            print(str(error), file=sys.stderr)

    jobs: list[tuple[str, dict[str, Any]]] = []
    for conference in census.get("conferences", []):
        name = str(conference["conference"])
        if name not in selected:
            continue
        for paper in conference.get("papers", []):
            if args.pending_only and paper.get("abstract"):
                continue
            if paper.get("abstract") and not args.refresh:
                continue
            previous = latest.get(key_for(name, str(paper["title"])))
            if previous and previous.get("status") == "fetched" and not args.refresh:
                continue
            jobs.append((name, paper))
    if args.limit:
        jobs = jobs[: args.limit]

    print(f"Enriching {len(jobs)} official metadata records with {args.workers} workers.")
    fetcher = StableFetcher(
        user_agent="awesome-coding-agent-papers-metadata/1.0 (+official-source-audit)",
        retry_policy=RetryPolicy(max_attempts=max(1, args.retries)),
        per_host_concurrency=max(1, args.per_host_concurrency),
        per_host_min_interval=max(0.0, args.per_host_delay),
    )
    results: list[dict[str, Any]] = []
    checkpoint: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(fetch_record, name, paper, fetcher, args.timeout, forms): (
                name,
                paper["title"],
            )
            for name, paper in jobs
        }
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            checkpoint.append(result)
            if len(checkpoint) >= 100:
                append_manifest(checkpoint)
                checkpoint.clear()
            if index % 100 == 0 or index == len(futures):
                print(f"completed {index}/{len(futures)}")
    results.sort(key=lambda item: key_for(str(item["conference"]), str(item["title"])))
    append_manifest(checkpoint)
    update_census(census, results)
    write_census(census, only=selected)
    counts: dict[str, int] = {}
    for result in results:
        status = str(result.get("status", "pending"))
        counts[status] = counts.get(status, 0) + 1
    print("metadata summary:", ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
