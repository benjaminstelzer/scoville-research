# Development research

Use this route for technology selection, implementation discovery, repository landscapes, API or library comparisons, and questions where GitHub or comparable developer sources carry the evidence.

## Build the evidence lanes

Select only lanes that can change the decision:

1. official specification, documentation, API contract, or standards text;
2. source code and the real owner of the behavior;
3. releases, tags, changelog, compatibility policy, and migration notes;
4. tests, CI, examples, and reproducible benchmarks;
5. issues, pull requests, discussions, and maintainer responses for observed limits;
6. independent benchmarks, papers, incident reports, or practitioner evidence;
7. license, security, data boundary, dependencies, and maintenance state.

GitHub is often the center of this route, not the whole route. Also inspect the canonical package registry, upstream project, specification, GitLab or other forge, official benchmark repository, and linked paper or dataset when they own part of the answer.

## Search GitHub as evidence

Prefer structured access when available: connector or API for repository metadata, `gh search repos` for discovery, `gh search code` for implementations, and direct file or raw-content retrieval for inspection. Use the browser when structured access cannot expose the relevant page or discussion.

Run a funnel:

1. discover a broad candidate set with varied terms;
2. remove obvious mismatches using explicit requirements;
3. inspect the strongest few candidates deeply;
4. search their failure surfaces and independent comparisons;
5. stop when another candidate would not plausibly change the shortlist or recommendation.

Do not treat stars, forks, download counts, a recent commit, or a polished README as quality. Record them only when they answer an explicit adoption or maintenance question.

## Separate claim from behavior

For every serious candidate, distinguish:

- **Claimed:** documentation or maintainers state it.
- **Observed:** source, release, issue, test, or direct execution demonstrates it.
- **Inferred:** several observations imply it, with the inference named.
- **Unknown:** the available material does not establish it.

Check at least one real implementation owner before concluding that a feature exists. Check relevant releases or tags before calling behavior current. An issue proves that somebody reported a problem; it does not prove prevalence, root cause, or current status.

## Compare for the actual integration

Use the user's constraints as the matrix, not a generic feature contest. Useful dimensions may include:

- architectural fit and extension surface;
- supported runtime, language, operating system, and deployment model;
- migration and rollback cost;
- maintenance and compatibility promises;
- data, privacy, and security boundaries;
- operational failure behavior;
- license and dependency implications;
- evidence quality behind performance or reliability claims.

When the best remaining uncertainty is practical, recommend the smallest feasibility test with its input, observable result, and failure meaning. Run it only when implementation or experimentation is separately authorized.

## Report

Return the current landscape, the shortlist or working conclusion, the evidence that separates candidates, integration consequences, attractive traps, unresolved facts, and the cheapest decision-changing test. Link to exact docs, files, releases, issues, pull requests, papers, or benchmark artifacts rather than repository homepages when the narrower source carries the claim.
