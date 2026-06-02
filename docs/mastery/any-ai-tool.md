# Any AI tool

> **Last verified:** 2026-05-06 · **Drift risk:** low (this page is intentionally generic)

You'll use this page if your AI app isn't ChatGPT, Claude, Gemini, Grok, Perplexity, or Copilot — or if you don't know what you have. The method below works in almost any AI chat product.

## What you need

- An AI app you can open and type into.
- A notes app (Notes, Obsidian, Google Docs, a sticky note — anything).
- 10 minutes.

That's it. **No API key. No code. No install.**

## The universal method, in 10 steps

### 1. Describe the job in one sentence

Write down the job in plain language. One sentence. No jargon.

> Example: "Help me triage my overnight email into Now / Later / Reference / Trash."

### 2. Ask the AI to interview you before answering

Most AI apps will jump straight to an answer. Stop them. Paste this as your **first message**:

```
You will help me with this task: <your one-sentence job>.

Before you answer, ask me 5 short questions to learn:
1. What good output looks like (give me 1 example).
2. What bad output looks like (1 example).
3. What format I want (length, structure, tone).
4. What I want you to NEVER do.
5. Who else might read the output.

Wait for my answers. Do NOT start answering the task until I reply.
```

This works in any AI chat product. It forces the AI to learn your preferences before guessing.

### 3. Define the output format

Once it has interviewed you, paste the output schema you want:

```
Output format:
- A bulleted list grouped by Now / Later / Reference / Trash.
- One line per item, with a short reason.
- Maximum 12 items per group.
- Plain text only. No marketing language. No emojis.
```

### 4. Give an example of good and bad output

Paste a small example you'd accept and one you wouldn't. AI apps copy patterns. If you don't show one, they invent.

### 5. Save the prompt as a reusable template

Before you do anything else: copy the whole conversation prompt (including the interview, the format, and the examples) into your notes app. Title it after the task. **This is your reusable prompt.** You'll paste it next time.

### 6. Maintain a portable preference profile

Open a new note titled `My AI preferences`. Write down, in plain English:

- The tone and style you like (e.g., "no marketing language, sentence-case headings, no emojis").
- The mistakes you want the AI to avoid (e.g., "don't invent citations").
- The formats you usually want (e.g., "bulleted lists over paragraphs").
- The languages and date formats you use.

This is your **portable preference block**. Paste it after the system prompt in any new chat, in any AI app. It'll feel like the AI remembers you, even if it doesn't.

### 7. Build a manual repeat-run checklist

Open another note titled `<task name> playbook`. Write 5–7 lines:

```
1. Open my AI app.
2. Open the saved prompt for <task name>.
3. Paste the prompt.
4. Paste the preference block.
5. Paste today's input (e.g., "here are last night's emails: …").
6. Read the output. If it's wrong, say what's wrong; let it retry once.
7. Save anything worth keeping into my notes.
```

This is the lowest-tech "automation" that works in any product.

### 8. Probe what features your app exposes

Look in your app's interface for any of these labels:

- **"Memory"**, **"Saved info"**, **"Custom Instructions"**, **"Personalization"**, **"Profile"** → that's your memory rung.
- **"Projects"**, **"Workspaces"**, **"Spaces"**, **"Gems"**, **"Custom GPTs"**, **"Personas"**, **"Custom assistants"** → that's your project / custom-assistant rung.
- **"Files"**, **"Knowledge"**, **"Sources"**, **"Pinned files"** → attach reference files there.
- **"Tasks"**, **"Scheduled prompts"**, **"Run on a schedule"** → optional automation rung.
- **"Agent"**, **"Coworker"**, **"Browser"**, **"Computer use"** → optional agent rung. Treat with care.

If you find any of these, move your saved prompt + preference block into them. That makes them automatic next time.

### 9. If a feature is missing, use the nearest fallback

| Missing feature | Nearest fallback |
|---|---|
| Memory / Custom Instructions | Paste your preference block at the start of every chat. |
| Projects / Workspaces / Spaces | Save the prompt + preferences in a notes app. Use a fresh chat each time. |
| Custom assistant | Use a long-form prompt that contains the persona; save it in notes. |
| Skill / packaged behavior | A saved prompt + a checklist file is the fallback. |
| Files / Knowledge | Paste the relevant text directly into chat. Keep PHI/PII out. |
| Scheduled tasks | Add the run to your calendar or a Monday checklist. |
| Browser / computer use | Drive the browser yourself; use the AI to draft what to type. |

Your AI app being missing one or two of these isn't a problem. **It being missing most of them** is a signal to switch.

### 10. Decide whether to switch tools

The [Mastery index](index.md) has a capability matrix. If your current app is missing 3+ rungs you actually need, the next chapter covers each major product:

- [Claude](claude.md) — Projects, Skills, Artifacts, Computer use, Claude Code.
- [ChatGPT](chatgpt.md) — Custom GPTs, Tasks, Codex.
- [Gemini](gemini.md) — Gems, Workspace context, Antigravity.
- [Grok](grok.md) — consumer Grok, Grok on X, xAI API.
- [Any AI tool](any-ai-tool.md) — Spaces, Pages, Comet.
- [Coding agents](coding-agents.md) — Copilot, Claude Code, Codex CLI.

## Guided exercise — 10 minutes

> **Task:** "Turn a vague request into a reusable prompt and project plan in whatever AI app you have."

1. Open the AI app you use most.
2. Paste this as the first message:

   ```
   I want help turning a vague request into a reusable workflow.

   Vague request: "Plan my Q3 in 1 page."

   Before you answer:
   1. Ask me 5 short questions to learn what good output looks like.
   2. Wait for my answers.
   3. Then propose a 5-step plan I can paste into a notes app, plus a saved prompt I can reuse next quarter.
   4. Format: numbered list, 1 page max, no marketing language.
   ```
3. Answer its 5 questions. Be specific.
4. When it produces the plan and the saved prompt: copy both into your notes app.
5. Open your AI app again. Open a fresh chat. Paste your saved prompt. Confirm the AI behaves the same way.

If step 5 produces the same shape of output, you've successfully moved a one-off chat into a reusable workflow — without any developer tools.

## Free / subscription / API availability

Almost everything in this universal method works on **free** tiers of every major AI app. The handful of features that may require a paid plan (memory, projects, custom assistants, scheduled tasks, agent modes) all have fallbacks listed above.

You only need an **API** when you outgrow the app — and most readers don't.

## Level up this workflow

Once the universal method works for one task, ladder up:

1. Saved prompt → memory / custom instructions.
2. Memory → project / workspace / Gem / Custom GPT.
3. Project → custom assistant with attached files and a clear refusal block.
4. Custom assistant → skill / Action / Pages (where available).
5. Skill → scheduled task (manual-first, three clean runs before scheduling).
6. Scheduled task → agent / coworker / computer use (where available, in a sandbox).
7. Agent → developer / API (only if you outgrow the app).

If your app supports rung 4 (skills/actions), the [Claude](claude.md), [ChatGPT](chatgpt.md), and [Gemini](gemini.md) tracks cover the specifics.
