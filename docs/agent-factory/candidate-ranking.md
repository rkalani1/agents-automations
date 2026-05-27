> **Last verified:** 2026-05-06 · **Drift risk:** low

# Candidate ranking

Before any agent is specced or built, it should earn its place in the queue. The ranking stage evaluates candidates against a five-factor rubric, produces a numerical total, and gives the Sponsor a defensible basis for deciding which agents to fund. This is not a bureaucratic exercise — it is a way to prevent the loudest voice in the room from determining the build order.

## The five-factor rubric

Each factor is scored 1–5. Higher is better for Value, Feasibility, and Platform fit. For Safety and Maintenance burden, a higher score means less risk or less cost — the rubric is calibrated so that the total always favors candidates that are good on all dimensions.

### Factor 1 — Value (1–5)

How much does this agent improve the workflow it targets?

| Score | Anchor |
|---|---|
| 1 | Marginal convenience; the current approach takes minutes and works fine |
| 2 | Saves time but the workflow is low-frequency or low-priority |
| 3 | Saves meaningful time or reduces meaningful error in a regular workflow |
| 4 | Addresses a significant bottleneck or eliminates a high-error manual process |
| 5 | Unlocks a capability the team does not currently have; high strategic value |

### Factor 2 — Feasibility (1–5)

How achievable is this agent given the team's current capabilities and data access?

| Score | Anchor |
|---|---|
| 1 | Requires data or API access that does not exist or is unlikely to be granted |
| 2 | Requires significant infrastructure work before the agent can be built |
| 3 | Buildable with moderate effort; some dependencies need to be confirmed |
| 4 | Straightforward build; all dependencies are available |
| 5 | Near-trivial build; a recipe or template already exists for this agent type |

### Factor 3 — Safety (1–5)

How low is the potential for harm if the agent fails or is misused?

| Score | Anchor |
|---|---|
| 1 | High harm potential; write access to sensitive external systems or data |
| 2 | Moderate harm potential; outputs acted on with limited human review |
| 3 | Low-moderate harm; outputs reviewed before any action is taken |
| 4 | Low harm; easily caught and corrected; no external systems affected |
| 5 | Minimal harm; purely informational, no write access, output is advisory |

### Factor 4 — Maintenance burden (1–5)

How low is the expected ongoing cost to keep this agent working?

| Score | Anchor |
|---|---|
| 1 | Very high; relies on volatile APIs, a brittle prompt, and a single owner |
| 2 | High; one or two significant dependencies likely to change within a year |
| 3 | Moderate; standard maintenance cadence adequate |
| 4 | Low; stable dependencies, robust prompt, easy to test |
| 5 | Minimal; depends only on stable internal data; prompt is format-simple |

### Factor 5 — Platform fit (1–5)

How well does this agent match the capabilities of the platforms your team already uses?

| Score | Anchor |
|---|---|
| 1 | Requires a platform the team does not use and would need to procure |
| 2 | Requires significant adaptation to work on available platforms |
| 3 | Works on available platforms with some adaptation |
| 4 | Natural fit for one or more platforms already in use |
| 5 | Ideal fit; a built-in tool or integration on a platform already deployed |

## Worked ranking of five candidates

The five candidates below are drawn from a synthetic research-workflow context. Scores reflect plausible assessments; actual scores should be assigned by the Rank stage team with access to the intake forms.

| Candidate | Value | Feasibility | Safety | Maint. burden | Platform fit | Total |
|---|---|---|---|---|---|---|
| Literature triage agent (ranks abstracts from a weekly preprint feed) | 4 | 5 | 5 | 4 | 4 | 22 |
| Meeting scheduler agent (drafts calendar invitations for human approval) | 3 | 4 | 3 | 3 | 4 | 17 |
| Code review agent (comments on pull requests; no merge authority) | 4 | 4 | 4 | 3 | 4 | 19 |
| Email-send agent (sends emails on behalf of the user without per-send review) | 3 | 4 | 1 | 3 | 4 | 15 |
| PDF extraction agent (extracts structured data from uploaded research PDFs) | 4 | 4 | 5 | 3 | 4 | 20 |

**Top candidates by score:** Literature triage (22), PDF extraction (20), Code review (19).

## Reading the results

The email-send agent scores 15 despite moderate value and good feasibility, solely because of its low safety score. An agent that sends emails without per-send human review is Tier 3 by the risk-tiering definition in [Agent portfolio design](agent-portfolio-design.md), and a Safety score of 1 reflects that. The ranking does not forbid building it — a Sponsor who has reviewed the risk can still authorize it — but it makes the risk visible at the decision point.

The meeting scheduler agent scores 17. Its safety score of 3 (rather than 4 or 5) reflects that drafting calendar invitations, while human-reviewed before sending, can cause friction if the agent interprets meeting constraints incorrectly. It is buildable and valuable but not the highest priority given the alternatives.

## Tie-breaking and adjustments

When two candidates have the same total, prefer the one with the higher Safety score. A safe agent that is slightly less valuable is a better investment than a risky agent that is slightly more valuable, because the cost of a safety incident scales nonlinearly with harm severity.

If the Sponsor disagrees with a score, the disagreement should be documented in the ranking record with a rationale, and the final score adjusted. The rubric is a structured input to the decision, not the decision itself.

## Minimum score for proceeding

Candidates with a total below 12 should not proceed to the Spec stage without explicit Sponsor override and documented rationale. Candidates with a Safety score of 1 or 2 require Safety Lead sign-off before proceeding, regardless of total.
