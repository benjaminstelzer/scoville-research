# Research brief

## Research question

Which publicly inspectable Agent Skills and executable research workflows add mechanisms that Scoville Research v1.0.0 lacks or handles less effectively, and which gaps are material enough to justify a later change?

## Decision or reader

Benjamin needs a decision-ready gap analysis for the next Scoville Research revision. The result should distinguish changes worth implementing from attractive complexity that should remain outside the Skill.

## Scope

- Date: 2026-08-19.
- Inspect current public GitHub repositories, exact Skill or workflow files, official documentation, tests, releases, issues, and linked research where those sources own a material claim.
- Start with implementations not already carrying the current design, then use already-audited sources only where they provide a necessary comparator.
- Compare mechanisms rather than README claims, popularity, or fixed source counts.
- Exclude closed SaaS products whose underlying workflow cannot be inspected, generic web-search tools without a research contract, and implementation work on Scoville Research itself.
- Treat the published Scoville Research v1.0.0 package as the fixed comparison baseline.

Freshness boundary: public state inspected on 2026-08-19. Repository behavior can change after that date.

## Evidence lanes

1. Agent Skill contracts and activation boundaries.
2. Executable orchestration, retrieval, citation, and persistence mechanisms.
3. Tests, evaluation contracts, releases, issues, and failure handling.
4. Security, private-data, provenance, and prompt-injection boundaries.
5. Academic or institutional evidence for mechanisms that would materially change the recommendation.

## Deliverable

A source-backed report with a per-implementation comparison, confirmed gaps, rejected additions, unresolved questions, and the cheapest tests that would decide whether each recommended change earns inclusion.

## Data boundary

Only public repository and publication information may enter external searches. Local Scoville files are used solely as the private comparison baseline and are not copied into queries or remote requests.

Decision sufficiency is reached when each material Scoville contract area has at least one strong comparator or an explicit no-evidence result, every proposed gap maps to inspected implementation evidence, contradiction and gap queries no longer change the shortlist, and remaining uncertainties have bounded tests.
