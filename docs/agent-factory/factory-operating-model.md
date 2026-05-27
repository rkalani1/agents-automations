> **Last verified:** 2026-05-06 · **Drift risk:** low

# Factory operating model

The factory needs five roles and nine lifecycle stages. This page defines both and maps decision rights with a RACI-style table. The goal is that anyone on the team can answer two questions at any point in a factory run: "Who decides?" and "Who does the work?"

## Roles

**Owner.** The person accountable for the agent after it launches. The owner defines the business need at intake, approves the final spec, and signs the launch-readiness checklist. If the owner leaves the organization or transfers the agent to someone else, that transfer is recorded in the maintenance log and the new owner re-signs the checklist. An agent without a named owner cannot pass the launch gate.

**Builder.** The practitioner who turns a spec into a prompt pack, eval suite, and red-team suite. This is typically an ML engineer, prompt engineer, or AI-capable developer. The builder does not have authority to approve their own work — that separation is deliberate.

**Reviewer.** A second practitioner who reads the spec, the prompt pack, and the eval/red-team results and confirms that the candidate behaves as specified and does not do things it should not. The reviewer role can be shared across factory runs; one reviewer can cover multiple builders as long as the queue does not create a bottleneck.

**Safety Lead.** A person with explicit responsibility for identifying harm, bias, misuse potential, and compliance risk. On small teams this role may be held by the same person as the Reviewer, but the two roles should not be collapsed unless the team has documented why a single person is adequate for the risk tier of the agents in question. The Safety Lead has veto authority at the Red-team stage and at the launch gate.

**Sponsor.** An organizational stakeholder — typically a manager or team lead — who authorizes the resource expenditure for a factory run and is accountable to the broader organization for the portfolio of active agents. The Sponsor does not review technical artifacts in detail but must confirm at the Rank stage that the shortlist is worth building and at the Launch stage that the risk acceptance is appropriate for the organization.

## Lifecycle stages

**Intake.** A structured conversation with the requestor that captures what they want the agent to do, who bears the cost when it fails, what inputs and outputs are expected, and what conditions should cause the agent to stop and hand off to a human. Output: a completed intake form.

**Rank.** Scoring candidates on the five-factor rubric (value, feasibility, safety, maintenance burden, platform fit). Output: a ranked table; the Sponsor approves the shortlist.

**Spec.** Converting the intake form into a formal agent spec with job statement, inputs, outputs, tools, stop conditions, HITL gates, and an owner placeholder. Output: a signed spec.

**Build.** Generating the prompt pack (system prompt, n-shot exemplars, refusal prompts, error-recovery prompts, format-compliance scaffolding). Output: a versioned prompt pack.

**Eval.** Generating at least 20 golden test cases and running them against the candidate. Output: an eval report with pass rate.

**Red-team.** Generating at least 20 adversarial cases across relevant attack classes and confirming all critical failures are handled. Output: a red-team report with pass rate on critical cases.

**Port.** Translating the approved prompt pack to all target platforms. Output: one prompt pack per platform, each with a brief porting note.

**Launch.** Verifying all gate criteria; the owner signs the checklist. Output: a launch record with date, owner signature, threshold results, and cost ceiling.

**Maintain.** Scheduled re-evaluation, drift monitoring, and eventual retirement. Output: quarterly maintenance log entries; a retirement record when applicable.

## Decision rights and RACI table

R = Responsible (does the work), A = Accountable (owns the outcome), C = Consulted (input required), I = Informed (notified).

| Stage | Owner | Builder | Reviewer | Safety Lead | Sponsor |
|---|---|---|---|---|---|
| Intake | A/R | C | I | C | I |
| Rank | C | C | I | C | A/R |
| Spec | A | R | C | C | I |
| Build | I | R | C | I | I |
| Eval | I | R | A | C | I |
| Red-team | I | R | C | A/R | I |
| Port | I | R | A | I | I |
| Launch | A/R | C | C | C | A |
| Maintain | A/R | C | C | C | I |

A few points about this table:

The Owner is Accountable at Intake, Spec, Launch, and Maintain because those are the stages where the agent's real-world behavior is defined and activated. The Owner does not do most of the technical work, but they cannot delegate accountability.

The Safety Lead is Accountable at Red-team. This is the stage where the adversarial case suite is reviewed and where the Safety Lead's veto can send the run back to Build. Red-team results that do not meet the minimum critical pass rate are a hard stop — the agent does not proceed to Port.

The Sponsor is Accountable at Rank and co-Accountable at Launch. At Rank, the Sponsor confirms resource allocation. At Launch, the Sponsor accepts organizational risk. Neither of these can be delegated to the Builder.

The Reviewer is Accountable at Eval and Port. These are quality-assurance checkpoints — not safety checkpoints. The Reviewer confirms that the agent does what the spec says. The Safety Lead confirms that what the agent does is safe.

## Handling exceptions

When a team is small enough that one person must hold multiple roles, the minimum acceptable configuration is:

- Owner and Sponsor may be the same person if the agent is low-stakes and the team is fewer than five people.
- Reviewer and Safety Lead may be the same person if the agent is low-stakes and the team has documented the decision.
- Builder must never be the same person as Reviewer or Safety Lead for the same factory run, regardless of team size.

"Low-stakes" here corresponds to the risk tier defined in [Agent portfolio design](agent-portfolio-design.md). High-stakes agents always require distinct Reviewer and Safety Lead roles.

## Keeping the model lightweight

The operating model is intentionally minimal. It is designed to add just enough structure to prevent the most common failure modes — unowned agents, untested agents, and agents that launch without anyone accepting risk — without creating bureaucratic overhead that causes teams to skip the process. If your team finds that the process is being skipped, the first thing to examine is whether the role assignments are realistic given your team's size and workload, not whether the model should be abandoned.
