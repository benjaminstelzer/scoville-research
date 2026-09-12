# Development

The only installable package is [`scoville-research/`](../scoville-research/). Artifact-validator tests in this directory are not installed with the Skill.

## Validate

Run the deterministic artifact suite from the repository root:

```text
python -B -m unittest discover -s development/tests -v
```

Review the boundary with Scoville Brainstorm. Structural validation does not establish factual correctness, source quality, or citation support in a live research result.

## Retention

Keep current validator tests and this maintenance summary. Create research corpora, claim ledgers, queries, fetched sources, model outputs, audits, and reviews in temporary storage. Retain a concise evaluation summary only when it explains a useful result or
development lesson and a published release links it. Routine checks and
inconclusive miniature runs stay temporary.
