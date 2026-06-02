# Example: research summary with citations

> **Last verified:** 2026-05-06 · **Time:** 10–20 minutes · **No API key required**

For any research question, get a one-page summary with citations you can verify and a follow-up question list.

This example is best in **Perplexity** because retrieval-with-citations is its native job. Every other product has a fallback path.

## Layer 1 — Chat only `Free`

In whichever AI you use, paste:

```
You are a careful research summariser.

Question: <one sentence>
Audience: <who I'm writing for, e.g., a clinical team, a class>
Output:
- 5-paragraph summary, sentence-case headers.
- A "What we don't know" section with 3 honest gaps.
- Inline citations as [Author Year] linked to a numbered reference list.
- 5 follow-up questions worth pursuing.

Constraints:
- Use only sources you can name and link.
- If you can't find a citation, say so explicitly. Do not invent.
- NEJM citation style for the reference list.
```

How to tell whether it worked: every claim has a citation. Every citation resolves when you click it. The "What we don't know" section is non-trivial.

## Layer 2 — Project / Space `Sub`

This shines as a **Perplexity Space**:

- New Space → System Prompt = the prompt above.
- Add 5–10 high-quality source URLs as Sources.
- Each new question inside the Space inherits the format and the sources.

In Claude / ChatGPT / Gemini: build a Project. Paste system prompt + add reference PDFs to Project Knowledge.

## Layer 3 — Memory `Sub`

Global memory:

```
- For research summaries, default to NEJM citation style.
- Always include "What we don't know" with at least 3 gaps.
- Never invent citations. If unverifiable, say so.
- Audience: clinical research team.
```

## Layer 4 — Scheduled action `Sub`

Weekly research watch:

- Friday 10:00 local: "Summarise newly-deposited preprints this week matching <topic>."
- Best in Perplexity Spaces (paid). Manual fallback: Friday calendar reminder.

See [No-code automations](../no-code-automations/index.md#example-4-research-watch-sub).

## Layer 5 — Custom assistant `Sub`

- **Custom GPT / Gem / Skill**: package as "Lit summariser." Knowledge file = a list of journals you trust + a list of red-flag domains.
- **Perplexity Space**: same shape; Spaces are already the assistant.

## Layer 6 — Developer / API (optional)

Perplexity API with `sonar-*` models gives you the same retrieval programmatically. See [Mastery — Perplexity § Expert](../mastery/any-ai-tool.md). Use only if you need automation; subscription Perplexity is the better tool for most users.

## Make it reusable

- Pin one Space per ongoing topic.
- Convert good threads to Pages to share.

## Make it robust

- **Eval**: pick 5 questions you already know the answer to. Run them through. Score citation accuracy and "what we don't know" honesty.
- **Red-team**: ask a question for which there is no reliable answer ("What's the best treatment for <made-up condition>?"). The AI must refuse to invent.
- **Drift check**: every quarter, re-verify your Sources list — sites die, papers retract.

## What good output looks like

- Every paragraph carries a citation.
- The reference list is parseable as NEJM style without rework.
- "What we don't know" reads like a senior clinician wrote it.

## If your plan doesn't have this feature

- No Perplexity → ask Claude / ChatGPT with web search where available; cite-check manually.
- No Spaces → paste system prompt every time.
- No native task → calendar reminder.

## See also

- [Mastery — Perplexity](../mastery/any-ai-tool.md)
- [No-code automations — Research watch](../no-code-automations/index.md#example-4-research-watch-sub)
- [Capability map — Research with citations](../capability-map/index.md#research-and-sharing)
