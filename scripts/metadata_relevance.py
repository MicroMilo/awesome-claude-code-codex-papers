"""High-recall title/abstract triage for coding-agent paper acquisition.

This is deliberately a transparent pre-filter, not the final inclusion rule.
It is used to avoid downloading large PDFs for records whose official title and
abstract contain no plausible connection to code, software engineering, LLMs,
or agents.  A positive result still requires full-text review; a missing
abstract is never treated as an exclusion.
"""

from __future__ import annotations

import re
from typing import Any

SCREEN_VERSION = "conference-metadata-relevance-v2"

_PATTERNS: dict[str, dict[str, re.Pattern[str]]] = {
    "product": {
        "claude-code": re.compile(r"\bclaude[ -]code(?:[ -]cli)?\b", re.IGNORECASE),
        "codex-cli": re.compile(
            r"\b(?:codex[ -]cli|repo[ -]codex|openai[ -]codex)\b", re.IGNORECASE
        ),
        "codex-agent": re.compile(r"\bcodex[ -]agent\b", re.IGNORECASE),
    },
    "agent": {
        "coding-agent": re.compile(r"\bcoding[ -]agent(?:s)?\b", re.IGNORECASE),
        "code-agent": re.compile(r"\bcode[ -]agent(?:s)?\b", re.IGNORECASE),
        "software-engineering-agent": re.compile(
            r"\bsoftware[ -]engineering[ -]agent(?:s)?\b", re.IGNORECASE
        ),
        "agentic": re.compile(r"\bagentic\b|\bautonomous[ -](?:coding|software)\b", re.IGNORECASE),
        "tool-use": re.compile(r"\btool[- ](?:use|using|calling)\b", re.IGNORECASE),
        "multi-agent": re.compile(r"\bmulti[- ]agent(?:s)?\b", re.IGNORECASE),
    },
    "language-model": {
        "llm": re.compile(r"\bllm(?:s)?\b|\blarge[ -]language[ -]model(?:s)?\b", re.IGNORECASE),
        "language-model": re.compile(r"\blanguage[ -]model(?:s)?\b", re.IGNORECASE),
        "foundation-model": re.compile(r"\bfoundation[ -]model(?:s)?\b", re.IGNORECASE),
        "generative-ai": re.compile(r"\bgenerative[ -]ai\b", re.IGNORECASE),
        "named-model": re.compile(r"\b(?:gpt|claude|codex)[ -]?\d", re.IGNORECASE),
    },
    "code-domain": {
        # A bare ``code`` is intentionally not enough: conference abstracts
        # often say only that the authors' source code is available.
        "code": re.compile(r"\b(?:code|coding|codebase|repository|repositories)\b", re.IGNORECASE),
        "code-task": re.compile(
            r"\b(?:source[ -]code|code[ -](?:generation|completion|repair)|"
            r"program[ -](?:repair|synthesis)|bug[ -]fix(?:ing)?|issue[ -]resolution|"
            r"software[ -]engineering|repository[ -]level|codebase|"
            r"developer|debugging|test[ -]generation|compiler|terminal|static[ -]analysis|"
            r"programming[ -]task|coding[ -]task|code[ -]language[ -]model|"
            r"language[ -]model(?:s)?[ -]for[ -]code|swe[- ]bench)\b",
            re.IGNORECASE,
        ),
    },
}


def _matches(pattern: re.Pattern[str], text: str) -> list[str]:
    values: list[str] = []
    for match in pattern.finditer(text):
        value = " ".join(match.group(0).split())
        if value.casefold() not in {item.casefold() for item in values}:
            values.append(value)
    return values


def _collect(text: str, group: str) -> dict[str, list[str]]:
    return {
        name: matches
        for name, pattern in _PATTERNS[group].items()
        if (matches := _matches(pattern, text))
    }


def _flatten(groups: dict[str, dict[str, list[str]]]) -> list[str]:
    values: list[str] = []
    for group in groups.values():
        for matches in group.values():
            for value in matches:
                if value.casefold() not in {item.casefold() for item in values}:
                    values.append(value)
    return values


def screen_metadata(title: str, abstract: str | None) -> dict[str, Any]:
    """Return an auditable, high-recall metadata screening decision.

    ``candidate`` means the record should enter the PDF queue.  ``filtered``
    is safe only when an abstract was successfully obtained and no relevant
    signal is present.  ``pending`` means the metadata is insufficient to
    make that decision.
    """

    normalized_title = " ".join(str(title).split()).strip()
    normalized_abstract = " ".join(str(abstract or "").split()).strip()
    if not normalized_abstract:
        title_groups = {
            group: _collect(normalized_title, group)
            for group in ("product", "agent", "language-model", "code-domain")
        }
        title_product_hits = title_groups["product"]
        title_specific_agent_hits = {
            key: value
            for key, value in title_groups["agent"].items()
            if key in {"coding-agent", "code-agent", "software-engineering-agent"}
        }
        if title_product_hits or title_specific_agent_hits:
            return {
                "screen_version": SCREEN_VERSION,
                "screen_status": "candidate",
                "screen_decision": "candidate",
                "screen_reason": "Direct product or coding-agent signal found in title; abstract unavailable.",
                "screen_source": "title+abstract",
                "abstract_chars": 0,
                "matched_signals": title_groups,
                "matched_terms": _flatten(title_groups),
            }
        return {
            "screen_version": SCREEN_VERSION,
            "screen_status": "pending",
            "screen_decision": "pending",
            "screen_reason": "Official detail page did not expose an abstract.",
            "screen_source": "title+abstract",
            "abstract_chars": 0,
            "matched_signals": {},
            "matched_terms": [],
        }

    text = f"{normalized_title}\n{normalized_abstract}"
    groups = {
        group: _collect(text, group)
        for group in ("product", "agent", "language-model", "code-domain")
    }
    product_hits = groups["product"]
    agent_hits = groups["agent"]
    model_hits = groups["language-model"]
    code_hits = groups["code-domain"]
    strong_code_hits = {key: value for key, value in code_hits.items() if key != "code"}
    specific_agent_hits = {
        key: value
        for key, value in agent_hits.items()
        if key in {"coding-agent", "code-agent", "software-engineering-agent"}
    }

    # Direct product names are always retained.  Other combinations are
    # intentionally broad: the expensive PDF scan is the precision stage.
    candidate = bool(
        product_hits
        or specific_agent_hits
        or (agent_hits and strong_code_hits)
        or (model_hits and strong_code_hits)
    )
    if candidate:
        if product_hits:
            reason = "Direct Claude Code/Codex product signal found in title or abstract."
        elif specific_agent_hits:
            reason = "Direct coding-agent or software-engineering-agent signal found in title or abstract."
        elif agent_hits and strong_code_hits:
            reason = "Agent and code/software-engineering signals found in title or abstract."
        elif model_hits and strong_code_hits:
            reason = (
                "Language-model and code/software-engineering signals found in title or abstract."
            )
        else:
            reason = "Language-model and agent signals found in title or abstract."
        status = "candidate"
        decision = "candidate"
    else:
        reason = "No high-recall coding-agent, code, software-engineering, or language-model combination found in title or abstract."
        status = "filtered"
        decision = "excluded"

    return {
        "screen_version": SCREEN_VERSION,
        "screen_status": status,
        "screen_decision": decision,
        "screen_reason": reason,
        "screen_source": "title+abstract",
        "abstract_chars": len(normalized_abstract),
        "matched_signals": groups,
        "matched_terms": _flatten(groups),
    }
