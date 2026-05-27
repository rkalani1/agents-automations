# Tasks where agents shine

> **Last verified:** 2026-05-06 · **Drift risk:** low

Not every task benefits from an agent loop. This page lists the categories where the overhead of tool-calling and multi-step reasoning pays off, and explains why each one works.

## The pattern to look for

A task is a good candidate when it has three properties:

1. It requires information or actions that are not in the initial prompt (needs tools).
2. The next step depends on the result of the previous step (needs a loop).
3. You can describe what "done" looks like before you start (has a stop condition).

If any of these is missing, reconsider. See [When not to use an agent](when-not-to-use.md).

---

## Research synthesis across many sources

**Example:** "Read the 20 most-cited papers on X, extract findings, and produce a structured comparison table."

**Why it works:** Each source retrieval is a tool call. The model can decide which sources to read next based on what it has already found, filter out irrelevant material, and accumulate structured output over many turns. A single prompt cannot do this because the sources don't fit in one context window and the selection logic depends on what you find.

---

## Structured data extraction from unstructured documents

**Example:** Extracting drug dosage, indication, and adverse events from 500 clinical trial PDFs into a normalized schema.

**Why it works:** The loop handles document-by-document processing. The output schema is the stop condition. The model handles variation in format that a regex cannot. This works well when you have clear acceptance criteria for the schema (e.g., null vs. missing vs. not reported are distinct values).

!!! note
    For regulated data, make sure extraction outputs are reviewed before downstream use. See [Safety baseline](safety-baseline.md).

---

## Repetitive multi-step workflows with clear acceptance criteria

**Example:** For each of 200 GitHub issues, classify it by type, assign a severity, draft a one-sentence triage note, and post a label.

**Why it works:** The task is identical per item, the acceptance criteria are enumerable (valid label set, triage note under 100 characters), and errors are catchable at the item level. The agent loop maps naturally to a per-item iteration with a validation step after each action.

---

## Code refactors with a test suite

**Example:** "Migrate all uses of the deprecated `requests` library to `httpx`, keeping the test suite green."

**Why it works:** The test suite is the stop condition. The agent can run tests after each change, observe failures, and adjust. [Claude Code](https://code.claude.com/docs/en/setup) and [GitHub Copilot's coding agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) are built around exactly this pattern: code, test, observe, iterate. Without runnable tests, this becomes much harder to trust.

!!! tip
    The tighter your test coverage, the safer the refactor. An agent without tests is guessing.

---

## Browser-driven data collection from sites with no API

**Example:** Logging into an internal portal, navigating to a report, downloading it as CSV, and parsing the result.

**Why it works:** Browser control tools (see [Anthropic computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) and [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use)) let the model handle dynamic pages, login flows, and navigation that simple HTTP requests cannot. The task has clear success criteria (did we get the CSV? does it have the expected columns?) and the steps are repeatable.

!!! warning
    Browser automation against sites you do not own may violate terms of service. Check before building.

---

## Multi-source document drafting

**Example:** "Pull the latest quarterly earnings from three internal databases, compare against analyst estimates, and draft the executive summary section."

**Why it works:** The model needs to fetch heterogeneous data, reconcile formats, and apply judgment about what is material. These are sequential steps where each result informs the next. The draft is reviewable before it goes anywhere, making HITL natural.

---

## What these tasks have in common

| Property | Why it matters |
|----------|---------------|
| Enumerable subtasks | The agent can track progress and detect when it is stuck |
| External data or actions | Justifies the tool-calling overhead |
| Verifiable output | Gives you a stop condition and a way to catch errors |
| Acceptable latency (seconds to minutes) | Loops take time; real-time UX is a different problem |

If your task fits this table, proceed. If not, read [When not to use an agent](when-not-to-use.md) next.
