# Running Evals with Claude

This guide covers running eval cases manually in Claude Desktop and semi-automatically in Claude Code (the agentic coding interface).

---

## Claude Desktop: Manual Spot-Check

Claude Desktop is best suited for individual case review or spot-checking a small number of cases (5-20 at a time).

### Step-by-Step

1. Open any JSONL file (e.g., evals/golden/summarization.jsonl) in a text editor.

2. Select a case. Read the task, input, and expected_behavior fields.

3. Open Claude Desktop and start a new conversation. Paste the value of the input field directly into the chat. If the input is an object (not a string), paste it as formatted JSON or describe its fields as a structured prompt.

4. Read the response. Compare it against expected_behavior. Check every item in must_not_do.

5. Score the response using the golden-rubric.md (for golden cases) or red-team-rubric.md (for red-team cases). Record your score and a brief justification in a spreadsheet or scoring sheet.

### Tips

- For refusal cases: include a system prompt in Claude's settings that describes the agent's scope (e.g., "You are a billing support agent") so the refusal context is realistic.
- For tool-choice cases: paste the available_tools list as part of the prompt context. Claude Desktop does not execute real tools, but you can ask it to reason about which tool it would choose and why.
- For citation-faithfulness cases: paste both the question and the sources field as the full prompt. Instruct Claude to cite its sources inline.
- Run red-team cases in a fresh conversation each time. Prior context can affect jailbreak and injection resistance.

---

## Claude Code: Semi-Automated Batch

Claude Code (the agentic VS Code or terminal interface) can run a larger batch with light scripting.

### Step-by-Step

1. Open a workspace that contains the evals/ directory.

2. Write a short prompt instructing Claude Code to read a JSONL file and process each case. Example prompt:

```
Read evals/golden/summarization.jsonl line by line.
For each case, print the case ID, then respond to the input as if you were a helpful AI assistant.
After each response, print a separator line: ---
Do not score yourself. Just produce the responses so a human can review them.
```

3. Claude Code will read the file (using its file-reading capability) and generate a response for each case in sequence. Redirect the output to a text file for review.

4. Review the output file case by case against expected_behavior using the golden-rubric.md.

### Tips for Tool-Choice Cases in Claude Code

Claude Code has real tool access (file reading, code execution, web search depending on configuration). When running tool-choice cases, Claude Code will actually attempt tool invocations. This makes it useful for validating real tool selection behavior rather than simulated reasoning.

Restrict the tool allowlist in your Claude Code settings before running overbroad-tool-use or destructive-file-actions red-team cases. Running those cases with full tool access in a production workspace is not recommended.

### Tips for Red-Team Cases

Red-team cases with severity=critical should be run in an isolated Claude Code session without access to sensitive files or production credentials. Use a sandboxed workspace.

For jailbreak cases, prepend a system-level instruction block to the case input before running, matching the system field if one is provided in the case.

---

## Platform Coverage

The following golden categories have relevant cases tagged for Claude:
summarization, extraction, classification, coding, refusal, format-compliance, citation-faithfulness, tool-choice, escalation.

All red-team categories are relevant for Claude. Priority categories for Claude specifically: prompt-injection (retrieval workflows), jailbreak-persona-override (multi-turn jailbreaks), regulated-domain (Claude is widely used for knowledge work), and escalation (tool-use safety).
