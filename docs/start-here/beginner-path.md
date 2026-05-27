# Beginner path

> **Last verified:** 2026-05-06 · **Drift risk:** medium

This path takes you from zero to a working, personalized AI assistant in 30–60 minutes. You will not write any code. By the end you will have a Project with custom instructions, reference files, and a small evaluation log that tells you where the assistant helps and where it does not.

---

## Before you start

Pick one chat surface. Do not try all three at once.

- **ChatGPT** (chat.openai.com) — use [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) to organize everything.
- **Claude.ai** — use Projects for the same purpose.
- **Gemini** (gemini.google.com) — if you are already in the Google Workspace ecosystem.

The steps below use ChatGPT Projects as the example. The same pattern applies to Claude.ai Projects and Gemini with minor label differences.

---

## Step 1: Create a Project (5 minutes)

1. Open ChatGPT and click **Projects** in the left sidebar.
2. Click **New project** and give it a specific name tied to a real work task — for example, "Literature review assistant" or "Weekly report drafting."
3. Add a one-sentence description of what this project is for.

Why a Project and not a plain chat? Projects persist your custom instructions and uploaded files across all conversations in that project, so you do not have to re-explain context every time.

---

## Step 2: Write custom instructions (10–15 minutes)

Inside the project settings, find the custom instructions or system prompt field. Write three things:

1. **Role:** What is this assistant doing? Example: "You are a research assistant helping a clinical researcher summarize trial literature."
2. **Constraints:** What should it never do? Example: "Do not draw clinical conclusions. Flag anything that requires expert review."
3. **Output format:** How should responses look? Example: "Use bullet points. Keep summaries under 150 words. Always cite the paper title and year."

Keep this under 200 words. Longer system prompts are not always better — they can dilute the instructions that matter most.

!!! tip
    Write constraints before you run into problems, not after. Think about what a confident but wrong response would look like and add a constraint to catch it.

---

## Step 3: Attach 1–2 reference files (5 minutes)

Upload one or two documents that the assistant should know about — a style guide, a glossary, a template, a short FAQ. Keep files under 20 pages for now.

Do not upload sensitive PII or proprietary data until you have reviewed your platform's data handling policy and your organization's guidelines.

---

## Step 4: Run 3 evaluation prompts (15–20 minutes)

Before using this assistant for real work, test it with three prompts that represent your actual use case. For each prompt, record:

- What you asked
- What the assistant returned
- Whether the output was useful, partially useful, or not useful
- One specific thing you would change

Use a simple text file or a notes app for this log. Do not skip it — this is your baseline for knowing whether future changes to the instructions improve or degrade quality.

**Example evaluation prompts for a literature review assistant:**

1. "Summarize this abstract in three bullet points, then list any methodological limitations mentioned." (Paste a real abstract.)
2. "What are the main differences between RCTs and cohort studies for this type of intervention?" (A question in your domain.)
3. "I need to compare three papers on the same topic. What format should I use?" (A meta question about workflow.)

---

## Step 5: Write down what worked and what did not (5 minutes)

After your three test prompts, answer these questions in your log:

- Which prompt produced the most useful output? Why?
- Where did the assistant miss the mark? Was it the instructions, the question, or the model's limitations?
- What one change to the system prompt might improve the weakest result?

Make that one change, re-run the weakest prompt, and note whether it improved.

---

## What comes next

You now have a working assistant with a documented baseline. This is not an agent — there are no tools, no loop, and no external data yet. But you have the foundation:

- A named task with defined output format
- A small eval set you can rerun after changes
- A habit of logging what works

When you are ready to add tools (web search, file access, code execution), read the [Power-user path](power-user-path.md).

!!! note
    The most common beginner mistake is skipping the eval log. Without it, you cannot tell whether your next change helped or hurt.
