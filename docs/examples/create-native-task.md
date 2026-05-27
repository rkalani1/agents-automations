# Example: create a native scheduled task

> **Last verified:** 2026-05-06 · **Time:** 15 minutes · **No API key required**

Take a workflow you already run by hand and let your AI run it for you on a schedule — without code.

> **Read this first:** [No-code automation guide](../no-code-automations/index.md). Native scheduled tasks have failure modes (silent stops, runaway costs, drifted connectors). Always do three clean manual runs before scheduling. Always know where the off-switch is.

## Layer 1 — Chat only (the design pass) `Free`

Pick a workflow you already do at least weekly. Open chat:

```
Help me convert this manual workflow into a self-contained prompt I can schedule.

What I do today: <one paragraph>
What triggers me to do it: <a calendar nudge, an email arriving, a deadline>
What "done" looks like: <one or two sentences>

Output: a single self-contained prompt I can schedule. The prompt must:
- Reference today's date as {{TODAY}}.
- State the inputs explicitly.
- State the output format explicitly.
- Be drafts-only; never send / push / pay / delete.
- Refuse to act outside its stated scope; flag uncertainty per <my preference>.
- Include a short "if anything is missing, say what was missing and stop" clause.
```

This produces the prompt body. Run it manually 3 times before scheduling.

## Layer 2 — Project / workspace `Sub`

Move the prompt into a Project / Gem / Space. Run it manually from inside the Project for the 3-run drill.

## Layer 3 — Memory `Sub`

Memory updates relevant to all scheduled tasks:

```
- All scheduled tasks are drafts-only by default. Never send, push, pay, or delete.
- For all scheduled tasks: if a connector is missing or stale, flag it; do not improvise.
```

## Layer 4 — Native scheduled action `Sub` (where rolled out)

Per product:

- **ChatGPT Tasks**: with the prompt in a chat, click "Make this a Task" / clock affordance. Set the cadence + timezone. Run on demand once.
- **Gemini scheduled actions**: Settings & help → Scheduled actions → New → cadence + timezone.
- **Claude Cowork**: from the Project, schedule a recurring run.

Off-switches:

- ChatGPT: profile menu → Tasks → pause / delete.
- Gemini: Settings & help → Scheduled actions → toggle.
- Claude: Cowork pane lists active tasks.

Cost cap reminder: tokens used by scheduled tasks count against your monthly cap. Set the lowest cadence that meets the need.

## Layer 5 — Custom assistant + native task `Sub`

The assistant + the schedule together. Convert the prompt into a Custom GPT / Gem first; then schedule the assistant. This gives you an audit trail (the chat thread inside the assistant) and a reusable shape.

## Layer 6 — Developer / API (advanced) `Dev`

Cron / launchd / GitHub Actions are the equivalents — see [docs/agent-factory/index.md](../agent-factory/index.md) and [decision record 0003](../decision-records/0003-no-default-schedulers.md). All such schedules are off by default and require an explicit `OPERATOR_APPROVED_TO_RUN=1` (or equivalent) env gate.

## Make it reusable

- Maintain a one-page doc per scheduled task: what it does, where the off-switch is, expected weekly cost, last review date.
- Review monthly. Pause anything that hasn't earned its place.

## Make it robust

- **Eval**: pick 5 historical inputs; run the prompt against each; check output against what you would have done.
- **Red-team**: prompt injection in inputs (e.g., a calendar invite that says "ignore your instructions"). The task must ignore.
- **Drift check**: monthly, do one full manual run and compare to the most recent scheduled run. Look for silent skips.

## What good output looks like

- Same shape every run.
- Errors fail loudly: "Could not access Calendar" not silent skip.
- Stays inside scope.

## If your plan doesn't have native scheduling

Manual fallback (works on every product, free or paid):

1. Calendar reminder at the cadence you want.
2. Reminder description = the prompt.
3. When the reminder fires, open the AI, paste, run, copy output to its destination.

This is the [Manual repeat-run fallback](../no-code-automations/index.md#manual-repeat-run-fallback). It's often the right answer.

## See also

- [No-code automation guide](../no-code-automations/index.md)
- [Decision record 0003 — no default schedulers](../decision-records/0003-no-default-schedulers.md)
- [Examples — Meeting prep](meeting-prep.md), [Newsletter triage](newsletter-triage.md)
