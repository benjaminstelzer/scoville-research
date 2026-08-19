from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scoville-research" / "scripts" / "validate_research_artifacts.py"
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

    def write_jsonl(self, name: str, rows: list[dict]) -> None:
        (self.root / name).write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    def codes(self) -> set[str]:
        return {item["code"] for item in MODULE.validate(self.root)["diagnostics"]}

    def test_valid_package(self) -> None:
        result = MODULE.validate(self.root)
        self.assertTrue(result["valid"])
        self.assertEqual(result["summary"]["errors"], 0)

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
