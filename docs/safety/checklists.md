# Safety checklists

> **Last verified:** 2026-05-06 · **Drift risk:** low

Use these checklists at the stages where they appear. They are designed to be actionable: each item is a concrete thing you can verify or do, not a vague principle. Adapt them to your context — add items specific to your domain, remove items that do not apply.

For a copy-paste version suitable for embedding in a PR template or runbook, see the [safety checklist template](../template-library/safety-checklist.md).

---

## Pre-build checklist

Complete this before writing a line of agent code. Its purpose is to surface scope and risk issues while they are still cheap to resolve.

- [ ] Written a one-sentence job statement for the agent (what it does, for whom, in what context).
- [ ] Defined the agent's output types: read-only, advisory, or action-taking?
- [ ] Listed every tool the agent will be allowed to call.
- [ ] For each tool, documented the worst-case side effect if it is called incorrectly.
- [ ] Identified which operations are irreversible (sends messages, modifies records, triggers payments, merges code).
- [ ] Determined whether the agent needs access to personal data (PII, PHI, financial data) and whether that access is necessary for the task.
- [ ] Identified the data retention requirements for agent logs and conversation history.
- [ ] Named an owner who is accountable for the agent's behavior.
- [ ] Confirmed that a human-in-the-loop gate is required for each irreversible operation.
- [ ] Checked whether your use case is covered by your AI provider's acceptable use policy.

---

## Pre-deploy checklist

Complete this before moving any version of the agent into a production or user-facing environment.

### Scope and prompt

- [ ] System prompt includes an explicit description of what the agent will and will not do.
- [ ] System prompt includes explicit refusal behavior: what the agent says when asked to do something outside scope.
- [ ] System prompt names the tools the agent may use (explicit allowlist, not just "use tools as needed").
- [ ] System prompt names any tools the agent may NOT use.
- [ ] Tested that the agent refuses requests outside its defined scope.

### Tool configuration

- [ ] Every tool is configured with least-privilege access (read-only where write is not needed, scoped API keys, no admin credentials).
- [ ] Tool argument validation is in place server-side, not just in the prompt.
- [ ] Outbound URL calls are restricted to an allowlist of trusted hosts.
- [ ] There is a hard cap on the number of tool calls per agent session.

### Evals

- [ ] A golden eval set exists with at least 5 cases covering core tasks.
- [ ] Adversarial eval cases cover prompt injection, jailbreak attempts, and out-of-scope requests.
- [ ] All eval cases pass on the version being deployed.
- [ ] Evals are committed to version control and tagged to match the deployment version.

### Human-in-the-loop

- [ ] Every irreversible action has a HITL confirmation gate in place.
- [ ] The confirmation gate presents the user with a plain-language description of what will happen.
- [ ] A dry-run mode exists for operations that write to external systems.

### Auth and secrets

- [ ] All API keys and secrets are stored in a secrets manager, not in the prompt, code, or environment files committed to version control.
- [ ] API keys are scoped to the minimum required permissions.
- [ ] There is a documented process for rotating keys.
- [ ] The agent cannot read or output its own API keys.

### Logging

- [ ] All tool calls are logged with full argument values and response payloads.
- [ ] Logs are retained for at least 30 days (or longer if your compliance requirements demand it).
- [ ] Logs are stored in a system accessible to the security team, not only to the agent operator.
- [ ] PII in logs is redacted or access-controlled.

---

## Post-deploy checklist

Complete this within the first two weeks of a production deployment, and revisit on a regular cadence (monthly is reasonable for most agents).

- [ ] Evals are running automatically on every deployment (CI/CD integration).
- [ ] Production logs are being reviewed at least weekly for anomalies.
- [ ] A cost alert is configured to fire if token or API call spend exceeds 2x the expected baseline.
- [ ] A user feedback channel exists and is monitored.
- [ ] At least one person (not the original builder) has reviewed the agent's behavior in production.
- [ ] A red-team session has been completed since the last major change to the prompt, tools, or model version.
- [ ] The agent spec is up to date and matches the deployed configuration.
- [ ] Owner contact information is documented and reachable.

---

## Incident checklist

Use this if you suspect or confirm that the agent has behaved in an unintended way. See also [Incident response](incidents.md) for a fuller workflow.

- [ ] Agent has been paused or rate-limited to prevent further harm.
- [ ] All affected tool integrations have been temporarily disabled.
- [ ] Logs covering the incident time window have been preserved (do not rotate or delete).
- [ ] Timeline of events has been reconstructed from logs.
- [ ] Root cause has been identified: prompt failure, tool misconfiguration, eval gap, or external attack?
- [ ] Affected users or systems have been identified.
- [ ] Users affected by erroneous actions have been notified if required.
- [ ] A new eval case has been written to cover the failure mode.
- [ ] A fix has been deployed and validated against the new eval case.
- [ ] A post-mortem document has been written and shared with stakeholders.
- [ ] The safety checklist has been updated to reflect any new lessons.
