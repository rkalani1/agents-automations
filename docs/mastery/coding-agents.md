> **Last verified:** 2026-05-06 · **Drift risk:** medium · **Plan annotations:** Free / Sub / Team / Ent / API

# Coding agents mastery

A coding agent is a system that reads your code, makes edits, runs tests, and produces commits with varying degrees of autonomy. This page takes you from the simplest starting point — pasting code into a chat sidebar — through fully autonomous CLI agents that can write, test, and commit features while you do other work. The progression is deliberate: start with the most oversight-heavy tool; add autonomy only after you trust the agent's behaviour in your codebase.

---

## 1. Beginner: Copilot Chat in your editor and on github.com

### What you are looking at

GitHub Copilot integrates into VS Code and JetBrains IDEs as two complementary features: inline ghost text and a chat sidebar. You do not need the CLI for either.

**Ghost text** appears as grey suggested code while you type. Press Tab to accept the full suggestion. Press Escape or keep typing to dismiss it. Ghost text is generated from the surrounding file context. It is useful for boilerplate, repetitive patterns, and completing partially typed expressions.

**Copilot Chat sidebar** is a conversation panel where you describe what you want and Copilot responds with code, explanations, or diffs. To open it:

- VS Code: click the speech-bubble icon in the left Activity Bar, or press `Ctrl+Alt+I` (Windows/Linux) or `Cmd+Option+I` (macOS).
- JetBrains (IntelliJ, PyCharm, etc.): click the Copilot icon in the toolbar or open via the **Tools** menu.

### Slash commands

Inside the chat sidebar, slash commands provide structured shortcuts. Type `/` to see the full list. The most useful ones for beginners:

| Command | What it does |
|---|---|
| `/explain` | Explains the selected code or the open file in plain language |
| `/tests` | Generates unit tests for the selected function or class |
| `/fix` | Proposes a fix for an error, warning, or selected problematic code |
| `/doc` | Generates a docstring or comment block for the selected code |

### Pasting code and copying back patches

If Copilot Chat returns a code block, you have two copy-back options:

1. Click the **copy** icon on the code block to copy the entire snippet to clipboard, then paste it into your editor manually.
2. Click the **Insert at cursor** or **Apply in editor** button (where available) to insert the code at the current cursor position without leaving the chat.

Always review every line before accepting. Copilot does not know which tests are passing, what your broader architecture looks like, or what security constraints your organisation requires.

### Copilot Chat on github.com

Navigate to any repository on github.com that has Copilot enabled. Click the **Copilot** chat icon in the top navigation or on any file view. You can ask questions about the repository, request explanations of specific files, and generate code suggestions, all without opening a local IDE. This is useful for quick code reviews on mobile or when working on an unfamiliar machine.

---

## 2. Intermediate: repository instructions, selection-based chat, and inline edits

### The `.github/copilot-instructions.md` file

Copilot picks up a special file at `.github/copilot-instructions.md` in your repository root and uses it as standing context for every Copilot Chat and coding agent session in that repository. This is the single most important customisation file for teams. ([GitHub Copilot best practices](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results))

Create this file with content that tells the agent about your project:

```markdown
# Project conventions

## Build and test
- Build: `make build`
- Test: `pytest tests/ -v`
- Lint: `ruff check . && mypy .`

## Code standards
- Use Python 3.11+. Follow PEP 8.
- All public functions must have docstrings.
- All new features require unit tests in `tests/` using pytest.
- Do not add new dependencies without updating `requirements.txt`.

## Repository structure
- `src/` — application code
- `tests/` — all test files, mirroring the `src/` layout
- `docs/` — documentation source
```

Keep this file concise and factual. Copilot reads it at the start of every session, so vague instructions waste context tokens. Copilot also recognises `AGENTS.md` and `CLAUDE.md` files in the repository root as additional instruction sources, making instructions portable across coding agents.

### Equivalents for other coding agents

The same concept applies across tools:

| Tool | Instruction file location |
|---|---|
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Code | `CLAUDE.md` in the project root |
| Codex CLI | `AGENTS.md` in the project root (and sub-directories) |
| Gemini Code Assist | `GEMINI.md` |

### Selection-based chat

Select a block of code in your editor, then open Copilot Chat. The selected code is automatically included as context. You can then ask:

- `Explain this function` — Copilot describes what the selected code does, including edge cases.
- `Refactor this to reduce duplication` — Copilot rewrites the selection.
- `What could go wrong here?` — Copilot identifies potential bugs or security issues.

The selection scope is important. Selecting a single function gives a focused answer. Selecting hundreds of lines dilutes the context and produces less precise suggestions.

### Inline edits with Copilot

In VS Code, you can invoke inline edits (also called Copilot Edits or agent mode) from the chat sidebar by switching the chat mode to **Edit** or **Agent** (the exact label depends on the Copilot extension version). In Edit mode, Copilot proposes changes directly in the editor as tracked diffs. You accept or reject each change individually using the diff interface. This keeps you in control while removing the copy-paste step.

---

## 3. Advanced: GitHub Copilot cloud agent

### What the coding agent does

GitHub Copilot cloud agent, formerly called Copilot coding agent, works autonomously inside a GitHub Actions-powered environment. You give it a task, and it researches the repository, creates an implementation plan, makes code changes on a branch, and (optionally) opens a pull request. The entire process runs in the cloud, not on your machine. ([About GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent))

The agent can: fix bugs, improve test coverage, update documentation, resolve merge conflicts, address technical debt, and implement small incremental features. It is not well-suited for broad architectural refactors, tasks requiring cross-repository changes, or anything involving security-critical or production-blocking code.

**Plan note:** Copilot cloud agent is available with GitHub Copilot Pro, Pro+, Business, and Enterprise plans.

### Assigning an issue to Copilot

1. Open any GitHub issue in a repository where Copilot is enabled.
2. In the right sidebar, under **Assignees**, click the gear icon and select **Copilot** from the assignee list.
3. Copilot starts working in the background. A comment appears on the issue confirming it has accepted the task.
4. Alternatively, from the Copilot agents panel on github.com, describe the task directly as a prompt.

### Writing good issue prompts

The quality of the result depends heavily on the quality of the issue. A well-scoped issue includes:

- A clear description of the problem or the work required.
- Explicit acceptance criteria — for example, "the function should return an empty list rather than raising an exception when input is None, and a test should verify this."
- Which files or modules are likely involved, if known.
- How to build and run the tests (or a pointer to `.github/copilot-instructions.md` where this is documented). ([GitHub Copilot best practices](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results))

### Reviewing the resulting PR

When Copilot finishes, it creates a branch and optionally opens a pull request. Review it exactly as you would review a human contributor's PR:

1. Read the diff. Understand every changed line.
2. Run the tests locally or let CI run them.
3. If something is wrong, leave a comment on the PR mentioning `@copilot` and describe the issue. Copilot will push additional commits to address your feedback.
4. Only merge when you are satisfied the diff is correct, tests pass, and no unrelated files were changed.

### Best practices for the coding agent

- Keep issues small and well-scoped. One discrete task per issue produces better results than a large multi-objective task.
- Ensure your CI suite runs on every PR. The agent can build and test in its own ephemeral environment, but your CI is the gatekeeper for merging.
- Mandatory code review is non-negotiable. Every agent-generated PR must be reviewed by a human before merging.
- Add a `copilot-setup-steps.yml` file to pre-install project dependencies so the agent does not waste time discovering them by trial and error. ([GitHub Copilot best practices](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results))

---

## 4. Expert: Claude Code CLI, Codex CLI, MCP, and observability

### Claude Code CLI

Claude Code is Anthropic's terminal-based coding agent. It reads your codebase, edits files, runs commands, and integrates with git. It operates directly in your local environment (or in a container you control). ([Claude Code documentation](https://code.claude.com/docs/en))

**Install:**

```bash
# macOS, Linux, or WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

Verify the install: `claude --version`. Authenticate on first run by following the browser prompt. Requires a Claude Pro, Max, Team, or Enterprise account, or an Anthropic Console API key.

**The CLAUDE.md file:** Create a file named `CLAUDE.md` in your project root. Claude Code reads it at the start of every session. Use it to store build commands, test commands, code standards, architecture notes, and any conventions you want to persist across sessions:

```markdown
# Project: data-pipeline

## Build and test
- Install deps: `pip install -e ".[dev]"`
- Run tests: `pytest tests/ -v --tb=short`
- Type check: `mypy src/`

## Conventions
- Python 3.11. All modules in `src/data_pipeline/`.
- New features require tests in `tests/` with at least one edge case.
- Never hardcode credentials; use environment variables.
```

**Permission modes (most restrictive first):**

Claude Code operates in a permission mode that controls how much it can do without asking you. Start with the most restrictive mode and loosen it only when you are confident in the direction of the session. ([Claude Code permission modes](https://code.claude.com/docs/en/permission-modes))

| Mode | What runs automatically | Best for |
|---|---|---|
| `default` | Reads only | Getting started, unfamiliar codebases, sensitive work |
| `plan` | Reads only; presents a plan before acting | Exploring a codebase before any edits |
| `acceptEdits` | Reads and file edits | Iterating on code you are actively reviewing |
| `auto` | Reads, edits, and commands (with a safety classifier) | Long tasks; requires Max/Team/Ent/API plan |
| `bypassPermissions` | Everything | Isolated containers and VMs only; never use on your main machine |

Run Claude Code with a specific mode: `claude --permission-mode acceptEdits`.

**Slash commands:** Inside a Claude Code session, type `/` to see built-in commands:

| Command | Effect |
|---|---|
| `/help` | Show all available commands |
| `/config` | Configure settings interactively (model, theme, auto-update channel) |
| `/model` | Switch the model for the current session |
| `/allowed-tools` | Review or adjust which tools Claude may use |
| `/hooks` | Configure hooks (shell commands that run before or after agent actions) |
| `/mcp` | Manage MCP server connections |
| `/compact` | Compress conversation context to save tokens |
| `/clear` | Clear conversation history and start fresh |

**Hooks:** Hooks are shell commands that run at deterministic points in the agent's workflow — for example, automatically running `ruff format` after every file edit, or blocking a commit if tests are failing. They are defined in Claude Code settings and are not overridable by the model. Use hooks to enforce quality gates that apply regardless of what the agent is trying to do.

**Subagents:** Claude Code can spawn parallel subagents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results. Invoke this for large tasks by describing the decomposition in your prompt: `Split this task across subagents: one for the API layer, one for the tests, one for the documentation.`

### Codex CLI

OpenAI's Codex CLI is a terminal agent for code tasks that integrates with OpenAI models.

**Install:**

```bash
npm i -g @openai/codex
```

Verify: `codex --version`. On first run, authenticate with your ChatGPT account or an OpenAI API key.

**The AGENTS.md file:** Codex reads `AGENTS.md` files in your project root and sub-directories. This is the Codex equivalent of `CLAUDE.md`. The format is the same: plain Markdown with build commands, test commands, and conventions. Codex also respects `CLAUDE.md` and `.github/copilot-instructions.md` when present.

**Pinning a model:**

```bash
export OPENAI_MODEL="REPLACE_WITH_CURRENT_MODEL"
codex
```

Or in `~/.codex/config.toml`:

```toml
model = os.environ["OPENAI_MODEL"]
```

**Approval modes and sandbox modes (most restrictive first):** Codex separates two concerns: what it is technically allowed to do (sandbox mode) and when it must ask you before acting (approval policy). ([Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security))

Sandbox modes:

| Sandbox mode | Access |
|---|---|
| `read-only` | Can read files; no writes and no shell execution |
| `workspace-write` | Read and write within the current working directory; default for version-controlled folders |
| `danger-full-access` | Unrestricted file and shell access; use only in isolated containers |

Approval policies:

| Policy | Behaviour |
|---|---|
| `untrusted` | Prompt before every action |
| `on-request` | Run automatically within the sandbox; ask only when the agent requests escalation |
| `never` | No prompts; fully autonomous within the sandbox constraints |

The safe default for interactive development is `--sandbox workspace-write --ask-for-approval on-request`. Start there and adjust. Never use `danger-full-access` on your main machine or on a machine with access to production credentials.

**Start with maximum oversight and loosen gradually:**

```bash
# Step 1 — plan only, no changes
codex --sandbox read-only --ask-for-approval on-request

# Step 2 — allow file edits, review shell commands
codex --sandbox workspace-write --ask-for-approval untrusted

# Step 3 — allow edits and trusted commands, review escalations
codex --sandbox workspace-write --ask-for-approval on-request
```

### Antigravity

> **Drift risk: high.** Antigravity is an emerging category of AI coding tool with rapidly changing product positioning. Verify current capabilities at the vendor's site before building workflows around it.

### MCP for coding workflows

The Model Context Protocol (MCP) is an open standard that lets coding agents connect to external tools and data sources — for example, a Jira MCP server that lets the agent read tickets, or a database MCP server that lets the agent query a schema. Both Claude Code (`/mcp`) and Codex CLI support MCP. The GitHub MCP server is available by default with Copilot cloud agent and gives the agent access to issues, pull requests, and repository context.

To add an MCP server in Claude Code:

```bash
claude mcp add my-server --transport stdio -- npx -y @my-org/my-mcp-server
```

Use MCP to extend agents with data sources they cannot reach natively, such as internal wikis, ticketing systems, or proprietary APIs.

### Observability: token cost tracking and per-task evaluation

Running coding agents without measurement leads to runaway costs and regressions. Set up at minimum:

**Token and cost tracking:**

- Monitor API usage in the [OpenAI usage dashboard](https://platform.openai.com/usage) or [Anthropic Console](https://console.anthropic.com) per project.
- Set a per-day or per-session spending limit in your API portal before running long autonomous sessions.
- Log model name, input tokens, output tokens, and task description for every agent run. Review weekly.

**Evaluation per task type:**

Define what "good" looks like before you run a task, then check it after:

| Task type | Evaluation criterion |
|---|---|
| Add tests | Tests pass; no existing tests broken; new tests cover the specified cases |
| Fix a bug | Bug does not reproduce; no regression in related tests |
| Refactor | Tests still pass; diff contains only intended changes; no unrelated file changes |
| Add a feature | Acceptance criteria from the issue met; tests added; documentation updated if required |

Review diffs before accepting or merging. A common agent failure mode is "wide diff" — the agent solves your request but also reformats unrelated files, removes comments, or changes configuration it should not have touched. Narrow the diff to exactly what you asked for.

---

## 5. Level up ladder

1. Open Copilot Chat in VS Code; use `/explain` on a function you wrote last week.
2. Select a function with a bug; use `/fix` and review the suggested diff before accepting.
3. Use `/tests` to generate unit tests for a utility function; run them.
4. Create `.github/copilot-instructions.md` with build and test commands; verify Copilot references them in subsequent sessions.
5. Assign a simple bug-fix issue to the GitHub Copilot cloud agent; review the resulting PR in full.
6. Install Claude Code; run `claude` in a project with `--permission-mode plan`; let it describe what it would change without touching anything.
7. Write a `CLAUDE.md` for your project; verify Claude reads it by asking `what test command should I run?`
8. Switch Claude Code to `acceptEdits` mode; complete a feature addition; review each diff before moving on.
9. Install Codex CLI; create an `AGENTS.md`; run with `workspace-write` sandbox and `on-request` approvals.
10. Add an MCP server to Claude Code or Copilot cloud agent; complete a task that requires data from the connected source; log token usage; write down the evaluation criteria you used.

---

## 6. Guided exercise: add tests to a small Python module

This exercise demonstrates the same task at two levels of the ladder. You need a small Python module (50–200 lines) with at least one function that lacks tests. Use any module you own or create a trivial example.

### Part A: Beginner — Copilot Chat in VS Code

1. Open the Python file in VS Code.
2. Select the function you want to test.
3. Open Copilot Chat (`Cmd+Option+I` or `Ctrl+Alt+I`).
4. Type `/tests`. Copilot generates a test file targeting the selected function.
5. Click **Insert at cursor** or copy the test code into a new file at `tests/test_<module>.py`.
6. Run `pytest tests/test_<module>.py -v`. Note which tests pass, which fail, and which edge cases are missing.
7. Ask a follow-up: `Add a test for the case where the input is an empty list.` Copy the new test in.
8. Record: how many lines did the diff contain? Were any unrelated files changed? How many test cases did Copilot generate versus how many you would have written manually?

### Part B: Expert — Claude Code or Codex CLI

**Using Claude Code:**

1. Open a terminal in the project root.
2. Run: `claude --permission-mode acceptEdits`
3. Type: `Write comprehensive pytest tests for the function <name> in <file>. Tests should cover: happy path, empty input, None input, and at least two edge cases. Place tests in tests/test_<module>.py. Run the tests before finishing and fix any failures.`
4. Claude edits the test file, runs `pytest`, reads the output, and iterates until the tests pass.
5. Review the diff: `git diff`. Confirm only the intended test file was changed.

**Using Codex CLI:**

1. Open a terminal in the project root.
2. Run: `codex --sandbox workspace-write --ask-for-approval on-request`
3. Give the same instruction as above.
4. Approve each proposed action as it appears.
5. Review the diff: `git diff`.

**Compare the two approaches:**

| Criterion | Copilot Chat (Beginner) | Claude Code / Codex (Expert) |
|---|---|---|
| Unrelated file edits | Usually none — you accept manually | Can occur; check `git diff` carefully |
| Test coverage | Good for happy path; may miss edge cases | Better with explicit edge case instructions |
| Feedback loop | Manual copy-paste; you run tests | Agent runs tests and iterates automatically |
| Oversight | High — you review each snippet | Medium to low depending on permission mode |
| Time to complete | 5–15 minutes manual | 1–5 minutes autonomous |

Neither approach is universally better. Use Copilot Chat when you want to stay in the loop and understand every change. Use a CLI agent when you have written a precise prompt, set restrictive permissions, and verified the diff after completion.

---

## 7. Plan availability table

| Feature | Free | Sub (Pro/Pro+) | Team/Business | Ent | API |
|---|---|---|---|---|---|
| Copilot Chat (editor) | No | Yes | Yes | Yes | Via GitHub Models API |
| Ghost text suggestions | No | Yes | Yes | Yes | Not applicable |
| Repository instructions (`.github/copilot-instructions.md`) | No | Yes | Yes | Yes | Not applicable |
| Copilot cloud agent (issue assignment) | No | Yes (Pro/Pro+) | Yes | Yes (admin enable required) | Not applicable |
| Claude Code CLI | No | Yes (Pro or above, or API key) | Yes (Team plan) | Yes | Yes (Console API key) |
| Claude Code `auto` permission mode | No | No (Pro) | Yes | Yes | Yes |
| Codex CLI | No | No | No | No | Yes (OpenAI API key, usage-based) |
| Antigravity | — | — | — | — | Drift risk: high; verify at vendor site |
| MCP (coding agent extensions) | No | Yes (Claude Code) | Yes | Yes | Yes |
| GitHub Models API | Free (rate-limited) | Yes | Yes | Yes | Yes |

## 8. Fallback

If a tool listed above is unavailable on your plan, behind a feature flag, or has changed since this page was last verified, these alternatives apply:

- **No Copilot Chat / ghost text:** Use the AI chat interface in your browser (Perplexity, Claude, ChatGPT). Paste the relevant code block into the chat, describe what you need, and copy the response back into your editor. This is slower but fully free.
- **No repository instructions:** Paste your project conventions as the first message in each chat session manually. Keep a snippet file for this purpose so you do not have to retype it.
- **No Copilot cloud agent:** Use Copilot Chat in Edit mode or your IDE's agent mode with carefully scoped prompts; review each diff before accepting.
- **No Claude Code / Codex CLI (no API key or budget):** Continue with Copilot Chat or browser-based AI chat. Both require more manual effort but produce comparable results for small, well-scoped tasks.
- **No MCP:** Share context manually by pasting relevant excerpts from the external source (a ticket, a database schema, a design document) into the agent chat at the start of the session.

---

For Copilot cloud agent documentation, see [docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent). For best practices, see [docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results). For Claude Code setup, see [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup). For Codex CLI, see [developers.openai.com/codex/cli](https://developers.openai.com/codex/cli). For Codex security and approval modes, see [developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security).
