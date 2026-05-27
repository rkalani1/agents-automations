# First File-Editing Agent: Rewrite Markdown Notes for Clarity

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Use case

You have a folder of Markdown notes that are accurate but rough — dense sentences, inconsistent structure, awkward phrasing. You want an agent to rewrite them for clarity without changing the meaning, removing YAML frontmatter, or creating new files. The agent should produce a diff summary so you can review every change before committing.

Target completion time: 30–45 minutes.

---

## Best platform choice and why

**Primary: [Claude Code](https://code.claude.com/docs/en/setup)**

Claude Code is a command-line coding agent from Anthropic that operates directly on your local filesystem. It supports an explicit approval mode in which every proposed file modification is shown to you before it is applied. This makes it well suited for a first file-editing exercise: you maintain full control, you can inspect each change, and you can abort at any point. Claude Code also supports a `CLAUDE.md` file in your project root that lets you declare allowed and disallowed actions in plain language — a straightforward way to enforce constraints without custom tooling.

**Alternative: [Codex CLI](https://developers.openai.com/codex/cli)**

Codex CLI from OpenAI offers a similar local-agent experience with its own approval mode (`--approval-mode`). The setup is nearly identical. If you prefer the OpenAI ecosystem or already have an OpenAI API key configured, Codex CLI is a direct substitute. The `CLAUDE.md` constraint pattern does not apply; instead, pass constraints directly in the prompt or a `--system` flag.

---

## Prerequisites

- Node.js 18 or later (`node --version` to check).
- An Anthropic API key stored in the environment variable `ANTHROPIC_API_KEY`.
- Claude Code installed: follow the [official setup guide](https://code.claude.com/docs/en/setup).
- A Git repository initialized in a test directory (you will commit changes to a branch, not to main).
- The example notes folder from the Example input section below, or your own small set of 3 Markdown files.

---

## Setup steps

1. Install Claude Code per the [quickstart instructions](https://code.claude.com/docs/en/quickstart):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. Confirm installation:
   ```bash
   claude --version
   ```

3. Set your API key in the current shell session:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

4. Create and enter a test Git repository:
   ```bash
   mkdir clarity-rewrite-demo && cd clarity-rewrite-demo
   git init
   ```

5. Create the three example note files from the Example input section below, then commit them to `main`:
   ```bash
   git add . && git commit -m "initial notes"
   ```

6. Create a working branch so that `main` is never directly modified:
   ```bash
   git checkout -b clarity-rewrite
   ```

7. Create the `CLAUDE.md` file in the project root with the content from the Copyable instructions section below.

8. Run Claude Code in approval mode with the user prompt from the Copyable instructions section:
   ```bash
   claude --approval-mode
   ```

In approval mode, Claude Code will pause before writing any file and show you the proposed diff. Type `y` to accept or `n` to reject each individual change.

---

## Copyable instructions

### `CLAUDE.md` (place in project root)

```markdown
# Agent constraints for this project

## Allowed actions
- Read any .md file in this directory
- Overwrite existing .md files with improved versions
- Produce a diff summary at the end

## Disallowed actions
- Do NOT create new files unless explicitly asked
- Do NOT delete or rename any file
- Do NOT use any network tools or browse the internet
- Do NOT modify any file outside this directory
- Do NOT use `rm`, `mv`, or `cp` on any file
- Do NOT remove or modify YAML frontmatter blocks (lines between --- delimiters at the top of a file)
- Do NOT change the meaning of any sentence — only improve phrasing and structure
```

### User prompt (paste at the Claude Code prompt or pass with `--prompt`)

```
Please rewrite the Markdown notes in this directory for clarity.

Rules:
- Preserve the meaning of every sentence. Do not add, remove, or change any factual claim.
- Keep all YAML frontmatter blocks exactly as-is. Do not touch any content between --- delimiters.
- Do not create any new files.
- Do not remove any existing content — only restructure and rephrase for clarity.
- Prefer shorter sentences. Break up run-on sentences. Use active voice where possible.
- Keep bullet lists as bullet lists; keep headings as headings.
- After completing all rewrites, output a brief diff summary listing: for each file, what changed (e.g., "Broke one sentence into two", "Changed passive to active voice in paragraph 2").

Run in approval mode and wait for my confirmation before writing each file.
```

---

## Example input

Create these three files in `clarity-rewrite-demo/`:

**`notes/project-kickoff.md`**
```markdown
---
title: Project Kickoff Notes
date: 2025-04-10
author: team
---

# Project Kickoff

The project was kicked off in a meeting that was attended by the whole team on April 10th and it was discussed that the main goal of the project which is to migrate the internal dashboard to a new data pipeline would be completed by the end of Q2 and it was also noted that there might be some risks related to data quality that would need to be investigated further by the data team before work could begin.
```

**`notes/standup-2025-04-14.md`**
```markdown
---
title: Standup Notes
date: 2025-04-14
---

# Standup 14 April

Yesterday: worked on setting up local dev environment, encountered issues with Docker that were eventually resolved after checking documentation. Today: will begin writing the data ingestion module. Blockers: none at this time but there is a question about whether the staging database credentials have been rotated yet which should be confirmed with the platform team.
```

**`notes/retro-q1.md`**
```markdown
---
title: Q1 Retrospective
date: 2025-04-01
---

# Q1 Retro

Things that went well included the fact that deployments were largely smooth and team communication improved noticeably compared to last quarter when there were several miscommunications that caused delays. Things to improve: estimation accuracy is still a challenge, particularly for tasks involving third-party APIs whose behavior is not always predictable and which adds uncertainty to sprint planning.
```

---

## Expected output

After running with approval mode and accepting each change, you should have:

- Three overwritten `.md` files with clearer prose and identical frontmatter.
- A diff summary from the agent, similar to:

```
## Diff summary

**notes/project-kickoff.md**
- Split one 80-word run-on sentence into four shorter sentences.
- Changed passive constructions ("was kicked off", "was attended") to active voice.
- YAML frontmatter unchanged.

**notes/standup-2025-04-14.md**
- Broke the "Blockers" sentence into a statement and a separate follow-up question.
- Removed filler phrase "at this time".
- YAML frontmatter unchanged.

**notes/retro-q1.md**
- Split the "Things to improve" run-on into two sentences.
- Restructured "Things that went well" to lead with the main point.
- YAML frontmatter unchanged.
```

Verify the diff with `git diff clarity-rewrite main` before merging anything.

---

## Safety boundaries

- Run in approval mode every time. Never skip approval mode on a first pass over files you care about.
- Commit to the `clarity-rewrite` branch only. Do not run this against `main`.
- No network access. The `CLAUDE.md` file explicitly disallows network tool use. Verify in the Claude Code session log that no outbound requests were made.
- No new files. The constraint file and the prompt both prohibit file creation. If you see a new file appear, reject it.
- No `rm`, `mv`, or `cp`. These are blocked in `CLAUDE.md`. If the agent attempts them, reject the action and review whether the prompt was ambiguous.
- Back up first. Before running, `git stash` or ensure your working tree is clean so you can `git checkout .` to restore originals if needed.
- Do not run this against a directory containing credentials, private keys, or sensitive personal data.

---

## Eval / check steps

After the agent completes its run and you have reviewed and accepted the diffs:

1. **Semantic drift check.** Read the original and rewritten versions of each file side by side (`git diff clarity-rewrite main -- notes/project-kickoff.md`). Confirm that no factual claims were added or removed. Every piece of information in the original must still be present.

2. **Frontmatter preservation check.** Run the following and confirm the output is empty (no frontmatter lines were changed):
   ```bash
   git diff clarity-rewrite main | grep -A 5 "^---"
   ```
   If this shows changed frontmatter lines, the constraint was violated.

3. **No extra files check.** Confirm the file count is unchanged:
   ```bash
   git diff --name-only clarity-rewrite main | grep "^notes/" | wc -l
   ```
   The number should equal the number of files you started with. A higher number means new files were created against the constraint.

---

## Troubleshooting

**Claude Code is not pausing for approval.**
Confirm you launched with `--approval-mode`. Without this flag, Claude Code may apply changes automatically. Abort the session, restore from `git checkout .`, and re-run with the flag.

**The agent removed or changed YAML frontmatter.**
The `CLAUDE.md` constraint and the prompt both prohibit this. If it still happens, add a more explicit instruction: "The lines between the first pair of `---` delimiters at the top of each file are YAML frontmatter. Do not modify, reorder, or remove any of them." Then revert the affected file with `git checkout clarity-rewrite -- notes/filename.md` and re-run.

**The agent created a new file (e.g., a summary or changelog).**
Reject the file creation action in approval mode. If you already accepted it, delete the file and add it to `.gitignore` for the duration of this exercise. Tighten the `CLAUDE.md` instruction to include a line like "The directory must contain exactly the same files after your run as before."

**The rewrites introduce new claims or remove existing ones.**
This is a semantic drift failure. Revert the affected file with `git checkout`, tighten the prompt to say "your only allowed operation is rephrasing for clarity — do not add new information and do not omit any information", and re-run.

**The diff summary is missing or incomplete.**
Add a more explicit instruction at the end of the prompt: "Do not finish until you have output a diff summary in the format shown. List every file you changed."

---

Where to go next: [First Coding Agent](./first-coding-agent.md) — or see the [Claude Code starter kit](../starter-kits.md) for a more advanced workflow with multi-file projects.
