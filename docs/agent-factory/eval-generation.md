> **Last verified:** 2026-05-06 · **Drift risk:** low

# Eval generation

An eval suite is a set of test cases with known correct answers. Running the agent against the suite before launch tells you how well the prompt pack implements the spec. Running it again after any change tells you whether you introduced a regression. Without evals, agent quality is a matter of subjective impression; with evals, it is a measurable, improvable property.

This page covers how to generate 20 golden cases for a new agent. For ready-to-use eval cases organized by agent category, see [Evals](../evals/index.md).

## What makes a good golden case

A golden case has four parts:

- Input: the exact data the agent receives.
- Expected output: what a correct response looks like, specified precisely enough to be checkable automatically or by a reviewer without ambiguity.
- Pass criteria: a machine-checkable rule (schema validation, exact string match, regex, semantic similarity score above a threshold) or an explicit rubric for human judgment.
- Case label: a short identifier and a description of what aspect of behavior this case exercises.

A common mistake is writing expected outputs that are too specific (the case fails if the agent uses slightly different wording, even when the meaning is identical) or too vague (any response passes because the criteria are underspecified). The right level of precision depends on the output format: for JSON outputs, schema validation plus key-value checks are appropriate; for free-text outputs, a rubric with 3–5 criteria scored pass/fail is better than exact-match.

## The 20-case structure

Twenty golden cases is the minimum for a new agent. The cases should be distributed across the following categories:

| Category | Minimum cases | Purpose |
|---|---|---|
| Typical inputs | 8 | Confirm the agent works on the most common cases |
| Boundary inputs | 4 | Confirm the agent handles edge values (empty input, maximum length, minimum length) |
| Stop-condition triggers | 4 | Confirm the agent stops correctly when a stop condition is met |
| Format compliance | 4 | Confirm the output consistently matches the required schema or structure |

For agents with multiple output types, the format compliance cases should cover each type.

## Seeding from workflow logs

The highest-fidelity golden cases come from real workflow logs: records of the inputs the agent will actually receive and, if available, records of how a human expert handled those inputs. Using real inputs ensures the cases reflect the true distribution, not an idealized version of it.

When seeding from real logs, the process is:

1. Export a sample of logs from the relevant workflow. For a literature triage agent, this might be a log of abstracts that have been manually reviewed and labeled over the past three months.
2. Scrub PII and any other sensitive data. This step is mandatory before logs enter any agent development artifact. A simple approach: replace names with synthetic names, replace email addresses and identifiers with placeholders, and remove any free-text fields that might contain personal information. The scrubbed data should be reviewed by a second person before use.
3. Identify cases that represent each of the four categories above. Real logs will naturally contain typical and boundary inputs; stop-condition and format cases may need to be synthesized.
4. For each selected log entry, write the expected output based on how the human expert actually handled it — not based on how you think the agent should handle it. Human expert behavior is the ground truth.

Not all workflows have usable logs. A new process with no history, or a process whose records are too sensitive to use even after scrubbing, requires synthetic cases instead.

## Synthesizing cases without logs

When logs are not available, synthesize cases systematically rather than intuitively. Systematic synthesis means: enumerate the input dimensions (e.g., for literature triage: topic relevance, abstract length, abstract quality, language), choose representative values for each dimension, and generate cases by combining the values. This produces cases that cover the space of inputs rather than reflecting the builder's implicit assumptions about what matters.

For stop-condition cases, take each stop condition from the spec and write at least one input that should trigger it. If the spec has three stop conditions, the suite should have at least three stop-condition cases, one per condition.

For format compliance cases, take the output schema and write cases that test each required field, at least one case where the field is at maximum length, and at least one case where it would be easy for the agent to omit a required field.

## Recording cases and running the suite

Each case should be stored in a structured format (JSON or YAML) alongside the prompt pack version it was written against. A case that passes against prompt pack v1.0 but fails against v1.1 is a regression, and the structure of the record should make it possible to identify which change caused the failure.

The eval report submitted at the Launch gate should include:

- Total cases run.
- Number and percentage passing.
- Pass rate for each category.
- List of failing cases with brief failure analysis.
- Reviewer signature.

For the launch thresholds (minimum overall pass rate, minimum critical-case pass rate), see [Launch readiness](launch-readiness.md).

## Keeping evals fresh

Golden cases become stale when the domain changes — for example, when the papers being triaged shift to a new subfield, or when the team's output schema is updated. As part of the quarterly maintenance review, the owner and builder should:

- Check whether any cases have inputs that no longer represent the current distribution.
- Check whether any expected outputs need updating because the team's standards have changed.
- Add at least one new case per quarter if the workflow has produced interesting edge cases since the last review.

An eval suite that is never updated is a suite that gradually stops measuring what matters. Treat it as a living document, not a one-time artifact.
