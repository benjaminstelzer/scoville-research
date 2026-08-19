# Scoville Research

More links are easy. Better evidence is not.

It usually looks harmless:

- Six articles confirm a release claim. Five copied the sixth, which copied the
  press release.
- A paper reports a strong benchmark result, so the method is called
  production-ready before anyone checks the repository, license, or missing
  implementation pieces.
- A citation is real, current, and topically relevant. It still does not
  support the sentence attached to it.
- One retrieved page contains instructions for the agent. Apparently the web
  has promoted itself to project owner.

That is research slop: visible activity without a reliable evidence chain.
The result looks researched because the source list is long, while the actual
decision still rests on repetition, inference, or an uninspected abstract.

Scoville Research is a read-only Agent Skill for current multi-source web
research, GitHub-first implementation discovery, academic literature work, and
durable deep research. It routes each question to the evidence that can answer
it, preserves contradictions and inspection limits, and stops when the
remaining uncertainty is visible and another query would not change the
decision.

Do not use it for one known page or paper summary, an ordinary repository
inspection, pure brainstorming, planning, implementation, or wording work.

## Why "Scoville"?

The family is named for useful signal that remains detectable after dilution.
Research accumulates pages quickly. Its useful heat is the smaller evidence
chain that survives source tracing, contradiction search, and an honest check
of what was actually inspected.

## How to use

Name Scoville Research and the actual decision in the request. The Skill chooses
the smallest route that can answer it.

**Development** - investigate an implementation landscape rather than compare
README feature tables:

```text
Use Scoville Research to find open-source libraries for offline-first conflict handling on Windows. Inspect GitHub source, releases, issues, tests, licenses, and official documentation. Return a shortlist, the evidence that separates it, and the cheapest feasibility test. Do not implement anything.
```

**Academic** - trace papers at their real publication and inspection depth:

```text
Use Scoville Research for a literature review of agentic deep-research factuality. Distinguish preprints from peer-reviewed work, connect papers to code and data where available, preserve disagreements, and mark abstract-only findings as abstract-only.
```

**Deep** - keep an audit-ready investigation resumable across sessions:

```text
Use Scoville Research in Deep mode to determine whether a hybrid API and browser research agent is viable for this product. Preserve the brief, query log, source ledger, claim ledger, contradictions, and final report. Keep private project details out of public queries.
```

When a decision also needs deliberately different candidate mechanisms, request
Scoville Research and Scoville Brainstorm explicitly. Research then owns one
inspected prior-art lane; Brainstorm keeps the generators isolated from that
lane until convergence. Two landscape passes would look thorough, but mainly
create two owners for the same evidence.

Explicit `$scoville-research` invocation also works on hosts that support named
Skill invocation.

## Install

Use an Agent Skills-compatible host and Terra 5.6 Medium or a comparably
capable executor such as Opus 4.8. Ask the agent to install:

```text
Install this Agent Skill and refresh the available Skill list:
https://github.com/benjaminstelzer/scoville-research/tree/main/scoville-research
Keep the installed directory name scoville-research. Use Terra 5.6 Medium or a comparably capable executor such as Opus 4.8.
```

The final path must end in `<skills-dir>/scoville-research/SKILL.md`. For Claude
Code, use `~/.claude/skills/` globally or `.claude/skills/` inside one project.
Other hosts use their supported Skills directory.

**What it costs.** Research loads a 1,501-token Core. Development, Academic,
and Deep references load only when their route needs them, and real research
can use materially more time, browsing, and context than an answer without the
Skill. That cost buys a traceable claim-evidence chain, not a larger decorative
bibliography. Use it when current multi-source evidence can change a material
decision. See [benchmark evidence](docs/benchmark-evidence.md).

## What it enforces

- **The smallest sufficient route.** One known source stays a normal task;
  Development, Academic, and Deep behavior load only when the question needs
  them.
- **Evidence ownership.** Specifications own their contracts, repositories own
  observed implementation, papers own reported experiments, and none quietly
  inherits the authority of another.
- **Claim-level boundaries.** Reported claims, direct observations, inference,
  contradiction, and unresolved gaps remain distinguishable.
- **Exact evidence units.** Deep claims link to inspected passages or scoped
  observations with stable locators, not merely to an entire source.
- **Source independence.** Ten retellings of one origin still count as one
  origin.
- **Hostile-content resistance.** Retrieved pages, papers, issues, and tool
  output are untrusted data, not instructions.
- **Private/public separation.** Local or private material does not enter an
  external query unless the user explicitly authorizes that disclosure.
- **A decision stop.** Research ends when the decision-relevant evidence is
  sufficient or the remaining gap is explicit. More tabs are not promoted to
  rigor by seniority.

The complete contract is in [SKILL.md](scoville-research/SKILL.md).

## How it works

A request is routed as `NO`, `GENERAL`, `DEVELOPMENT`, `ACADEMIC`, or a mixed
route with the `DEEP` persistence overlay. The Core freezes the question and
data boundary, discovers canonical sources, inspects the actual evidence,
traces claims, searches for contradictions, fills the weakest remaining gap,
and stops at decision sufficiency.

Deep mode adds `brief.md`, `run.json`, `queries.jsonl`, `sources.jsonl`,
`evidence.jsonl`, `claims.jsonl`, and `REPORT.md`. The run manifest binds the
exact Skill package, phase, resume point, and optional external-job state.
Evidence records preserve the smallest practical locator, excerpt, or scoped
observation behind each claim. Optional source fields keep accessibility, link
health, and content quality separate; time-sensitive claims may carry their own
`as_of` date. None of those fields becomes a credibility score.

The bundled standard-library validator checks structural integrity, Skill-byte
continuity, state transitions, references, headings, and citation IDs without a
network call. Legacy v1 packages remain readable and are never silently
migrated. Valid JSON still does not prove truth or semantic support. The Skill
installs no executable dependency and requires no particular research provider.

## Scoville family

Each Skill works independently. Combine only the concerns the task actually
needs:

- [Brainstorm](https://github.com/benjaminstelzer/scoville-brainstorm) explores
  materially different mechanisms before selection.
- [Research](https://github.com/benjaminstelzer/scoville-research) turns web,
  GitHub, and scholarly evidence into a decision-ready, claim-traceable result.
- [Code](https://github.com/benjaminstelzer/scoville-code-anti-ai-slop) owns
  engineering scope, implementation, risk, and validation.
- [UI](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop) owns
  interface hierarchy, framework fit, accessibility, and rendered evidence.
- [Scribe](https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop) owns
  wording, terminology, factual meaning, and source fidelity.
- [Plan](https://github.com/benjaminstelzer/scoville-plan) owns durable Plans,
  Work Items, Decisions, and lifecycle state.
- [Handoff](https://github.com/benjaminstelzer/scoville-handoff) transfers active
  work to another agent or session.

## Status

The v1.1.0 candidate passed **13/13 open Validation cases**, **4/4 one-shot
sealed holdout cases**, and **35/35 deterministic artifact-validator tests**.
Its frozen suite covers Deep v2, external-job boundaries, final citation state,
private-query safety, source independence, mechanism convergence, activation
near-misses, and the explicit Brainstorm composition. SkillOpt used 49 calls to
propose one change; that proposal fell to **12/13** and was rejected.

Those results establish the frozen local corpus, package routing, and structural
contract. They do not establish arbitrary truth, exhaustive web coverage, or
identical behavior on every host and model. See the
[qualification manifest](docs/evidence/w006-research-brainstorm-qualification.json)
and [benchmark evidence](docs/benchmark-evidence.md).

## Sources

- [Agent Skills specification](https://agentskills.io/specification) and
  [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) for the
  portable package and progressive-disclosure contract.
- [OpenAI Deep research guidance](https://developers.openai.com/api/docs/guides/deep-research)
  for public/private data separation, auditability, and prompt-injection risk.
- [Xiaomi MiMo Deep Research](https://github.com/XiaomiMiMo/MiMo-Code/blob/5ecca0daeebc8d5415bf6b5c9c3a2903f20552d5/packages/opencode/src/skill/builtin/.bundle/deep-research/SKILL.md)
  and [topic survey](https://github.com/XiaomiMiMo/MiMo-Code/blob/1e8af9190a7f7c349331ebb5227baf14d405a901/packages/opencode/src/skill/builtin/.bundle/super-research/references/topic-survey.md)
  for durable briefs, gap-driven retrieval, claim ledgers, and saturation.
- [Cited but Not Verified](https://arxiv.org/abs/2605.06635),
  [DRNOISE](https://arxiv.org/abs/2607.17291), and
  [Beyond Single-shot Writing](https://aclanthology.org/2026.acl-long.609/)
  for citation-support, misleading-source, and revision-regression risks.
- [Beyond Browsing](https://aclanthology.org/2025.findings-acl.577/) and
  [FS-Researcher](https://aclanthology.org/2026.acl-long.288/) for structured
  evidence interfaces and durable filesystem state.

Every inspected source, contribution, limit, license note, publication status,
and design claim is recorded in the
[source and provenance audit](docs/research/source-audit.md).
The v1.1.0 comparison against other Research Skills, services, and scholarly
evidence is preserved separately with its
[report](docs/research/research-skills-gap-analysis/REPORT.md),
[27-source ledger](docs/research/research-skills-gap-analysis/sources.jsonl), and
[32-claim ledger](docs/research/research-skills-gap-analysis/claims.jsonl).

## License

MIT - see [LICENSE](LICENSE).
