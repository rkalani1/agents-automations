# Templates

> **Last verified:** 2026-05-06 · **Drift risk:** low

This section contains reusable templates for the most common artifacts you will need to build, document, and operate an AI agent. Each template is designed to be copied and adapted — remove sections that do not apply, add sections specific to your domain.

## Available templates

| Template | Description |
|---|---|
| [Agent spec](agent-spec.md) | A structured specification document that defines an agent's job, inputs, outputs, tools, stop conditions, error handling, HITL gates, and ownership. Use this before building. |
| [Prompt template](prompt.md) | A structured system prompt with sections for role, constraints, tool allowlist, output format, examples, refusal behavior, and safety reminders. Includes a filled example for a clinical-evidence summarizer. |
| [Eval rubric](eval-rubric.md) | A scoring rubric for evaluating agent outputs against a 1-5 scale across six criteria: task completion, tool usage correctness, output format compliance, citation faithfulness, safety compliance, and cost. |
| [Safety checklist](safety-checklist.md) | A 25-40 item copy-paste task list covering all major risk areas: scope, tools, data, auth, HITL, logging, evals, operations, and people. |
| [Agent PRD](agent-prd.md) | A product requirements document template for an agent: problem statement, users, success metrics, scope, non-goals, UX flow, tools, risks, eval plan, rollout plan, and open questions. |

## How to use these templates

Copy the raw Markdown for the template you need into a new file in your project. Fill in the sections relevant to your agent. Delete placeholder text and sections that are not applicable — a shorter, accurate document is more useful than a complete but inaccurate one.

Templates are versioned alongside this guide. If you use a template as the basis for a living document, note the version of the template you started from so you can incorporate updates when the template changes.

These templates are intentionally format-agnostic: the content and structure matter more than the specific tool you use to store or render them.
