from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[2] / "scoville-research" / "scripts" / "validate_research_artifacts.py"
SPEC = importlib.util.spec_from_file_location("validate_research_artifacts", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ValidateResearchArtifactsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.write_valid()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_valid(self) -> None:
        (self.root / "brief.md").write_text(
            "# Research brief\n\n"
            "## Research question\nQuestion.\n\n"
            "## Decision or reader\nReader.\n\n"
            "## Scope\nScope.\n\n"
            "## Evidence lanes\nLanes.\n\n"
            "## Deliverable\nReport.\n\n"
            "## Data boundary\nPublic only.\n",
            encoding="utf-8",
        )
        self.write_jsonl(
            "queries.jsonl",
            [
                {"id": "Q001", "query": "topic", "lane": "general", "purpose": "discovery", "result": "new-source", "source_ids": ["S001"]},
                {"id": "Q002", "query": "topic failure", "lane": "general", "purpose": "contradiction", "result": "new-source", "source_ids": ["S002"]},
                {"id": "Q003", "query": "topic gap", "lane": "general", "purpose": "gap", "result": "no-new-evidence", "source_ids": []},
            ],
        )
        self.write_jsonl(
            "sources.jsonl",
            [
                {"id": "S001", "url": "https://example.com/spec", "title": "Specification", "kind": "spec", "publisher": "Example", "published": "2026-08-01", "accessed": "2026-08-19", "inspection": "section", "disposition": "used", "notes": "Owns the contract."},
                {"id": "S002", "url": "https://example.com/failure", "title": "Failure report", "kind": "issue", "publisher": "Example", "published": None, "accessed": "2026-08-19", "inspection": "full", "disposition": "contradiction", "notes": "Documents a conflicting case."},
            ],
        )
        self.write_jsonl(
            "claims.jsonl",
            [
                {"id": "C001", "claim": "The feature exists with a known exception.", "basis": "inferred", "status": "mixed", "support": ["S001"], "contradict": ["S002"]}
            ],
        )
        (self.root / "REPORT.md").write_text(
            "# Research report\n\n"
            "## Answer\nSupported with an exception [S001] [S002].\n\n"
            "## Method and coverage\nFrozen sources.\n\n"
            "## Findings\nFinding.\n\n"
            "## Contradictions and open questions\nException.\n\n"
            "## Implications and next step\nTest it.\n\n"
            "## Sources\nS001 and S002.\n",
            encoding="utf-8",
        )

    def write_valid_v2(self) -> None:
        self.write_valid()
        skill_sha256 = MODULE.compute_skill_sha256()
        (self.root / "run.json").write_text(
            json.dumps(
                {
                    "schema": "scoville-research-run.v2",
                    "skill_sha256": skill_sha256,
                    "created": "2026-08-19T12:00:00Z",
                    "updated": "2026-08-19T12:30:00Z",
                    "phase": "complete",
                    "status": "complete",
                    "last_completed_query": "Q003",
                    "external_jobs": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.write_jsonl(
            "evidence.jsonl",
            [
                {
                    "id": "E001",
                    "source_id": "S001",
                    "locator": "Contract section paragraph 2",
                    "relation": "supports",
                    "inspection": "section",
                    "excerpt": "The feature is supported.",
                    "observation": None,
                    "content_sha256": "1" * 64,
                },
                {
                    "id": "E002",
                    "source_id": "S002",
                    "locator": "Failure report paragraph 4",
                    "relation": "contradicts",
                    "inspection": "full",
                    "excerpt": None,
                    "observation": "The reported exception reproduces under the stated version.",
                    "content_sha256": None,
                },
            ],
        )
        self.write_jsonl(
            "claims.jsonl",
            [
                {
                    "id": "C001",
                    "claim": "The feature exists with a known exception.",
                    "basis": "inferred",
                    "status": "mixed",
                    "support": ["E001"],
                    "contradict": ["E002"],
                }
            ],
        )

    def write_jsonl(self, name: str, rows: list[dict]) -> None:
        (self.root / name).write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    def codes(self) -> set[str]:
        return {item["code"] for item in MODULE.validate(self.root)["diagnostics"]}

    def test_valid_package(self) -> None:
        result = MODULE.validate(self.root)
        self.assertTrue(result["valid"])
        self.assertEqual(result["summary"]["errors"], 0)
        self.assertEqual(result["package_version"], 1)
        self.assertTrue(result["legacy"])

    def test_valid_v2_package(self) -> None:
        self.write_valid_v2()
        result = MODULE.validate(self.root)
        self.assertTrue(result["valid"])
        self.assertEqual(result["package_version"], 2)
        self.assertFalse(result["legacy"])
        self.assertEqual(result["summary"]["evidence"], 2)
        self.assertEqual(result["summary"]["external_jobs"], 0)

    def test_v2_requires_evidence_file(self) -> None:
        self.write_valid_v2()
        (self.root / "evidence.jsonl").unlink()
        self.assertIn("missing_file", self.codes())

    def test_evidence_without_run_is_rejected(self) -> None:
        self.write_jsonl("evidence.jsonl", [])
        self.assertIn("mixed_package_version", self.codes())

    def test_unknown_run_schema_is_rejected(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["schema"] = "scoville-research-run.v99"
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("unsupported_schema", self.codes())

    def test_complete_status_requires_complete_phase(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["phase"] = "gap"
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("run_state_mismatch", self.codes())

    def test_last_completed_query_must_exist(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["last_completed_query"] = "Q999"
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("unknown_query", self.codes())

    def test_skill_drift_is_rejected(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["skill_sha256"] = "0" * 64
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("skill_drift", self.codes())

    def test_run_timestamps_must_be_ordered(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["updated"] = "2026-08-19T11:59:59Z"
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("invalid_timestamp_order", self.codes())

    def test_blocked_status_requires_blocked_phase(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["status"] = "blocked"
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("run_state_mismatch", self.codes())

    def test_evidence_requires_known_source(self) -> None:
        self.write_valid_v2()
        rows = [
            {
                "id": "E001",
                "source_id": "S999",
                "locator": "Paragraph 2",
                "relation": "supports",
                "inspection": "section",
                "excerpt": "Claim text.",
                "observation": None,
                "content_sha256": None,
            }
        ]
        self.write_jsonl("evidence.jsonl", rows)
        self.assertIn("unknown_source", self.codes())

    def test_evidence_requires_excerpt_or_observation(self) -> None:
        self.write_valid_v2()
        rows = [
            {
                "id": "E001",
                "source_id": "S001",
                "locator": "Paragraph 2",
                "relation": "supports",
                "inspection": "section",
                "excerpt": None,
                "observation": None,
                "content_sha256": None,
            }
        ]
        self.write_jsonl("evidence.jsonl", rows)
        self.assertIn("missing_evidence_content", self.codes())

    def test_evidence_excerpt_is_bounded(self) -> None:
        self.write_valid_v2()
        rows = [
            {
                "id": "E001",
                "source_id": "S001",
                "locator": "Paragraph 2",
                "relation": "supports",
                "inspection": "section",
                "excerpt": "x" * 1001,
                "observation": None,
                "content_sha256": None,
            }
        ]
        self.write_jsonl("evidence.jsonl", rows)
        self.assertIn("excerpt_too_long", self.codes())

    def test_claim_references_evidence_not_source(self) -> None:
        self.write_valid_v2()
        rows = [
            {"id": "C001", "claim": "Claim.", "basis": "reported", "status": "supported", "support": ["S001"], "contradict": []}
        ]
        self.write_jsonl("claims.jsonl", rows)
        self.assertIn("unknown_evidence", self.codes())

    def test_claim_relation_must_match_evidence_relation(self) -> None:
        self.write_valid_v2()
        rows = [
            {"id": "C001", "claim": "Claim.", "basis": "reported", "status": "supported", "support": ["E002"], "contradict": []}
        ]
        self.write_jsonl("claims.jsonl", rows)
        self.assertIn("evidence_relation_mismatch", self.codes())

    def test_same_source_can_support_and_contradict_through_distinct_evidence(self) -> None:
        self.write_valid_v2()
        evidence = [
            {
                "id": "E001",
                "source_id": "S001",
                "locator": "Paragraph 2",
                "relation": "supports",
                "inspection": "section",
                "excerpt": "Supports one scope.",
                "observation": None,
                "content_sha256": None,
            },
            {
                "id": "E002",
                "source_id": "S001",
                "locator": "Paragraph 8",
                "relation": "contradicts",
                "inspection": "section",
                "excerpt": "Contradicts another scope.",
                "observation": None,
                "content_sha256": None,
            },
        ]
        self.write_jsonl("evidence.jsonl", evidence)
        rows = [
            {"id": "C001", "claim": "Claim.", "basis": "inferred", "status": "mixed", "support": ["E001"], "contradict": ["E002"]}
        ]
        self.write_jsonl("claims.jsonl", rows)
        result = MODULE.validate(self.root)
        self.assertTrue(result["valid"], result["diagnostics"])

    def test_v2_accepts_optional_accessibility_without_scoring_it(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["accessibility"] = "public"
        self.write_jsonl("sources.jsonl", rows)
        self.assertTrue(MODULE.validate(self.root)["valid"])

    def test_v2_accepts_redirect_target_and_link_status(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["final_url"] = "https://example.com/canonical-spec"
        rows[0]["link_status"] = "redirected"
        self.write_jsonl("sources.jsonl", rows)
        self.assertTrue(MODULE.validate(self.root)["valid"])

    def test_redirected_source_requires_final_url(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["link_status"] = "redirected"
        self.write_jsonl("sources.jsonl", rows)
        self.assertIn("missing_final_url", self.codes())

    def test_v2_accepts_descriptive_content_quality(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["content_quality"] = "usable"
        self.write_jsonl("sources.jsonl", rows)
        self.assertTrue(MODULE.validate(self.root)["valid"])

    def test_mismatched_content_cannot_support_a_claim(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["content_quality"] = "mismatched"
        self.write_jsonl("sources.jsonl", rows)
        self.assertIn("invalid_support", self.codes())

    def test_v2_accepts_claim_as_of_for_time_sensitive_claim(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "claims.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["as_of"] = "2026-08-19"
        self.write_jsonl("claims.jsonl", rows)
        self.assertTrue(MODULE.validate(self.root)["valid"])

    def test_v2_claim_as_of_must_be_an_iso_date_or_null(self) -> None:
        self.write_valid_v2()
        rows = [json.loads(line) for line in (self.root / "claims.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["as_of"] = "current"
        self.write_jsonl("claims.jsonl", rows)
        self.assertIn("invalid_date", self.codes())

    def test_legacy_v1_rejects_v2_optional_source_fields(self) -> None:
        rows = [json.loads(line) for line in (self.root / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
        rows[0]["link_status"] = "unchecked"
        self.write_jsonl("sources.jsonl", rows)
        self.assertIn("unknown_keys", self.codes())

    def test_private_external_upload_requires_authorization(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["external_jobs"] = [
            {
                "id": "J001",
                "backend": "Example Research API",
                "trust_boundary": "Third-party hosted service",
                "estimated_cost_usd": 1.5,
                "timeout_seconds": 1800,
                "job_id": "job-123",
                "status": "completed",
                "last_polled": "2026-08-19T12:20:00Z",
                "disclosed_data": "One private project brief",
                "upload_sha256": ["2" * 64],
                "contains_private_data": True,
                "private_upload_authorized": False,
                "cleanup_status": "complete",
            }
        ]
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("unauthorized_private_upload", self.codes())

    def test_running_external_job_requires_poll_timestamp(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["status"] = "in-progress"
        run["phase"] = "inspection"
        run["external_jobs"] = [
            {
                "id": "J001",
                "backend": "Example Research API",
                "trust_boundary": "Third-party hosted service",
                "estimated_cost_usd": 0,
                "timeout_seconds": 600,
                "job_id": "job-123",
                "status": "running",
                "last_polled": None,
                "disclosed_data": "Public query text only",
                "upload_sha256": [],
                "contains_private_data": False,
                "private_upload_authorized": False,
                "cleanup_status": "pending",
            }
        ]
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("missing_poll_state", self.codes())

    def test_complete_run_requires_terminal_jobs_and_cleanup(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["external_jobs"] = [
            {
                "id": "J001",
                "backend": "Example Research API",
                "trust_boundary": "Third-party hosted service",
                "estimated_cost_usd": None,
                "timeout_seconds": 600,
                "job_id": "job-123",
                "status": "completed",
                "last_polled": "2026-08-19T12:20:00Z",
                "disclosed_data": "Public query text only",
                "upload_sha256": [],
                "contains_private_data": False,
                "private_upload_authorized": False,
                "cleanup_status": "pending",
            }
        ]
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("incomplete_cleanup", self.codes())

    def test_external_job_requires_exact_disclosure_keys(self) -> None:
        self.write_valid_v2()
        path = self.root / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        run["external_jobs"] = [{"id": "J001", "backend": "Example"}]
        path.write_text(json.dumps(run) + "\n", encoding="utf-8")
        self.assertIn("missing_keys", self.codes())

    def test_missing_file(self) -> None:
        (self.root / "brief.md").unlink()
        self.assertIn("missing_file", self.codes())

    def test_invalid_json(self) -> None:
        (self.root / "queries.jsonl").write_text("{broken\n", encoding="utf-8")
        self.assertIn("invalid_json", self.codes())

    def test_unknown_source_reference(self) -> None:
        rows = [{"id": "C001", "claim": "Claim.", "basis": "reported", "status": "supported", "support": ["S999"], "contradict": []}]
        self.write_jsonl("claims.jsonl", rows)
        self.assertIn("unknown_source", self.codes())

    def test_mixed_status_requires_both_sides(self) -> None:
        rows = [{"id": "C001", "claim": "Claim.", "basis": "reported", "status": "mixed", "support": ["S001"], "contradict": []}]
        self.write_jsonl("claims.jsonl", rows)
        self.assertIn("status_mismatch", self.codes())

    def test_snippet_cannot_support_claim(self) -> None:
        rows = [
            {"id": "S001", "url": "https://example.com/spec", "title": "Specification", "kind": "spec", "publisher": "Example", "published": None, "accessed": "2026-08-19", "inspection": "snippet", "disposition": "used", "notes": "Snippet only."},
            {"id": "S002", "url": "https://example.com/failure", "title": "Failure report", "kind": "issue", "publisher": "Example", "published": None, "accessed": "2026-08-19", "inspection": "full", "disposition": "contradiction", "notes": "Conflict."},
        ]
        self.write_jsonl("sources.jsonl", rows)
        self.assertIn("snippet_support", self.codes())

    def test_report_rejects_unknown_citation(self) -> None:
        path = self.root / "REPORT.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nUnknown [S999].\n", encoding="utf-8")
        self.assertIn("unknown_citation", self.codes())

    def test_requires_contradiction_and_gap_queries(self) -> None:
        rows = [{"id": "Q001", "query": "topic", "lane": "general", "purpose": "discovery", "result": "new-source", "source_ids": ["S001"]}]
        self.write_jsonl("queries.jsonl", rows)
        self.assertIn("missing_query_purpose", self.codes())


if __name__ == "__main__":
    unittest.main()
