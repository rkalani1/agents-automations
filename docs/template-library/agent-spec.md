# Agent spec template

> **Last verified:** 2026-05-06 · **Drift risk:** low

An agent spec is a concise, authoritative document that describes what an agent does, how it should behave, what it is allowed to do, and who is responsible for it. Write it before building. Update it whenever the agent's behavior, tools, or ownership changes.

---

## Template

### Job statement

One sentence. Start with a verb. Describes what the agent does, for whom, in what context.

> [Agent name] [does what] for [whom] by [means / using what].

---

### Inputs

What the agent receives at the start of a session. Include data type, source, and whether it is required or optional.

| Input | Type | Source | Required? | Notes |
|---|---|---|---|---|
| | | | | |

---

### Outputs

What the agent produces. Include format, destination, and whether the output is advisory (shown to a human) or action-taking (triggers a downstream effect).

| Output | Format | Destination | Type (advisory/action) | Notes |
|---|---|---|---|---|
| | | | | |

---

### Tools

List every tool the agent is allowed to call. For each tool, provide the least-privilege rationale: why does the agent need this tool, and what is the minimum permission level required?

| Tool name | Permission level | Least-privilege rationale | Worst-case side effect |
|---|---|---|---|
| | | | |

Tools NOT on this list must not be called. This is an explicit allowlist.

---

### Stop conditions

The agent must stop when any of the following is true:

- [ ] [Condition 1 — e.g., the task has been completed and a result returned]
- [ ] [Condition 2 — e.g., the maximum step count has been reached]
- [ ] [Condition 3 — e.g., a required input is missing and cannot be retrieved]
- [ ] [Condition 4 — e.g., a tool returns an error that cannot be recovered from]

---

### Error handling

| Error type | Expected behavior |
|---|---|
| Tool call fails with a retryable error | Retry up to [N] times with [backoff strategy], then surface error to user |
| Tool call fails with a non-retryable error | Stop and return a plain-language explanation to the user |
| Required input is missing | Ask the user for the missing input before proceeding |
| Model produces output that fails format validation | Retry once, then return raw output with a warning |
| Step budget is exhausted | Stop, return partial results with a note that the task was incomplete |

---

### HITL gates

List every point at which the agent must pause and wait for human confirmation before proceeding.

| Trigger | Gate type | Confirmation prompt |
|---|---|---|
| [e.g., About to send an email] | Approve-before-act | [Full text of what the agent shows the user] |
| [e.g., About to update more than 10 records] | Dry-run + approve | [Full text] |

If no HITL gates are needed (read-only, advisory-only agents), state that explicitly.

---

### Eval set reference

| Eval set file | Version | # Cases | Last run |
|---|---|---|---|
| | | | |

Link to the eval set in version control.

---

### Owner

| Role | Name | Contact |
|---|---|---|
| Primary owner | | |
| On-call contact | | |
| Escalation contact | | |

---

### Review cadence

- Scheduled review: [monthly / quarterly / on major change]
- Last reviewed: [date]
- Next review due: [date]

---

## Filled example: Literature triage agent

### Job statement

The literature triage agent retrieves, scores, and summarizes clinical research papers for systematic review coordinators working in a medical research context.

---

### Inputs

| Input | Type | Source | Required? | Notes |
|---|---|---|---|---|
| Search query | String | User prompt | Yes | PICO-format queries supported |
| Date range | ISO date pair | User prompt | No | Defaults to last 5 years |
| Max results | Integer | User prompt | No | Defaults to 20, max 100 |

---

### Outputs

| Output | Format | Destination | Type | Notes |
|---|---|---|---|---|
| Ranked paper list | Markdown table | User display | Advisory | Title, year, DOI, relevance score |
| Per-paper summary | Markdown paragraphs | User display | Advisory | Background, methods, findings |
| Exclusion log | Plain text | User display | Advisory | Papers fetched but excluded, with reason |

---

### Tools

| Tool name | Permission level | Least-privilege rationale | Worst-case side effect |
|---|---|---|---|
| `pubmed_search` | Read | Retrieve paper metadata by query | None (read-only API) |
| `fetch_abstract` | Read | Retrieve abstract text by DOI | None (read-only API) |
| `score_relevance` | Internal | Score paper against PICO criteria | None (internal computation) |
| `summarize_text` | Internal | Generate structured summary | None (internal computation) |

Tools NOT on this list: `send_email`, `write_file`, `fetch_url` (arbitrary), `database_write`.

---

### Stop conditions

- [ ] All papers have been scored and summaries generated for the top N results.
- [ ] The step budget of 50 tool calls has been reached.
- [ ] The PubMed API returns an error that cannot be retried.
- [ ] No papers are returned for the query (agent returns a no-results message).

---

### Error handling

| Error type | Expected behavior |
|---|---|
| PubMed rate limit | Wait 2 seconds and retry up to 3 times, then inform the user |
| DOI not found | Log exclusion with reason "abstract unavailable", continue |
| Relevance score below threshold | Include in exclusion log, do not surface in main results |
| Step budget exhausted | Return results gathered so far with a note on how many papers were not processed |

---

### HITL gates

This agent is read-only and advisory. No HITL gates are required. All outputs are presented to the user for review before any downstream action is taken.

---

### Eval set reference

| Eval set file | Version | # Cases | Last run |
|---|---|---|---|
| `evals/lit-triage-golden-v2.jsonl` | v2 | 18 | 2026-05-01 |
| `evals/lit-triage-adversarial-v1.jsonl` | v1 | 6 | 2026-05-01 |

---

### Owner

| Role | Name | Contact |
|---|---|---|
| Primary owner | Research Eng team | research-eng@example.com |
| On-call contact | On-call rotation | PagerDuty: research-agents |
| Escalation contact | Head of Research Eng | Slack: #research-escalation |

---

### Review cadence

- Scheduled review: monthly
- Last reviewed: 2026-05-01
- Next review due: 2026-06-01
