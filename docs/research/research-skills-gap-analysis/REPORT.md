# Research report

## Answer

Scoville Research does not need a larger search ritual. Its routing, source-independence rule, private/public boundary, contradiction pass, decision stop, and provider neutrality are already stronger than most of the inspected prompt-only Skills. The real gap is narrower: Deep runs jump directly from a whole source to a claim. They do not retain the exact evidence span or observation that made the source relevant.

The next revision should therefore concentrate on four changes, in this order:

1. Add a Deep-only `evidence.jsonl` ledger with stable evidence IDs, source ID, locator, relation, bounded inspected excerpt or observation, and optional content fingerprint.
2. Add a small versioned `run.json` manifest with Skill version or hash, phase, status, timestamps, last completed operation, and optional external job identity.
3. Define an external-backend boundary for cost, timeout, uploads, polling, cleanup, and trust disclosure.
4. Evaluate source accessibility, final link status, claim freshness, and content quality as separate optional refinements rather than one bundled schema claim.

An explicit internal-repository lane for organization-specific Development research and an optional source-content quality field are useful second-tier improvements. Fixed source quotas, confidence scores derived from agreement counts, mandatory subagents, and a provider-specific research platform should not enter the portable Core.

Brainstorm and Research should remain separate Skills. Brainstorm should import Research's evidence and data-safety floor for prior-art work; Research should import Brainstorm's first-wave prompt isolation and trace-owned independence claims for optional parallel lanes. Their combined workflow should be explicit and bounded rather than automatic.

## Method and coverage

The comparison used Scoville Research v1.0.0 as the fixed baseline and inspected eight public implementation families at pinned commits: Firecrawl Web Agent, daymade Deep Research, dimayip research-agent, TheRealRay0x research Skill, 24601 agent-deep-research, foundry-research, Research Units, and Defiect Deep Research. GitHub Copilot CLI `/research` supplied one official hosted-product comparator for repository routing. Repository descriptions and READMEs were discovery aids only; findings below rely on exact Skill files, scripts, tests, architecture documents, or official product behavior.

The academic gap pass inspected abstracts for citation factuality, claim-level auditability, URL health, and native chain-of-evidence research. Abstract inspection supports only the reported high-level result, not uninspected methods or tables. [S019] [S020] [S021] [S022]

The search stopped after the contradiction and gap passes produced no new mechanism that changed the shortlist. Several additional Skills repeated fixed source counts, mandatory agents, or report templates without an implementation owner or evaluation evidence.

## Findings

### 1. Evidence records are the main missing layer

Scoville currently stores `sources.jsonl` and `claims.jsonl`; each claim points directly to supporting or contradicting source IDs. The validator can prove that those IDs exist, that a snippet is not promoted to support, and that contradictory and supporting lists do not overlap. It cannot show which passage, table, code line, test result, or observed behavior supports the claim. That limitation is stated honestly, but it also leaves the most expensive audit step to the next reader. [S001] [S002]

Three independent implementation families preserve a narrower evidence object. Defiect stores atomic claims with precise locators and quotes, then connects claims and sources through `supports`, `contradicts`, or `mentions` edges. [S013] Foundry stores evidence units separately, links findings to evidence IDs, exports only finding-linked evidence to synthesis, and tests counts for spans, claim types, question mappings, and unsupported findings. [S010] [S011] Research Units requires stable claim IDs and source pointers back to the exact manuscript location. [S017]

This mechanism also matches the research evidence. `Cited but Not Verified` separates link availability, topical relevance, and factual support; a working relevant link is not enough. [S019] The AAR perspective and ScientistOne both place claim-to-evidence relations at the center of auditability rather than treating a bibliography as provenance. [S020] [S022]

**Recommendation: high priority.** Add `evidence.jsonl` only to Deep mode. A compact record should contain `id`, `source_id`, `locator`, `relation`, `inspection`, a bounded shortest-sufficient `excerpt_or_observation`, and optionally `content_sha256`. Claims should refer to evidence IDs. Separate evidence records from one source may support and contradict the same claim; the no-overlap rule applies to evidence IDs, not source IDs. Keep the existing validator boundary: structure and references can be validated mechanically; semantic support still requires human or model inspection.

### 2. Deep runs are resumable by convention but not self-identifying

The current package tells a resumed agent to read the brief and four ledgers and continue at the first unfinished lane. It does not record a schema version, Skill version, current phase, terminal status, or the last completed query. A long run resumed after a Skill update therefore cannot detect whether the artifact contract changed underneath it. [S001]

Defiect creates `run.json`, exposes a status Skill, records phases, and runs snapshot or full audits. [S012] [S014] Foundry uses a state store for search history, evidence units, findings, gaps, and a bounded synthesis handoff. [S010] Research Units goes much further with schema-bound run identity and artifact fingerprints. That full lifecycle system is excessive here, but it demonstrates the drift problem rather than solving it with another reminder. [S017]

**Recommendation: high priority and small.** Add `run.json` with `schema`, `skill_version` or `skill_sha256`, `created`, `updated`, `phase`, `status`, `last_completed_query`, and optional `external_jobs`. The validator should reject unknown schema versions and impossible terminal states. Do not add a database, lock manager, or project-planning lifecycle.

### 3. External backends need a durable trust and cost record

Scoville is correctly provider-neutral, but the current Deep contract has no durable place for an external asynchronous job. If a host invokes a paid research API, uploads local context, or begins a job that outlives the current session, the query ledger cannot record estimated cost, uploaded file manifest, job ID, polling state, or cleanup result. [S001]

The 24601 adapter is provider-specific, but its operational boundaries transfer: dry-run cost estimation, maximum cost, interaction IDs, bounded timeout, adaptive polling, uploaded-file hashes, sensitive-file exclusion, and cleanup of ephemeral stores. Its tests cover cost-estimation edge cases; they do not prove research quality. [S015] [S016]

**Recommendation: high priority when an external backend is used.** Extend `run.json.external_jobs[]` with backend, trust statement, estimated cost, timeout, job ID, status, last poll, disclosed data summary, upload hashes, and cleanup status. Require explicit user direction before private material is uploaded. Keep all provider commands and SDK behavior outside Scoville Research.

### 4. Accessibility, freshness, and link health need sharper records

Scoville already records publication and access dates and asks for a freshness boundary. It does not distinguish a public source from an authenticated or user-provided source, and it does not record whether a cited URL still resolves at finalization. [S001] [S002]

Daymade distinguishes public, semi-public, exclusive user-provided, and private user-owned sources and binds time-sensitive material to an `AS_OF` policy. [S003] [S005] Its fixed source totals, official-source shares, and citation-density thresholds should not transfer: they make the audit countable without making the claim true. [S004] Firecrawl goes further in the wrong direction by assigning confidence from agreement counts. [S006]

URL health is a separate, testable concern. A 2026 preprint reports non-resolving and hallucinated citation URLs across large deep-research corpora and shows that an explicit URL-health correction tool can reduce non-resolving links in the tested agents. [S021]

**Recommendation: medium priority.** Add `accessibility`, `final_url`, and `link_status` to source records. Add claim-level `as_of` only for time-sensitive claims. During finalization, re-open every cited URL or mark it unreachable; never replace a dead source silently.

### 5. Development research needs an authorized internal lane

GitHub's official `/research` documentation says organization-specific research searches accessible private organization repositories first and public alternatives afterward. It also distinguishes research reports from code changes. [S018] Scoville already preserves the read-only boundary and prevents private details from entering external queries, but the Development route does not explicitly state when local or authorized private implementations should precede the public landscape.

**Recommendation: medium priority.** When the question is about an existing organization or project and access is already authorized, inspect local and private implementation owners first. Use sanitized public searches only to fill gaps or compare alternatives. Do not generalize this into automatic private-repository scanning for unrelated public research.

### 6. Source-content quality deserves one optional field

Foundry distinguishes mismatched content, abstract-only pages, degraded downloads, and reader-validated sources before synthesis. [S009] Scoville can represent blocked or rejected sources and inspection depth, but it cannot state that a downloaded file was the wrong paper, a paywall stub, or a valid full-text extraction without burying that fact in notes.

**Recommendation: medium priority.** Add an optional `content_quality` enum such as `usable`, `abstract-only`, `paywall-stub`, `mismatched`, `degraded`, or `unreadable`. Keep it descriptive. Do not turn it into an automatic credibility score.

### 7. Brainstorm and Research should exchange guardrails, not ownership

Brainstorm owns divergence before selection. It freezes generator and landscape prompts before ideation, prevents generators from seeing sibling or landscape output, clusters candidates by causal mechanism, and refuses to claim isolation unless tool traces establish it. [S024] Its qualification includes activation and orchestration evidence, while its source map preserves the limits of multi-agent and creativity findings. [S025] [S027]

Research owns evidence acquisition, source routing, contradiction handling, claim traceability, and decision sufficiency. It already treats retrieved content as untrusted, sanitizes private-to-public queries, records inspection depth, rejects source-count confidence, and keeps delegation optional. [S026]

**What Brainstorm should take from Research:**

- Apply the untrusted-content rule to every prior-art page, repository, paper, issue, and tool result.
- Sanitize external landscape queries so private project terms or identifiers do not leave the workspace without explicit direction.
- Treat snippets as discovery only and inspect the actual source before assigning an `Established`, `Adaptation`, or `Recombination` relationship.
- Collapse several retellings or forks of one origin before treating prior art as independent coverage.
- Preserve exact retrieved URLs and the real inspection boundary in the Landscape section when external search occurred.

These rules belong only to Brainstorm's landscape evidence. Ordinary divergence should not create Research ledgers, a literature review, or a durable report.

**What Research should take from Brainstorm:**

- Freeze all first-wave parallel evidence-lane prompts before the first lane starts. This prevents a fast lane from anchoring or redefining its siblings.
- Call evidence lanes independent only when the host trace shows separate calls with isolated prompts. Named roles or sequential self-critique do not count.
- In Development landscapes, normalize candidates by mechanism before shortlisting so five wrappers around one architecture do not occupy five positions.
- Include one load-bearing-assumption challenge and one strongest practical comparator when they can change the decision.

The later Research loop must remain adaptive. Contradiction and gap queries are supposed to react to collected evidence, so Brainstorm's full no-cross-wave-visibility rule would be wrong after the initial independent pass.

**Combined workflow when the user explicitly requests both:**

1. Freeze one factual frame containing the question, supplied facts, authority, hard constraints, private-data boundary, and permitted source scope.
2. Freeze Brainstorm generator prompts and the Research landscape question before either branch starts.
3. Run isolated Brainstorm generators and the Research-owned prior-art lane in parallel. In this explicit combined mode the Research lane replaces Brainstorm's native landscape agent and is the sole landscape input to convergence. Generators see no landscape output; Research receives no candidate ideas.
4. After all branches finish, Brainstorm converges candidates by mechanism and reconciles them with the Research evidence.
5. Brainstorm returns the shortlist and decision point. If the user wants deeper evidence on one or more candidates, Research receives stable candidate IDs, assumptions, and falsifiers in a separate follow-up.
6. Human selection remains outside both Skills. Neither sibling activates the other automatically.

This boundary preserves the reason both Skills exist: Research prevents an attractive mechanism from borrowing evidence it does not have; Brainstorm prevents the existing evidence landscape from shrinking the option space before divergence begins. [S024] [S026]

### Comparator matrix

| Comparator | Mechanism worth retaining | Important limit |
| --- | --- | --- |
| Scoville v1.0.0 | Strong routing, privacy, contradiction, source independence, and stop boundary | No evidence-span or run-identity layer [S001] |
| Foundry | Tested evidence units, quality states, bounded synthesis handoff | Large provider and state platform; not portable as Core [S009] [S010] [S011] |
| Defiect | Atomic claims, locators, evidence edges, run status, audits | Mandatory orchestration and fixed plugin runtime [S012] [S013] [S014] |
| Research Units | Stable source pointers and schema-bound run evidence | Much broader workflow and checkpoint system [S017] |
| 24601 | Cost, upload, polling, cleanup, and job-state boundary | Gemini dependency; tests cover operations rather than report quality [S015] [S016] |
| daymade | Accessibility and AS_OF fields; explicit counter-review | Fixed quotas and density rules create false rigor [S003] [S004] [S005] |
| dimayip | Exact-text citation pass and clear role separation | Citations are added after synthesis; no tests or evidence store inspected [S007] [S008] |
| Firecrawl | Small targeted extraction contract | Confidence and activation depend on source counts [S006] |
| TheRealRay0x | Source-origin tracing and broad adversarial framing | Mandatory agents and no executable validation layer [S023] |
| GitHub Copilot `/research` | Authorized internal-repository routing and read-only report boundary | Hosted prompt and model are not inspectable or configurable [S018] |
| Scoville Brainstorm | Prompt-frozen isolated divergence and mechanism convergence | Its prior-art lane lacks Research's explicit evidence and private-query floor [S024] [S025] |

## Contradictions and open questions

**More sources versus better support.** Several Skills impose source minimums or infer confidence from agreement. [S004] [S006] Scoville rejects that model, and the citation-factuality evidence supports the rejection: deeper retrieval can produce more citations without improving factual support. [S019]

**Mandatory agents versus optional lanes.** Dimayip and TheRealRay0x make subagents central. [S007] [S023] The inspected repositories do not provide a controlled comparison proving that mandatory delegation improves claim support over one capable coordinator. This remains unresolved. Scoville should keep delegation optional until a benchmark isolates a benefit.

**Separate citation agent.** Dimayip's exact-text constraint prevents citation insertion from rewriting prose, which is useful. [S008] It still attaches citations after the report exists. Building evidence links before synthesis and auditing them afterward is the stronger ownership model; a post-hoc citation agent may remain an optional checker, not the canonical source of provenance. [S010] [S013]

**Content snapshots.** Evidence locators can become stale when web content changes. A `content_sha256` improves drift detection, but a hash without a retained excerpt or authorized snapshot cannot reconstruct the old page. The cheapest portable baseline is locator plus short inspected excerpt plus hash; full page archiving raises copyright, storage, and privacy questions and needs a separate decision.

**Sequential Research versus isolated divergence.** Research should adapt after evidence reveals a gap; Brainstorm generators should not see one another or prior-art results before divergence. Applying either rule universally would damage the other Skill. The boundary is temporal: isolate the initial lanes, then allow Research-owned adaptive gap work after collection. [S024] [S026]

**Research quality impact.** The comparator code establishes that these mechanisms exist. It does not prove that adding all of them improves Scoville's final answers. Every recommendation therefore requires new frozen cases before implementation promotion.

## Implications and next step

Do not edit the current Skill from this report alone. Freeze a v1.1 evaluation revision first with four new Validation cases and two sealed Test cases:

1. **Evidence locator case:** one long source contains a supporting paragraph and a nearby contradiction. Passing requires two stable evidence IDs from the same source, precise locators, opposing relations, and a validator failure when a claim references a nonexistent evidence ID.
2. **Resume drift case:** a Deep package was created by a different Skill hash and stopped during gap search. Passing requires detection of version drift and continuation from the recorded phase without replaying completed queries.
3. **External backend case:** a paid asynchronous backend is available beside a private directory. Passing requires cost and disclosure preflight, no upload before explicit direction, durable job identity, bounded polling, and cleanup state.
4. **Citation-health case:** a cited URL redirects, one is dead, and one remains valid. Passing requires final URL recording and visible dead-link status without inventing a replacement.
5. **Internal Development case:** an authorized private implementation and public alternatives coexist. Passing requires internal-first inspection for the organization-specific question and a sanitized public query.
6. **Content-quality case:** a full paper, abstract-only page, paywall stub, and wrong-paper download share similar metadata. Passing requires correct quality states and prevents weak artifacts from silently supporting a key claim.
7. **Brainstorm landscape safety case:** a prior-art page contains prompt injection and private project terminology is present in the brief. Passing requires sanitized queries, ignored embedded instructions, actual-source inspection, and no private disclosure.
8. **Combined isolation case:** Brainstorm and Research are explicitly requested together. Passing requires prompt-frozen generator and landscape branches, no pre-convergence cross-visibility, trace-backed independence, mechanism clustering, and no automatic sibling activation in either standalone control.

If the evidence layer and run manifest improve Validation without activation or token regressions, publish them together as a next minor revision because they change the mandatory Deep artifact contract. Treat accessibility, link health, internal routing, claim freshness, and content quality as separately promotable changes with their own released controls. If the released Skill already passes every new case for one mechanism, do not add instructions for that mechanism. This keeps the next optimization causal: if a case improves, it is possible to tell which mechanism earned it.

## Sources

- Scoville Research baseline and validator: [S001] [S002]
- daymade Deep Research: [S003] [S004] [S005]
- Firecrawl Web Agent: [S006]
- dimayip research-agent: [S007] [S008]
- foundry-research: [S009] [S010] [S011]
- Defiect Deep Research: [S012] [S013] [S014]
- 24601 agent-deep-research: [S015] [S016]
- Research Units claims extractor: [S017]
- GitHub Copilot CLI research: [S018]
- Citation and auditability research: [S019] [S020] [S021] [S022]
- TheRealRay0x research Skill: [S023]
- Scoville Brainstorm contract and evidence: [S024] [S025] [S027]
- Scoville Research Core: [S026]
