# First Read-Only Agent: Summarize a Folder of Notes into a One-Pager

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Use case

You have a folder of Markdown notes — meeting summaries, reading notes, research snippets — and you want an agent to read them and produce a structured one-page summary. The agent must stay within the provided corpus: no web search, no file writes, no external API calls. This is the safest possible agent pattern and a good first step before you give any agent access to live data or tools.

Target completion time: 20–35 minutes.

---

## Best platform choice and why

**Primary: [ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)**

ChatGPT Projects lets you attach files directly to a persistent project context and write a system instruction that applies to every conversation in that project. There is no code to install, no API key to manage for this task, and the file attachment interface makes it easy to control exactly what the agent can see. The project does not have tool use enabled by default, which means there is no risk of the agent browsing the web or calling external services unless you explicitly turn those on.

**Alternative: Claude Projects (Anthropic)**

Claude Projects offers equivalent functionality: file attachments, persistent instructions, and no outbound tool use by default. The choice between them largely depends on which account you already have. If you use Claude regularly, the experience is nearly identical. The system prompt syntax described below works in both.

---

## Prerequisites

- A ChatGPT account (Plus, Team, or Enterprise — Projects is not available on the free tier at time of writing).
- 3–5 short Markdown files you are comfortable uploading to a third-party service. If you do not have real notes, use the synthetic corpus provided in the Example input section below.
- No API key, no terminal, no package installation required.

---

## Setup steps

1. Log in to [ChatGPT](https://chatgpt.com) and navigate to the left sidebar.
2. Click "Projects" and then "New project". Name it something like `journal-club-summarizer`.
3. In the project settings, paste the system instruction from the Copyable instructions section below.
4. Upload your 3–5 Markdown files using the file attachment button in the project settings. Keep each file under 50 KB for this exercise.
5. Confirm that "Web search" and "Code interpreter" are toggled off in the project tools panel.
6. Open a new conversation inside the project and paste the user prompt from the Copyable instructions section below.

Per [ChatGPT Projects documentation](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), files attached to a project are available in every conversation within that project.

---

## Copyable instructions

### System instruction (paste into project settings)

```
You are a research assistant whose only job is to synthesize the documents attached to this project. 

Rules you must follow without exception:
- Do not browse the web, call any external service, or retrieve any information not present in the attached files.
- Do not fabricate citations. Every claim you make must be traceable to a specific attached file. When you cite a source, name the file explicitly (e.g., "According to meeting-notes-2025-03-01.md...").
- Do not write any files or execute any code.
- If you are asked about something not covered in the attached files, say so explicitly. Do not guess.
- Format all summaries with the following headings in this order: Overview, Key Themes, Action Items or Open Questions, Sources Referenced.
```

### User prompt (paste into the conversation)

```
Please read all the attached documents and produce a one-page summary.

Structure your response using exactly these headings:
## Overview
## Key Themes
## Action Items or Open Questions
## Sources Referenced

Under "Sources Referenced", list each document you drew from by filename and include a one-sentence description of what it contributed.

Keep the total response under 500 words. Do not include information that is not in the attached files.
```

---

## Example input

Create three files locally and upload them. You can use this synthetic corpus about running a journal club:

**`journal-club-purpose.md`**
```markdown
# Why We Run a Journal Club

The journal club meets every two weeks to keep the team current on ML research.
Goals: shared vocabulary, critical reading skills, cross-team collaboration.
Started in Q1 2024 with 6 members; grew to 14 by Q3 2024.
```

**`journal-club-process.md`**
```markdown
# How We Run Each Session

1. One presenter selects a paper at least one week in advance.
2. All members read the abstract and introduction; presenter reads the full paper.
3. Session runs 45 minutes: 15 min overview, 20 min discussion, 10 min action items.
4. Notes are posted in the shared Notion page within 24 hours.
Open issue: attendance drops when sessions conflict with sprint planning.
```

**`journal-club-retrospective-2025.md`**
```markdown
# 2025 Retrospective Notes

Strengths: high engagement on applied papers, good psychological safety for questions.
Weaknesses: inconsistent note quality, no archive of past paper selections.
Suggestions from members: rotate facilitator role, create a paper backlog.
Next steps: assign a note-taking rotation by end of January.
```

---

## Expected output

The agent should produce something structured like this (exact wording will vary):

```
## Overview
The journal club is a bi-weekly meeting that has grown from 6 to 14 members 
since Q1 2024. Its core goals are shared vocabulary, critical reading skills, 
and cross-team collaboration. Sessions follow a structured 45-minute format.

## Key Themes
- Structured format with defined time blocks for overview and discussion
- Growth in membership alongside inconsistency in documentation quality
- Member-driven suggestions for sustainability (rotating roles, paper backlog)

## Action Items or Open Questions
- Assign a note-taking rotation (due end of January per retrospective)
- Resolve attendance conflicts with sprint planning
- Create an archive of past paper selections

## Sources Referenced
- journal-club-purpose.md: Background on goals and membership growth
- journal-club-process.md: Session format and an open scheduling issue
- journal-club-retrospective-2025.md: Strengths, weaknesses, and next steps
```

---

## Safety boundaries

This quickstart is designed to be fully read-only. Enforce the following:

- No file writes. The agent has no file-writing tool enabled in this configuration.
- No external requests. Web search and browsing must be disabled in the project settings before you run this.
- No scheduling. This is a manually triggered, single-turn interaction. Do not set up any automated triggers or scheduled runs.
- No sensitive data. Do not upload files containing passwords, API keys, personal health information, or data subject to confidentiality obligations.
- Scope control. The system instruction explicitly limits the agent to the attached corpus. If you see the agent referencing external knowledge, tighten the instruction or check that web search is disabled.

---

## Eval / check steps

Run these three checks after the agent responds:

1. **Corpus containment check.** Read through the response and verify that every claim maps back to one of the uploaded files. If the agent references something not present in any file, that is a hallucination. Fail.

2. **Heading structure check.** Confirm the response contains exactly the four required headings: Overview, Key Themes, Action Items or Open Questions, Sources Referenced. If any heading is missing or renamed, the system instruction was not followed. Note whether the agent self-corrects if you ask again.

3. **Source refusal check.** In a follow-up message, ask: "What papers did the journal club discuss in 2024?" The corpus does not contain this information. The agent should say it does not have that information rather than fabricating an answer. If it fabricates, adjust the system instruction to add a stronger prohibition on guessing.

---

## Troubleshooting

**The agent mixes up which file said what.**
This is common when files are short and thematically similar. Add a header line to each file (e.g., `Source: journal-club-process.md`) so the model can ground its citations more reliably. Alternatively, reduce the number of attached files so there is less context to track.

**The agent produces headings different from the ones requested.**
The model may reformulate headings to feel more natural. If structural compliance matters, add the instruction "Use exactly the heading text specified, do not paraphrase the heading names" to the system instruction.

**The agent summarizes only one or two files and ignores the others.**
This can happen when one file is significantly longer or placed earlier in context. Try making the files more uniform in length, or explicitly name the files in the user prompt: "Please draw from all three files: journal-club-purpose.md, journal-club-process.md, and journal-club-retrospective-2025.md."

**The agent adds information from its training data.**
Disable web search and restate the boundary in the system instruction: "Your only knowledge source is the attached files. Do not use any information from your training data."

---

Where to go next: [First File-Editing Agent](./first-file-editing-agent.md) — or explore the [OpenAI Agents SDK Python kit](../starter-kits.md) for a programmatic approach to the same read-only pattern.
