# Scoville Research

A source list can look convincing while the answer rests on very little. Five
articles may repeat the same press release. A real citation may concern the
right topic without supporting the sentence attached to it.

Scoville Research follows claims back to the evidence that can answer the
question. It covers current web research, GitHub-first implementation discovery,
academic literature and longer investigations that need saved records. It
keeps contradictions and gaps visible and stops when another search would no
longer change the decision.

Use it for questions that need several sources examined together. A summary of
one known page or paper, ordinary repository inspection, brainstorming,
implementation or wording work belongs with the corresponding task.

## Why "Scoville"?

The family is named for useful signal that remains detectable after dilution.
In Research, that means tracing a claim back through its retellings to the evidence that supports it.

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
inspected prior-art lane. Brainstorm keeps the generators isolated from that
lane until convergence. This avoids researching the same landscape twice.

Explicit `$scoville-research` invocation also works on hosts that support named
Skill invocation.

## Compatibility

Any Agent Skills host that can read references/. Requires web search and fetching actual source pages. Deep mode also needs a writable workspace and Python 3 for scripts/validate_research_artifacts.py. Subagents are optional and capacity-bound: without a documented close control, report open targets and skip lanes that do not fit. Developed for Codex and Claude Code; other hosts untested.

## Install

### Install this Skill

In a local Codex or Claude Code session, ask:

```text
Install this Agent Skill for all my projects from this exact package directory:
https://github.com/benjaminstelzer/scoville-research/tree/main/scoville-research
Preserve existing customizations and ask before overwriting conflicting files.
Report the installed location and whether the host discovers the Skill.
```

The agent needs source access and permission to write to its personal Skills
location. Manual fallback: [Codex Skills guide](https://learn.chatgpt.com/docs/build-skills)
or [Claude Code Skills guide](https://code.claude.com/docs/en/skills).

Install only the linked package for the focused option.

### Install the complete Scoville suite

```text
Install the complete Scoville Skill suite for all my projects. Fetch and install every exact package directory below:

https://github.com/benjaminstelzer/scoville-brainstorm/tree/main/scoville-brainstorm
https://github.com/benjaminstelzer/scoville-research/tree/main/scoville-research
https://github.com/benjaminstelzer/scoville-code-anti-ai-slop/tree/main/scoville-code-anti-ai-slop
https://github.com/benjaminstelzer/scoville-design-anti-ai-slop/tree/main/scoville-design-anti-ai-slop
https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop/tree/main/scoville-ui-anti-ai-slop
https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop/tree/main/scoville-scribe-anti-ai-slop
https://github.com/benjaminstelzer/scoville-plan/tree/main/scoville-plan
https://github.com/benjaminstelzer/scoville-handoff/tree/main/scoville-handoff

Preserve existing customizations and ask before overwriting conflicting files. Report every installed location and whether the host discovers each Skill.
```

## What it enforces

- **Scoped report writing.** Requested saved research artifacts may be written
  at the agreed output path. Investigated systems and source material remain
  read-only. Chat-only research creates no files, including in Deep mode.
- **The smallest sufficient route.** One known source stays a normal task.
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
  sufficient or the remaining gap is explicit.

The complete contract is in [SKILL.md](scoville-research/SKILL.md).

## How it works

The Core frames the question and data boundary, inspects canonical sources,
traces claims, searches for contradictions, and stops at decision sufficiency.
Development and Academic routes select the relevant evidence. Deep adds durable
research artifacts only when saving them is requested.

A saved Deep run preserves the brief, queries, sources, passage-level evidence,
claims, contradictions, and report. The optional standard-library validator
checks structure, references, and package continuity without a network call.
It does not prove that a citation supports its claim. Legacy records are never
silently migrated. See the [Deep contract](scoville-research/references/deep-research.md).

## How it was developed

I developed Research through source inspection, research tasks and model
evaluations. The difficult part is often the connection between a claim and
its source. A relevant link can still support a different statement, and
several agreeing pages may all repeat the same origin.

I read complete research histories to see where that connection breaks, where
the question loses its scope and where more queries stop changing the answer.
Those observations guide the revisions in the [changelog](CHANGELOG.md).
[SkillOpt proposals](https://github.com/benjaminstelzer/scoville-research/blob/8777b872c64a45db4703591ba777c567a457228b/CHANGELOG.md)
that lost required cases were rejected. Reducing the instructions would not
help if the research became less reliable.

## Scoville family

Each Skill works independently. Combine only the concerns the task actually
needs:

- [Brainstorm](https://github.com/benjaminstelzer/scoville-brainstorm) explores
  materially different mechanisms before selection.
- [Research](https://github.com/benjaminstelzer/scoville-research) turns web,
  GitHub, and scholarly evidence into a decision-ready, claim-traceable result.
- [Code](https://github.com/benjaminstelzer/scoville-code-anti-ai-slop) owns
  engineering scope, implementation, risk, and validation.
- [Design](https://github.com/benjaminstelzer/scoville-design-anti-ai-slop) owns
  visual definition, art direction, design systems, critique, and repair.
- [UI](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop) owns
  framework-aligned implementation, interface mechanics, accessibility, and
  rendered evidence, with a standalone design fallback.
- [Scribe](https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop) owns
  wording, terminology, factual meaning, and source fidelity.
- [Plan](https://github.com/benjaminstelzer/scoville-plan) owns durable Plans,
  Work Items, Decisions, and lifecycle state.
- [Handoff](https://github.com/benjaminstelzer/scoville-handoff) transfers active
  work to another agent or session.

## Current Codex lifecycle limitation

On 2026-09-09, the tested Codex Desktop tool surface exposed no control whose
documented semantics close a completed subagent thread and free its slot. Other
Codex hosts may expose an equivalent control under a different name. Research
therefore discovers lifecycle controls by documented behavior, reports unavailable
cleanup before delegation, skips optional evidence lanes that do not fit, and
blocks a required composed lane when capacity is insufficient. Interrupting,
archiving, deleting a task, or killing a process is not assumed to free a
subagent slot.

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

## License

MIT. See [LICENSE](LICENSE).
