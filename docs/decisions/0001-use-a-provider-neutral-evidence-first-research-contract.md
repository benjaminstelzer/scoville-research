---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-08-19
accepted: 2026-08-19
scope: skill/research-contract
---

# Use a provider-neutral evidence-first research contract

## Decision

Build Scoville Research as a provider-neutral orchestration and integrity Skill with a compact shared Core, separate Development, Academic, and Deep Research references, optional independent evidence lanes, one coordinating synthesis owner, and deterministic validation that checks artifact integrity without pretending to verify truth.

## Problem

Codex can already search, browse, inspect repositories, call structured APIs, and synthesize sources. What it does not receive from a generic research request is one stable contract for deciding when research is warranted, routing different evidence types, preserving claim-to-source provenance, searching for contradictions, stopping at decision sufficiency, and reporting the difference between observed evidence, inference, and unresolved gaps. A useful Skill must add that discipline without replacing native tools, requiring a paid provider, or turning every current-information lookup into a research project.

## Drivers

- Development research should prefer official documentation, specifications, source code, releases, issues, pull requests, tests, and reproducible benchmarks, with GitHub and structured APIs treated as evidence interfaces rather than mere link catalogs.
- Academic research must distinguish preprints, peer-reviewed versions, metadata records, full text, citation relationships, associated code, and associated data.
- Source quantity is not a correctness measure; claim support, contradiction handling, source independence, and evidence-chain completion matter more.
- Long research runs need durable, resumable state, while ordinary bounded research should not create a filesystem ceremony by default.
- Web content is untrusted input. No retrieved page may alter scope, authority, permissions, or tool policy.
- Private or local material must not be placed in external search queries, URLs, browsing requests, or remote API calls unless the user explicitly directs that disclosure for the current task.
- The Skill must remain portable across Agent Skills-compatible hosts and useful with whichever read-only search, browser, API, connector, or local inspection tools the host actually provides.

## Considered alternatives

- A monolithic research prompt would keep everything in one file, but it would load irrelevant Development, Academic, and deep-artifact detail on every activation and make routing harder to test.
- A wrapper around one external deep-research service would simplify execution, but it would add provider, account, cost, availability, and data-boundary dependencies while hiding much of the evidence process behind one response.
- Mandatory multi-agent or multi-vendor voting would create visible breadth, but agreement between models does not prove that a cited passage supports a claim. It would also make the Skill unusable on hosts without delegation.
- Fixed source quotas would make runs easy to count, but they would reward redundant retrieval and could turn one canonical specification into an excuse to collect nine weaker summaries.

## Consequences

- `SKILL.md` will own activation, scope, the general-web route, research contract, shared evidence rules, route selection, the gap loop, stopping logic, and the final answer boundary.
- `references/development-research.md` will own GitHub-first implementation and technology research.
- `references/academic-research.md` will own scholarly discovery, version status, citation chasing, and paper-code-data relationships.
- `references/deep-research.md` will overlay general, Development, or Academic research when depth, interruption risk, or an explicit durable report requires persistent briefs, query logs, source and claim ledgers, resumability, saturation checks, and a report package.
- A standard-library validator will verify deep-research artifact shape, identifiers, references, and internal consistency. It will state explicitly that it cannot verify whether a source is true or whether a passage semantically proves a claim.
- Subagents may gather independent evidence lanes when the host supports them and the task benefits. The coordinating agent retains scope, conflict resolution, and final synthesis; a single-agent run remains valid and must not claim independent verification.
- Bounded research may remain in conversation. Deep or interruption-prone research uses a dedicated workspace and durable artifacts.
- The Skill will cost additional context and time only when the request crosses its activation and route boundaries.

## Confirmation

Confirm the choice through Agent Skill structural validation, deterministic script tests, realistic general-web, Development, and Academic research cases, activation near-misses, misleading-source, contradiction, prompt-injection, private-to-public disclosure, revision-preservation, stopping, and artifact cases. Freeze a network-disabled fixture corpus, scorer-only gold, metrics, and hard gates before the no-Skill baseline. Publication requires the exact final candidate hash to pass validation and its sole authorized evaluation on one previously untouched held-out split; a failed held-out attempt requires a new sealed split before a later candidate lineage can seek promotion.

## Revisit when

Revisit the contract if Agent Skills standardize research artifacts or citation semantics, if a host provides a verifiable native claim-evidence store, if SkillOpt evidence shows the routed structure harms task quality or activation precision, or if a required research domain cannot fit Development, Academic, or shared Deep routing without a distinct evidence contract.
