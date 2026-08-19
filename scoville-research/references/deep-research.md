# Deep research

Add this route when the user explicitly asks for deep, exhaustive, comprehensive, audit-ready, long-running, or interruption-prone research. It overlays the applicable General, Development, or Academic route.

## Create durable state

Use the user-specified output path or create `research/<lowercase-kebab-topic>/` in the current workspace. Keep all research artifacts inside it:

```text
research/<topic>/
|-- brief.md
|-- queries.jsonl
|-- sources.jsonl
|-- claims.jsonl
`-- REPORT.md
```

Do not create this package for bounded research that fits cleanly in the conversation.

### `brief.md`

Use these headings:

```text
# Research brief
## Research question
## Decision or reader
## Scope
## Evidence lanes
## Deliverable
## Data boundary
```

Record the date, material assumptions, explicit exclusions, freshness requirement, and what would count as decision sufficiency.

### `queries.jsonl`

Append one JSON object per material query or retrieval attempt:

```json
{"id":"Q001","query":"exact query or endpoint purpose","lane":"general","purpose":"discovery","result":"new-source","source_ids":["S001"]}
```

Allowed lanes: `general`, `development`, `academic`. Allowed purposes: `discovery`, `verification`, `contradiction`, `gap`. Allowed results: `new-source`, `new-claim`, `no-new-evidence`, `dead-end`, `blocked`.

Do not put secrets or private source text into this log. Record a sanitized description when the actual input must remain private.

### `sources.jsonl`

Keep one current record per stable source ID:

```json
{"id":"S001","url":"https://example.com/source","title":"Source title","kind":"docs","publisher":"Example","published":"2026-08-01","accessed":"2026-08-19","inspection":"section","disposition":"used","notes":"Owns the API contract."}
```

Allowed kinds: `spec`, `docs`, `code`, `release`, `issue`, `pull-request`, `benchmark`, `paper`, `preprint`, `dataset`, `institutional`, `community`, `other`. Allowed inspection values: `full`, `section`, `abstract`, `metadata`, `snippet`. Allowed dispositions: `used`, `context`, `contradiction`, `rejected`, `dead`, `blocked`.

Keep rejected, dead, and blocked sources. They are part of the audit trail, but they never become supporting citations.

### `claims.jsonl`

Keep one current record per atomic claim:

```json
{"id":"C001","claim":"The documented API supports conditional requests.","basis":"reported","status":"supported","support":["S001"],"contradict":[]}
```

Allowed basis values: `supplied`, `reported`, `observed`, `inferred`. Allowed status values: `supported`, `single-source`, `mixed`, `unresolved`, `rejected`.

- `supported` has one or more adequate supporting sources; independence is explained when it matters.
- `single-source` has exactly one supporting source and no contradicting source.
- `mixed` has both supporting and contradicting sources.
- `unresolved` preserves a material gap or conflict without a false verdict.
- `rejected` records a candidate claim that the gathered evidence does not support.

Source IDs in `support` and `contradict` must exist and must not overlap.

### `REPORT.md`

Use these headings unless the user requested another compatible form:

```text
# Research report
## Answer
## Method and coverage
## Findings
## Contradictions and open questions
## Implications and next step
## Sources
```

Cite source IDs inline as `[S001]`. Every cited ID must exist in `sources.jsonl`; every non-obvious factual claim must map to inspected evidence rather than memory.

## Work in passes

1. Freeze the brief and initial evidence lanes.
2. Run a discovery pass with varied terms and source types.
3. Inspect the strongest sources and build the first claim set.
4. Run a dedicated contradiction and later-version pass.
5. Run gap queries against the weakest decision-relevant claims.
6. Draft once the stop conditions are met; do not draft around missing evidence.
7. Recheck every affected claim after revising the report. A correction must not silently regress an earlier supported claim or citation.

On resume, read `brief.md` and the four ledgers, identify the first unfinished evidence lane, and continue without repeating completed queries merely to look busy.

## Stop honestly

Deep does not mean infinite. Stop when the Core conditions hold and the dedicated contradiction and gap passes no longer change a decision-relevant claim. If blocked access, paywalls, missing full text, rate limits, or incompatible evidence prevent closure, preserve the gap and narrow the answer.

## Validate the package

When Python 3 and the bundled script are available, run:

```text
python <skill-dir>/scripts/validate_research_artifacts.py <research-directory> --format json
```

Exit `0` with `valid: true` proves only required files, JSONL shape, stable IDs, cross-references, report headings, and citation identifiers. It does not prove source truth, source independence, semantic claim support, completeness, or research quality. Fix structural errors, then perform the semantic evidence check yourself.
