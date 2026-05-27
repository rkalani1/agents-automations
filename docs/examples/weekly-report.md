# Example: weekly status report

> **Last verified:** 2026-05-06 · **Time:** 10 minutes for chat · **No API key required**

A short, honest weekly report you can send (or post) on Friday afternoons: wins, blockers, decisions needed, what's next.

## Layer 1 — Chat only `Free`

```
Help me write my weekly status report. Here's the raw material:

Wins this week:
- <bullet>

Blockers:
- <bullet>

Decisions I need from others:
- <bullet>

Plans for next week:
- <bullet>

Format the report with:
- A 2-sentence summary up top.
- Headers: Wins / Blockers / Decisions needed / Next week.
- Total length under 300 words.
- No marketing language. No flattery. Don't add things I didn't list.

Output as markdown. Drafts only.
```

How to tell whether it worked: every bullet is something you actually said. Nothing is invented. The 2-sentence summary captures the gestalt.

## Layer 2 — Project `Sub`

Build a "Weekly status" Project. System prompt: the format above + your role + team norms.

What to click: see [meeting-prep example, Layer 2](meeting-prep.md#layer-2-project-sub).

## Layer 3 — Memory `Sub`

Global memory addition:

```
- Weekly status reports: 2-sentence summary, headers Wins/Blockers/Decisions/Next, ≤300 words, no flattery, no inventions.
- My team uses sentence-case headers and Markdown bullets.
```

## Layer 4 — Scheduled action `Sub`

Schedule a Friday 15:00 local prompt that asks **you** for the bullets, then formats the report. The scheduled run drafts the email/Slack post.

Manual fallback: Friday calendar reminder + saved prompt.

## Layer 5 — Custom assistant `Sub`

Custom GPT / Gem / Skill:

- **Knowledge file**: a 1-page "team norms" doc (who reads the report, what they care about, what's already decided).
- **Sample prompts**: 3 example bullet pastes + the reports they should produce.

## Layer 6 — Developer / API (optional)

A script that pulls bullets from a Notion / Linear / Jira query and formats the report. Drafts only. See [Agent Factory](../agent-factory/index.md).

## Make it reusable

- Save the Project / Gem / Custom GPT.
- Save bullets to a "running list" doc throughout the week so Friday is paste-and-format.

## Make it robust

- **Eval**: write last week's report by hand, run the AI on the same bullets, compare.
- **Red-team**: paste vague bullets ("did stuff") — the AI should ask, flag, or skip per your uncertainty setting.
- **Drift check**: monthly, ask which bullets the AI consistently mis-frames.

## What good output looks like

- Says things you'd say.
- Calls out blockers without softening them.
- Decisions are framed as questions a reader can answer in a single Slack message.

## If your plan doesn't have this feature

- No Project → paste the system prompt every Friday.
- No Memory → paste team norms in the prompt.
- No native task → Friday calendar reminder.
- No Custom GPT → save the prompt; it's the same effort.

## See also

- [Mastery — ChatGPT](../mastery/chatgpt.md), [Claude](../mastery/claude.md)
- [Memory and preferences](../preferences-memory/index.md)
