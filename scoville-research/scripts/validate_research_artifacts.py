#!/usr/bin/env python3
"""Validate the structural integrity of a Scoville Research deep-run package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


LEGACY_REQUIRED_FILES = ("brief.md", "queries.jsonl", "sources.jsonl", "claims.jsonl", "REPORT.md")
V2_REQUIRED_FILES = (
    "brief.md",
    "run.json",
    "queries.jsonl",
    "sources.jsonl",
    "evidence.jsonl",
    "claims.jsonl",
    "REPORT.md",
)
V2_SCHEMA = "scoville-research-run.v2"
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
RUN_KEYS = {
    "schema",
    "skill_sha256",
    "created",
    "updated",
    "phase",
    "status",
    "last_completed_query",
    "external_jobs",
}
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
SOURCE_OPTIONAL_KEYS = {"accessibility", "final_url", "link_status", "content_quality"}
EVIDENCE_KEYS = {
    "id",
    "source_id",
    "locator",
    "relation",
    "inspection",
    "excerpt",
    "observation",
    "content_sha256",
}
CLAIM_KEYS = {"id", "claim", "basis", "status", "support", "contradict"}
CLAIM_OPTIONAL_KEYS = {"as_of"}
EXTERNAL_JOB_KEYS = {
    "id",
    "backend",
    "trust_boundary",
    "estimated_cost_usd",
    "timeout_seconds",
    "job_id",
    "status",
    "last_polled",
    "disclosed_data",
    "upload_sha256",
    "contains_private_data",
    "private_upload_authorized",
    "cleanup_status",
}
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
ACCESSIBILITY_STATES = {"public", "authenticated", "user-provided", "private", "unknown"}
LINK_STATUSES = {"live", "redirected", "dead", "blocked", "unchecked"}
CONTENT_QUALITY_STATES = {"usable", "abstract-only", "paywall-stub", "mismatched", "degraded", "unreadable", "unknown"}
EVIDENCE_RELATIONS = {"supports", "contradicts", "context"}
CLAIM_BASES = {"supplied", "reported", "observed", "inferred"}
CLAIM_STATUSES = {"supported", "single-source", "mixed", "unresolved", "rejected"}
RUN_PHASES = {
    "brief",
    "discovery",
    "inspection",
    "contradiction",
    "gap",
    "synthesis",
    "validation",
    "complete",
    "blocked",
}
RUN_STATUSES = {"in-progress", "complete", "blocked"}
EXTERNAL_JOB_STATUSES = {"planned", "submitted", "running", "completed", "failed", "cancelled"}
TERMINAL_JOB_STATUSES = {"completed", "failed", "cancelled"}
CLEANUP_STATUSES = {"not-required", "pending", "complete", "failed"}
ID_PATTERNS = {
    "query": re.compile(r"^Q[0-9]{3,}$"),
    "source": re.compile(r"^S[0-9]{3,}$"),
    "evidence": re.compile(r"^E[0-9]{3,}$"),
    "claim": re.compile(r"^C[0-9]{3,}$"),
    "external_job": re.compile(r"^J[0-9]{3,}$"),
}
SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
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

    def read_json(self, name: str) -> dict[str, Any] | None:
        text = self.read_text(name)
        if text is None:
            return None
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            self.error("invalid_json", name, f"Invalid JSON object: {exc.msg}", exc.lineno)
            return None
        if not isinstance(value, dict):
            self.error("invalid_record", name, "Artifact must contain one JSON object")
            return None
        return value

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


def compute_skill_sha256(skill_root: Path | None = None) -> str:
    """Hash the exact portable Skill files using a stable relative-path manifest."""
    root = (skill_root or Path(__file__).resolve().parents[1]).resolve()
    files = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix.lower() != ".pyc"
        ),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


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
    line: int | None,
    record: dict[str, Any],
    expected: set[str],
    optional: set[str] | None = None,
) -> None:
    allowed = expected | (optional or set())
    missing = sorted(expected - record.keys())
    unknown = sorted(record.keys() - allowed)
    if missing:
        validation.error("missing_keys", file, f"Missing keys: {', '.join(missing)}", line)
    if unknown:
        validation.error("unknown_keys", file, f"Unknown keys: {', '.join(unknown)}", line)


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nullable_string(value: Any) -> bool:
    return value is None or _string(value)


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_string(item) for item in value) and len(value) == len(set(value))


def _sha256(value: Any, *, nullable: bool = False) -> bool:
    return (value is None and nullable) or (isinstance(value, str) and SHA256_PATTERN.fullmatch(value) is not None)


def _sha256_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) == len(set(value)) and all(_sha256(item) for item in value)


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


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or TIMESTAMP_PATTERN.fullmatch(value) is None:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _unicode_scalar_count(value: str) -> int | None:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        return None
    return len(value)


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


def _validate_external_jobs(validation: Validation, run: dict[str, Any]) -> int:
    jobs = run.get("external_jobs")
    if not isinstance(jobs, list):
        validation.error("invalid_value", "run.json", "external_jobs must be a list")
        return 0

    job_records: list[tuple[int, dict[str, Any]]] = []
    for index, value in enumerate(jobs, start=1):
        if not isinstance(value, dict):
            validation.error("invalid_record", "run.json", "Each external_jobs item must be an object", index)
            continue
        job_records.append((index, value))
    job_ids = _collect_ids(validation, "run.json", job_records, "external_job")

    for index, job in job_records:
        _check_keys(validation, "run.json", index, job, EXTERNAL_JOB_KEYS)
        for key in ("backend", "trust_boundary", "disclosed_data"):
            if not _string(job.get(key)):
                validation.error("invalid_value", "run.json", f"{key} must be a non-empty string", index)
        cost = job.get("estimated_cost_usd")
        if cost is not None and (isinstance(cost, bool) or not isinstance(cost, (int, float)) or cost < 0):
            validation.error("invalid_value", "run.json", "estimated_cost_usd must be non-negative or null", index)
        timeout = job.get("timeout_seconds")
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
            validation.error("invalid_value", "run.json", "timeout_seconds must be a positive integer", index)

        status = job.get("status")
        if status not in EXTERNAL_JOB_STATUSES:
            validation.error("invalid_value", "run.json", f"Invalid external job status: {status!r}", index)
        job_id = job.get("job_id")
        if status == "planned":
            if job_id is not None:
                validation.error("job_state_mismatch", "run.json", "A planned job must not have a provider job_id", index)
        elif status in EXTERNAL_JOB_STATUSES and not _string(job_id):
            validation.error("job_state_mismatch", "run.json", "A submitted or terminal job requires job_id", index)

        last_polled = job.get("last_polled")
        if last_polled is not None and _parse_timestamp(last_polled) is None:
            validation.error("invalid_timestamp", "run.json", "last_polled must be RFC 3339 or null", index)
        if status in {"running", "completed", "failed", "cancelled"} and _parse_timestamp(last_polled) is None:
            validation.error("missing_poll_state", "run.json", f"A {status} job requires last_polled", index)

        if not _sha256_list(job.get("upload_sha256")):
            validation.error("invalid_sha256", "run.json", "upload_sha256 must be a unique SHA-256 list", index)
        private = job.get("contains_private_data")
        authorized = job.get("private_upload_authorized")
        if not isinstance(private, bool) or not isinstance(authorized, bool):
            validation.error("invalid_value", "run.json", "Private-data fields must be booleans", index)
        elif private and not authorized:
            validation.error("unauthorized_private_upload", "run.json", "Private uploads require explicit authorization", index)

        cleanup = job.get("cleanup_status")
        if cleanup not in CLEANUP_STATUSES:
            validation.error("invalid_value", "run.json", f"Invalid cleanup_status: {cleanup!r}", index)
        if status == "planned" and cleanup != "not-required":
            validation.error("job_state_mismatch", "run.json", "A planned job cleanup must be not-required", index)
        if run.get("status") == "complete":
            if status not in TERMINAL_JOB_STATUSES:
                validation.error("unfinished_external_job", "run.json", "A complete run cannot retain a non-terminal external job", index)
            if cleanup not in {"not-required", "complete"}:
                validation.error("incomplete_cleanup", "run.json", "A complete run requires completed or unnecessary cleanup", index)

    return len(job_ids)


def _validate_run(
    validation: Validation,
    run: dict[str, Any] | None,
    query_ids: dict[str, tuple[int, dict[str, Any]]],
) -> int:
    if run is None:
        return 0
    _check_keys(validation, "run.json", None, run, RUN_KEYS)
    if run.get("schema") != V2_SCHEMA:
        validation.error("unsupported_schema", "run.json", f"schema must be {V2_SCHEMA!r}")

    skill_hash = run.get("skill_sha256")
    if not _sha256(skill_hash):
        validation.error("invalid_sha256", "run.json", "skill_sha256 must be a SHA-256 digest")
    elif skill_hash.lower() != compute_skill_sha256():
        validation.error("skill_drift", "run.json", "Recorded Skill bytes differ from the executing Skill package")

    created = _parse_timestamp(run.get("created"))
    updated = _parse_timestamp(run.get("updated"))
    if created is None:
        validation.error("invalid_timestamp", "run.json", "created must be RFC 3339")
    if updated is None:
        validation.error("invalid_timestamp", "run.json", "updated must be RFC 3339")
    if created is not None and updated is not None and updated < created:
        validation.error("invalid_timestamp_order", "run.json", "updated must not precede created")

    phase = run.get("phase")
    status = run.get("status")
    if phase not in RUN_PHASES:
        validation.error("invalid_value", "run.json", f"Invalid phase: {phase!r}")
    if status not in RUN_STATUSES:
        validation.error("invalid_value", "run.json", f"Invalid status: {status!r}")
    if (status == "complete") != (phase == "complete"):
        validation.error("run_state_mismatch", "run.json", "complete status and phase must occur together")
    if (status == "blocked") != (phase == "blocked"):
        validation.error("run_state_mismatch", "run.json", "blocked status and phase must occur together")

    last_query = run.get("last_completed_query")
    if last_query is not None and (not _string(last_query) or last_query not in query_ids):
        validation.error("unknown_query", "run.json", f"Unknown last_completed_query: {last_query!r}")
    return _validate_external_jobs(validation, run)


def validate(root: Path) -> dict[str, Any]:
    validation = Validation(root)
    run_exists = (root / "run.json").is_file()
    evidence_exists = (root / "evidence.jsonl").is_file()
    if not run_exists and evidence_exists:
        validation.error("mixed_package_version", "evidence.jsonl", "evidence.jsonl requires a v2 run.json declaration")

    run = validation.read_json("run.json") if run_exists else None
    declared_v2 = run is not None and run.get("schema") == V2_SCHEMA
    v2_intent = run_exists
    package_version: int | None = 2 if declared_v2 else (None if run_exists else 1)
    legacy = not run_exists

    brief = validation.read_text("brief.md")
    report = validation.read_text("REPORT.md")
    queries = validation.read_jsonl("queries.jsonl")
    sources = validation.read_jsonl("sources.jsonl")
    evidence = validation.read_jsonl("evidence.jsonl") if v2_intent else []
    claims = validation.read_jsonl("claims.jsonl")

    if brief is not None:
        _check_headings(validation, "brief.md", brief, BRIEF_HEADINGS)
    if report is not None:
        _check_headings(validation, "REPORT.md", report, REPORT_HEADINGS)

    query_ids = _collect_ids(validation, "queries.jsonl", queries, "query")
    source_ids = _collect_ids(validation, "sources.jsonl", sources, "source")
    evidence_ids = _collect_ids(validation, "evidence.jsonl", evidence, "evidence") if v2_intent else {}
    claim_ids = _collect_ids(validation, "claims.jsonl", claims, "claim")

    purposes: set[str] = set()
    for line, record in queries:
        _check_keys(validation, "queries.jsonl", line, record, QUERY_KEYS)
        if not _string(record.get("query")):
            validation.error("invalid_value", "queries.jsonl", "query must be a non-empty string", line)
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
        _check_keys(
            validation,
            "sources.jsonl",
            line,
            record,
            SOURCE_KEYS,
            SOURCE_OPTIONAL_KEYS if v2_intent else None,
        )
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
        if v2_intent:
            if "accessibility" in record and record.get("accessibility") not in ACCESSIBILITY_STATES:
                validation.error("invalid_value", "sources.jsonl", f"Invalid accessibility: {record.get('accessibility')!r}", line)
            if "final_url" in record and record.get("final_url") is not None and not _valid_url(record.get("final_url")):
                validation.error("invalid_url", "sources.jsonl", "final_url must be an absolute HTTP(S) URL or null", line)
            if "link_status" in record and record.get("link_status") not in LINK_STATUSES:
                validation.error("invalid_value", "sources.jsonl", f"Invalid link_status: {record.get('link_status')!r}", line)
            if record.get("link_status") == "redirected" and not _valid_url(record.get("final_url")):
                validation.error("missing_final_url", "sources.jsonl", "A redirected source requires final_url", line)
            if "content_quality" in record and record.get("content_quality") not in CONTENT_QUALITY_STATES:
                validation.error("invalid_value", "sources.jsonl", f"Invalid content_quality: {record.get('content_quality')!r}", line)

    if v2_intent:
        for line, record in evidence:
            _check_keys(validation, "evidence.jsonl", line, record, EVIDENCE_KEYS)
            source_id = record.get("source_id")
            if not _string(source_id) or source_id not in source_ids:
                validation.error("unknown_source", "evidence.jsonl", f"Unknown source ID: {source_id!r}", line)
            if not _string(record.get("locator")):
                validation.error("invalid_value", "evidence.jsonl", "locator must be a non-empty string", line)
            if record.get("relation") not in EVIDENCE_RELATIONS:
                validation.error("invalid_value", "evidence.jsonl", f"Invalid relation: {record.get('relation')!r}", line)
            if record.get("inspection") not in INSPECTIONS:
                validation.error("invalid_value", "evidence.jsonl", f"Invalid inspection: {record.get('inspection')!r}", line)
            excerpt = record.get("excerpt")
            observation = record.get("observation")
            if not _nullable_string(excerpt) or not _nullable_string(observation):
                validation.error("invalid_value", "evidence.jsonl", "excerpt and observation must be non-empty strings or null", line)
            if not _string(excerpt) and not _string(observation):
                validation.error("missing_evidence_content", "evidence.jsonl", "Evidence requires an excerpt or scoped observation", line)
            if isinstance(excerpt, str):
                scalar_count = _unicode_scalar_count(excerpt)
                if scalar_count is None:
                    validation.error("invalid_value", "evidence.jsonl", "excerpt contains a non-scalar Unicode value", line)
                elif scalar_count > 1000:
                    validation.error("excerpt_too_long", "evidence.jsonl", "excerpt exceeds 1,000 Unicode scalar values", line)
            if not _sha256(record.get("content_sha256"), nullable=True):
                validation.error("invalid_sha256", "evidence.jsonl", "content_sha256 must be a SHA-256 digest or null", line)

    for line, record in claims:
        _check_keys(
            validation,
            "claims.jsonl",
            line,
            record,
            CLAIM_KEYS,
            CLAIM_OPTIONAL_KEYS if v2_intent else None,
        )
        if not _string(record.get("claim")):
            validation.error("invalid_value", "claims.jsonl", "claim must be a non-empty string", line)
        if record.get("basis") not in CLAIM_BASES:
            validation.error("invalid_value", "claims.jsonl", f"Invalid basis: {record.get('basis')!r}", line)
        if v2_intent and "as_of" in record and not _valid_date(record.get("as_of"), nullable=True):
            validation.error("invalid_date", "claims.jsonl", "as_of must be an ISO date or null", line)
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
            noun = "Evidence" if v2_intent else "Sources"
            validation.error("overlapping_evidence", "claims.jsonl", f"{noun} both support and contradict: {', '.join(overlap)}", line)

        support_source_ids: set[str] = set()
        if v2_intent:
            for role, refs, expected_relation in (
                ("support", support, "supports"),
                ("contradict", contradict, "contradicts"),
            ):
                for ref in refs:
                    evidence_record = evidence_ids.get(ref)
                    if evidence_record is None:
                        validation.error("unknown_evidence", "claims.jsonl", f"Unknown {role} evidence ID: {ref}", line)
                        continue
                    item = evidence_record[1]
                    if item.get("relation") != expected_relation:
                        validation.error("evidence_relation_mismatch", "claims.jsonl", f"Evidence {ref} cannot serve as {role}", line)
                    source_id = item.get("source_id")
                    if role == "support" and isinstance(source_id, str):
                        support_source_ids.add(source_id)
                        source = source_ids.get(source_id)
                        if source and source[1].get("disposition") in {"rejected", "dead", "blocked"}:
                            validation.error("invalid_support", "claims.jsonl", f"Source {source_id} cannot support a claim with its disposition", line)
                        if source and source[1].get("content_quality") in {"paywall-stub", "mismatched", "unreadable"}:
                            validation.error("invalid_support", "claims.jsonl", f"Source {source_id} cannot support a claim with its content_quality", line)
                    if role == "support" and item.get("inspection") == "snippet":
                        validation.error("snippet_support", "claims.jsonl", f"Evidence {ref} is only a snippet and cannot support a claim", line)
        else:
            for role, refs in (("support", support), ("contradict", contradict)):
                for ref in refs:
                    if ref not in source_ids:
                        validation.error("unknown_source", "claims.jsonl", f"Unknown {role} source ID: {ref}", line)
            support_source_ids = set(support)
            for ref in support:
                source = source_ids.get(ref)
                if source and source[1].get("disposition") in {"contradiction", "rejected", "dead", "blocked"}:
                    validation.error("invalid_support", "claims.jsonl", f"Source {ref} cannot support a claim with its disposition", line)
                if source and source[1].get("inspection") == "snippet":
                    validation.error("snippet_support", "claims.jsonl", f"Source {ref} is only a snippet and cannot support a claim", line)

        if status == "supported" and (not support or contradict):
            validation.error("status_mismatch", "claims.jsonl", "supported requires support and no contradiction", line)
        if status == "single-source" and (len(support_source_ids) != 1 or not support or contradict):
            validation.error("status_mismatch", "claims.jsonl", "single-source requires support from exactly one source and no contradiction", line)
        if status == "mixed" and (not support or not contradict):
            validation.error("status_mismatch", "claims.jsonl", "mixed requires support and contradiction", line)

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

    external_jobs = _validate_run(validation, run, query_ids) if v2_intent else 0
    errors = len(validation.diagnostics)
    return {
        "schema_version": 1,
        "package_version": package_version,
        "legacy": legacy,
        "valid": errors == 0,
        "root": str(root),
        "summary": {
            "errors": errors,
            "warnings": 0,
            "files_checked": validation.files_checked,
            "queries": len(query_ids),
            "sources": len(source_ids),
            "evidence": len(evidence_ids),
            "claims": len(claim_ids),
            "external_jobs": external_jobs,
        },
        "diagnostics": [asdict(item) for item in validation.diagnostics],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", help="Deep-research artifact directory")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    parser.add_argument("--print-skill-sha256", action="store_true", help="Print the executing portable Skill package hash")
    args = parser.parse_args(argv)

    if args.print_skill_sha256:
        print(compute_skill_sha256())
        return 0
    if not args.root:
        parser.error("root is required unless --print-skill-sha256 is used")

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        result = {
            "schema_version": 1,
            "package_version": None,
            "legacy": None,
            "valid": None,
            "root": str(root),
            "summary": {
                "errors": 1,
                "warnings": 0,
                "files_checked": 0,
                "queries": 0,
                "sources": 0,
                "evidence": 0,
                "claims": 0,
                "external_jobs": 0,
            },
            "diagnostics": [asdict(Diagnostic("invalid_root", ".", None, "Root is not a readable directory"))],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else "invalid_root: Root is not a readable directory")
        return 2

    result = validate(root)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "valid" if result["valid"] else "invalid"
        version = result["package_version"] if result["package_version"] is not None else "unknown"
        print(f"{status}: package v{version}; {result['summary']['errors']} error(s)")
        for item in result["diagnostics"]:
            location = item["file"] + (f":{item['line']}" if item["line"] is not None else "")
            print(f"{location}: {item['code']}: {item['message']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
