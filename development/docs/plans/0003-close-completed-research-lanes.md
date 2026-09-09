---
format_version: 1
id: PLAN-0003
status: completed
created: 2026-09-09
updated: 2026-09-09
---

# Close completed Research lane agents

## Goal

Bound optional and composed Research lane agents so evidence and continuation provenance survive verified closure while missing close capability and required-lane capacity remain explicit.

## Non-goals

- Do not change research routes, evidence standards, citations, durable Deep schemas, or composition ownership.
- Do not raise global agent limits or rewrite benchmarks, snapshots, evaluations, backups, vendor files, or outputs.
- Do not publish, release, or replace installed Skill bytes.

## Work items

### W-001 Add and validate Research lane closure
Status: done
Depends on: []
Blocked by: []
Decisions: []
Outcome: Optional evidence lanes and the required Research-owned landscape lane preserve evidence before cleanup and report honest capacity limits.
Acceptance: The Skill checks close capability before lane spawns; preserves targets, sources, gaps, limits, and explicit follow-up state before verified closure; protects active descendants; skips optional lanes or blocks required lanes when capacity is insufficient; status questions resume waiting; blockers surface immediately; the Skill validator and lifecycle scenarios pass without claiming a live close.
Steps:
1. Add one bounded subagent-lifecycle section without changing evidence routes.
2. Inspect the package-only diff and run existing tests and the Skill validator.
3. Exercise optional-lane, required-composed-lane, active-descendant, closed-continuation, status-question, and blocker scenarios without spawning an agent.
Evidence: [35 repository tests passed; Skill quick validation passed; lifecycle contract scenarios passed without live close_agent execution, Native profile validation passed with zero diagnostics]
