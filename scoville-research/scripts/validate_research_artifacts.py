#!/usr/bin/env python3
"""Validate the structural integrity of a Scoville Research deep-run package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


REQUIRED_FILES = ("brief.md", "queries.jsonl", "sources.jsonl", "claims.jsonl", "REPORT.md")
BRIEF_HEADINGS = (
    "# Research brief",
    "## Research question",
    "## Decision or reader",
    "## Scope",
    "## Evidence lanes",
    "## Deliverable",
    "## Data boundary",
)
REPORT_HEADINGS = (
    "# Research report",
    "## Answer",
    "## Method and coverage",
    "## Findings",
    "## Contradictions and open questions",
    "## Implications and next step",
    "## Sources",
)
QUERY_KEYS = {"id", "query", "lane", "purpose", "result", "source_ids"}
SOURCE_KEYS = {
    "id",
    "url",
    "title",
    "kind",
    "publisher",
    "published",
    "accessed",
    "inspection",
    "disposition",
    "notes",
}
CLAIM_KEYS = {"id", "claim", "basis", "status", "support", "contradict"}
QUERY_LANES = {"general", "development", "academic"}
QUERY_PURPOSES = {"discovery", "verification", "contradiction", "gap"}
QUERY_RESULTS = {"new-source", "new-claim", "no-new-evidence", "dead-end", "blocked"}
SOURCE_KINDS = {
    "spec",
    "docs",
    "code",
    "release",
    "issue",
    "pull-request",
    "benchmark",
    "paper",
    "preprint",
    "dataset",
    "institutional",
    "community",
    "other",
}
INSPECTIONS = {"full", "section", "abstract", "metadata", "snippet"}
DISPOSITIONS = {"used", "context", "contradiction", "rejected", "dead", "blocked"}
CLAIM_BASES = {"supplied", "reported", "observed", "inferred"}
CLAIM_STATUSES = {"supported", "single-source", "mixed", "unresolved", "rejected"}
ID_PATTERNS = {
    "query": re.compile(r"^Q[0-9]{3,}$"),
    "source": re.compile(r"^S[0-9]{3,}$"),
    "claim": re.compile(r"^C[0-9]{3,}$"),
}
REPORT_CITATION = re.compile(r"\[(S[0-9]{3,})\]")


@dataclass(frozen=True)
class Diagnostic:
    code: str
    file: str
    line: int | None
    message: str


class Validation:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.diagnostics: list[Diagnostic] = []
        self.files_checked = 0

    def error(self, code: str, file: str, message: str, line: int | None = None) -> None:
        self.diagnostics.append(Diagnostic(code, file, line, message))

    def read_text(self, name: str) -> str | None:
        path = self.root / name
        if not path.is_file():
            self.error("missing_file", name, "Required artifact is missing")
            return None
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.error("unreadable_file", name, f"Cannot read UTF-8 artifact: {exc}")
            return None
        self.files_checked += 1
        return text

    def read_jsonl(self, name: str) -> list[tuple[int, dict[str, Any]]]:
        text = self.read_text(name)
        if text is None:
            return []
        records: list[tuple[int, dict[str, Any]]] = []
        for line_number, raw in enumerate(text.splitlines(), start=1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                self.error("invalid_json", name, f"Invalid JSON object: {exc.msg}", line_number)
                continue
            if not isinstance(value, dict):
                self.error("invalid_record", name, "Each JSONL line must be one object", line_number)
                continue
            records.append((line_number, value))
        return records


def _check_headings(validation: Validation, file: str, text: str, expected: Iterable[str]) -> None:
    positions: list[int] = []
    for heading in expected:
        match = re.search(rf"(?m)^{re.escape(heading)}\s*$", text)
        if match is None:
            validation.error("missing_heading", file, f"Missing heading: {heading}")
            continue
        positions.append(match.start())
    if positions != sorted(positions):
        validation.error("heading_order", file, "Required headings are out of order")


def _check_keys(
    validation: Validation,
    file: str,
    line: int,
    record: dict[str, Any],
    expected: set[str],
) -> None:
    missing = sorted(expected - record.keys())
    unknown = sorted(record.keys() - expected)
    if missing:
        validation.error("missing_keys", file, f"Missing keys: {', '.join(missing)}", line)
    if unknown:
        validation.error("unknown_keys", file, f"Unknown keys: {', '.join(unknown)}", line)


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_string(item) for item in value) and len(value) == len(set(value))


def _valid_date(value: Any, *, nullable: bool = False) -> bool:
    if value is None:
        return nullable
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _collect_ids(
    validation: Validation,
    file: str,
    records: list[tuple[int, dict[str, Any]]],
    kind: str,
) -> dict[str, tuple[int, dict[str, Any]]]:
    result: dict[str, tuple[int, dict[str, Any]]] = {}
    for line, record in records:
        identifier = record.get("id")
        if not isinstance(identifier, str) or not ID_PATTERNS[kind].fullmatch(identifier):
            validation.error("invalid_id", file, f"Invalid {kind} ID: {identifier!r}", line)
            continue
        if identifier in result:
            validation.error("duplicate_id", file, f"Duplicate ID: {identifier}", line)
            continue
        result[identifier] = (line, record)
    return result


def validate(root: Path) -> dict[str, Any]:
    validation = Validation(root)
    brief = validation.read_text("brief.md")
    report = validation.read_text("REPORT.md")
    queries = validation.read_jsonl("queries.jsonl")
    sources = validation.read_jsonl("sources.jsonl")
    claims = validation.read_jsonl("claims.jsonl")

    if brief is not None:
        _check_headings(validation, "brief.md", brief, BRIEF_HEADINGS)
    if report is not None:
        _check_headings(validation, "REPORT.md", report, REPORT_HEADINGS)

    query_ids = _collect_ids(validation, "queries.jsonl", queries, "query")
    source_ids = _collect_ids(validation, "sources.jsonl", sources, "source")
    claim_ids = _collect_ids(validation, "claims.jsonl", claims, "claim")

    purposes: set[str] = set()
    for line, record in queries:
        _check_keys(validation, "queries.jsonl", line, record, QUERY_KEYS)
        for key in ("query",):
            if not _string(record.get(key)):
                validation.error("invalid_value", "queries.jsonl", f"{key} must be a non-empty string", line)
        for key, allowed in (("lane", QUERY_LANES), ("purpose", QUERY_PURPOSES), ("result", QUERY_RESULTS)):
            if record.get(key) not in allowed:
                validation.error("invalid_value", "queries.jsonl", f"Invalid {key}: {record.get(key)!r}", line)
        if record.get("purpose") in QUERY_PURPOSES:
            purposes.add(record["purpose"])
        refs = record.get("source_ids")
        if not _string_list(refs):
            validation.error("invalid_value", "queries.jsonl", "source_ids must be a unique string list", line)
        else:
            for ref in refs:
                if ref not in source_ids:
                    validation.error("unknown_source", "queries.jsonl", f"Unknown source ID: {ref}", line)

    for required_purpose in ("contradiction", "gap"):
        if required_purpose not in purposes:
            validation.error("missing_query_purpose", "queries.jsonl", f"No {required_purpose} query is recorded")

    for line, record in sources:
        _check_keys(validation, "sources.jsonl", line, record, SOURCE_KEYS)
        for key in ("title", "publisher", "notes"):
            if not _string(record.get(key)):
                validation.error("invalid_value", "sources.jsonl", f"{key} must be a non-empty string", line)
        if not _valid_url(record.get("url")):
            validation.error("invalid_url", "sources.jsonl", "url must be an absolute HTTP(S) URL", line)
        if record.get("kind") not in SOURCE_KINDS:
            validation.error("invalid_value", "sources.jsonl", f"Invalid kind: {record.get('kind')!r}", line)
        if record.get("inspection") not in INSPECTIONS:
            validation.error("invalid_value", "sources.jsonl", f"Invalid inspection: {record.get('inspection')!r}", line)
        if record.get("disposition") not in DISPOSITIONS:
            validation.error("invalid_value", "sources.jsonl", f"Invalid disposition: {record.get('disposition')!r}", line)
        if not _valid_date(record.get("published"), nullable=True):
            validation.error("invalid_date", "sources.jsonl", "published must be an ISO date or null", line)
        if not _valid_date(record.get("accessed")):
            validation.error("invalid_date", "sources.jsonl", "accessed must be an ISO date", line)

    for line, record in claims:
        _check_keys(validation, "claims.jsonl", line, record, CLAIM_KEYS)
        if not _string(record.get("claim")):
            validation.error("invalid_value", "claims.jsonl", "claim must be a non-empty string", line)
        if record.get("basis") not in CLAIM_BASES:
            validation.error("invalid_value", "claims.jsonl", f"Invalid basis: {record.get('basis')!r}", line)
        status = record.get("status")
        if status not in CLAIM_STATUSES:
            validation.error("invalid_value", "claims.jsonl", f"Invalid status: {status!r}", line)
        support = record.get("support")
        contradict = record.get("contradict")
        if not _string_list(support) or not _string_list(contradict):
            validation.error("invalid_value", "claims.jsonl", "support and contradict must be unique string lists", line)
            continue
        overlap = sorted(set(support) & set(contradict))
        if overlap:
            validation.error("overlapping_evidence", "claims.jsonl", f"Sources both support and contradict: {', '.join(overlap)}", line)
        for role, refs in (("support", support), ("contradict", contradict)):
            for ref in refs:
                if ref not in source_ids:
                    validation.error("unknown_source", "claims.jsonl", f"Unknown {role} source ID: {ref}", line)
        if status == "supported" and (not support or contradict):
            validation.error("status_mismatch", "claims.jsonl", "supported requires support and no contradiction", line)
        if status == "single-source" and (len(support) != 1 or contradict):
            validation.error("status_mismatch", "claims.jsonl", "single-source requires exactly one support and no contradiction", line)
        if status == "mixed" and (not support or not contradict):
            validation.error("status_mismatch", "claims.jsonl", "mixed requires support and contradiction", line)
        for ref in support:
            source = source_ids.get(ref)
            if source and source[1].get("disposition") in {"contradiction", "rejected", "dead", "blocked"}:
                validation.error("invalid_support", "claims.jsonl", f"Source {ref} cannot support a claim with its disposition", line)
            if source and source[1].get("inspection") == "snippet":
                validation.error("snippet_support", "claims.jsonl", f"Source {ref} is only a snippet and cannot support a claim", line)

    if report is not None:
        cited = set(REPORT_CITATION.findall(report))
        if source_ids and not cited:
            validation.error("missing_citations", "REPORT.md", "Report contains no source-ID citation")
        for ref in sorted(cited - source_ids.keys()):
            validation.error("unknown_citation", "REPORT.md", f"Unknown cited source ID: {ref}")
        expected_citations = {
            source_id
            for source_id, (_, source) in source_ids.items()
            if source.get("disposition") in {"used", "contradiction"}
        }
        for ref in sorted(expected_citations - cited):
            validation.error("uncited_used_source", "REPORT.md", f"Used or contradicting source is not cited: {ref}")

    errors = len(validation.diagnostics)
    return {
        "schema_version": 1,
        "valid": errors == 0,
        "root": str(root),
        "summary": {
            "errors": errors,
            "warnings": 0,
            "files_checked": validation.files_checked,
            "queries": len(query_ids),
            "sources": len(source_ids),
            "claims": len(claim_ids),
        },
        "diagnostics": [asdict(item) for item in validation.diagnostics],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Deep-research artifact directory")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        result = {
            "schema_version": 1,
            "valid": None,
            "root": str(root),
            "summary": {"errors": 1, "warnings": 0, "files_checked": 0, "queries": 0, "sources": 0, "claims": 0},
            "diagnostics": [asdict(Diagnostic("invalid_root", ".", None, "Root is not a readable directory"))],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else "invalid_root: Root is not a readable directory")
        return 2

    result = validate(root)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "valid" if result["valid"] else "invalid"
        print(f"{status}: {result['summary']['errors']} error(s)")
        for item in result["diagnostics"]:
            location = item["file"] + (f":{item['line']}" if item["line"] is not None else "")
            print(f"{location}: {item['code']}: {item['message']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
