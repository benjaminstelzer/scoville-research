---
format_version: 1
id: ADR-0002
status: accepted
created: 2026-08-19
accepted: 2026-08-19
scope: skill/deep-evidence
transition_batch: 9b21ae7b33fae66f253105632f1eb503f33448957715e77df0bc14b2e1b2e7f5
transition_batch_members: [ADR-0002, ADR-0003]
---

# Add a versioned evidence layer to Deep Research

## Decision

Recommend a versioned Deep artifact contract that adds `run.json` and `evidence.jsonl`, makes exact evidence records the internal support owner for claims, and retains read-only validation for legacy v1 packages. Provider-specific execution remains outside the portable Skill.

## Problem

Scoville Research v1.0.0 records a brief, queries, whole sources, claims, and the final report. That is enough to prove that identifiers and citation relations are structurally coherent, but not enough to show which passage, code line, table, test result, or observation supports a claim. A resumed run also cannot tell which Skill bytes created its artifacts, which phase completed last, or whether an external asynchronous job remains active.

The gap matters because a valid URL and a topically relevant page do not establish factual support. The current validator states that limit correctly. It simply has no narrower evidence object to inspect.

## Drivers

- Every decision-relevant claim should trace to the smallest practical inspected evidence unit, not only to a whole source.
- A long run should detect schema or Skill drift before resuming under a changed contract.
- External backends may introduce cost, uploads, polling, job identity, and cleanup state without becoming mandatory Skill dependencies.
- Existing v1 research packages are retained evidence and must remain readable without a silent rewrite.
- The package must stay provider-neutral, standard-library-validatable, and smaller than the research platforms used as comparators.
- Structural validation must not be renamed semantic verification merely because the structure becomes more precise.

## Considered alternatives

- Keep claims linked directly to source IDs. This preserves the smallest package, but leaves the most expensive audit question - which exact evidence supports this claim - unresolved.
- Add optional locator fields directly to claims. This is compatible and compact, but mixes claim identity with evidence extracted from several sources and makes contradiction relations harder to address independently.
- Adopt a database-backed evidence graph and provider framework. This improves querying and orchestration, but would replace a portable Skill with a research application and its operational dependencies.
- Archive complete source pages and PDFs. That can improve reproducibility, but introduces storage, copyright, access-control, and private-data problems that a general Skill cannot settle automatically.

## Consequences

- New Deep runs use a v2 package containing `brief.md`, `run.json`, `queries.jsonl`, `sources.jsonl`, `evidence.jsonl`, `claims.jsonl`, and `REPORT.md`.
- `run.json` records schema, Skill version or SHA-256, timestamps, current phase, status, last completed query, and optional external job records.
- Each evidence record has a stable ID, source ID, locator, relation, inspection description, and the shortest sufficient excerpt or observation. An excerpt is capped at 1,000 Unicode scalar values and is omitted when retention would expose private material or exceed the permitted source boundary; a locator and scoped observation remain. A content hash is optional when the inspected bytes are available.
- Claims link support and contradiction through evidence IDs. Reader-facing reports may continue citing stable source IDs.
- In v2 the overlap constraint applies to evidence IDs. One source may legitimately produce separate supporting and contradicting evidence records for the same claim.
- Source records may gain optional accessibility, final URL, link status, and content-quality fields through separately promoted refinements. Claim-level freshness remains optional and is recorded only when time changes the claim.
- External job records disclose backend, trust boundary, estimated cost, timeout, job ID, poll state, uploaded-data summary, hashes where available, and cleanup state. Private uploads still require explicit user direction.
- The validator selects v2 only when `run.json` declares the accepted v2 schema. A package without `run.json` follows the legacy v1 path and returns a successful result with `package_version: 1` and `legacy: true` when structurally valid. It performs no automatic migration and never creates new v1 packages.
- Tests and public claims retain the distinction between structural integrity, link health, and semantic support.

## Confirmation

Freeze the v2 schema, migration boundary, benchmark cases, hard gates, and sealed Test before candidate work. Confirmation requires deterministic validator fixtures for v1 and v2, evidence-locator and drift failures, and external-backend disclosure and cleanup cases. Accessibility, citation health, content quality, and claim freshness receive separate frozen cases and promotion decisions. The exact candidate must also pass Agent Skill validation, a no-Skill or v1 control, SkillOpt qualification, and one untouched Test evaluation.

## Revisit when

Revisit if Agent Skills standardize claim-evidence artifacts, if content retention creates an unacceptable privacy or copyright boundary, if v1 compatibility materially complicates the Core, or if frozen evaluation shows that the additional evidence layer increases ceremony without improving auditability or decisions.
