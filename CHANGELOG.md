# Changelog

## v1.1.4 - 2026-09-09

- Respect observable task capacity for optional evidence lanes without assuming
  that interruption or archiving frees a slot.
- Keep status questions inside the active run and report material blockers
  immediately.

## v1.1.2 - 2026-09-05

- Allow explicitly requested research artifacts at the agreed path while
  keeping investigated systems and sources read-only.
- Keep chat-only Deep Research file-free and require authorization before
  migrating legacy artifacts.

## v1.1.0 - 2026-08-19

- Added Deep v2 research records with claim-to-evidence links, source dates,
  drift detection, and read-only validation of legacy v1 records.
- Added bounded external-job records for cost, timeout, identity, polling,
  disclosed data, upload authorization, and cleanup state.
- Added optional source accessibility, final URL, link status, and content
  quality fields.
- Added an explicit Research and Brainstorm composition protocol with one
  Research-owned landscape lane and no automatic dependency.

## v1.0.0 - 2026-08-19

- Added current multi-source web research, GitHub-first development research,
  academic research, and durable Deep investigations.
- Added route-specific evidence contracts, contradiction and gap checks,
  source-independence checks, prompt-injection resistance, and private/public
  data separation.
- Added interruption-safe Deep records with explicit truth boundaries and a
  decision-sufficiency stop.
