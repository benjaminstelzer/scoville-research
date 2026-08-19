---
format_version: 1
id: PLAN-0002
status: active
created: 2026-08-19
updated: 2026-08-19
current_item: W-007
---

# Strengthen Research evidence and the Brainstorm boundary

## Goal

Qualify a next Scoville Research revision that traces Deep claims to exact evidence, resumes from versioned state, handles external backends and citation health explicitly, and composes with Scoville Brainstorm without collapsing evidence research and isolated divergence into one Skill.

## Non-goals

- Do not implement, publish, tag, release, or replace installed Skill bytes under this planning-only request.
- Do not merge Research and Brainstorm or make either sibling an automatic dependency.
- Do not add fixed source quotas, citation-density targets, confidence derived from source counts, or mandatory multi-agent execution.
- Do not add a database, provider SDK, paid research service, report renderer, full source archive, or project-management runtime to the portable Skill.
- Do not treat a structural validator, URL check, model agreement, or working citation as proof that evidence semantically supports a claim.
- PLAN-0002 never edits the Brainstorm repository. Any Brainstorm change must be performed and closed under a separate valid Brainstorm-native Plan after the relevant Decision is accepted.

## Work items

### W-001 Resolve the proposed update and family-boundary Decisions

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0002, ADR-0003]
Outcome: The evidence-layer architecture and Research-Brainstorm boundary are decision-ready, Fable-reviewed proposals with no unresolved factual or structural defect hidden as agreement.
Acceptance: The Deep research package validates with zero structural diagnostics; every recommendation maps to inspected evidence and a stated limit; Fable 5 High and Codex independently review the Plan, both Decisions, the Research report, and both Skill contracts; after the last correction one complete follow-up pass returns no blocking finding; the user receives the remaining proposed choices without either Decision being silently accepted.
Steps:
1. Validate the completed Research audit and its claim-source package.
2. Ask Fable 5 High to critique the Plan and both proposed Decisions against the two current Skill contracts.
3. Correct factual, ownership, sequencing, compatibility, and acceptance defects and run one full follow-up review after the last correction.
4. Complete only when a full review returns no blocking finding; after three review rounds with an unresolved finding, keep W-001 todo and present the disagreement to the user.
5. Present ADR-0002 and ADR-0003 for explicit accept, reject, or revise direction.
Evidence: [Research artifact validator passed 12 queries 27 sources and 32 claims with zero diagnostics, native Plan validator passed 2 Plans 10 Work Items and 3 Decisions with zero diagnostics, Fable 5 High session 3d874a61-517b-4285-9cbc-6508956bd55b returned AGREE after five blocking corrections, Codex concurs that the corrected proposals preserve evidence and divergence ownership, user explicitly accepted ADR-0002 and ADR-0003 and requested implementation on 2026-08-19]

### W-002 Implement the versioned Deep evidence and run foundation

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002]
Outcome: Scoville Research creates and validates a provider-neutral v2 Deep core with exact evidence records, durable run identity, legacy v1 inspection, and bounded external-job state.
Acceptance: ADR-0002 is accepted before work starts; the package and validator implement only the accepted core schema; v1 fixtures remain read-only-valid with `package_version: 1` and `legacy: true`; v2 fixtures cover evidence IDs, locators, relations, same-source opposing evidence, claim links, drift, phases, terminal states, external job disclosure, upload authorization, polling, and cleanup; no validator result claims semantic proof; focused tests, Agent Skill validation, and scoped diffs pass.
Steps:
1. Freeze v2 and legacy-v1 schemas plus deterministic validator cases before changing the Skill.
2. Add `run.json` and `evidence.jsonl` to the Deep contract and route claims through evidence IDs.
3. Extend the standard-library validator and fixtures without automatic migration or network dependence.
4. Add the external-backend record without provider code.
5. Recompute package cost and verify progressive disclosure.
Evidence: [ADR-0002 accepted in transition batch 9b21ae7b33fae66f253105632f1eb503f33448957715e77df0bc14b2e1b2e7f5 before implementation, frozen red run failed 12 tests and raised 1 error before production changes, 27 deterministic v1 and v2 validator tests pass, v2 fixtures cover evidence relations same-source opposition exact Skill drift phases terminal state query resume polling private-upload authorization and cleanup, legacy v1 returns package_version 1 and legacy true without migration, Python compilation passes, Agent Skill quick validation passes, git diff check passes, portable package SHA-256 is 9f3ee47bccc5e17522eab5f1c9bed15c66c0b494ad65105264a25024204d775b, Core SKILL.md remains 7528 bytes while the Deep-only reference grows from 5045 to 9554 bytes and the portable package is 53795 bytes]

### W-003 Strengthen Research Development routing and source finalization

Status: done
Depends on: [W-002]
Blocked by: []
Decisions: [ADR-0001, ADR-0002]
Outcome: Separately promotable Research refinements handle authorized internal implementation evidence, source accessibility, citation health, claim freshness, and content quality without turning those fields into one bundled quality score.
Acceptance: ADR-0002 is accepted before v2 fields change; authorized internal-first routing remains owned by accepted ADR-0001 and does not depend on ADR-0003; accessibility, final URL and link status, claim freshness, and content quality remain optional v2 fields with separate frozen cases, control results, and promotion decisions; a passing released control produces no instruction change for that mechanism; private-query, dead-link, redirect, paywall, abstract-only, mismatched-content, and no-network validator cases pass for each promoted refinement.
Steps:
1. Freeze separate cases and released controls for each optional refinement before changing instructions or schemas.
2. Sharpen the existing Development funnel with authorized internal-first inspection and sanitized public gap queries.
3. Add only the accessibility, citation-health, freshness, and content-quality fields whose own cases show a decision-relevant improvement.
4. Keep every field descriptive and prevent counts or labels from becoming automatic credibility scores.
5. Validate each promoted refinement independently against private-query and near-miss controls.
Evidence: [Separate frozen controls covered authorized internal-first routing accessibility redirect and dead-link state claim freshness and content quality, released v1.0.0 passed the internal-first behavior with no private disclosure so Development instructions remained unchanged, unhinted controls exposed missing durable field ownership and incorrect freshness scope, v2 now accepts accessibility final_url link_status content_quality and claim as_of independently without an aggregate score, mismatched paywall-stub and unreadable content cannot silently support a claim, legacy v1 still rejects v2-only fields, 35 deterministic validator tests pass]

### W-004 Strengthen Research first-wave lane integrity and mechanism convergence

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0003]
Outcome: Research first-wave lanes are genuinely isolated when claimed and Development shortlists distinct mechanisms rather than several wrappers around one approach while later contradiction and gap work stays adaptive.
Acceptance: ADR-0003 is accepted before work starts; first-wave prompts freeze before dispatch; independence language requires observed isolated calls; the existing Development funnel gains mechanism clustering, one strongest practical comparator, and one load-bearing-assumption challenge only where they can change the decision; later gap queries remain adaptive; standalone activation, near-miss, topology, source-independence, and decision-stop cases pass without Brainstorm becoming a dependency.
Steps:
1. Freeze standalone and lane-topology cases before changing Core or Development instructions.
2. Add first-wave prompt freezing and trace-owned independence reporting to the optional-lane contract.
3. Sharpen the existing Development funnel instead of adding a second comparison workflow.
4. Keep contradiction and gap work adaptive after initial collection.
5. Validate that no Brainstorm dependency or originality language entered Research.
Evidence: [released controls preserved standalone activation and private-query and source-independence behavior, candidate Validation passed first-wave isolation and mechanism convergence and decision-stop and near-miss gates, explicit combined mode loads brainstorm-composition.md exactly once, no Brainstorm dependency entered standalone routes, canonical explicit_combined topology passed open Validation and untouched Test]

### W-005 Coordinate and verify the Brainstorm landscape update

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0003]
Outcome: The Brainstorm repository independently owns any landscape change while this Plan verifies the resulting candidate or release hash against the accepted family boundary and combined protocol.
Acceptance: ADR-0003 is accepted before coordination starts; a separate valid Brainstorm-native Plan owns all Brainstorm case freezing, edits, qualification artifacts, tags, releases, installation changes, and closure; PLAN-0002 performs no Brainstorm repository mutation; Brainstorm's observed candidate or release treats retrieved content as untrusted, sanitizes private queries, inspects actual sources, collapses shared origins, preserves exact URLs and inspection limits, substitutes the Research-owned lane for its native landscape agent only in explicit combined mode, and retains standalone operation without Research ledgers or dependencies.
Steps:
1. Wait for an independently created and activated Brainstorm-native Plan after Decision acceptance.
2. Read its frozen boundary, candidate hash, qualification evidence, and release state without editing that repository.
3. Verify the combined protocol uses the Research-owned lane as the sole landscape input and preserves generator isolation.
4. Record only observed Brainstorm hashes and results as coordination evidence.
Evidence: [Brainstorm PLAN-0002 independently accepted ADR-0003 through transition batch b130fa9bd375c28ee18755ad3a38d9db9592f1d7fc9d5e5e5fa0be2456cb147e, observed Brainstorm package SHA256 fc204947ed837424b24eb2067491d2ded3126381d952ebdeaed55d3765b06d2a, Brainstorm open Validation passed 6/6 including five standalone retention gates, fresh Brainstorm Test ran once with 1/3 raw and 3/3 adjudicated Skill score and zero candidate changes, Brainstorm native evidence is recorded in docs/evidence/w003-research-composition-qualification.json]

### W-006 Qualify the exact Research candidate and combined protocol

Status: done
Depends on: [W-002, W-003, W-004, W-005]
Blocked by: []
Decisions: [ADR-0002, ADR-0003]
Outcome: The exact Research candidate passes its frozen standalone contract and the composition harness verifies it against an independently qualified Brainstorm hash without changing the sibling repository.
Acceptance: Research Train, Validation, scoring dimensions, hard gates, released-version controls, per-mechanism ablations, prompt-injection cases, private-data cases, topology evidence, and sealed Test membership freeze before candidate generation; if a released control passes every new case for one mechanism, that mechanism receives no instruction change; SkillOpt runs against the exact Research package; promotion requires strict decision-relevant improvement without losing any released hard pass; the promoted lineage receives one untouched Test evaluation; the combined harness binds the independently supplied Brainstorm hash and proves one Research-owned landscape lane, no second Brainstorm landscape agent, no pre-convergence cross-visibility, and no standalone dependency; package validators, deterministic tests, cost measurements, and retained raw evidence pass.
Steps:
1. Freeze Research standalone and composition evaluation revisions against exact released controls.
2. Run controls and preserve mechanisms that show no observable gap.
3. Use SkillOpt conservatively and reject changes that trade reliability for shorter or more elaborate instructions.
4. Evaluate the exact promoted Research hash once on its untouched Test split.
5. Verify composition against the Brainstorm hash supplied by its native Plan and reconcile public claims to observed evidence.
Evidence: [exact Research package SHA256 2078a61307a7055ce924e5e6db0d2ae9e959b37d769ea49f4fc1f4aff9e8c262, 35 deterministic validator tests and Agent Skill validation pass, final open SkillOpt Validation passed 13/13 with every behavior and efficiency invariant, SkillOpt run research-v10-skillopt-train-r1 used 49 calls and 2939506 tokens and proposed SHA256 981d3a920e99db8e2921595a3f09c584fa4456bf7e79ff8c4ea7b1631725367b, the SkillOpt proposal was rejected at 12/13 because it lost mechanism convergence, the exact source candidate passed its fresh Test once at 4/4 with zero retries, Fable 5 High returned READY with zero blockers, docs/evidence/w006-research-brainstorm-qualification.json binds both packages and the one-landscape protocol]

### W-007 Publish Research and verify the independently released sibling

Status: in_progress
Depends on: [W-006]
Blocked by: []
Decisions: [ADR-0002, ADR-0003]
Outcome: After explicit publication authorization, one immutable Research release exposes the qualified contract and this Plan verifies - but does not perform - the independently owned Brainstorm release and synchronization.
Acceptance: The user explicitly authorizes Research publication after reviewing W-006 evidence; the Research repository uses an intentionally scoped clean worktree, factual imitate-me public text, an immutable compatible SemVer tag, and a normal GitHub Release; remote main, tag, release, package path, source audit, benchmark evidence, and installed Codex and Claude Research package hashes are verified; any Brainstorm tag, release, public text, installed bytes, and Plan closure were produced by the Brainstorm-native Plan and are only observed here; Research Plan closure advances only Research main and never moves either release tag.
Steps:
1. Present the exact Research candidate hash, version recommendation, public claims, and installation scope for authorization.
2. Publish and verify Research without changing Brainstorm.
3. Read the independently published Brainstorm release and installation evidence when available.
4. Synchronize only Research installations under this Plan.
5. Record exact remote and installed hashes before completing PLAN-0002.
Evidence: [User explicitly authorized publication and local Codex and Claude installation on 2026-08-19, v1.1.0 README and changelog and benchmark evidence and source audit are prepared]
Next action: Run final release validation and inspect the complete v1.1.0 release diff before committing.
