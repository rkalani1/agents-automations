# Agent PRD template

> **Last verified:** 2026-05-06 · **Drift risk:** low

A product requirements document (PRD) for an agent serves a different purpose than an agent spec. The spec describes what the agent does technically; the PRD explains why it should be built, who it serves, how success is measured, and how it will be rolled out. Write the PRD before the spec — it provides the context that makes spec decisions legible.

---

## Template

---

### Problem

Describe the problem this agent solves. Be specific about the pain point, who experiences it, and why it matters now. Avoid describing the solution in this section.

> **Example:** Clinical systematic review coordinators spend 6-10 hours per review manually screening hundreds of abstracts for relevance before shortlisting papers for full-text review. The manual process is slow, introduces inter-rater variability, and scales poorly as research output grows.

---

### Users

Who are the primary users of this agent? Include secondary users and system-level consumers if relevant.

| User type | Description | Volume (if known) |
|---|---|---|
| Primary | | |
| Secondary | | |
| System (API consumer) | | |

---

### Success metrics

How will you know the agent is working? List metrics you will track. Include a baseline (current state) and a target (desired state) for each.

| Metric | Baseline | Target | Measurement method |
|---|---|---|---|
| [e.g., Time to complete abstract screening per review] | | | |
| [e.g., Recall rate on held-out test set] | | | |
| [e.g., User satisfaction (CSAT)] | | | |
| [e.g., False negative rate (relevant papers excluded)] | | | |

Do not list vanity metrics. Every metric should be something you would act on if it missed target.

---

### Scope

What is in scope for the first version of this agent? Be explicit — anything not listed here is out of scope.

- [Feature or capability 1]
- [Feature or capability 2]
- [Feature or capability 3]

---

### Non-goals

What is explicitly out of scope? List things that users might reasonably expect but that you are not building.

- [Non-goal 1 — include a brief rationale]
- [Non-goal 2]
- [Non-goal 3]

---

### UX flow

Describe the user's experience in plain language. How does the user initiate a session? What happens at each step? What does the user see when the agent needs input, hits an error, or requires confirmation?

```
1. User opens [interface / sends message to / calls API endpoint].
2. User provides [input].
3. Agent [does X].
4. [Optional] Agent presents [confirmation / dry-run output] and waits for user input.
5. Agent returns [output].
6. [If error] Agent returns [error message] and [suggests next step].
```

---

### Tools

List the tools the agent will use. For each, note whether it is read-only or action-taking, and the justification for including it.

| Tool | Read/Action | Justification |
|---|---|---|
| | | |

Tools that are action-taking must be justified explicitly. If the same goal can be achieved with a read-only tool, prefer that.

---

### Risks

What could go wrong? For each risk, rate the likelihood (L/M/H) and impact (L/M/H) and describe the mitigation.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [e.g., Agent produces incorrect summaries that users act on without verification] | | | |
| [e.g., Prompt injection from retrieved content] | | | |
| [e.g., Model API outage] | | | |
| [e.g., Cost overrun from runaway tool calls] | | | |

---

### Eval plan

How will you measure the agent's quality before and after deployment?

- Eval set location: [link to version-controlled eval file]
- Eval set size: [N cases at launch]
- Eval criteria: [Reference to rubric, e.g., eval-rubric-v1]
- Automated eval cadence: [On every deployment / daily / weekly]
- Human review cadence: [Weekly spot-check / monthly full review]
- Minimum pass rate to deploy: [e.g., 90% of golden cases, 100% of safety cases]

---

### Rollout plan

How will the agent be deployed? Include stages, gating criteria, and rollback procedure.

| Stage | Audience | Gating criteria | Rollback trigger |
|---|---|---|---|
| Alpha | [Internal team only] | [All evals pass, red-team complete] | [Any safety failure] |
| Beta | [Invited external users] | [Alpha CSAT > X, no P0 incidents] | [Error rate > Y%] |
| GA | [All users] | [Beta metrics meet targets] | [Any P1 incident] |

Rollback procedure: [Describe in 2-3 sentences how to disable the agent quickly and how to notify users.]

---

### Open questions

Questions that are unresolved at the time of writing. Assign each to an owner with a target resolution date.

| Question | Owner | Target date |
|---|---|---|
| | | |

---

## Filled example (abbreviated): Literature triage agent PRD

### Problem

Clinical systematic review coordinators at academic care centers spend 6-10 hours per review manually screening 200-400 abstracts for relevance before any full-text review begins. This is the slowest step in the pipeline, introduces variability between reviewers, and creates a bottleneck when coordinators are managing multiple reviews simultaneously.

### Users

| User type | Description | Volume |
|---|---|---|
| Primary | Systematic review coordinators at academic care centers | ~50 internal users |
| Secondary | Research librarians validating search strategies | ~10 internal users |

### Success metrics

| Metric | Baseline | Target | Measurement method |
|---|---|---|---|
| Abstract screening time per review | 7 hours | < 2 hours | User self-report at task completion |
| Recall rate (relevant papers not excluded) | 95% (human baseline) | >= 95% | Held-out test set with expert labels |
| User satisfaction (CSAT) | N/A (new tool) | >= 4/5 | In-product rating after each session |
| False negative rate | 5% | <= 5% | Held-out test set |

### Scope (v1)

- PubMed abstract retrieval by PICO query and date range.
- Relevance scoring and ranking of retrieved papers.
- Structured per-paper summary (background, methods, findings, limitations, evidence quality).
- Exclusion log with reasons.

### Non-goals (v1)

- Full-text retrieval and analysis (planned for v2 — licensing complexity is out of scope now).
- Integration with systematic review management tools like Covidence (API access not yet provisioned).
- Multi-reviewer consensus tracking (requires a separate workflow layer).

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Agent excludes a relevant paper (false negative) | M | H | Recall rate eval with >= 95% gate; exclusion log is always shown to user for manual review |
| Prompt injection from abstract content | L | M | Delimited tool output, adversarial evals, output-only mode (no action tools) |
| PubMed API rate limits during large reviews | M | M | Retry with backoff, user-visible progress indicator, step budget cap |

### Eval plan

- Eval set: `evals/lit-triage-golden-v2.jsonl` (18 cases) + `evals/lit-triage-adversarial-v1.jsonl` (6 cases)
- Rubric: `eval-rubric-v1`
- Automated eval: runs on every pull request to main
- Minimum to deploy: 100% of safety cases, >= 90% of golden cases

### Rollout plan

| Stage | Audience | Gating criteria | Rollback trigger |
|---|---|---|---|
| Alpha | Research Eng team (5 people) | All evals pass, red-team session complete | Any output with fabricated citations |
| Beta | 10 invited review coordinators | Alpha CSAT >= 4/5, zero P0 incidents | Error rate > 10% or any safety failure |
| GA | All internal coordinators | Beta recall rate >= 95%, CSAT >= 4/5 | Any P1 incident or recall rate drop below 92% |

Rollback: set the `lit-triage-enabled` feature flag to false. Sessions in progress will complete; new sessions will route to the previous manual workflow. Users are notified via in-product banner.

### Open questions

| Question | Owner | Target date |
|---|---|---|
| Will we use GPT-4o or Claude for the summarization step? Run cost/quality comparison. | Research Eng | 2026-05-20 |
| What is the minimum recall rate that coordinators consider acceptable? Survey 5 users. | PM | 2026-05-15 |
