# First MCP Agent: Summarize Local Files with Claude Desktop

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Use case

You want Claude Desktop to be able to read files in a specific local folder and produce a summary of their contents — but with no access to any other part of your filesystem. This quickstart introduces the Model Context Protocol (MCP), a standard interface that lets AI assistants call local tools safely. The filesystem MCP server, scoped to a single sandbox directory, is the simplest possible MCP configuration and a good starting point before adding more capable servers.

Target completion time: 25–40 minutes.

---

## Best platform choice and why

**Primary: Claude Desktop + [MCP filesystem server](https://github.com/modelcontextprotocol/servers)**

Claude Desktop has built-in support for MCP servers, configured via a single JSON file. The official MCP filesystem server is maintained by Anthropic and implements a read-only filesystem interface that you can scope to one or more directories. This combination requires no coding: you install Node, edit one config file, and restart the app.

The filesystem server is deliberately minimal. It exposes file listing and file reading. It does not expose file writing, deletion, or network access. This makes it appropriate for a first MCP exercise where the goal is to understand the configuration pattern without taking on write risk.

For background on local MCP servers in Claude Desktop, see the [official getting started guide](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).

---

## Prerequisites

- Claude Desktop installed and running (download from [claude.ai/download](https://claude.ai/download)).
- Node.js 18 or later installed (`node --version` to check). The filesystem MCP server is a Node package run via `npx`.
- A sandbox directory created specifically for this exercise. Do not use your home directory or any directory containing sensitive files.
- 3 short Markdown files to place in the sandbox directory (use the examples from the Example input section below or your own).

---

## Setup steps

1. Create the sandbox directory and add the sample files:
   ```bash
   mkdir -p ~/agent-sandbox
   ```
   Place three Markdown files in `~/agent-sandbox/` (see Example input below).

2. Locate the Claude Desktop configuration file.

   On macOS:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   On Windows:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

   If the file does not exist, create it. If it exists, open it in a text editor.

3. Add the filesystem server configuration from the Copyable instructions section below. If `claude_desktop_config.json` already has content, merge the `mcpServers` block into the existing JSON rather than replacing the entire file.

4. Save the file, then fully quit and relaunch Claude Desktop. The MCP server is loaded at startup; changes are not picked up without a restart.

5. Open a new conversation in Claude Desktop. In the toolbar below the message input, you should see a tools icon (a hammer or wrench symbol). Click it to confirm that `filesystem` tools are listed. If the tools do not appear, see the troubleshooting section.

6. Paste the user prompt from the Copyable instructions section to run the first test.

---

## Copyable instructions

### `claude_desktop_config.json` — filesystem server block

Add this to your config file. Replace `/Users/you/agent-sandbox` with the absolute path to your actual sandbox directory. On Windows, use a Windows-style path such as `C:\\Users\\you\\agent-sandbox` (note double backslashes in JSON).

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/you/agent-sandbox"
      ]
    }
  }
}
```

This configuration tells Claude Desktop to start the [MCP filesystem server](https://github.com/modelcontextprotocol/servers) when it launches, scoped to the single directory you specify. The `-y` flag on `npx` allows the package to be downloaded automatically if it is not already cached locally.

If you have an existing `claude_desktop_config.json` with other servers configured, add `"filesystem": { ... }` as an additional entry inside the existing `"mcpServers"` object rather than creating a second `"mcpServers"` key.

### User prompt (paste into a Claude Desktop conversation)

```
Using the filesystem tools, list all files in the sandbox directory, then read each one and produce a structured summary.

Format the summary with these sections:
## Files Found
## Summary of Each File
## Common Themes

Under "Files Found", list filenames only.
Under "Summary of Each File", write 2-3 sentences about each file individually.
Under "Common Themes", identify 1-3 themes that appear across multiple files.

Important: only read files you found in the sandbox directory. Do not attempt to read any file outside that location.
```

---

## Example input

Create these three files in `~/agent-sandbox/`:

**`~/agent-sandbox/team-norms.md`**
```markdown
# Team Norms

We write documentation before code, not after.
Code reviews are expected to be completed within one business day.
All breaking changes require a migration guide in the same pull request.
Meetings over 30 minutes require a written agenda shared 24 hours in advance.
```

**`~/agent-sandbox/onboarding-checklist.md`**
```markdown
# New Hire Onboarding Checklist

Week 1: Set up development environment, read the architecture overview, meet with each team member.
Week 2: Complete first good-first-issue ticket with a pair programming session.
Week 3: Lead a standup for the first time, begin solo ticket work.
All new hires should have access to the internal wiki and the staging environment by day 2.
```

**`~/agent-sandbox/engineering-principles.md`**
```markdown
# Engineering Principles

Prefer reversible decisions over irreversible ones.
Optimize for readability over cleverness.
Small, frequent deploys reduce risk compared to large batch releases.
Documentation is a first-class artifact, not a post-launch chore.
Automate the thing you do more than twice.
```

---

## Expected output

Claude Desktop should use the filesystem tools — you will see tool calls appear inline in the conversation — and then produce a response structured like this:

```
## Files Found
- team-norms.md
- onboarding-checklist.md
- engineering-principles.md

## Summary of Each File

**team-norms.md**: Describes four behavioral norms for the team covering documentation 
timing, code review turnaround, change management, and meeting preparation. Emphasizes 
process and written communication.

**onboarding-checklist.md**: A week-by-week onboarding plan for new hires spanning 
three weeks. Covers environment setup, first contributions, and early independence. 
Notes that infrastructure access should be available within the first two days.

**engineering-principles.md**: Five engineering philosophy statements covering 
decision-making, code quality, deployment cadence, documentation, and automation. 
Prioritizes safety, readability, and sustainable habits.

## Common Themes
1. Written documentation is treated as a primary deliverable, not an afterthought.
2. Process norms are designed to reduce risk and increase predictability.
3. New contributors and existing team members are both expected to work incrementally.
```

---

## Safety boundaries

- Scope filesystem access to one directory only. The config above passes a single directory path as the argument to the server. Do not pass `/` (the root), `~` (the home directory), or any path that contains credentials, private keys, or personal data.
- Never include credentials in the config file. The `claude_desktop_config.json` is a plain text file. Do not put API keys, passwords, or tokens in it.
- This kit has no network egress. The filesystem MCP server does not make outbound network calls. It only reads the local filesystem within its scoped path.
- Do not add write-capable servers in the same config for this exercise. Adding servers like a database connector or a shell-execution server alongside this one changes the risk profile significantly. Complete this quickstart with only the filesystem server active.
- Do not run MCP servers as root or with elevated privileges.
- Do not place the `claude_desktop_config.json` itself inside the sandbox directory. The agent should not be able to read its own configuration.

---

## Eval / check steps

After the agent responds:

1. **Tool list check.** Before sending any prompt, click the tools icon in Claude Desktop and confirm that only filesystem-related tools are listed (typically `list_directory`, `read_file`, and similar). If you see tools from other servers you did not intend to activate, review your config file for unintended entries.

2. **Path containment check.** Ask the agent directly: "Can you read the file `/etc/hosts`?" (on macOS/Linux) or `"C:\\Windows\\System32\\drivers\\etc\\hosts"` (on Windows). The agent should refuse or report that it cannot access that path, because it is outside the scoped directory. If it succeeds, the server is not scoped correctly — stop and re-check your config.

3. **No network egress check.** This server makes no outbound calls by design. If you want to verify this formally, use a network monitoring tool (such as `lsof -i` on macOS or Resource Monitor on Windows) to confirm no unexpected connections are made during the agent run.

---

## Troubleshooting

**The tools icon does not appear after restarting Claude Desktop.**
The most common cause is a JSON syntax error in `claude_desktop_config.json`. Open the file in a text editor with JSON syntax highlighting and look for: missing commas between entries, unmatched braces, or single quotes instead of double quotes (JSON requires double quotes). Validate the file with a JSON linter such as [jsonlint.com](https://jsonlint.com) before restarting again.

**Config path on Windows is not found.**
On Windows, `%APPDATA%` resolves to a path like `C:\Users\YourName\AppData\Roaming`. If you cannot locate the file, open a Command Prompt and run `echo %APPDATA%` to get the exact path, then navigate to `%APPDATA%\Claude\claude_desktop_config.json`.

**Claude Desktop started but the filesystem tools are not listed.**
Check that Node.js is installed and that `npx` is on the system PATH. Run `npx --version` in a terminal to confirm. If `npx` is not found, install Node.js from [nodejs.org](https://nodejs.org) and restart your terminal and Claude Desktop. Also confirm that the path you passed to the server actually exists on disk.

**The agent reads files outside the sandbox directory.**
This should not be possible with a correctly scoped server. If it happens, verify that the path in your config exactly matches the sandbox directory (no typos, correct separator for your OS). On Windows, ensure you are using double backslashes or forward slashes in the JSON string.

**Restart is not picked up.**
Claude Desktop must be fully quit — not just the window closed. On macOS, right-click the Dock icon and choose Quit, or use Cmd+Q. On Windows, use the system tray to exit fully. Then relaunch. Config changes require a full restart.

---

Where to go next: return to the [Quickstarts index](./index.md) for a summary of all five patterns, or explore the [MCP servers repository](https://github.com/modelcontextprotocol/servers) for additional official servers — database connectors, git tools, and more.
