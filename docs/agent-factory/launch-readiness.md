> **Last verified:** 2026-05-06 · **Drift risk:** low

# Launch readiness

No agent produced by the factory is active until it passes the launch gate. The gate is a set of verifiable criteria that must all be satisfied before the owner signs the launch-readiness checklist. This page defines the criteria, the numerical thresholds, and the checklist format.

## What the gate is checking

The gate checks five things: eval quality, red-team quality, owner accountability, operational controls, and maintenance commitment. An agent can be technically excellent but still fail the gate because no one has agreed to own it, or because no kill-switch exists. All five areas must pass.

## Area 1 — Eval quality

The agent must pass its golden eval suite above the threshold for its risk tier.

| Risk tier | Overall pass rate | Critical-case pass rate |
|---|---|---|
| Tier 1 (low stakes) | 80% | 100% |
| Tier 2 (medium stakes) | 90% | 100% |
| Tier 3 (high stakes) | 95% | 100% |

The critical-case pass rate is always 100% regardless of tier. A critical case is a golden test case labeled as such during eval generation — typically one that covers a hard constraint or a stop condition. An agent that fails any critical case has a known behavior gap in a situation where the spec says behavior must be correct. That is not acceptable at any risk tier.

The overall pass rate reflects the agent's general reliability. A Tier 1 agent is advisory and its outputs are easily checked by the user; an 80% pass rate means 1 in 5 typical cases may not meet the standard, which is acceptable when the cost of a wrong answer is low and the output is reviewed. A Tier 3 agent has write access to external systems or handles sensitive data; a 95% pass rate still means 1 in 20 cases may fail, which is why Tier 3 agents require closer human review even after launch.

## Area 2 — Red-team quality

| Risk tier | Overall adversarial pass rate | Critical-case pass rate |
|---|---|---|
| Tier 1 | 80% | 100% |
| Tier 2 | 90% | 100% |
| Tier 3 | 95% | 100% |

The same tier structure applies. Critical adversarial cases — those covering hard constraints like "never send an email without per-send approval" or "never reproduce the full text of a confidential document" — must pass at 100%.

For Tier 3 agents, the Safety Lead must personally review all failing non-critical adversarial cases and document why they are being accepted rather than remediated. Blanket acceptance is not permitted; each case requires a specific rationale.

## Area 3 — Owner accountability

The following must be confirmed and recorded:

- A named owner is identified and has agreed to the owner responsibilities defined in [Factory operating model](factory-operating-model.md).
- The owner has reviewed the prompt pack and the eval and red-team reports.
- The owner has signed the launch checklist (physically or via an auditable digital record).
- A succession plan is documented: if the owner leaves, who is the first person to contact?

An agent without a named owner who has personally signed off cannot pass the gate, regardless of eval and red-team scores.

## Area 4 — Operational controls

Three controls must be verified before launch:

**Kill switch.** A mechanism must exist to disable the agent without deploying a code change — for example, a feature flag, an environment variable, or an admin toggle in the platform. The kill switch must be tested: the gate cannot be passed on the assumption that the switch works. The test record (who tested it, when, and what the result was) must be in the launch record.

**Cost ceiling.** If the agent makes API calls or consumes compute in proportion to usage, a cost ceiling must be defined and enforced. The ceiling does not need to be tight, but it must exist. An agent with no cost ceiling can produce unbounded spend if it enters a loop or receives unexpectedly high traffic. The ceiling should be set at a level that would trigger investigation before causing material harm.

**Error logging.** The agent's outputs and any errors must be logged in a form that the owner can review. "Logged" means stored in a retrievable system with at least 30 days of retention, not merely printed to a terminal. The logging configuration must be confirmed as working before launch.

## Area 5 — Maintenance commitment

The owner must confirm:

- The maintenance cadence agreed upon (quarterly minimum for all tiers; monthly for Tier 3).
- The eval and red-team suites will be re-run at each scheduled review.
- Any dependency that changes between reviews will trigger an unscheduled re-run of the relevant test cases.
- Retirement criteria are understood: if the agent fails two consecutive quarterly reviews without a clear remediation path, it will be retired.

## The launch-readiness checklist

The following checklist is the canonical format for the launch record. All items must be marked complete and the Owner signature line must be filled in.

```
Launch-readiness checklist
Agent name:
Version (prompt pack):
Date:
Risk tier:

Eval quality
[ ] Overall pass rate: ___% (threshold: ___%)
[ ] Critical-case pass rate: 100%
[ ] Reviewer signature:

Red-team quality
[ ] Overall adversarial pass rate: ___% (threshold: ___%)
[ ] Critical adversarial pass rate: 100%
[ ] Safety Lead signature:

Owner accountability
[ ] Named owner:
[ ] Succession contact:
[ ] Owner has reviewed prompt pack, eval report, and red-team report

Operational controls
[ ] Kill switch tested (date, tester):
[ ] Cost ceiling defined (amount, enforcement mechanism):
[ ] Error logging confirmed (system, retention period):

Maintenance commitment
[ ] Scheduled review cadence:
[ ] Owner acknowledges retirement criteria

Owner signature:
Date:
```

## What happens when a gate item fails

If any item fails, the agent returns to the appropriate stage:

- Eval failure → return to Build (revise prompt pack) or Eval (investigate and fix failing cases).
- Red-team failure → return to Build (address the adversarial gaps) or Red-team (add remediation and re-run).
- Owner accountability failure → the factory run is paused until an owner is confirmed.
- Operational control failure → the engineering work to implement the missing control must be completed and re-verified.
- Maintenance commitment failure → the Sponsor must address the resource or staffing gap before the agent can launch.

A failed gate is not a failure of the factory process. It is the process working correctly.
