# Local Scripts and Schedulers

> **Last verified:** 2026-05-06 · **Drift risk:** low — the underlying patterns (Python scripts, environment variables, cron) are stable; API SDK details may drift
> **Official sources:** [openai/openai-agents-python on GitHub](https://github.com/openai/openai-agents-python), [OpenAI API reference](https://platform.openai.com/docs/api-reference)

---

## What this surface is

A local script is a Python (or other language) file that you run on your own machine or server. It calls an LLM API directly, uses your own tools and file system, and produces output that you inspect. A scheduler is a mechanism that runs that script automatically at a fixed time or interval — cron on Linux/macOS, launchd on macOS, or Windows Task Scheduler on Windows.

This page covers:

1. How to write a Python script that calls the OpenAI API.
2. How to manage credentials safely.
3. How to test the script thoroughly before automating it.
4. How to wire it to a scheduler — as a deliberate, opt-in step that you take only after the script is stable and reviewed.

**Read this warning before continuing:** Scheduled scripts that call an LLM API run automatically, without a human reviewing each execution. They consume API credits silently. They write to files, send output, or take actions on your behalf without prompting you. A script that looks fine in three manual tests can behave unexpectedly on edge-case inputs, when your notes folder is empty, or when the API returns an error. Do not add a scheduler entry until you have run the script manually at least three times and reviewed the output each time.

---

## Who it is best for

- Developers comfortable with the command line who want a lightweight automation that runs on their own machine.
- Teams that need a simple recurring task (digest, summary, audit) and do not want to deploy a hosted service.
- Anyone learning how API-based agents work before committing to a more complex platform.

---

## Prerequisites

- Python 3.9 or newer.
- An OpenAI API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
- The `openai` package (or `openai-agents` for the full SDK):

```bash
pip install openai
```

- A folder of Markdown notes (for the worked example). The script uses `.md` files as input. An empty folder is valid — the script handles it gracefully.

---

## Credential management

Never put API keys directly in your script source code. Even in a private repository, this is a security risk: keys can leak through shell history, log files, error messages, or accidental commits.

### Option 1: environment variable (simplest)

```bash
export OPENAI_API_KEY="sk-..."
```

Set this in your shell profile (`~/.zshrc`, `~/.bashrc`) or in a terminal session before running the script. The script reads it with `os.environ.get("OPENAI_API_KEY")`.

### Option 2: `.env` file with `python-dotenv`

Create a `.env` file in your project directory:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL
```

Add `.env` to your `.gitignore` immediately:

```bash
echo ".env" >> .gitignore
```

Read it in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("OPENAI_API_KEY")
```

Install `python-dotenv`:

```bash
pip install python-dotenv
```

### Option 3: direnv (per-directory automatic loading)

`direnv` loads a `.envrc` file automatically when you `cd` into a directory and unloads it when you leave. This keeps credentials scoped to the directory and avoids polluting your global shell environment. See [direnv.net](https://direnv.net) for installation.

```bash
# .envrc
export OPENAI_API_KEY="sk-..."
```

Allow it once:

```bash
direnv allow .
```

### Option 4: a secrets manager

Tools like `pass` (GPG-based, Linux/macOS) or the 1Password CLI (`op`) let you retrieve secrets at runtime without storing them in plain text anywhere on disk. The pattern is:

```bash
export OPENAI_API_KEY=$(op read "op://Personal/OpenAI API Key/credential")
```

This is the most secure option for sensitive keys but requires more setup. Use this if the script is running on a shared machine or in a context where disk encryption is not guaranteed.

**General rule:** the secret should exist in exactly one place, have no unencrypted copies, and not appear in any log or version control history.

---

## The worked example: a 20-line Markdown digest script

This script reads a folder of Markdown notes, sends them to an LLM, and asks for a daily digest summary.

```python
#!/usr/bin/env python3
"""daily_digest.py — Summarize a folder of Markdown notes with an LLM.

Usage:
    NOTES_DIR=/path/to/notes OPENAI_API_KEY=sk-... OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL python daily_digest.py

Output: Prints a plain-text daily digest to stdout.
"""

import os
import sys
from pathlib import Path
from openai import OpenAI

NOTES_DIR = Path(os.environ.get("NOTES_DIR", "./notes"))
MAX_CHARS = 12000  # Rough limit to stay well within context window

def collect_notes(directory: Path) -> str:
    if not directory.exists():
        return ""
    parts = []
    for md_file in sorted(directory.glob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if content:
            parts.append(f"### {md_file.name}\n{content}")
    return "\n\n".join(parts)

def generate_digest(notes_text: str) -> str:
    client = OpenAI()  # Reads OPENAI_API_KEY from environment automatically
    if not notes_text:
        return "No notes found in the specified directory."
    truncated = notes_text[:MAX_CHARS]
    model = os.environ.get("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Set OPENAI_MODEL to a current model ID before running.")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a personal assistant. Given a collection of Markdown notes, "
                    "produce a concise daily digest. List the main topics covered, "
                    "highlight any action items or decisions, and flag anything time-sensitive. "
                    "Write in plain prose. No bullet points unless listing action items."
                ),
            },
            {"role": "user", "content": f"Here are today's notes:\n\n{truncated}"},
        ],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    notes = collect_notes(NOTES_DIR)
    digest = generate_digest(notes)
    print(digest)
```

### How to run it manually

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="REPLACE_WITH_CURRENT_MODEL"
export NOTES_DIR="/path/to/your/notes"
python daily_digest.py
```

Read the output. Check:

- Does it correctly summarize your notes?
- Does it handle edge cases (empty folder, very short notes, notes with unusual formatting)?
- Are there any error messages?
- Is the API call cost reasonable for the note length?

**Run it manually at least three times on different days or with different input before adding any scheduling.** Understand what it does on empty input, on long input, and on notes that contain ambiguous content.

---

## Testing before scheduling

### What to check

1. **Empty input:** What happens when `NOTES_DIR` contains no `.md` files? The script above returns a "No notes found" message. Verify this is acceptable behavior for your scheduler (it will not fail silently).
2. **Large input:** What happens when the notes total more than `MAX_CHARS`? The script truncates. Verify the truncated output is still useful.
3. **API errors:** Simulate an error by setting `OPENAI_API_KEY` to an invalid value. The OpenAI client will raise an `AuthenticationError`. Decide how you want the script to handle this — at minimum, it should exit with a non-zero status code so the scheduler knows it failed.
4. **Encoding issues:** Notes with non-ASCII characters (accented characters, CJK) should be tested. The script uses `encoding="utf-8"` which handles most cases.
5. **Cost per run:** For a folder of typical notes, estimate the number of tokens sent and received. Multiply by the selected model's current per-token rate from the provider pricing page. If your notes folder grows, costs grow with it.

### Add basic error handling before scheduling

```python
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def generate_digest(notes_text: str) -> str:
    try:
        # ... (as above)
    except Exception as e:
        logging.error("API call failed: %s", e)
        sys.exit(1)
```

A scheduler that catches non-zero exit codes can alert you or log the failure. Without this, a failed run is invisible.

---

## How to wire it to a scheduler — opt-in step

Only proceed here after completing at least three successful manual runs and reviewing the output.

### cron (Linux and macOS)

cron runs scripts on a schedule defined in a crontab. To edit your crontab:

```bash
crontab -e
```

A cron entry to run the digest at 7:00 AM every day:

```
0 7 * * * OPENAI_API_KEY=sk-... OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL NOTES_DIR=/path/to/notes /usr/bin/python3 /path/to/daily_digest.py >> /path/to/digest.log 2>&1
```

**Warnings specific to cron:**

- cron runs in a minimal environment. Your shell profile is not sourced. Set all required environment variables explicitly in the cron entry or in a wrapper shell script that sources them.
- Do not put your API key directly in the crontab if other users can read it (`crontab -l` may be visible). Use a wrapper script that reads from a credentials file with restricted permissions (`chmod 600`).
- The `>> /path/to/digest.log 2>&1` appends both stdout and stderr to a log file. Without this, you will never know if the script failed.
- cron does not send you notifications on failure unless you configure `MAILTO` at the top of the crontab.

A safer pattern using a wrapper script:

```bash
#!/bin/bash
# run_digest.sh — source credentials and run script
set -e
source /home/youruser/.secrets/openai.env   # chmod 600 this file
export NOTES_DIR="/path/to/notes"
/usr/bin/python3 /path/to/daily_digest.py
```

```
0 7 * * * /path/to/run_digest.sh >> /path/to/digest.log 2>&1
```

### launchd (macOS)

launchd is the macOS system for scheduling recurring tasks. Create a plist file at `~/Library/LaunchAgents/com.yourname.digest.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.yourname.digest</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/path/to/daily_digest.py</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>OPENAI_API_KEY</key>
    <string>sk-...</string>
    <key>NOTES_DIR</key>
    <string>/path/to/notes</string>
  </dict>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>7</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/path/to/digest.log</string>
  <key>StandardErrorPath</key>
  <string>/path/to/digest.err.log</string>
</dict>
</plist>
```

Load the agent:

```bash
launchctl load ~/Library/LaunchAgents/com.yourname.digest.plist
```

**Warning:** The `EnvironmentVariables` key in a plist stores credentials in plain text in a file on disk. For better security, use a wrapper script that reads from a `chmod 600` credentials file, the same as the cron approach above.

### Windows Task Scheduler

On Windows, open Task Scheduler and create a new task:

1. Set the trigger to "Daily" at your chosen time.
2. Set the action to run `python.exe` with the script path as the argument.
3. Set environment variables in the task's settings or use a `.bat` wrapper script that sets them before calling `python`.

Use the Windows Credential Manager or a `chmod`-equivalent (NTFS permissions) to restrict access to any file containing the API key.

---

## Limits and gotchas

- **Silent cost accumulation.** The script runs without asking you. If your notes folder grows from 10 files to 500 files, so does the token count and cost. Implement a `MAX_CHARS` guard (as shown) and add a cost-ceiling check if needed.
- **Credential leakage in log files.** If your script ever prints the API key (e.g., in an error traceback), that key appears in your log file. Avoid logging the key or any headers that contain it. Use a secrets manager that never puts the key in an environment variable visible in process listings on shared machines.
- **Scheduler environment is minimal.** cron and launchd do not source your shell profile. Any command or path that works interactively may fail in a scheduled context. Test your wrapper script by running it directly before scheduling it.
- **No retry logic by default.** If the API is temporarily unavailable, the script fails and produces no digest. Add retry logic with exponential back-off for production use.
- **Output goes nowhere unless you capture it.** Redirect stdout and stderr to a log file. Review the log regularly.
- **The `MAX_CHARS` truncation is blunt.** If important notes are in files that sort late alphabetically and your folder is large, they may be truncated. Consider sorting by modification date or implementing smarter chunking for production use.

---

## Confirmed by docs vs. practical inference

| Claim | Source |
|---|---|
| `client = OpenAI()` reads `OPENAI_API_KEY` from environment | [Confirmed — OpenAI API reference](https://platform.openai.com/docs/api-reference) |
| `pip install openai` installs the client library | [Confirmed — OpenAI API reference](https://platform.openai.com/docs/api-reference) |
| `python-dotenv` loads `.env` files | [Confirmed — python-dotenv project docs](https://pypi.org/project/python-dotenv/) |
| cron runs in a minimal environment without shell profile | [Confirmed — standard cron behavior, POSIX] |
| launchd plist format for macOS scheduling | [Confirmed — Apple developer documentation] |
| `chmod 600` restricts file read permissions to owner | [Confirmed — standard POSIX file permissions] |
| Three manual runs before scheduling — specific number | **Practical inference** — this is a judgment call based on common practice; not a documented standard |
| `MAX_CHARS = 12000` stays within context window | **Practical inference** — conservative limit based on typical model context windows; not a documented API constraint |
| Cost accumulation proportional to folder size | **Practical inference** — follows from token-based pricing; not an API guarantee |

---

## Cost and rate-limit notes

This script uses the OpenAI Chat Completions API directly. Each run sends your notes as input tokens and receives a summary as output tokens. Set `OPENAI_MODEL` to a current model ID from the [OpenAI model documentation](https://platform.openai.com/docs/models), then estimate cost from the current pricing page before enabling scheduling. Scheduled runs accumulate: 365 days of daily runs at even a small per-run cost adds up. Set a usage alert in the [OpenAI platform dashboard](https://platform.openai.com/settings/organization/billing) before enabling scheduling.

---

## Where to go next in this guide

- For a programmatic agent with multiple tools, handoffs, and tracing, see [OpenAI API and Agents SDK](openai-api.md).
- For a terminal-based coding agent that works interactively inside a repository, see [Codex CLI](codex.md).
- For a no-code interface to the same underlying models, see [ChatGPT Projects](chatgpt.md).
