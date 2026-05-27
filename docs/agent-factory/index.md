> **Last verified:** 2026-05-06 · **Drift risk:** low

# Agent Factory — section overview

The Agent Factory is a repeatable, human-gated workflow for taking an agent idea all the way from a vague request to a production-ready artifact. It does not automate deployment. Every artifact the factory produces is a candidate: inert until a human owner reviews it, approves it, and deliberately activates it inside a system that is already governed.

The factory exists because agent-building without a shared process produces waste in predictable ways: teams spec the same agent twice, nobody owns maintenance, safety review happens at the last moment (or not at all), and agents drift quietly after launch until something breaks. The factory addresses each of those failure modes with a corresponding stage.

## What the factory is — and is not

The factory is a process, not a platform. It runs on whichever tools your team already uses for documentation, code review, and quality assurance. The only hard requirements are that every candidate passes a minimum eval and red-team threshold before a human approves it, and that every active agent has a named owner who has agreed to a maintenance cadence.

The factory is not an autonomous pipeline that ships agents without review. It is not a registry of live agents. It is not a substitute for your organization's existing change-management or security processes. It adds a structured on-ramp in front of those processes.

## The nine lifecycle stages

| Stage | One-line description |
|---|---|
| Intake | Capture what the requester actually needs and what "failure" means to them |
| Rank | Score candidate agents on value, feasibility, safety, maintenance burden, and platform fit |
| Spec | Write a tight job statement, define inputs/outputs/tools, and establish stop conditions |
| Build | Generate system prompts, n-shot exemplars, refusal prompts, and error-recovery scaffolding |
| Eval | Produce at least 20 golden test cases and run them against the candidate |
| Red-team | Produce at least 20 adversarial cases and confirm the agent handles all critical failures |
| Port | Translate the approved prompt pack to every platform your team needs to support |
| Launch | Verify all gate criteria are met; the owner signs the launch-readiness checklist |
| Maintain | Re-evaluate on a cadence; retire agents that no longer meet the standard |

## Sub-pages in this section

| Page | What it covers |
|---|---|
| [Factory operating model](factory-operating-model.md) | Roles, lifecycle stages, and decision rights in RACI form |
| [Agent portfolio design](agent-portfolio-design.md) | How to manage a collection of agents as a portfolio, including retirement |
| [Requirements intake](requirements-intake.md) | A short intake form with a worked example |
| [Candidate ranking](candidate-ranking.md) | The 5-factor rubric and a worked ranking of 5 examples |
| [Prompt-pack generation](prompt-pack-generation.md) | From a spec to a complete prompt pack, with a worked example |
| [Eval generation](eval-generation.md) | Producing 20 golden cases from a spec or workflow logs |
| [Red-team generation](red-team-generation.md) | Producing 20 adversarial cases and reviewing them with a red-team agent |
| [Cross-platform porting](cross-platform-porting.md) | Translating one agent across Claude, OpenAI, Gemini, and Copilot |
| [Launch readiness](launch-readiness.md) | The gate criteria with concrete numerical thresholds |
| [Maintenance and drift](maintenance-and-drift.md) | Keeping active agents healthy and retiring them when the time comes |
| [Worked example](worked-example.md) | A complete factory run from 25 candidates to 5 launch-ready agents |

## How this section connects to the rest of the guide

The factory stages reference three other sections heavily.

[Recipes](../recipes/index.md) provide ready-made prompt packs for common agent types. When the Build stage produces a prompt pack, the recipes section is the first place to look for a starting point rather than writing from scratch.

[Evals](../evals/index.md) provide ready-to-use golden and adversarial test cases organized by agent category. The Eval and Red-team stages draw directly from those libraries rather than generating every case from scratch.

[Template library](../template-library/index.md) holds the canonical spec template, intake form template, launch-readiness checklist, and maintenance log format. Every factory artifact should start from the template-library version so that outputs are consistent across teams.

## How to use this section

If you are new to the factory, read [Factory operating model](factory-operating-model.md) first to understand who does what at each stage. Then read [Agent portfolio design](agent-portfolio-design.md) to understand why the factory gates matter even for small portfolios. After that, work through the remaining pages in order the first time you run a factory cycle. On subsequent runs, jump directly to the stage you are at.

If you want to see everything working together before you read the individual pages, start with [Worked example](worked-example.md). It covers a full research-workflow portfolio from candidate generation through the approval gate, and references the relevant sub-pages at each step.

## The non-negotiable: human approval before activation

Every output of the factory — prompts, evals, red-team suites, porting tables, launch checklists — is a candidate artifact. No agent produced by this workflow is active until a human owner explicitly approves it and records that approval. This constraint is not a formality. Agents that run without an identified owner have no one accountable for their outputs, no one to call when they regress, and no one to retire them when the underlying platform changes. The factory's value comes entirely from the combination of structured process and deliberate human sign-off.
