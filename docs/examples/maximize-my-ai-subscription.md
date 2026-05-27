# Example: maximize my AI subscription

> **Last verified:** 2026-05-06 · **Time:** 30–45 minutes · **No API key required**

You already pay for an AI. This example finds the highest-leverage features you haven't tried yet — and gets you to use one of them this week.

It's also the example that reveals when to switch tools.

## Step 0 — Pick your product

Whichever AI you spend the most time in. If you have multiple paid products, pick the one you opened today.

## Step 1 — Build your Portable AI Profile

If you don't have one, do this first. It pays back in every other workflow:

- Open [Memory and preferences](../preferences-memory/index.md).
- Copy the [Portable AI profile](../preferences-memory/index.md#portable-ai-profile) template.
- Fill it out. ~10 minutes.
- Paste into your AI's memory / Custom Instructions / Saved info / Profile.

Now every chat in that product knows your tone, role, and constraints.

## Step 2 — Run the audit

Paste this in your primary AI:

```
Audit how I'm using you. Based on this conversation and what you remember about me,
list 5 features in <ChatGPT/Claude/Gemini/Grok/Perplexity/Copilot — pick yours>
that I have probably not used yet, ranked by leverage for my work.

For each feature:
- Name it as it appears in the UI.
- One sentence on what it does.
- One sentence on why it would help me specifically.
- One sentence on the easiest first use.
- Plan availability (Free / Paid / Team / Developer).

If a feature is gated by a plan I don't have, say so and suggest the closest free fallback.
Do not invent features. If unsure, say so.
```

Read the output. Cross-check against the [Capability map](../capability-map/index.md) and your AI's Mastery page.

## Step 3 — Pick one. Use it this week.

The point is **using one new feature**, not building a perfect plan.

Common wins by product (drift risk: medium):

### ChatGPT

- Custom Instructions (Free) → set tone + role + "avoid" list.
- Memory (Sub) → tell it your role and a few constraints.
- Projects (Sub) → group all chats about one topic; instructions follow you.
- Custom GPTs (Sub) → publish your most-repeated workflow.
- Tasks (Sub, where rolled out) → schedule a daily/weekly prompt. Manual-test first.
- Canvas → for any document longer than half a page.

### Claude

- Profile preferences (Sub).
- Projects + Project Knowledge (Sub).
- Artifacts (Free / Sub) → for code, docs, web mockups.
- Skills (Sub, growing) → package a process as a `SKILL.md`.
- Cowork (Sub, where rolled out) → schedule a recurring task.

### Gemini

- Saved info (Sub).
- Gems (Sub) → reusable assistants.
- Workspace integration (Sub) → Drive / Calendar / Mail context.
- Deep Research (Sub) → use it for one question a week.
- Scheduled actions (Adv, where rolled out).

### Grok

- Personalization (Sub, where rolled out).
- Model picker → run the same question through two variants; learn which you'll trust.
- Grok on X → quick second opinions on threads you're already reading.

### Perplexity

- Spaces (Sub) → one Space per topic, with sources.
- Profile + AI tone (Sub).
- Pages (Sub) → convert research into shareable articles.
- Deep Research → for citation-heavy questions.
- Comet (Sub) → AI-native browser, where rolled out.

### GitHub Copilot

- `.github/copilot-instructions.md` (Free) → repo-aware prompt.
- Selection-based chat (Free) → highlight code, refactor selection only.
- Slash-prompts in `.github/prompts/` (Free) → reusable patterns per repo.
- Coding agent (Paid) → assign an issue. Review the PR like a junior dev's.
- Copilot Extensions (Team / Ent).

## Step 4 — Decide whether to switch tools

Sometimes the highest-leverage move is a different AI. Use this rule of thumb:

| If your top need is | And your current AI is weak there | Consider |
|---|---|---|
| Citations | ChatGPT / Claude / Gemini | Perplexity |
| Long documents | ChatGPT / Gemini / Grok | Claude |
| Sharing assistants with a team | Claude / Grok | ChatGPT / Gemini |
| Email & calendar | Grok / Perplexity | Gemini (Workspace) / ChatGPT |
| Code in a repo | Anything except Copilot | GitHub Copilot |

See the [Capability map](../capability-map/index.md) for the full version.

## Step 5 — Lock in the win

End-of-week:

1. Did you use the new feature at least three times?
2. Did you save the prompt or assistant somewhere you'll find it?
3. Add a one-line note to your portable AI profile under "Recent changes."

If yes to all three, you've raised your floor.

## Layered version

This example is itself a workflow. You can package the audit prompt as a Project / Gem / Custom GPT and re-run it quarterly.

## What good output looks like

- 5 features that are real and named correctly.
- Each one is plausibly the next thing for *you*.
- At least one is in your current plan; at least one is in a higher plan with a fallback.

## If your plan doesn't have a feature the audit suggests

That's the fallback question. Read the [Capability map](../capability-map/index.md) row for that capability. Use the manual workflow until the upgrade is worth it.

## See also

- [Capability map](../capability-map/index.md)
- [Memory and preferences](../preferences-memory/index.md)
- [Mastery hub](../mastery/index.md)
- [Universal 7-mission learning path](../learning-path/index.md)
