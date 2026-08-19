---
format_version: 1
id: ADR-0003
status: accepted
created: 2026-08-19
accepted: 2026-08-19
scope: family/research-brainstorm
transition_batch: 9b21ae7b33fae66f253105632f1eb503f33448957715e77df0bc14b2e1b2e7f5
transition_batch_members: [ADR-0002, ADR-0003]
---

# Keep Research and Brainstorm distinct with an isolated composition protocol

## Decision

Recommend that Scoville Research and Scoville Brainstorm remain standalone Skills with separate outputs and no automatic sibling activation. Exchange only concern-specific guardrails, and define one explicit combined protocol that keeps Brainstorm generators isolated from Research landscape evidence until convergence.

## Problem

The two Skills meet at prior art, assumptions, and decision support, but they solve opposite early-stage problems. Research narrows uncertainty by collecting and challenging evidence. Brainstorm protects divergence from early convergence and anchoring. Running Research first can shrink the option space before Brainstorm generates; running Brainstorm's no-cross-wave rule through the whole Research loop would prevent evidence-driven gap and contradiction queries.

The current boundary is directionally correct but incomplete. Brainstorm's landscape pass does not state Research's untrusted-content, private-query, inspection-depth, or source-independence floor. Research permits optional evidence lanes but does not freeze first-wave prompts or make independence claims explicitly trace-owned.

## Drivers

- Brainstorm must retain materially different mechanism generation before prior art anchors the generators.
- Research must remain adaptive after evidence reveals gaps or contradictions.
- Retrieved landscape content must never change authority, reveal private details, or count snippets and retellings as independent evidence.
- Independence and parallelism are observed tool properties, not names assigned in prose.
- Both Skills must remain useful when the other is absent, inactive, or inapplicable.
- Human selection stays outside both Skills.

## Considered alternatives

- Merge both Skills into one discovery Skill. This removes a handoff, but makes activation ambiguous and combines deliberate divergence with evidence convergence in one loaded contract.
- Always run Research before Brainstorm. This improves prior-art awareness, but exposes generators to the existing landscape and can turn novelty search into variation around the first plausible comparator.
- Always run Brainstorm before Research. This protects divergence, but postpones basic factual checks even when one supplied assumption would invalidate the entire idea space.
- Leave both Skills unchanged and rely on a coordinator to improvise composition. This preserves size, but makes privacy, isolation, evidence ownership, and reporting depend on unstated host behavior.

## Consequences

- Brainstorm adopts Research's untrusted-content, private-query sanitization, actual-source inspection, source-independence, and exact-URL rules only for its landscape and prior-art work.
- Brainstorm does not create Deep ledgers, expand into a literature review, or require Research.
- Research freezes every first-wave parallel evidence-lane prompt before the first lane starts and calls lanes independent only when separate isolated calls are visible in the execution trace.
- Later Research contradiction and gap queries remain adaptive and may use prior results.
- Development research sharpens its existing candidate funnel by clustering candidates by underlying mechanism before shortlisting and by naming one load-bearing-assumption challenge and strongest practical comparator when they can change the decision.
- On explicit combined invocation, one factual frame is frozen first. Brainstorm generator prompts and the Research landscape question are then frozen and run in isolated parallel branches. The Research-owned lane replaces Brainstorm's native landscape agent for that combined run and becomes the sole landscape input to Brainstorm convergence; Brainstorm does not launch a second landscape agent. Generators receive no landscape output and Research receives no candidate ideas before collection. The Brainstorm-native Plan must encode and test this substitution before its package changes.
- Brainstorm owns post-collection mechanism convergence and the decision point. Research may deepen evidence for stable candidate IDs in a later user-requested step.
- Neither Skill activates, installs, requires, or simulates the other. Originality labels remain Brainstorm-owned; claim-evidence status remains Research-owned.
- Any Brainstorm package change requires a separate Brainstorm-native Plan before implementation. This Research repository remains the coordination and evidence owner for the proposed family boundary.

## Confirmation

Add standalone negative controls and combined-workflow cases before editing either Skill. Confirmation requires prompt-injection and private-query cases in Brainstorm landscape work, source-origin collapse, Research first-wave prompt freezing, trace-backed independence, mechanism clustering, an explicit combined run with no pre-convergence cross-visibility, and standalone runs proving that neither sibling became a dependency. Fable and Codex must agree that the final wording preserves both owners before implementation starts.

## Revisit when

Revisit if the hosts expose a standard isolated research-lane primitive, if combined use becomes common enough to justify a dedicated coordinator Skill, if trace evidence cannot distinguish the required topology, or if benchmarks show that isolated prior-art comparison harms decision quality more than it protects divergence.
