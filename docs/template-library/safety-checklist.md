# Safety checklist template

> **Last verified:** 2026-05-06 · **Drift risk:** low

Copy this checklist into your project (a PR description, a Notion page, a runbook, or a wiki). Check off items as you complete them. Add domain-specific items at the end of each section. Remove items that genuinely do not apply — but be deliberate about removals and note why.

For the checklist organized by deployment phase (pre-build, pre-deploy, post-deploy, incident), see [Safety checklists](../safety/checklists.md).

---

## Scope

- [ ] Written a one-sentence job statement for the agent.
- [ ] Defined what the agent will NOT do (explicit non-goals).
- [ ] Confirmed the agent's use case is covered by the AI provider's acceptable use policy.
- [ ] Identified the domain (e.g., healthcare, finance, legal) and checked whether domain-specific regulations apply.
- [ ] Named a human owner who is accountable for the agent's behavior.
- [ ] Documented a review cadence (at minimum: on major changes and quarterly).

---

## Tools

- [ ] Listed every tool the agent is allowed to call (explicit allowlist).
- [ ] Listed any tools the agent must NOT call, even if available.
- [ ] For each tool, documented the worst-case side effect if called incorrectly.
- [ ] Confirmed each tool operates with least-privilege permissions (read-only where write is not needed).
- [ ] Tool argument validation is enforced server-side, not only in the prompt.
- [ ] Outbound URL calls are restricted to an allowlist of trusted hosts.
- [ ] A hard cap on tool calls per session is implemented in the agent runtime.
- [ ] Dry-run / preview mode exists for tools that write to external systems.

---

## Data

- [ ] Identified whether the agent handles personal data (PII) or protected health information (PHI).
- [ ] Confirmed that access to personal data is limited to what is strictly necessary for the task.
- [ ] Confirmed that personal data is not stored in agent logs beyond the minimum required retention period.
- [ ] PII and PHI in logs are redacted or access-controlled.
- [ ] Synthetic or de-identified data is used in eval sets and test environments (no real user data in tests).
- [ ] Data retention and deletion policies are documented.

---

## Auth

- [ ] All API keys and secrets are stored in a secrets manager, not in the prompt, source code, or committed environment files.
- [ ] API keys are scoped to the minimum required permissions.
- [ ] A documented process exists for rotating compromised or expired keys.
- [ ] The agent cannot read or output its own API keys or secrets.
- [ ] OAuth tokens are scoped to the minimum required permissions and have expiry enforced.
- [ ] Service accounts used by the agent are separate from human user accounts.

---

## HITL

- [ ] Every irreversible action has a human-in-the-loop confirmation gate.
- [ ] Irreversible actions are explicitly defined and documented (writes to external systems, sending messages, financial transactions, code merges, actions affecting other people).
- [ ] Confirmation prompts present the full content of the proposed action in plain language.
- [ ] A cancel path is at least as easy as the confirm path.
- [ ] HITL gates are logged: what was proposed, what the user decided, and when.
- [ ] The number of HITL gates is kept low enough that users read them (gate fatigue is documented if more than 3 gates exist).

---

## Logging

- [ ] All tool calls are logged with full argument values and response payloads.
- [ ] All agent reasoning steps (if exposed) are logged.
- [ ] Logs are timestamped and include user or session identifiers.
- [ ] Logs are retained for at least 30 days (or longer if compliance requires it).
- [ ] Logs are stored in a system accessible to the security team.
- [ ] A cost alert is configured to fire if token or API call spend exceeds 2x the expected baseline per session.
- [ ] Alerts are configured for outbound calls to hosts not on the allowlist.

---

## Evals

- [ ] A golden eval set with at least 5 hand-crafted cases exists and is committed to version control.
- [ ] Adversarial eval cases cover: prompt injection, jailbreak attempts, out-of-scope requests, and error handling.
- [ ] A held-out test set (separate from the development eval set) exists.
- [ ] Evals run automatically on every deployment (CI/CD integration).
- [ ] All eval cases pass on the version being deployed.
- [ ] A process exists to convert production failures into new eval cases before fixing the bug.
- [ ] Eval results are versioned and historical results are retained for comparison.

---

## Operations

- [ ] A kill switch exists that can pause or disable the agent without a code deployment.
- [ ] A runbook exists for the most likely failure modes.
- [ ] Monitoring covers: error rate, tool call volume, cost per session, and latency.
- [ ] On-call contact information for the agent owner is documented and up to date.
- [ ] A post-deploy review is scheduled within two weeks of the first production deployment.
- [ ] A red-team session has been completed before the first public deployment.

---

## People

- [ ] At least one person outside the original builder has reviewed the agent's behavior.
- [ ] The team knows how to reach the on-call contact for this agent.
- [ ] Users have a way to report problems (feedback button, email address, or support ticket).
- [ ] Users are informed that they are interacting with an AI agent (where required by law or policy).
- [ ] Affected users will be notified if an incident causes incorrect actions on their behalf.
- [ ] A post-mortem process exists and team members know how to initiate it.
