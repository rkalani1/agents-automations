# 0003 — No background automations or schedulers by default

- **Status:** Accepted
- **Date:** 2026-05-06
- **Deciders:** maintainers

## Context

Many "agent" tutorials default to running models on a schedule — cron, launchd, GitHub Actions cron, Windows Task Scheduler, hosted "always-on" agents. In practice this:

- runs up real costs silently,
- runs unreviewed tool calls against the user's accounts,
- and creates a long tail of dormant credentials and orphaned processes.

## Decision

This guide:

- documents schedulers as **manual-only examples** that the reader has to deliberately enable,
- never includes a working scheduled job in any starter template,
- and explicitly warns when an example, if scheduled, would touch external services.

## Consequences

- **Pros**
  - Lower blast radius when readers copy/paste examples.
  - Aligns with the safety baseline (HITL by default).
  - Easier to teach evals and red-teaming before automation.
- **Cons**
  - Some legitimate use cases (recurring digests, monitoring) need extra effort to wire up.
  - This guide is *not* a how-to for "always-on" agents. Other guides cover that.

## Alternatives considered

- **Provide cron examples by default with strong warnings** — warnings get ignored. Defaults matter more than disclaimers.
- **Provide a hosted scheduler** — out of scope; this is a documentation site.
