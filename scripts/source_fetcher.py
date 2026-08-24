"""Durable, polite HTTP fetching primitives for official conference sources.

This module deliberately stays small and dependency-light.  It provides the
parts that a conference adapter should not have to reimplement: per-host
concurrency and pacing, explicit retry classification, resumable atomic PDF
downloads, content hashes, and an append-only JSONL ledger that can survive a
process interruption.

It is not a stealth crawler.  A challenge page or CAPTCHA is recorded as a
pending source and is never handled by proxy rotation or challenge bypass.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import random
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter

RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}
CHALLENGE_MARKERS = (
    "challenge verification required",
    "captcha",
    "cf-chl-",
    "cloudflare ray id",
)


class FetchError(RuntimeError):
    """An HTTP or transport failure with enough context for an audit record."""

    def __init__(
        self,
        message: str,
        *,
        url: str,
        status_code: int | None = None,
        attempts: int = 0,
        error_class: str = "fetch-error",
        challenge: bool = False,
    ) -> None:
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        self.attempts = attempts
        self.error_class = error_class
        self.challenge = challenge


@dataclass(frozen=True)
class RetryPolicy:
    """Bounded exponential retry settings.

    The random jitter is injected into ``StableFetcher`` so tests can be
    deterministic without disabling the production backoff.
    """

    max_attempts: int = 5
    base_delay: float = 1.0
    max_delay: float = 60.0
    jitter: float = 0.25


@dataclass(frozen=True)
class FetchMetadata:
    url: str
    status_code: int
    content_type: str
    etag: str | None
    last_modified: str | None
    sha256: str
    byte_size: int
    attempts: int
    retrieved_at: str


@dataclass(frozen=True)
class FetchedBytes:
    body: bytes
    metadata: FetchMetadata


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    """Write a snapshot without exposing a half-written final file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".part")
    partial.write_bytes(payload)
    partial.replace(path)


def parse_retry_after(value: str | None, now: datetime | None = None) -> float | None:
    """Return a non-negative delay for an HTTP ``Retry-After`` value."""

    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        current = now or datetime.now(timezone.utc)
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return max(0.0, (parsed - current).total_seconds())
    except (TypeError, ValueError, OverflowError):
        return None


def is_challenge_body(payload: bytes) -> bool:
    sample = payload[:8192].decode("utf-8", errors="replace").lower()
    return any(marker in sample for marker in CHALLENGE_MARKERS)


def decode_undocumented_gzip(payload: bytes) -> bytes:
    """Decode gzip bytes when an upstream omits its Content-Encoding header."""

    if not payload.startswith(b"\x1f\x8b"):
        return payload
    try:
        return gzip.decompress(payload)
    except OSError:
        return payload


class HostLimiter:
    """Apply a concurrency cap and a minimum inter-request interval per host."""

    def __init__(
        self,
        *,
        max_concurrency: int,
        min_interval: float,
        sleep: Callable[[float], None],
    ) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")
        if min_interval < 0:
            raise ValueError("min_interval cannot be negative")
        self.max_concurrency = max_concurrency
        self.min_interval = min_interval
        self._sleep = sleep
        self._semaphores: dict[str, threading.BoundedSemaphore] = {}
        self._last_request: dict[str, float] = {}
        self._lock = threading.Lock()

    def _semaphore(self, host: str) -> threading.BoundedSemaphore:
        with self._lock:
            value = self._semaphores.get(host)
            if value is None:
                value = threading.BoundedSemaphore(self.max_concurrency)
                self._semaphores[host] = value
            return value

    @contextmanager
    def slot(self, host: str) -> Iterator[None]:
        semaphore = self._semaphore(host)
        semaphore.acquire()
        try:
            with self._lock:
                previous = self._last_request.get(host)
                now = time.monotonic()
                delay = 0.0 if previous is None else self.min_interval - (now - previous)
                self._last_request[host] = now + max(0.0, delay)
            if delay > 0:
                self._sleep(delay)
            yield
        finally:
            semaphore.release()


class StableFetcher:
    """Fetch official pages and files with explicit, auditable failure modes."""

    def __init__(
        self,
        *,
        user_agent: str,
        retry_policy: RetryPolicy | None = None,
        per_host_concurrency: int = 2,
        per_host_min_interval: float = 0.25,
        session_factory: Callable[[], Any] = requests.Session,
        sleep: Callable[[float], None] = time.sleep,
        random_value: Callable[[], float] = random.random,
    ) -> None:
        self.user_agent = user_agent
        self.retry_policy = retry_policy or RetryPolicy()
        self._session_factory = session_factory
        self._sleep = sleep
        self._random = random_value
        self._local = threading.local()
        self._per_host_concurrency = max(1, per_host_concurrency)
        self._limiter = HostLimiter(
            max_concurrency=self._per_host_concurrency,
            min_interval=per_host_min_interval,
            sleep=sleep,
        )

    def _session(self) -> Any:
        session = getattr(self._local, "session", None)
        if session is None:
            session = self._session_factory()
            if hasattr(session, "mount"):
                adapter = HTTPAdapter(
                    pool_connections=4,
                    pool_maxsize=self._per_host_concurrency,
                    max_retries=0,
                )
                session.mount("http://", adapter)
                session.mount("https://", adapter)
            if hasattr(session, "headers"):
                session.headers.update(
                    {
                        "User-Agent": self.user_agent,
                        "Accept-Encoding": "identity",
                    }
                )
            self._local.session = session
        return session

    def _delay_for_attempt(self, attempt: int, retry_after: str | None) -> float:
        server_delay = parse_retry_after(retry_after)
        if server_delay is not None:
            return min(self.retry_policy.max_delay, server_delay)
        exponential = min(
            self.retry_policy.max_delay,
            self.retry_policy.base_delay * (2 ** max(0, attempt - 1)),
        )
        return min(
            self.retry_policy.max_delay,
            exponential + (self._random() * self.retry_policy.jitter),
        )

    def _sleep_before_retry(self, attempt: int, retry_after: str | None) -> None:
        self._sleep(self._delay_for_attempt(attempt, retry_after))

    def request_bytes(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: tuple[float, float] = (15.0, 90.0),
    ) -> FetchedBytes:
        """Fetch a bounded-size page or export and return its body plus metadata."""

        request_headers = dict(headers or {})
        last_error: FetchError | None = None
        for attempt in range(1, self.retry_policy.max_attempts + 1):
            response = None
            try:
                host = urlparse(url).netloc.lower()
                with self._limiter.slot(host):
                    response = self._session().request(
                        method,
                        url,
                        params=params,
                        data=data,
                        headers=request_headers,
                        timeout=timeout,
                        stream=True,
                        allow_redirects=True,
                    )
                    status = int(response.status_code)
                    content_type = str(response.headers.get("content-type", ""))
                    if status in RETRYABLE_STATUS_CODES:
                        retry_after = response.headers.get("retry-after")
                        if attempt < self.retry_policy.max_attempts:
                            response.close()
                            self._sleep_before_retry(attempt, retry_after)
                            continue
                        raise FetchError(
                            f"HTTP {status} after {attempt} attempts",
                            url=url,
                            status_code=status,
                            attempts=attempt,
                            error_class=f"http-{status}",
                        )
                    body = decode_undocumented_gzip(
                        b"".join(response.iter_content(chunk_size=1024 * 1024))
                    )
                    if status >= 400:
                        challenge = status == 403 or is_challenge_body(body)
                        raise FetchError(
                            f"HTTP {status} for {url}",
                            url=url,
                            status_code=status,
                            attempts=attempt,
                            error_class="challenge" if challenge else f"http-{status}",
                            challenge=challenge,
                        )
                    metadata = FetchMetadata(
                        url=url,
                        status_code=status,
                        content_type=content_type,
                        etag=response.headers.get("etag"),
                        last_modified=response.headers.get("last-modified"),
                        sha256=sha256_bytes(body),
                        byte_size=len(body),
                        attempts=attempt,
                        retrieved_at=utc_now(),
                    )
                    return FetchedBytes(body=body, metadata=metadata)
            except FetchError as error:
                last_error = error
                if error.challenge or error.status_code not in RETRYABLE_STATUS_CODES:
                    raise
                if attempt >= self.retry_policy.max_attempts:
                    raise
            except requests.RequestException as error:
                last_error = FetchError(
                    str(error),
                    url=url,
                    attempts=attempt,
                    error_class="transport-error",
                )
                if attempt >= self.retry_policy.max_attempts:
                    raise last_error from error
                self._sleep_before_retry(attempt, None)
            finally:
                if response is not None:
                    response.close()
        raise last_error or FetchError("request failed", url=url)

    def download(
        self,
        url: str,
        destination: Path,
        *,
        timeout: tuple[float, float] = (15.0, 180.0),
        refresh: bool = False,
        expected_prefix: bytes | None = None,
    ) -> FetchMetadata:
        """Download a file with a resumable ``.part`` file and atomic replace."""

        destination.parent.mkdir(parents=True, exist_ok=True)
        cached_prefix_ok = True
        if destination.exists() and expected_prefix:
            with destination.open("rb") as handle:
                cached_prefix_ok = handle.read(len(expected_prefix)) == expected_prefix
        if destination.exists() and not refresh and cached_prefix_ok:
            return FetchMetadata(
                url=url,
                status_code=200,
                content_type="cached",
                etag=None,
                last_modified=None,
                sha256=sha256_file(destination),
                byte_size=destination.stat().st_size,
                attempts=0,
                retrieved_at=utc_now(),
            )

        partial = destination.with_suffix(destination.suffix + ".part")
        if partial.exists() and expected_prefix:
            with partial.open("rb") as handle:
                partial_prefix_ok = handle.read(len(expected_prefix)) == expected_prefix
            if not partial_prefix_ok:
                partial.unlink()
        last_error: FetchError | None = None
        for attempt in range(1, self.retry_policy.max_attempts + 1):
            response = None
            start_at = partial.stat().st_size if partial.exists() else 0
            request_headers: dict[str, str] = {}
            if start_at:
                request_headers["Range"] = f"bytes={start_at}-"
            try:
                host = urlparse(url).netloc.lower()
                with self._limiter.slot(host):
                    response = self._session().get(
                        url,
                        headers=request_headers,
                        timeout=timeout,
                        stream=True,
                        allow_redirects=True,
                    )
                    status = int(response.status_code)
                    if status in RETRYABLE_STATUS_CODES:
                        retry_after = response.headers.get("retry-after")
                        if attempt < self.retry_policy.max_attempts:
                            response.close()
                            self._sleep_before_retry(attempt, retry_after)
                            continue
                        raise FetchError(
                            f"HTTP {status} after {attempt} attempts",
                            url=url,
                            status_code=status,
                            attempts=attempt,
                            error_class=f"http-{status}",
                        )
                    body_sample = b""
                    if start_at and status == 416:
                        partial.unlink(missing_ok=True)
                        continue
                    if status >= 400:
                        body_sample = response.content[:8192]
                        challenge = status == 403 or is_challenge_body(body_sample)
                        raise FetchError(
                            f"HTTP {status} for {url}",
                            url=url,
                            status_code=status,
                            attempts=attempt,
                            error_class="challenge" if challenge else f"http-{status}",
                            challenge=challenge,
                        )
                    append = start_at > 0 and status == 206
                    mode = "ab" if append else "wb"
                    with partial.open(mode) as handle:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                if not body_sample:
                                    body_sample = chunk[:8192]
                                handle.write(chunk)
                    if expected_prefix:
                        with partial.open("rb") as handle:
                            actual_prefix = handle.read(len(expected_prefix))
                        if actual_prefix != expected_prefix:
                            raise FetchError(
                                "downloaded content does not have the expected prefix",
                                url=url,
                                status_code=status,
                                attempts=attempt,
                                error_class="content-mismatch",
                            )
                    partial.replace(destination)
                    return FetchMetadata(
                        url=url,
                        status_code=status,
                        content_type=str(response.headers.get("content-type", "")),
                        etag=response.headers.get("etag"),
                        last_modified=response.headers.get("last-modified"),
                        sha256=sha256_file(destination),
                        byte_size=destination.stat().st_size,
                        attempts=attempt,
                        retrieved_at=utc_now(),
                    )
            except FetchError as error:
                last_error = error
                if error.challenge or error.error_class == "content-mismatch":
                    raise
                if error.status_code not in RETRYABLE_STATUS_CODES:
                    raise
                if attempt >= self.retry_policy.max_attempts:
                    raise
            except requests.RequestException as error:
                last_error = FetchError(
                    str(error),
                    url=url,
                    attempts=attempt,
                    error_class="transport-error",
                )
                if attempt >= self.retry_policy.max_attempts:
                    raise last_error from error
                self._sleep_before_retry(attempt, None)
            finally:
                if response is not None:
                    response.close()
        raise last_error or FetchError("download failed", url=url)


class JsonlLedger:
    """Append-only source ledger with latest-record lookup and crash tolerance."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def latest(self) -> dict[str, dict[str, Any]]:
        records: dict[str, dict[str, Any]] = {}
        if not self.path.exists():
            return records
        with self.path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    # A process can be killed after writing only part of the
                    # final line.  Preserve earlier complete records.
                    continue
                key = record.get("source_key")
                if key:
                    records[str(key)] = record
        return records

    def append(self, record: dict[str, Any]) -> dict[str, Any]:
        payload = dict(record)
        payload.setdefault("recorded_at", utc_now())
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
        return payload


def metadata_dict(metadata: FetchMetadata) -> dict[str, Any]:
    return asdict(metadata)
