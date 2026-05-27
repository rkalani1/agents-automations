> **Last verified:** 2026-05-06 · **Drift risk:** low

# Maintenance and drift

An agent that passed the launch gate six months ago is not necessarily still passing it today. Models change. APIs change. The team's standards evolve. The domain the agent works in shifts. Any of these changes can degrade agent quality without any code change — a phenomenon called drift. Maintenance is the practice of detecting and correcting drift before it causes problems.

## Why drift happens

Drift has three main sources:

**Model drift.** When the underlying language model is updated, the agent's behavior may change even if the prompt pack is identical. Updates can shift the model's tone, its tendency to refuse certain requests, its sensitivity to formatting instructions, or its accuracy on specific tasks. Most model updates improve average quality but introduce regressions on specific cases.

**Dependency drift.** When an external API, data source, or tool the agent uses changes its interface, the agent may begin failing tool calls, producing incorrectly formatted outputs, or receiving data that does not match its expected input schema. Dependency drift is often abrupt — an API version is deprecated and the agent stops working on a specific date — rather than gradual.

**Specification drift.** The team's expectations change over time. A format that was acceptable a year ago may no longer match the downstream system that consumes the agent's outputs. A scope boundary that was sensible at launch may need to expand or contract. If the spec is not updated to reflect these changes, the eval suite and the agent's behavior will both measure the wrong thing.

## The minimum maintenance cadence

Quarterly review is the floor for all agents. For Tier 3 (high-stakes) agents, the minimum is monthly. "Review" means:

1. Re-run the full eval suite against the current agent and prompt pack.
2. Re-run at least the critical-case subset of the red-team suite.
3. Check all external dependencies for breaking changes since the last review.
4. Review the agent's production logs for error patterns or anomalies.
5. Confirm the owner is still the named owner and the succession plan is current.

If all checks pass, record the review date and findings in the maintenance log. If any check fails, initiate the appropriate remediation.

## When vendor documentation changes

Vendor documentation changes are a specific trigger for unscheduled maintenance. The [Source audit](../source-audit.md) flow documents how to detect and respond to platform documentation changes. The key principle is: when a platform publishes a breaking change or a significant behavioral update, every agent that depends on that platform should be evaluated against the change before the change takes effect, not after.

Specific signals to watch per platform:

- Claude: Anthropic publishes release notes for model updates and API changes. Subscribe to the Anthropic changelog and check the [Claude Code setup documentation](https://code.claude.com/docs/en/setup) for any changes to how project instructions are processed.
- OpenAI Agents SDK: Watch the [GitHub repository](https://github.com/openai/openai-agents-python) for releases and breaking-change notices. The SDK is under active development and breaking changes are documented in the changelog.
- OpenAI structured outputs: Check the [structured outputs documentation](https://platform.openai.com/docs/guides/structured-outputs) when model versions are updated, as schema support and behavior can change between versions.
- Gemini: Monitor the [Gemini function calling documentation](https://ai.google.dev/gemini-api/docs/function-calling) and the Google AI changelog for changes to the function declaration format or response schema behavior.
- GitHub Copilot agent: Watch the [Copilot cloud agent documentation](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) for changes to how `copilot-instructions.md` is processed and what capabilities the agent has access to.

When a documentation change is detected, the process is:

1. Identify all agents in the portfolio that depend on the affected platform.
2. Run the eval suite and the critical red-team cases for each affected agent.
3. If all pass, record the check in the maintenance log and continue.
4. If any fail, escalate to the owner and Safety Lead and initiate a Build-and-re-eval cycle.

## Retirement triggers

The following conditions should prompt a formal retirement evaluation. The evaluation does not automatically result in retirement, but the outcome of the evaluation — continue, remediate, or retire — must be recorded.

**Deprecated platform.** The platform or API the agent depends on has published an end-of-life date. The agent should be evaluated for porting before the deprecation date, not after. An agent that continues to run on a deprecated API is a maintenance liability and a potential security risk.

**Repeated evaluation failure.** The agent fails its quarterly eval (overall pass rate below threshold) two consecutive times without a clear remediation path. "No clear remediation path" means the builder has investigated the failures and cannot identify changes to the prompt pack that would fix them within the maintenance budget. This condition often indicates that the underlying model has changed in a way that is fundamentally incompatible with the current prompt design.

**Owner vacancy.** The named owner has left the organization or transferred away from the relevant team, and no successor has accepted ownership within 60 days. An agent without an owner has no one to authorize changes, accept risk for its outputs, or retire it when the time comes.

**Zero usage.** The agent has received no real user requests in two consecutive quarterly review periods. An unused agent is not harmless — it still consumes maintenance attention and carries organizational liability. If there is a plausible reason for the usage drop (seasonal workflow, temporary team change), the owner can defer retirement with documented justification. Otherwise, retirement is the appropriate action.

## The retirement record

When an agent is retired, the following must be recorded:

- Agent name and version.
- Retirement date.
- Retirement trigger (which condition above applied).
- Final eval results (even if below threshold).
- Disposition of dependencies (credentials revoked, API registrations removed, data access terminated).
- Archive location of the prompt pack and eval suite (for reference if a similar agent is proposed in the future).
- Owner signature on the retirement record.

Retirement records should be stored alongside the launch records in the factory's document archive. They are any organizational memory of what was built, why it was retired, and where the artifacts went. A future factory run proposing a similar agent should begin by reviewing the retirement record of its predecessor.
