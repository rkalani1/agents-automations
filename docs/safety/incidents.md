# Incident response for agent operators

> **Last verified:** 2026-05-06 · **Drift risk:** low

An incident is any event in which an agent behaved in a way that was unintended, harmful, or outside its defined scope — or any event in which you cannot rule out that this occurred. Incidents range from minor (wrong tool called, no external effect) to severe (data exfiltrated, financial transaction executed incorrectly, harmful content sent to a user).

Having a response plan before an incident occurs makes the difference between a contained, recoverable event and a chaotic one. This page walks through the five phases: detect, contain, investigate, remediate, and communicate.

---

## Phase 1: Detect

You cannot respond to an incident you do not know about. Detection depends on having instrumentation in place before the incident occurs.

**Logs.** Every tool call, agent reasoning step, and final output should be logged with timestamps, user identifiers, and full argument and response payloads. Logs are your primary forensic resource.

**Evals in production.** Running a subset of your eval set against production traffic (shadow scoring) can surface behavioral drift before users notice. A sudden drop in eval pass rate is an early warning signal.

**User reports.** Build a lightweight feedback mechanism — even a simple "this response was wrong" button — and make sure it routes to someone who reads it. Users often detect problems before automated systems do.

**Alerts.** Set threshold-based alerts on:
- Per-session tool call count exceeding a defined maximum.
- Outbound calls to hosts not on the allowlist.
- Error rate from tool calls exceeding a baseline.
- Token or API spend exceeding 2x expected levels.

**Signs that may indicate an incident:**
- A user reports that the agent sent a message, modified a record, or took an action the user did not request.
- Logs show a tool called with arguments that do not correspond to anything in the conversation.
- A tool call fails in a way that suggests the argument was constructed from injected content.
- The agent output contains content that looks like it came from the system prompt.
- Cost anomalies: a session that consumed 10x the typical token budget.

---

## Phase 2: Contain

The priority in containment is to stop the agent from taking further unintended actions. Do this before investigating — understanding what happened is secondary to preventing more harm.

**Kill switch.** Every production agent should have a mechanism to pause or disable it with a single action that does not require a code deployment. This can be a feature flag, a configuration value, or a rate-limit that you set to zero. Document where it is and who can activate it.

**Rotate keys.** If there is any possibility that an API key, OAuth token, or other credential was exposed or misused, rotate it immediately. Do not wait for confirmation. Key rotation is cheap; exposure is not.

**Disable connectors.** If the incident involves a specific tool integration (email, database, external API), disable that connector specifically rather than the entire agent if that is sufficient to stop further harm.

**Preserve logs.** Before taking any other action, confirm that the logs covering the incident time window are preserved and will not be rotated or overwritten. Archive them to a location that cannot be modified.

---

## Phase 3: Investigate

With the agent contained and logs preserved, reconstruct what happened.

**Timeline reconstruction.** Work backward from the observed problem. Identify the exact timestamp of the problematic action, then trace the conversation and tool call sequence that led to it. Most agent incidents have a clear trigger that you can identify in the logs.

Questions to answer:
- What was the user's input that initiated the session?
- What tool calls were made, in what order, with what arguments?
- Did any tool output contain content that could have redirected the agent's behavior (prompt injection)?
- Was the action within the agent's defined scope, or did it require the agent to deviate?
- Was a HITL gate present for this action? If so, what did the user confirm?
- Is this a one-off or does the same pattern appear in other sessions?

**Root cause categories.**

Most agent incidents fall into one of these categories:

- **Prompt failure:** The system prompt did not adequately constrain the behavior, or an edge case was not covered.
- **Tool misconfiguration:** A tool had broader permissions than intended, or argument validation was insufficient.
- **Eval gap:** The failure mode was predictable but no eval case covered it.
- **External attack:** A user or external data source deliberately injected instructions.
- **Model regression:** A model update changed behavior in a way that existing evals did not catch.

---

## Phase 4: Remediate

Remediation has three parts: fixing the immediate cause, preventing recurrence, and validating the fix.

**Fix the cause.** Based on root cause category:
- Prompt failure: revise the system prompt, tighten scope, add explicit constraints.
- Tool misconfiguration: reduce permissions, add server-side validation, restrict allowlists.
- Eval gap: write the eval case before writing the fix (so you can verify the fix works).
- External attack: add prompt injection mitigations, tighten input parsing, add suspicious-content detection.
- Model regression: pin to the previous model version while you assess the impact of the new version.

**Write a regression eval case.** Before deploying any fix, write an eval case that would have caught the incident. Add it to your eval set. Run it against the broken version (it should fail) and against the fixed version (it should pass). This creates a permanent record that the fix works.

**Validate in a staging environment.** Deploy the fix to a non-production environment and run the full eval set, including the new regression case. Do not deploy to production until all evals pass.

---

## Phase 5: Communicate

Who needs to know about the incident, and what do they need to know?

**Internal stakeholders.** The agent owner, the security team, and any product or engineering leads who depend on the agent should receive a brief summary: what happened, what the impact was, what was done to contain it, and what the fix is.

**Affected users.** If a user experienced incorrect agent behavior — especially if an irreversible action was taken on their behalf — notify them directly. Explain what happened in plain language, what the outcome was, and what you are doing to prevent it from happening again. Avoid jargon. Do not minimize the impact.

**Regulators or compliance teams.** If your domain is regulated (healthcare, finance, legal) or if personal data was involved, check your breach notification obligations. When in doubt, involve your legal or compliance team.

**Post-mortem.** Write a post-mortem document that covers: timeline, root cause, impact, what worked in your response, what did not, and what changes are being made. Share it with the team. File it in a place that future team members can access. The goal is not to assign blame but to improve your systems.

Update the [safety checklist](checklists.md) and, if applicable, the agent spec to reflect any new lessons learned.
