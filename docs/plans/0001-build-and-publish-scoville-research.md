---
format_version: 1
id: PLAN-0001
status: active
created: 2026-08-19
updated: 2026-08-19
current_item: W-003
---

# Build and publish Scoville Research

## Goal

Publish a provider-neutral Scoville Research Agent Skill that turns current web, GitHub, and scholarly research requests into decision-ready, claim-evidence-traceable results, with a complete source-provenance audit and SkillOpt evidence against a no-Skill baseline.

## Non-goals

- Do not bundle or require a paid or external research provider.
- Do not turn simple lookups, ordinary code work, brainstorming, planning, or single-paper explanation into deep-research runs.
- Do not claim exhaustive coverage or factual correctness from source volume, model agreement, valid URLs, or polished synthesis alone.
- Do not advertise the new Skill across the Scoville family or profile repository before its own validation and publication complete.
- Do not install the Skill into global Codex or Claude directories; the requested local deliverable is the repository under `Z:/Projekts/AI/scoville-research`.

## Work items

### W-001 Establish the agreed implementation contract

Status: done
Depends on: []
Blocked by: []
Decisions: []
Outcome: One repository-owned implementation plan defines the Skill boundary, research modes, evidence model, source routing, stopping rules, artifact set, and validation strategy accepted by Codex and Fable.
Acceptance: The plan contains the complete build and validation contract, and a persistent Fable 5 High review returns no unresolved blocking finding while Codex independently concurs.
Steps:
1. Inspect current Scoville repository conventions, SkillOpt requirements, and source provenance.
2. Draft the implementation and evaluation contract in this Work Item and any necessary Decision record.
3. Ask Fable 5 High for a read-only critique and revise until both reviewers agree.
Evidence: [Fable 5 High session 58bf3848-10bd-4e67-8415-0d95140a6ad2 returned VERDICT AGREE after correction; Codex concurred on 2026-08-19]

### W-002 Deliver and qualify the Skill

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001]
Outcome: The repository contains the complete portable Skill package, public documentation in Benjamin's voice, source-provenance audit, deterministic validation, and a SkillOpt-qualified final candidate.
Acceptance: Agent Skill validation passes; all referenced files and scripts pass focused checks; the source audit maps every material borrowed idea to an inspected source; a frozen evaluation contract defines every scoring dimension and hard gate before the first baseline run; the exact promoted candidate exceeds the no-Skill baseline under that contract, passes validation without a hard-gate regression, and passes one previously untouched test split on its sole authorized evaluation.
Steps:
1. Implement a compact provider-neutral Core plus Development, Academic, and Deep Research references.
2. Add a standard-library deep-artifact validator with tests that prove shape and reference integrity without claiming factual verification.
3. Write the source-provenance audit, README, metadata, license, changelog, repository description and topics, and public evaluation contract; apply `imitate-me` to every public GitHub text without changing facts, technical meaning, structure, or evidence.
4. Freeze the SkillOpt corpus, split membership, scoring dimensions, hard gates, and no-Skill control before the first baseline; keep all runs network-disabled, expose only frozen fixture sources to the target, and keep gold answers scorer-only.
5. Cover activation, general web research, Development, Academic, contradiction, misleading-source, prompt-injection, private-to-public data separation, revision preservation, stopping, and artifact boundaries across train, validation, and sealed test cases.
6. Run SkillOpt baseline, training, and candidate validation; evaluate one exact candidate lineage once on the untouched test split, and require a new sealed split before any later lineage can make another promotion attempt after a test failure.
7. Promote only the exact passing candidate hash and re-run final Skill, repository, link, paper-status, public-copy, and provenance checks on the promoted tree.
Evidence: [Agent Skill validation and Python compilation passed, artifact validator tests passed 8/8, all 47 publishable external links returned success and all relative Markdown links resolved, source audit contains 29 unique inspected-source IDs, candidate SHA-256 3394161B93AC8DC8AB7A732440A28A174D58DDCF0C7E6D59505D4C670B5D7E03, no-Skill Validation run scoville-research-v4-no-skill-val-full-r1 passed 5/6, candidate Validation run scoville-research-v4-initial-val-full-r1 passed 6/6, SkillOpt run scoville-research-v4-train-v1 rejected its 5/6 proposal and retained the initial Skill, sole authorized sealed Test run scoville-research-v4-promoted-test-r1 passed 3/3, repository description topics and public visibility verified 2026-08-19]

### W-003 Publish and integrate the Scoville family

Status: in_progress
Depends on: [W-002]
Blocked by: []
Decisions: []
Outcome: The validated Skill is published as an immutable GitHub release, every existing Scoville README presents Scoville Research consistently, and BenjaminStelzer.md separates general Codex Skills from the Scoville family.
Acceptance: The new repository's main branch, release tag, and GitHub Release resolve to the verified commit; release notes and every other public GitHub text use `imitate-me` without changing facts or evidence; all six existing Scoville repositories link Scoville Research in their Family section; BenjaminStelzer.md has a Codex Skills section containing Ask Claude for Codex and a separate Scoville family section containing all seven family Skills; each affected remote is updated from an intentionally scoped clean worktree; W-003 and PLAN-0001 close with the observed commit, tag, release, link, and remote-state evidence.
Steps:
1. Commit and push the verified Skill, set the public repository description and topics, create its initial SemVer tag and GitHub Release, and verify remote state.
2. Update the Family section in each existing Scoville README using the same `imitate-me` public wording.
3. Restructure BenjaminStelzer.md into separate Codex Skills and Scoville family sections after the Skill release exists, also using `imitate-me`.
4. Commit, push, and verify every affected repository.
5. Record exact publication and integration evidence, then complete W-003 and PLAN-0001.
Evidence: []
Next action: Commit and push the verified v1.0.0 tree, then create and verify its immutable GitHub release before editing sibling Family sections or the profile repository.
