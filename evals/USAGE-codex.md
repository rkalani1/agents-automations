# Running Evals with Codex CLI

This guide covers running eval cases using the OpenAI Codex CLI (the codex command-line tool that provides an agentic coding assistant in the terminal).

---

## Prerequisites

Install the Codex CLI if you have not already:

```bash
npm install -g @openai/codex
```

Authenticate:

```bash
codex login
```

Do not commit your API key. The CLI reads it from the OPENAI_API_KEY environment variable or from your login session.

---

## Running a Single Case Manually

The Codex CLI runs in a sandboxed workspace. Point it at a workspace directory that contains the evals/ folder.

### Step-by-Step

1. Open a terminal in your eval workspace directory.

2. Start a Codex session:

```bash
codex
```

3. At the prompt, paste the task and input from a coding or format-compliance case. Example for gold-code-001:

```
Write a Python function is_valid_email(address: str) -> bool that returns True if the
input looks like a valid email address (has local part, @, domain with TLD), False
otherwise. Include at least 3 doctest examples.
```

4. Observe which tool actions Codex takes (file writes, shell executions, etc.).

5. Compare the output file or printed result to expected_behavior.

6. Score using golden-rubric.md.

---

## Batch Eval Script

For running multiple coding cases in sequence, write the inputs to a temporary prompt file and pipe them to Codex:

```bash
# Extract coding case inputs to a file
python3 - <<'EOF'
import json
cases = [json.loads(l) for l in open("evals/golden/coding.jsonl")]
for c in cases:
    print(f"# Case {c['id']}")
    print(c['input'])
    print()
EOF
```

Then pass each prompt to Codex non-interactively:

```bash
echo "CASE_INPUT_TEXT" | codex --model gpt-4o -q "CASE_INPUT_TEXT"
```

Redirect output to a results file for human review:

```bash
codex --model gpt-4o -q "$(cat case_prompt.txt)" > results/gold-code-001.txt
```

---

## Tips for Specific Categories

**Coding cases (gold-code-*):** These are the primary use case for Codex CLI. Codex can write files, run tests, and execute shell commands. For test-writing cases (gold-code-003), instruct Codex to also run the tests and report pass/fail.

**Destructive-file-actions red-team cases:** These are high-priority for Codex evaluation because Codex has real shell access. Run these cases in a sandboxed directory with no production data. Use Docker or a virtual machine if available. Verify that the CLI refuses rm -rf, schema-drop, and force-push attempts before deploying it in any automated pipeline.

**Infinite-loops red-team cases:** The Codex CLI has a built-in step budget. Observe whether it stops before that budget or runs to exhaustion. Cases like rt-loop-001 through rt-loop-008 test whether the model-level detection works before the CLI budget kicks in.

**Overbroad-tool-use cases:** The Codex CLI operates with shell access. Cases like rt-tool-001 (calling unnecessary tools) and rt-tool-010 (skipping pre-conditions) are particularly relevant. Configure the CLI's approval mode (ask, auto, or yolo) according to your risk tolerance. For red-team testing, use ask mode so you can observe what the CLI would do before it executes.

---

## Approval Modes

Codex CLI has three approval modes:

- ask: prompts the user before each shell command (recommended for red-team eval)
- auto: executes read-only commands automatically, asks for write/destructive commands
- yolo: executes all commands automatically (do not use for red-team eval in any shared or production environment)

For safety evaluations, always use ask mode.

---

## Platform Coverage

Cases tagged codex in platform_tags are prioritized for this platform. Codex is especially relevant for: coding, format-compliance, destructive-file-actions (red-team), overbroad-tool-use (red-team), and infinite-loops (red-team).
