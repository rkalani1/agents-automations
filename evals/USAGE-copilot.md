# Running Evals with GitHub Copilot

This guide covers running eval cases with GitHub Copilot, primarily the Copilot coding agent in VS Code and GitHub.com. Note that Copilot is harder to script programmatically than standalone API-based agents. Most eval use with Copilot will be manual or semi-manual.

---

## Caveats

GitHub Copilot is a tightly integrated IDE tool, not a standalone API with a simple request/response interface. Running eval cases programmatically against Copilot requires GitHub Copilot Workspace (available on GitHub.com) or the VS Code extension with the API Access preview feature. Most teams will use Copilot evals manually.

Copilot does not support a configurable system prompt in the same way that Claude or ChatGPT do. The "agent" behavior is shaped by the repository context, the open files, and the workspace configuration. This means eval cases that assume a specific system prompt context need to be adapted.

---

## VS Code Copilot Chat: Manual Spot-Check

### Step-by-Step

1. Open VS Code with the GitHub Copilot extension installed and authenticated.

2. Open the evals/ directory as a VS Code workspace.

3. Open Copilot Chat (Ctrl+Shift+I or the chat icon).

4. Select a coding, format-compliance, or refusal case from the relevant JSONL file.

5. Paste the input value into the Copilot Chat window. For coding cases, prefix with @workspace to give Copilot access to the workspace context.

6. Observe the response. Compare to expected_behavior.

7. Score using golden-rubric.md.

---

## Copilot Inline Suggestions: Coding Cases

For coding eval cases (gold-code-*), a natural test method is to use Copilot's inline suggestion feature:

1. Create a new file (e.g., eval_task.py).

2. Write a comment or function signature that matches the input field of the case. For example, for gold-code-001:

```python
# Write a function is_valid_email(address: str) -> bool
# Returns True if address has local part, @, and domain with TLD
# Include at least 3 doctest examples
def is_valid_email(address: str) -> bool:
```

3. Wait for Copilot's suggestion (Tab to accept).

4. Compare the suggestion to expected_behavior. Run the doctests to verify correctness.

---

## Copilot Workspace (GitHub.com): Agent Tasks

Copilot Workspace on GitHub.com supports agent-style task execution. It is the closest Copilot equivalent to a standalone coding agent.

### Step-by-Step

1. Open a repository on GitHub.com that contains the evals/ directory.

2. Create a new Issue describing the coding task from a golden eval case.

3. Click "Open in Copilot Workspace." Copilot will plan and propose code changes.

4. Review the proposed plan and implementation. Compare to expected_behavior.

5. For red-team cases (particularly destructive-file-actions): draft an issue with the red-team input and observe whether Copilot Workspace refuses, warns, or proceeds. Do not merge any branch created by a red-team test run.

---

## Tips for Specific Categories

**Coding cases:** Best coverage. Copilot is designed for code generation and bug fixing. Run gold-code-001 through gold-code-015 manually using either inline suggestions or Copilot Chat.

**Format-compliance cases:** Copilot Chat can produce JSON, YAML, and Markdown tables. Test these by pasting the format specification and content into chat. Note that Copilot sometimes wraps output in code fences even when not requested; check format-compliance criterion 3/4 accordingly.

**Refusal cases:** Copilot has content policies but does not support a custom system prompt. Refusal behavior will reflect Copilot's default policies rather than an agent-defined scope. Treat these as baseline refusal tests rather than scope-enforcement tests.

**Destructive-file-actions (red-team):** Copilot Workspace can create PRs and modify files in a repository. Run destructive red-team cases in a throwaway fork. Verify that Copilot does not create a PR that executes rm -rf, drops schemas, or force-pushes to main.

**Scripting limitation:** There is no public API to submit arbitrary prompts to Copilot and collect responses in bulk. If your team has access to the GitHub Copilot API Access preview, refer to GitHub's API documentation for batch automation. Otherwise, use the OpenAI API (USAGE-programmatic.md) as a proxy for automated batch evals on coding cases.

---

## Platform Coverage

Cases tagged copilot in platform_tags are prioritized for this platform: coding, format-compliance, and destructive-file-actions (red-team). Cases requiring a configurable system prompt or explicit tool allowlist are best tested on Claude, OpenAI, or Gemini instead.
