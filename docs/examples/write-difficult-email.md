# Example: write a difficult email

> **Last verified:** 2026-05-06 · **Time:** 5–10 minutes for the chat version · **No API key required**

You have to write an email you don't want to write — to push back politely, to deliver bad news, to ask for something awkward, to follow up after silence. This example walks through the whole workflow at every level of your AI, from a single chat to a saved Skill / Gem / Custom GPT.

## What you need

- An AI app you already use: ChatGPT, Claude, Gemini, Grok, Perplexity, Copilot, or anything else.
- The few facts of the situation: who, what, what you want, the constraint you're working inside.
- 5 minutes. (Less, the third time you do this.)

---

## Layer 1 — Chat only `Free`

Paste this in any AI chat:

```
You're helping me draft a difficult email.

Situation: <one sentence about the situation>
Recipient: <name + relationship to me>
What I want from this email: <one sentence>
Tone: respectful, direct, no apology padding, no marketing language.

Draft three versions:
1. Short (≤ 80 words).
2. Standard (≤ 160 words).
3. Long, with a one-paragraph context up front (≤ 240 words).

For each version, list two assumptions you made about my situation that I should verify before sending.

Drafts only. I will send the email myself.
```

Read the three drafts, pick one, edit, send. Done.

**How to tell whether it worked**: the email says exactly what you'd say if you were on a great day. It doesn't sound like marketing copy. It doesn't apologise for things you don't owe an apology for.

**Fallback if your AI doesn't keep memory**: paste the same prompt every time. The point is the structure.

---

## Layer 2 — Project / workspace version `Sub`

Once you've drafted a few of these, package the prompt into a Project (Claude, ChatGPT) or Space (Perplexity) or Gem (Gemini). The system prompt becomes your reusable "difficult email coach." Every new chat inside the Project is a one-line situation paste away from a draft.

Project / Gem / Space instructions to paste:

```
You are my draft-email coach. I open this project when I have to write
a difficult email — pushing back, delivering bad news, asking for an
awkward favour, following up after silence.

For every chat, I'll give you the situation. You give me three drafts:
short, standard, and long-with-context. Always list two assumptions
you made that I should verify. Always mark drafts as drafts.

Tone: direct, respectful, no apology padding, no marketing copy.
Format: markdown headers per draft.
Authority: drafts only. Never claim you sent anything.
```

What to click:

- **ChatGPT**: sidebar → New Project → name "Difficult email coach" → paste into Instructions.
- **Claude**: sidebar → Projects → New → paste into Project Instructions.
- **Gemini**: sidebar → Gems → New Gem → paste into Instructions.
- **Perplexity**: sidebar → Spaces → New Space → paste into System Prompt.
- **Grok**: paste it as message 1 of every new chat (no Project equivalent on most plans).
- **Copilot / other**: paste as the first message of a fresh chat each time.

---

## Layer 3 — Memory / preferences version `Sub`

Move the *style* part into global memory so every chat (not just this Project) knows your voice.

Paste into your AI's memory / Custom Instructions / Saved info / Profile preferences:

```
When I'm drafting emails, prefer:
- direct, respectful tone
- no apology padding
- no marketing language
- no exclamation points
- short subject lines (under 8 words)
- always treat outputs as drafts; do not claim to have sent anything
```

Now when you use the Project, the AI inherits these rules without you re-typing them.

---

## Layer 4 — Native task / scheduled action `Sub` (where rolled out)

Most "difficult emails" don't need scheduling — they're triggered by life. But two versions do:

- **Weekly follow-up sweep.** Every Friday, ask the AI to scan for emails you haven't replied to in 5+ days and draft a one-sentence "still on my radar" reply. **Drafts only.**
- **Monthly relationship maintenance.** First Monday of each month, draft a 3-line check-in to one named person.

What to click:

- **ChatGPT Tasks**: in the chat where you ran the prompt, look for the "Make this a Task" affordance. Set Friday 16:00 local. Verify three weeks before walking away.
- **Gemini scheduled action**: Settings & help → Scheduled actions → weekly. Same drill.
- **Claude Cowork**: scheduled task on the "Difficult email coach" Project.

If your plan doesn't have native scheduling: a calendar reminder + the saved prompt does the same job.

See the [No-code automation guide](../no-code-automations/index.md) for the full safety drill before scheduling.

---

## Layer 5 — Skill / Custom GPT / Gem `Sub`

For a shareable, named assistant, package the system prompt + your style preferences into a Custom GPT / Gem / Claude Skill.

- **Custom GPT (ChatGPT)**: open `chatgpt.com/gpts/editor` → name it "Email coach" → paste system prompt in Configure → optionally upload a knowledge file with examples of *good* drafts you've sent before.
- **Gem (Gemini)**: same shape; in the Gem manager.
- **Claude Skill**: write a `SKILL.md` (see the [Claude feature map](https://claude.ai/)) that contains the prompt, style rules, and a 3-example template folder. Skills shine when you want to share with a team.

---

## Layer 6 — Developer / API (optional, advanced)

Only if you want this in a script (e.g., to pre-draft replies to a label in a personal mailbox):

- Use the OpenAI / Anthropic / Gemini / xAI / Perplexity SDK of your choice.
- Pass the same system prompt as `instructions`.
- Always store outputs as **drafts** (Gmail draft, Outlook draft); never auto-send.
- This Task Builder hides this path in Beginner Mode for a reason. See [Agent Factory](../agent-factory/index.md) when you're ready.

---

## Make it reusable (intermediate)

- Save the Project / Gem / Custom GPT name in your phone's notes app.
- Paste the canonical prompt into your `~/Notes/ai-prompts/` for portability.
- Add one good draft per month to the Knowledge files. The AI gets better at *your* voice.

## Make it robust (expert)

- **Eval set.** Write 5 situations, draft each, and grade against your real "would I send this?" bar. Iterate the system prompt until 4/5 pass.
- **Red-team probes.** Ask the AI to draft an email that crosses a line — confidential gossip, an apology you don't owe, an over-promise. The AI should refuse the line-crossing and produce an alternative.
- **Drift check.** Once a quarter, paste your saved prompt back into the AI and ask: "Would you change anything about this prompt to produce better drafts of difficult emails for me, given the kinds of emails I write?"

---

## What good output looks like

- Short. Under 200 words unless you asked for context.
- Says exactly what you mean. No softeners that change the meaning.
- Marks itself as a draft.
- Lists assumptions you can verify before sending.

## If your plan doesn't have this feature

- No Projects → paste the system prompt as message 1 of every chat.
- No Memory → keep style rules in a notes file; paste once per session.
- No native task → a Friday calendar reminder + the saved prompt is just as effective.
- No Custom GPT / Gem / Skill → save the prompt in a notes file. The "assistant" is just a saved prompt.

## See also

- [Mastery — ChatGPT](../mastery/chatgpt.md) and [Claude](../mastery/claude.md)
- [Memory and preferences](../preferences-memory/index.md)
- [No-code automations](../no-code-automations/index.md)
