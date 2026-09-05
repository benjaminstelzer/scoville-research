# Scoville Research source and provenance audit

This audit records what informed Scoville Research, what each source actually contributed, and what it did not prove. A source appearing here does not mean its wording, code, or full workflow was copied. The point is narrower and more useful: another reader can reconstruct why a design choice exists, follow the evidence, and see where the evidence stops.

Access date for web sources: **2026-08-19**.

## Method

Sources are grouped by how they were used:

- **Contract source** defines a platform or package rule.
- **Design source** contributed a workflow mechanism considered for adaptation.
- **Empirical source** reports an experiment or benchmark relevant to the mechanism.
- **Discovery only** was found during landscape search but did not carry a design or public claim.

GitHub sources that materially informed the design are pinned to inspected commits. Repository popularity was used only for discovery, never as evidence of quality. For papers, the audit distinguishes peer-reviewed publications from arXiv preprints. Abstract inspection supports only the claim stated in the abstract; it does not quietly become a full-paper review because the title was persuasive.

## Platform and package contracts

### A01 - Agent Skills specification

- Source: [Agent Skills specification](https://agentskills.io/specification)
- Type: Contract source
- Inspected: Directory structure, required frontmatter, optional resources, file references, validation, and progressive disclosure.
- Contribution: Portable `SKILL.md` package boundary, matching directory and Skill name, concise description, and on-demand references.
- Limit: The specification defines format, not research quality or host-identical activation behavior.

### A02 - OpenAI Build skills

- Source: [OpenAI documentation: Build skills](https://learn.chatgpt.com/docs/build-skills)
- Type: Contract source
- Inspected: Skill anatomy, progressive disclosure, implicit and explicit invocation, description matching, and Codex loading locations.
- Contribution: Compact Core, discriminating activation metadata, and conditional references rather than one large research manual.
- Limit: Product documentation does not establish that any proposed research workflow improves factual accuracy.

### A03 - OpenAI Web search

- Source: [OpenAI documentation: Web search](https://learn.chatgpt.com/docs/web-search)
- Type: Contract source
- Inspected: Search availability, live versus indexed behavior, transcript visibility, configuration boundaries, and the requirement to treat results as untrusted input.
- Contribution: Freshness-aware search and an explicit untrusted-content boundary.
- Limit: Search availability and mode vary by host and workspace configuration.

### A04 - OpenAI Deep research API guide

- Source: [OpenAI API guide: Deep research](https://developers.openai.com/api/docs/guides/deep-research)
- Type: Design and safety source
- Inspected: Supported search and analysis tools, background execution, MCP use, prompt-injection risk, logging, separation of public and private data phases, and link screening.
- Contribution: Public-web and private-data separation, tool-call auditability, and prompt-injection defenses.
- Limit: This is an API workflow, not the runtime contract of a standalone Codex Skill.

## Inspected Agent Skills and implementations

### A05 - OpenAI research router

- Source: [research-router-skill at `fb0a183`](https://github.com/openai/plugins/blob/fb0a18376bcd9f2604047fbe7459ec5aed70c64b/plugins/life-science-research/skills/research-router-skill/SKILL.md)
- Type: Design source
- Inspected: Research-lane classification, entity normalization, minimum useful downstream selection, bounded delegation, conflict reconciliation, and evidence-aware output.
- Contribution: Router before retrieval, evidence lanes, minimum sufficient tool set, and coordinator-owned synthesis.
- Limit: The implementation is specific to life sciences and its available downstream Skills.
- License note: No repository-level SPDX license was exposed by GitHub during inspection. No text or code is copied.

### A06 - OpenAI GitHub Skill

- Source: [GitHub Skill at `1540745`](https://github.com/openai/plugins/blob/1540745b82d5d139be8912fc3db42dadf2da60a7/plugins/github/skills/github/SKILL.md)
- Type: Design source
- Inspected: Connector-first repository orientation, local `git` and `gh` fallback boundaries, context resolution, and routing to specialist workflows.
- Contribution: Prefer structured GitHub access for repository evidence, then use local or CLI paths for gaps the connector does not cover.
- Limit: The Skill handles repository work, not open-ended technology research.

### A07 - OpenAI Hugging Face papers Skill

- Source: [Hugging Face papers Skill at `d58c20d`](https://github.com/openai/plugins/blob/d58c20d407d49fd63ac2fb07c0c4dcdf7bbdc35d/plugins/hugging-face/skills/papers/SKILL.md)
- Type: Design source
- Inspected: arXiv identifier normalization, structured paper metadata, Markdown retrieval, and links between papers, models, datasets, Spaces, project pages, and GitHub repositories.
- Contribution: Treat a paper, its implementation, and its data as related but distinct evidence objects.
- Limit: Hugging Face coverage is AI-focused and not a complete academic index.

### A08 - Xiaomi MiMo Deep Research

- Source: [deep-research at `5ecca0d`](https://github.com/XiaomiMiMo/MiMo-Code/blob/5ecca0daeebc8d5415bf6b5c9c3a2903f20552d5/packages/opencode/src/skill/builtin/.bundle/deep-research/SKILL.md)
- Type: Design source
- License: MIT
- Inspected: Triage, depth modes, durable brief, independent angles, gap reflection, single-writer synthesis, resumability, and source-backed report rules.
- Contribution: Research brief, bounded follow-up rounds, gap-driven delta queries, and one synthesis owner.
- Rejected unchanged: Hard source targets and mandatory subagent counts. Counts remain planning bounds, not evidence quality.

### A09 - Xiaomi MiMo topic survey

- Source: [topic-survey at `1e8af91`](https://github.com/XiaomiMiMo/MiMo-Code/blob/1e8af9190a7f7c349331ebb5227baf14d405a901/packages/opencode/src/skill/builtin/.bundle/super-research/references/topic-survey.md)
- Type: Design source
- License: MIT
- Inspected: Question decomposition, query variants, source and claim ledgers, dead-end logging, contradiction handling, scholarly API use, citation snowballing, and saturation.
- Contribution: Claim-to-source traceability, explicit rejected sources, contradiction search, and stopping when new retrieval stops changing the claim set.
- Rejected unchanged: The exact 15/30 source defaults and the rule that absence of contradiction is inherently suspicious.

### A10 - 199 Biotechnologies Deep Research

- Source: [deep-research at `a9d9fae`](https://github.com/199-biotechnologies/claude-deep-research-skill/blob/a9d9faee0c186604c67ce2824a0ab7e1546dabb8/SKILL.md)
- Type: Design source
- License note: The README declares MIT, while GitHub exposed no recognized repository license during inspection. No text or code is copied.
- Inspected: Stable source identities, append-only evidence and claim stores, run manifests, claim-support validation, report validation, and packaging.
- Contribution: Separate source, evidence, claim, and run records; validate their internal relationships deterministically.
- Rejected unchanged: Three sources for every major claim, mandatory long-form reports, and automatic HTML/PDF packaging.

### A11 - K-Dense Parallel Web

- Source: [parallel-web at `b085e11`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/b085e116c5de7d244fccbd666f1a9e73257999e4/skills/parallel-web/SKILL.md)
- Type: Design source
- License: MIT
- Inspected: Capability routing, academic source priority, command construction, untrusted-result handling, context chaining, polling limits, and deep-research adapter behavior.
- Contribution: Route by operation shape and preserve untrusted-data and bounded-polling rules.
- Rejected unchanged: Required Parallel service, CLI, API key, processor tiers, and provider-specific result contracts.

### A12 - NVIDIA AI-Q Research

- Source: [aiq-research at `e8ac07f`](https://github.com/NVIDIA/skills/blob/e8ac07fb15a93920460145426c1443d7be1593a5/skills/aiq-research/SKILL.md)
- Type: Design source
- License: Apache-2.0
- Inspected: Backend trust disclosure, health checks, asynchronous job polling, interruption recovery, version compatibility, citation preservation, and failure reporting.
- Contribution: External research backends, when used, need explicit trust, resumable job identity, bounded polling, and intact source URLs.
- Rejected unchanged: AI-Q deployment and endpoint dependency.

### A13 - LifeOS Research

- Source: [Research Skill at `be9e8ef`](https://github.com/danielmiessler/LifeOS/blob/be9e8ef889f00a29f4fd677dee4772fdf32e07ce/LifeOS/install/skills/Research/SKILL.md)
- Type: Design source
- License: MIT
- Inspected: Depth routing, URL verification, community-source routing, confidence tags, multi-provider orchestration, persistent investigation state, and claim-level adversarial verification.
- Contribution: Verify source accessibility, route sentiment to primary community evidence, and keep deep investigations resumable.
- Rejected unchanged: Mandatory activation on the word `research`, LifeOS-specific notifications and paths, required vendor roster, confidence-by-label, and large fixed agent counts.

## Empirical research used in the design

### E01 - BrowseComp

- Citation: Wei, J. et al. (2025). [BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents](https://arxiv.org/abs/2504.12516). arXiv:2504.12516.
- Status: arXiv preprint and OpenAI benchmark publication.
- Inspected: Abstract and published benchmark summary.
- Finding used: Difficult browsing requires persistence, strategic reformulation, and assembling fragmented clues; short-answer retrieval remains narrower than open-ended research reporting.

### E02 - DeepResearch Bench

- Citation: Du, M., Xu, B., Zhu, C., Wang, X., and Mao, Z. (2025). [DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents](https://arxiv.org/abs/2506.11763). arXiv:2506.11763.
- Status: arXiv preprint.
- Inspected: Abstract and benchmark dimensions.
- Finding used: Report quality and retrieval quality require separate evaluation; effective citation count and citation accuracy are useful but incomplete measures.

### E03 - Deep Research Bench with RetroSearch

- Citation: FutureSearch et al. (2025). [Deep Research Bench: Evaluating AI Web Research Agents](https://arxiv.org/abs/2506.06287). arXiv:2506.06287.
- Status: arXiv preprint.
- Inspected: Abstract.
- Finding used: Frozen web corpora make longitudinal agent comparisons more reproducible and expose hallucination, tool-use, and forgetting behavior.

### E04 - BrowseComp-Plus

- Citation: Chen, Z. et al. (2026). [BrowseComp-Plus: A Fair and Disentangled Evaluation Benchmark for Deep Search Agents](https://aclanthology.org/2026.acl-long.1023/). ACL 2026.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract and reported comparison.
- Finding used: A fixed, human-verified corpus can separate retrieval quality from reasoning quality and make evaluation more reproducible.

### E05 - ResearchArena

- Citation: Kang, H. and Xiong, C. (2025). [ResearchArena: Benchmarking Large Language Models' Ability to Collect and Organize Information as Research Agents](https://aclanthology.org/2025.findings-emnlp.303/). Findings of EMNLP 2025.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Finding used: Academic survey work separates discovery, selection, and organization; simple keyword retrieval remained a meaningful baseline in the reported experiments.

### E06 - Beyond Browsing

- Citation: Song, Y., Xu, F. F., Zhou, S., and Neubig, G. (2025). [Beyond Browsing: API-Based Web Agents](https://aclanthology.org/2025.findings-acl.577/). Findings of ACL 2025.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract and reported WebArena result.
- Finding used: Structured APIs and hybrid API/browser agents can outperform browser-only interaction. This supports GitHub and scholarly APIs as first-class evidence interfaces.
- Limit: WebArena interaction success is not direct evidence of long-form research quality.

### E07 - Cited but Not Verified

- Citation: Onweller, H. et al. (2026). [Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents](https://arxiv.org/abs/2605.06635). arXiv:2605.06635.
- Status: arXiv preprint.
- Inspected: Abstract.
- Finding used: Working links and topical relevance do not establish factual support. The reported ablation found that substantially more tool calls did not improve citation factuality and reduced it in the tested setting.

### E08 - DRNOISE

- Citation: Nie, J. et al. (2026). [DRNOISE: Benchmarking Deep Research Agents in Misleading Evidence Environments](https://arxiv.org/abs/2607.17291). arXiv:2607.17291.
- Status: arXiv preprint.
- Inspected: Abstract.
- Finding used: A plausible direct-looking false document can displace a correct indirect evidence chain; generic verification prompts do not fully resolve that failure.

### E09 - Misleading knowledge and false conclusions

- Citation: Zhu, P., Li, L., Yang, L., and Su, S. (2026). [Is Deep Research Reliable? Misleading Knowledge Induces False Conclusions](https://arxiv.org/abs/2607.20891). arXiv:2607.20891.
- Status: arXiv preprint.
- Inspected: Abstract.
- Finding used: Reliability needs verification and correction at the workflow level, not only stronger planning or retrieval.

### E10 - FS-Researcher

- Citation: [FS-Researcher: Test-Time Scaling for Long-Horizon Research Tasks with File-System-Based Agents](https://aclanthology.org/2026.acl-long.288/). ACL 2026.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Finding used: A persistent filesystem workspace can preserve evidence and scale long research trajectories beyond one context window.

### E11 - Multi-turn report revision

- Citation: Chen, B. et al. (2026). [Beyond Single-shot Writing: Deep Research Agents are Unreliable at Multi-turn Report Revision](https://aclanthology.org/2026.acl-long.609/). ACL 2026.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Finding used: Revisions can regress previously correct content and citation quality. The final Skill therefore treats earlier evidence as state to preserve and rechecks affected claims after revision.

### E12 - DREAM

- Citation: Ben Avraham, E. et al. (2026). [DREAM: Deep Research Evaluation with Agentic Metrics](https://aclanthology.org/2026.acl-long.448/). ACL 2026.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Finding used: Fluent synthesis can hide factual and temporal defects; evaluation needs current tool-using verification when freshness is part of the claim.

### E13 - DeepFact

- Citation: Huang, Y. et al. (2026). [DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality](https://aclanthology.org/2026.acl-long.1586/). ACL 2026.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Finding used: Claim-level factuality evaluation is difficult even for experts and benefits from auditable evidence and revisable adjudication rather than a single opaque score.

### E14 - PaperScope

- Citation: Xiong, L. et al. (2026). [PaperScope: A Multi-Modal Multi-Document Benchmark for Agentic Deep Research Across Massive Scientific Papers](https://aclanthology.org/2026.findings-acl.394/). Findings of ACL 2026.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Finding used: Scientific research may depend on evidence distributed across text, tables, and figures in many papers; abstract-only research cannot claim full-paper coverage.

### E15 - Claim-level auditability perspective

- Citation: Rasheed, R. A., Banerjee, S., Mukherjee, A., and Hazra, R. (2026). [From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents](https://arxiv.org/abs/2602.13855). arXiv:2602.13855.
- Status: Perspective preprint, not an empirical benchmark.
- Inspected: Abstract.
- Contribution: Provenance coverage, provenance soundness, contradiction transparency, and audit effort are useful design dimensions.
- Limit: The source argues for a standard; it does not by itself validate the proposed Scoville implementation.

### E16 - ManuSearch

- Citation: [ManuSearch: Democratizing Deep Search in Large Language Models with a Transparent and Open Multi-Agent Framework](https://aclanthology.org/2025.findings-emnlp.130/). Findings of EMNLP 2025.
- Status: Peer-reviewed conference paper.
- Inspected: Abstract.
- Contribution: Separate planning, retrieval, and structured evidence extraction are plausible orchestration boundaries.
- Limit: Scoville Research does not infer that the same work must be split across agents.

## Discovery-only sources

These sources were found during the landscape pass. They helped classify the space but do not support a README claim or a copied mechanism:

- [mayrsascha/deep-research-skill](https://github.com/mayrsascha/deep-research-skill) - context-aware prompt generator for external research products; MIT.
- [24601/agent-deep-research](https://github.com/24601/agent-deep-research) - Gemini Interactions API adapter with RAG and polling; MIT.
- [xpepper/perplexity-agent-skill](https://github.com/xpepper/perplexity-agent-skill) - Perplexity CLI adapter; MIT.
- [PaperSearchQA](https://aclanthology.org/2026.eacl-long.88/) - scientific-paper search-agent benchmark.
- [AssistantBench](https://aclanthology.org/2024.emnlp-main.505/) - realistic, time-consuming web-agent tasks.
- [TurkingBench](https://aclanthology.org/2025.naacl-long.188/) - challenging web-agent tasks.
- [ReportLogic](https://aclanthology.org/2026.acl-long.384/) - logical quality and reader-centered auditability.
- [DR-Arena](https://aclanthology.org/2026.acl-long.1249/) - automated evaluation framework for deep-research agents.
- [Deep Research with Open-Domain Evaluation and Multi-Stage Guardrails](https://aclanthology.org/2026.acl-long.2010/) - stage-wise open-domain safety evaluation.
- [CogGen](https://aclanthology.org/2026.findings-acl.296/) - recursive deep-research report generation.

## Claim-to-source design map

| Design claim | Supporting sources | Resulting boundary |
| --- | --- | --- |
| Research needs routing before retrieval. | A05, E05, E16 | Freeze the question and evidence lanes before searching deeply. |
| More retrieval is not automatically better evidence. | E07, E08, E09 | Use gap-driven retrieval and saturation; never promote source count to correctness. |
| GitHub and scholarly APIs are evidence interfaces, not optional conveniences. | A06, A07, E06 | Prefer structured API and repository inspection where available, with browser fallback. |
| Long research should survive context loss. | A08, A10, A13, E10 | Deep mode writes a brief, query log, source ledger, claim ledger, and report. |
| A citation must connect a claim to inspected evidence. | A09, A10, E02, E07, E13, E15 | Track claim-source relationships and contradictions; link validity alone is insufficient. |
| Misleading sources require active reconciliation. | E08, E09 | Search for record-level corroboration and preserve unresolved conflicts. |
| One final synthesis owner reduces section-level drift risk. | A05, A08 | Parallel retrieval is optional; final scope and synthesis remain coordinated. |
| Evaluation must isolate routing, retrieval, synthesis, and artifacts. | E02, E03, E04, E05, E12 | Use gold-isolated cases, a no-Skill baseline, validation, and untouched test evidence. |

## Local implementation evidence

These local sources define family consistency and the evaluation procedure. They are operational evidence, not external inspiration:

- [Scoville Brainstorm](https://github.com/benjaminstelzer/scoville-brainstorm)
- [Scoville Code](https://github.com/benjaminstelzer/scoville-code-anti-ai-slop)
- [Scoville Handoff](https://github.com/benjaminstelzer/scoville-handoff)
- [Scoville Plan](https://github.com/benjaminstelzer/scoville-plan)
- [Scoville Scribe](https://github.com/benjaminstelzer/scoville-scribe-anti-ai-slop)
- [Scoville UI](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop)
- [BenjaminStelzer profile repository](https://github.com/benjaminstelzer/BenjaminStelzer)
- Local SkillOpt Studio snapshot: `AGENTS.md`, `README.md`, and `configs/default.yaml`

They contributed the shared README order, Family copy, release and evidence style, profile grouping requirement, and the exact SkillOpt isolation, split, promotion, and stop gates. Their current bytes were re-read before the public documentation and evaluation work.

## Attribution boundary

Scoville Research is an original synthesis of these constraints and findings. It copies no source Skill text, implementation, template, or script. MIT and Apache-2.0 sources remain credited because their mechanisms materially informed the comparison. Sources with unclear repository licensing are used only as inspected prior art and receive no code or prose reuse.
