# Claude Code

> **Last verified:** 2026-05-06 · **Drift risk:** medium
> **Official sources:** [Setup](https://code.claude.com/docs/en/setup), [Quickstart](https://code.claude.com/docs/en/quickstart)

---

## What This Surface Is

Claude Code is Anthropic's terminal-based coding agent. You install it as a command-line tool, open a terminal in any repository, and interact with it in natural language. Claude Code reads your project files as needed, proposes code changes, runs commands, manages git operations, and writes tests—all without you manually feeding it files or explaining the codebase structure.

Claude Code is not the same as Claude Desktop. Claude Desktop is a native app for general-purpose conversations with optional local tool integrations. Claude Code is purpose-built for software development workflows, operates entirely in a terminal, and has deeper integration with your shell, git, and test runners.

---

## Who It Is Best For

- Developers who are comfortable in a terminal and want an AI that can navigate a codebase autonomously
- Teams who want to add Claude Code to CI/CD pipelines via GitHub Actions or GitLab
- Anyone who prefers working outside an IDE and finds chat-based interfaces slow for coding tasks
- Developers on any OS—Claude Code supports macOS, Linux, WSL, and native Windows

---

## Prerequisites

- **Operating system**: macOS 13.0+, Windows 10 1809+ or Windows Server 2019+, Ubuntu 20.04+, Debian 10+, Alpine Linux 3.19+
- **Hardware**: 4 GB RAM minimum, x64 or ARM64 processor
- **Shell**: Bash, Zsh, PowerShell, or CMD. On native Windows, Git for Windows is strongly recommended.
- **Account**: A Claude Pro, Max, Team, Enterprise, or Console account. The free plan does not include Claude Code access per [the setup docs](https://code.claude.com/docs/en/setup). Alternatively, access via Amazon Bedrock, Google Vertex AI, or Microsoft Foundry is supported.
- **Network**: An internet connection. Claude Code does not run fully offline.

---

## Step-by-Step Setup

### 1. Install Claude Code

Choose the method that matches your environment.

**macOS, Linux, or WSL (recommended):**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

Shell confusion note from the [setup docs](https://code.claude.com/docs/en/setup): if you see `The token '&&' is not a valid statement separator`, you are in PowerShell, not CMD. If you see `'irm' is not recognized`, you are in CMD, not PowerShell. Your prompt shows `PS C:\` in PowerShell and `C:\` without the `PS` in CMD.

**Homebrew (macOS):**

```bash
brew install --cask claude-code
```

**WinGet (Windows):**

```powershell
winget install Anthropic.ClaudeCode
```

**npm (Node.js 18+ required):**

```bash
npm install -g @anthropic-ai/claude-code
```

Native installs auto-update in the background. Homebrew, WinGet, and npm installs do not; you must run the upgrade command manually for those.

### 2. Verify the installation

```bash
claude --version
claude doctor
```

`claude doctor` runs a self-check and reports any missing dependencies or configuration problems.

### 3. Log in

Start an interactive session:

```bash
claude
```

On first run, Claude Code prompts you to log in. Follow the browser prompts to authenticate with your Anthropic account. Credentials are stored locally. To switch accounts later, use the `/login` slash command inside a session.

Account types supported per the [quickstart](https://code.claude.com/docs/en/quickstart):

- Claude Pro, Max, Team, or Enterprise (recommended)
- Claude Console (API access with pre-paid credits; a "Claude Code" workspace is created automatically in the Console on first login)
- Amazon Bedrock, Google Vertex AI, or Microsoft Foundry

### 4. Open a project and start a session

```bash
cd /path/to/your/project
claude
```

You will see a welcome screen showing session information, recent conversations, and the latest release notes.

---

## Building Your First Useful Agent: Writing Tests for a Small Repo

This worked example uses a small Python project with a `calculator.py` module that has no tests yet. The goal is to have Claude Code generate a full test suite.

### Starting the session

```bash
cd ~/projects/my-calculator
claude
```

### Understanding the project first

Before asking for changes, let Claude explore:

```
what does this project do?
```

```
explain the folder structure
```

```
what technologies does this project use?
```

Claude reads the files it needs and responds. You do not need to paste code.

### Generating the tests

```
write unit tests for the calculator functions in calculator.py
```

Claude Code will:

1. Read `calculator.py` to understand the functions
2. Check whether a test file already exists
3. Show you the proposed test file
4. Ask for your approval before writing it
5. Optionally run the tests if a test runner is configured

You can refine:

```
add edge case tests for division by zero and overflow
```

```
run the tests and fix any that fail
```

### Committing the result

```
commit my changes with a descriptive message
```

Claude Code uses git on your behalf and writes a commit message that describes what changed.

---

## Customization

### CLAUDE.md

`CLAUDE.md` is a project-level instructions file that Claude Code reads at the start of every session in that directory. Place it at the root of your repository. Use it to encode conventions Claude should follow—test framework preferences, code style rules, commands to run before committing, or context about the project architecture.

Example `CLAUDE.md`:

```markdown
# Project conventions

- Use pytest for all tests. Test files go in tests/.
- Follow PEP 8. Run `ruff check .` before committing.
- Do not modify requirements.txt without asking first.
- The main entry point is src/main.py.
```

This is analogous to a `GEMINI.md` file in the Gemini CLI, or a system prompt in a chat interface. It persists across sessions and does not consume interactive context budget.

### Slash commands

Inside a session, type `/` to see all available commands. Commonly useful ones per the [quickstart](https://code.claude.com/docs/en/quickstart):

| Command | What it does |
|---------|-------------|
| `/help` | Show available commands |
| `/login` | Switch accounts |
| `/clear` | Clear conversation history for the current session |
| `/resume` | Continue a previous conversation |

### /init

Running `/init` (if available in your version) analyzes the repository and generates a starter `CLAUDE.md` file based on what it finds. This is a useful shortcut for existing projects.

### One-shot commands

You can drive Claude Code non-interactively from a shell script:

```bash
# Run a task and exit
claude "write unit tests for src/calculator.py"

# Run a one-off query and print the result, then exit
claude -p "summarize the authentication module"

# Continue the most recent conversation in this directory
claude -c
```

The `-p` flag is useful in scripts where you want to capture Claude's output as a string.

---

## Limits and Gotchas

- **Requires a paid plan.** The free Claude.ai tier does not include Claude Code access per the [setup docs](https://code.claude.com/docs/en/setup). Verify current plan eligibility at [claude.ai/upgrade](https://claude.ai/upgrade).
- **Sandboxing is WSL-only.** Command execution sandboxing is supported only in WSL 2 on Windows. Native Windows runs without sandboxing. Keep this in mind when running arbitrary shell commands.
- **Git for Windows is not optional on native Windows.** Without it, Claude Code falls back to PowerShell for shell commands, which limits what it can do. Install Git for Windows before using Claude Code on a native Windows machine.
- **Auto-updates only apply to the native installer.** Homebrew, WinGet, apt, dnf, apk, and npm installations do not update automatically. Run the appropriate upgrade command periodically.
- **Alpine Linux requires extra dependencies.** You must install `libgcc`, `libstdc++`, and `ripgrep`, and set `USE_BUILTIN_RIPGREP=0` in `settings.json` before installing on Alpine per the [setup docs](https://code.claude.com/docs/en/setup).
- **Context limits apply.** Claude Code reads files as needed, but very large repositories or many open files will approach context window limits. The `/clear` command resets conversation history if you notice degraded quality.
- **Always asks before modifying files by default.** Claude Code will not silently edit files. You can enable "Accept all" mode for a session to skip individual approvals, but this means changes will be applied without your review.

---

## Confirmed by Docs vs. Practical Inference

| Claim | Status |
|-------|--------|
| Native install command (curl \| bash) | Confirmed by [setup docs](https://code.claude.com/docs/en/setup) |
| Homebrew and WinGet install commands | Confirmed by [setup docs](https://code.claude.com/docs/en/setup) |
| npm install via `@anthropic-ai/claude-code` | Confirmed by [setup docs](https://code.claude.com/docs/en/setup) |
| Free plan does not include Claude Code | Confirmed by [setup docs](https://code.claude.com/docs/en/setup) |
| `/login`, `/clear`, `/help`, `/resume` commands | Confirmed by [quickstart](https://code.claude.com/docs/en/quickstart) |
| CLAUDE.md as project instructions file | Referenced indirectly; behavior is consistent with documented "custom skills" and project context patterns |
| `/init` command generating CLAUDE.md | Practical inference; not explicitly confirmed in the pages fetched—verify with `claude /help` |
| WSL 2 required for sandboxing | Confirmed by [setup docs](https://code.claude.com/docs/en/setup) Windows table |
| Claude Code available in GitHub Actions | Mentioned in [quickstart](https://code.claude.com/docs/en/quickstart) ("available... in CI/CD with GitHub Actions") |

---

## Cost and Rate-Limit Notes

Claude Code usage counts against your plan's usage allowance. Complex sessions with many file reads, shell commands, and multi-step tasks consume allowance faster than plain conversation. Claude Console accounts (API-based) incur per-token charges. If you hit usage limits during a session, Claude Code will notify you; you can continue after the limit resets or upgrade your plan. Specific prices are not listed here—check [claude.ai/upgrade](https://claude.ai/upgrade) for current rates.

---

## Where to Go Next

- [Claude Desktop](claude-desktop.md) — for local tool integrations outside a coding workflow
- [Claude Projects](claude-projects.md) — for persistent system instructions in the browser interface
- [Claude Code setup docs](https://code.claude.com/docs/en/setup) — for advanced installation options, binary integrity verification, and enterprise deployment
