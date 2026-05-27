# Power-user path

> **Last verified:** 2026-05-06 · **Drift risk:** medium

This path is for someone already using ChatGPT or Claude daily who wants to move from chat to a real agentic workflow: a CLI agent with filesystem access, a versioned prompt, and a small eval set. Budget 1–2 hours for initial setup.

---

## Prerequisites

- A paid subscription to ChatGPT Plus/Pro or Claude.ai Pro/Max, or API access.
- Comfort with a terminal (you do not need to be a software engineer, but you need to run commands).
- A concrete task you do repeatedly — something that takes 10–30 minutes of your time today.

---

## Step 1: Install a coding-capable CLI agent (20–30 minutes)

Pick one:

**Claude Code** — runs in your terminal, has direct shell and filesystem access, and supports MCP servers.
- Installation and setup: [Claude Code docs](https://code.claude.com/docs/en/setup).
- Requires a Claude subscription or API key.

**OpenAI Codex CLI** — a terminal-native agent using OpenAI models.
- Details at [Codex CLI on GitHub](https://developers.openai.com/codex/cli).
- Requires an OpenAI API key.

**Gemini CLI** — Google's terminal agent.
- Install from [gemini-cli on GitHub](https://github.com/google-gemini/gemini-cli).
- Requires a Google account and API key.

Install whichever matches your existing subscription. Verify the install by running a trivial task: "list the files in this directory and tell me which one is largest."

---

## Step 2: Connect one MCP server (20–30 minutes)

MCP (Model Context Protocol) is the standard way to give an agent access to tools beyond what ships by default. The canonical first MCP server is a filesystem server — it lets the agent read and write files in a directory you specify.

1. Find the official [MCP filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) (part of the reference servers in the MCP project).
2. Follow the installation instructions for your CLI agent. Most agents accept an MCP config file (often `mcp.json` or a section in a config YAML) where you list server paths and arguments.
3. Restrict the server to a single test directory — not your home directory. Example: `~/agent-workspace/`.
4. Verify it works: ask the agent to read a file from that directory.

!!! warning
    Do not point the filesystem MCP server at sensitive directories (source control, secrets, credentials) until you understand exactly what actions the agent can take.

The [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18) describes the protocol if you want to understand what is happening under the hood.

---

## Step 3: Build one repeatable workflow (20–30 minutes)

Pick the repetitive task you identified in the prerequisites. Design it as a workflow the agent can run end-to-end:

1. Write a short task description (3–5 sentences) that specifies input, output, and acceptance criteria.
2. Identify which tools the agent needs: file reads? shell commands? web search?
3. Run the workflow manually the first time, watching what the agent does and where it gets stuck.
4. Adjust the task description and re-run.

**Example:** "Read all `.md` files in `~/notes/weekly/`, extract action items (lines starting with `- [ ]`), and write a consolidated `action-items.md` file sorted by date."

This is a good first workflow because the output is verifiable (did the file get created? does it contain the right items?), the tools are limited (file read/write only), and failure is not catastrophic.

---

## Step 4: Capture an eval set of 5–10 prompts (15 minutes)

An eval set is a collection of inputs with known-good expected outputs. You will use it to detect regressions when you change prompts or upgrade models.

For each item in your eval set, record:

- The exact input (task description + any input files)
- The expected output (or expected properties of the output)
- The actual output from your first run
- A pass/fail judgment

Store this in a plain text file or a simple spreadsheet. Version it with git or your notes app.

!!! tip
    Five carefully chosen eval cases beat fifty vague ones. Pick cases that represent the edges of your task: the happy path, a malformed input, and a case where the model is likely to be overconfident.

---

## Step 5: Version your prompts (10 minutes)

Your task description is a prompt. Treat it like code:

- Store it in a file (e.g., `prompts/weekly-summary.md`).
- Add a comment at the top with the date you last changed it and why.
- Commit changes to git (or copy to a dated file if you do not use git).

When the model is upgraded or you change the prompt, re-run your eval set and compare. This takes 10 minutes and saves hours of confusion about "it used to work better."

---

## What comes next

- For team-wide deployment of this workflow, see [Team path](team-path.md).
- For data residency or air-gap requirements, see [Local-first path](local-first-path.md).
- For safety practices before expanding the agent's tool access, see [Safety baseline](safety-baseline.md).
