> **Last verified:** 2026-05-06 · **Drift risk:** low

# Agent portfolio design

A single agent is a tool. Ten agents are a portfolio. Managing them as a portfolio changes how you think about adding, maintaining, and removing agents — and it surfaces costs and risks that are invisible when you treat each agent in isolation.

## Why portfolio thinking matters

The most common failure mode for teams that build agents without a portfolio view is unbounded growth. Agents are added when requests come in; they are almost never retired. After six months, the team has twenty active agents, four of which are used daily, eight of which are used occasionally, and eight of which nobody touches but nobody wants to delete because "they might be useful." The unused agents still require maintenance attention when their underlying platform changes, still consume review capacity when they need updates, and still carry organizational liability if they produce harmful or inaccurate outputs.

A portfolio view forces two constraints that individual-agent thinking does not: coverage targets (what gaps does the portfolio need to fill?) and concentration limits (how many agents can we sustain well?).

## Concentration versus coverage

Coverage is the extent to which the portfolio addresses the important workflows in your domain. A research team might define coverage across five dimensions: literature discovery, data extraction, synthesis, writing assistance, and code generation. A portfolio that covers all five but does each badly is worse than a portfolio that covers three and does them well.

Concentration is the reverse risk: a portfolio so focused on one workflow that any failure in that area takes down a large share of the team's capacity. If seven of your ten agents all interact with the same external API, a change to that API degrades most of the portfolio at once.

A practical design principle is to cap any single dependency — platform, API, data source — at 40% of the active portfolio. When a new agent proposal would push a dependency above that threshold, the factory Rank stage should flag it explicitly so the Sponsor can make a deliberate choice.

## Risk tiering

Every agent in the portfolio should be assigned a risk tier before it launches. The tier governs the eval and red-team thresholds at the launch gate (see [Launch readiness](launch-readiness.md)) and the frequency of maintenance review.

**Tier 1 — Low stakes.** The agent's outputs are advisory, easily verified by the user, and have no direct effect on external systems. Example: an agent that summarizes papers and returns a ranked reading list. Failure modes are annoying but not harmful.

**Tier 2 — Medium stakes.** The agent's outputs are acted on with moderate human review, or the agent has write access to internal systems with limited blast radius. Example: an agent that drafts calendar invitations for human approval. A failure can cause friction or rework but is recoverable.

**Tier 3 — High stakes.** The agent has write access to external systems, handles sensitive data, or its outputs are likely to be acted on with minimal review. Example: an agent that sends emails on behalf of a user. A failure can cause reputational, financial, or compliance harm.

Tier assignment should be re-evaluated any time the agent's tools, permissions, or typical usage pattern changes. A Tier 1 agent that gets file-write access is no longer Tier 1.

## Maintenance cost as a first-class dimension

When teams evaluate whether to build an agent, they almost always focus on the value it will create. They rarely estimate the ongoing cost to keep it working. The factory's five-factor ranking rubric (see [Candidate ranking](candidate-ranking.md)) includes maintenance burden explicitly to force this consideration at the decision point rather than after the agent is already running.

The main drivers of maintenance cost are:

- Dependency volatility: how often do the external APIs, models, or data sources this agent relies on change their interfaces?
- Prompt brittleness: does the agent's behavior degrade significantly when the underlying model is updated, or is it robust to minor changes?
- Eval decay: do the golden test cases become stale quickly because the domain evolves (e.g., literature in a fast-moving research area)?
- Owner stability: is there a realistic succession path if the current owner leaves?

An agent with high dependency volatility and a single owner who is likely to move on within a year has a high maintenance cost regardless of its value. The factory should surface this before the build decision, not after.

## Keeping the portfolio healthy

A healthy portfolio has roughly these properties:

- Every agent has a named owner who has reviewed it within the last quarter.
- No dependency accounts for more than 40% of the portfolio.
- The ratio of agents under active development to agents in steady-state maintenance is low enough that the Reviewer and Safety Lead are not bottlenecked.
- The retirement rate is nonzero — at least some agents are retired each year as needs change.

Reviewing the portfolio as a whole, rather than agent by agent, should be a regular practice. A quarterly portfolio review meeting with the Sponsor present is the minimum cadence.

## How to retire agents

Retirement is a first-class operation in the factory. It is not the same as disabling an agent. Retirement means:

1. The owner confirms the agent is no longer needed or no longer meeting its standard.
2. Any dependencies the agent held (API credentials, data access, compute allocations) are revoked.
3. The prompt pack and eval suite are archived with the retirement date and reason, so they can be referenced if a similar agent is proposed in the future.
4. The maintenance log is closed with a final entry.

The triggers that should prompt a retirement evaluation are: the underlying platform has deprecated the features the agent relies on; the agent has failed its quarterly eval two consecutive times without a clear remediation path; the owner has left and no successor has accepted ownership; or usage has dropped to near zero for two consecutive quarters.

Retirement is not a failure. A portfolio that never retires agents is one that is not being managed honestly.
