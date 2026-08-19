# Changelog

## 2026-08-19: Public validation wording (v1.1.1)

### Changed

- Removed external model-review approval from the public Status and release
  history.
- Kept the measured qualification results, evidence links, Skill package, and
  behavior unchanged.

### Validation

- README and Changelog no longer publish external approval as completion
  evidence.
- The unchanged Agent Skill package passes canonical validation.

## 2026-08-19: Scoville Research v1.1.0

### Added

- Added the versioned Deep v2 package with `run.json`, `evidence.jsonl`, exact
  claim-to-evidence links, Skill-byte drift detection, and read-only legacy-v1
  validation.
- Added bounded external-job records for trust boundary, cost, timeout, job
  identity, polling, disclosed data, upload authorization, and cleanup state.
- Added optional source accessibility, final URL, link status, and content
  quality fields plus claim-level `as_of` dates for time-sensitive claims.
- Added an explicit Research and Brainstorm composition protocol with one
  Research-owned landscape lane and no automatic sibling dependency.
- Added the complete Research-Skill gap-analysis audit with 27 inspected
  sources and 32 claim records.

### Validation

- Agent Skill package and native Scoville Plan validation passed.
- The artifact validator passed 35/35 deterministic tests.
- The exact candidate passed 13/13 open Validation cases and 4/4 one-shot
  sealed holdout cases under Terra 5.6 Medium.
- SkillOpt proposed one change after 49 calls and 2,939,506 tokens; the proposal
  passed only 12/13 Validation cases and was rejected.

## 2026-08-19: Scoville Research v1.0.0

### Added

- Added the first installable `scoville-research` package for current
  multi-source web research, GitHub-first Development research, Academic
  research, and durable Deep investigations.
- Added route-specific evidence contracts, contradiction and gap passes,
  source-independence checks, prompt-injection resistance, private/public data
  separation, and a decision-sufficiency stop.
- Added an interruption-safe Deep artifact package with a standard-library
  structural validator and explicit truth boundary.
- Added a complete source and provenance audit covering platform contracts,
  inspected Agent Skills, empirical research, rejected mechanisms, and
  discovery-only sources.
- Added the frozen evaluation contract, no-Skill control runner, deterministic
  validator tests, and public benchmark evidence.

### Validation

- Agent Skill package validation passed.
- The artifact validator passed 8/8 deterministic tests.
- The exact candidate passed 6/6 Validation cases against 5/6 for the no-Skill
  arm under the same Terra 5.6 Medium boundary.
- SkillOpt rejected its one proposed change after it reduced hard Validation to
  5/6.
- The retained candidate passed 3/3 one-shot sealed holdout cases.
