# Example: personal study plan

> **Last verified:** 2026-05-06 · **Time:** 10 minutes · **No API key required**

Turn "I want to learn X" into a 1-page weekly plan with study blocks, sources, and self-checks.

## Layer 1 — Chat only `Free`

```
Help me build a 1-week study plan.

Topic: <e.g., causal inference for observational data>
Hours per week: <e.g., 5>
My background: <2 lines>
Goal: <what I want to be able to do at the end>

Output:
- 5 study blocks of 25 minutes each, with topic + source + a 2-question self-check.
- Order from easier to harder.
- One "stretch block" if I have a 6th hour.
- One "skip if tired" block.

Constraints:
- Cite real sources. If unsure, say so.
- Plain markdown.
```

How to tell whether it worked: every block has a real source you can find. The self-checks are non-trivial.

## Layer 2 — Project `Sub`

Build a "Learning coach" Project / Gem with your background, your tools, and how you like to learn (visual, math-first, examples-first).

## Layer 3 — Memory `Sub`

Global memory:

```
- For study plans: 25-minute blocks, easier-to-harder, real cited sources.
- I prefer math-first explanations with one concrete example.
- Background: epidemiology, comfortable with R; learning Mendelian randomization.
```

## Layer 4 — Scheduled action `Sub`

Sunday 17:00 local: "Draft next week's study plan based on my saved goals." Manual fallback: Sunday calendar reminder.

See [No-code automations — Weekly learning plan](../no-code-automations/index.md#example-3-weekly-learning-plan-sub).

## Layer 5 — Custom assistant `Sub`

Custom GPT / Gem / Skill named "Study coach":

- **Knowledge files**: textbook table of contents, a list of trusted authors, a sample completed week.
- **Sample prompts**: 3 different topics the coach handled well.

## Layer 6 — Developer / API (optional)

A daily script that reminds you of the next block + asks for a self-check answer. Drafts only; never auto-grade. See [Agent Factory](../agent-factory/index.md).

## Make it reusable

- Save the Project. Each Sunday, paste a 1-line "this week's emphasis."
- Keep a "what I learned" log; paste it back for next week's plan.

## Make it robust

- **Eval**: try the plan for 2 weeks; rate each block 1–5 for usefulness.
- **Red-team**: ask the coach to recommend a source from a journal you don't trust. It should refuse or flag.
- **Drift check**: monthly, ask: "Given what I've actually completed, what plan would you draft now?"

## What good output looks like

- Real, findable sources.
- Self-checks you can't pass without doing the reading.
- Honest about prerequisites.

## If your plan doesn't have this feature

- No Project → paste prompt + background each Sunday.
- No Memory → keep your background in a notes file; paste once per session.
- No native task → Sunday calendar reminder.

## See also

- [Mastery — ChatGPT](../mastery/chatgpt.md), [Claude](../mastery/claude.md)
- [Memory and preferences](../preferences-memory/index.md)
- [No-code automations](../no-code-automations/index.md)
