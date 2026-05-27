# First Coding Agent: Add Tests to a Python Module

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Use case

You have a small Python module with several public functions and no test coverage. You want a coding agent to read the module, generate a pytest test suite covering all public functions including edge cases, and produce a short summary of what was written. The agent must not modify the implementation — only add tests.

Target completion time: 30–50 minutes.

---

## Best platform choice and why

**Primary: [Codex CLI](https://developers.openai.com/codex/cli)**

Codex CLI is OpenAI's command-line coding agent. It runs locally, operates on files in your working directory, supports approval mode so you can inspect changes before they are written, and is straightforward to scope to a single task via its prompt interface. For test generation specifically, Codex CLI is a practical choice because the task is bounded and deterministic: the agent reads one file and writes one new file. There is minimal risk of unintended side effects compared to a more open-ended agentic task.

**Alternatives:**

- [Claude Code](https://code.claude.com/docs/en/quickstart): Nearly identical capability and workflow. If you have already completed the file-editing quickstart, the setup will be familiar. Claude Code's `CLAUDE.md` makes it easy to add a machine-readable constraint file.
- Cursor: A VS Code-based IDE with an integrated agent. Good if you prefer a graphical interface. Less scriptable than CLI tools.
- GitHub Copilot agent mode: Available inside VS Code. Convenient if Copilot is already part of your workflow, but harder to run in a fully isolated environment.

---

## Prerequisites

- Python 3.10 or later.
- `pip` and the ability to create a virtual environment.
- An OpenAI API key in the environment variable `OPENAI_API_KEY`.
- Codex CLI installed (see setup steps below).
- Git initialized in your test directory.

---

## Setup steps

1. Install Codex CLI:
   ```bash
   npm install -g @openai/codex
   ```

2. Confirm installation:
   ```bash
   codex --version
   ```

3. Set your API key:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

4. Create and enter a test project directory:
   ```bash
   mkdir test-gen-demo && cd test-gen-demo
   git init
   ```

5. Create a Python virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

6. Install pytest and coverage:
   ```bash
   pip install pytest pytest-cov
   ```

7. Create `calculator.py` with the content from the Example input section below. Commit it:
   ```bash
   git add calculator.py && git commit -m "add calculator module"
   ```

8. Create a feature branch:
   ```bash
   git checkout -b add-tests
   ```

9. Run Codex CLI in approval mode with the prompt from the Copyable instructions section:
   ```bash
   codex --approval-mode
   ```

---

## Copyable instructions

### User prompt (paste at the Codex CLI prompt)

```
Read the file `calculator.py` in the current directory.

Write a pytest test suite in a new file called `test_calculator.py`.

Requirements:
- Use pytest as the testing framework. Do not use unittest.
- Write at least one test function for each public function in `calculator.py` (add, subtract, multiply, divide).
- Each test function must have a descriptive name that explains what it tests (e.g., `test_add_positive_integers`, `test_divide_by_zero_raises`).
- Include edge cases: division by zero, multiplication by zero, addition of negative numbers, subtraction producing a negative result.
- Every assert statement must include a failure message as the second argument (e.g., `assert result == 4, "Expected 4"`).
- Do NOT modify `calculator.py` under any circumstances. Only create `test_calculator.py`.
- After writing the file, output a short summary listing each test function and what it covers.

Scope: only work within the current directory. Do not install packages, do not access the network, do not modify any file other than creating `test_calculator.py`.
```

---

## Example input

Create this file as `calculator.py` in `test-gen-demo/`:

```python
# calculator.py

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return a minus b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return a divided by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

---

## Expected output

After accepting the generated file in approval mode, `test_calculator.py` should look broadly like this (exact names and assertions will vary):

```python
# test_calculator.py

import pytest
from calculator import add, subtract, multiply, divide


def test_add_positive_integers():
    assert add(2, 3) == 5, "Expected 2 + 3 = 5"


def test_add_negative_numbers():
    assert add(-1, -1) == -2, "Expected -1 + -1 = -2"


def test_add_zero():
    assert add(0, 5) == 5, "Expected 0 + 5 = 5"


def test_subtract_positive():
    assert subtract(10, 4) == 6, "Expected 10 - 4 = 6"


def test_subtract_producing_negative():
    assert subtract(3, 10) == -7, "Expected 3 - 10 = -7"


def test_multiply_positive():
    assert multiply(4, 5) == 20, "Expected 4 * 5 = 20"


def test_multiply_by_zero():
    assert multiply(7, 0) == 0, "Expected 7 * 0 = 0"


def test_multiply_negative():
    assert multiply(-3, 4) == -12, "Expected -3 * 4 = -12"


def test_divide_positive():
    assert divide(10, 2) == 5.0, "Expected 10 / 2 = 5.0"


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)
```

The agent should also output a summary listing each test function and what it covers.

---

## Safety boundaries

- Work on the `add-tests` branch only. Do not run this from `main`.
- The agent must not modify `calculator.py`. This is enforced by the prompt; verify it with `git diff add-tests main -- calculator.py` after the run (should be empty).
- Run tests in the virtual environment. Do not use system Python or a shared environment that could affect other projects.
- No network access. The prompt explicitly prohibits it. The agent should not attempt to install packages or fetch any external resource.
- Do not push to main. Review `test_calculator.py` and confirm the tests pass before merging.
- Do not use real production code as the input module for this exercise. Use the synthetic `calculator.py` or another module you own and can freely modify.

---

## Eval / check steps

After accepting the generated `test_calculator.py`:

1. **Tests pass.** Run the suite in the virtual environment:
   ```bash
   pytest test_calculator.py -v
   ```
   All tests must pass. If any fail, inspect the failure message. A failing test on correct implementation code means the test itself has an error — do not fix `calculator.py`.

2. **Coverage threshold.** Run with coverage and confirm 100% coverage of the public functions:
   ```bash
   pytest test_calculator.py --cov=calculator --cov-report=term-missing
   ```
   The report should show 100% coverage for `calculator.py`. If lines are missed, ask Codex CLI to add the missing cases.

3. **No implementation changes.** Verify `calculator.py` was not touched:
   ```bash
   git diff add-tests main -- calculator.py
   ```
   This diff must be empty. If it is not, revert `calculator.py` immediately with `git checkout main -- calculator.py` and re-run the agent with a stricter constraint.

4. **Edge cases included.** Confirm the test file contains at least one test for each of: division by zero, multiplication by zero, addition of negative numbers, subtraction producing a negative result. A quick check:
   ```bash
   grep -i "zero\|negative" test_calculator.py
   ```
   If this returns no results, the edge cases are missing.

---

## Troubleshooting

**Tests fail with `ImportError: cannot import name 'add' from 'calculator'`.**
Codex CLI may have created the test file in a subdirectory or with the wrong import path. Confirm `test_calculator.py` is in the same directory as `calculator.py` and that the import at the top reads `from calculator import add, subtract, multiply, divide`.

**Misnamed test functions (e.g., `test_1`, `test_2`).**
The prompt asked for descriptive names. If the agent ignored this, add a stronger constraint: "Every test function name must start with `test_` followed by the function under test and a description of the scenario (e.g., `test_divide_by_zero_raises_value_error`)." Re-run on the same branch.

**Assert statements without failure messages.**
The prompt required a message as the second argument to every `assert`. If messages are missing, add to the prompt: "Every assert must include a human-readable failure message as the second argument. No bare assert statements." Run Codex CLI again and ask it to update `test_calculator.py` only.

**Coverage is less than 100%.**
Identify the uncovered lines in the `--cov-report=term-missing` output. Ask Codex CLI to add a test specifically for those lines, referencing the line numbers in your prompt.

**The agent attempts to modify `calculator.py`.**
Reject the change in approval mode. Review whether the prompt wording was ambiguous. Adding the word "forbidden" is sometimes more effective than "do not": "Modifying `calculator.py` is forbidden."

---

Where to go next: [First Browser Agent](./first-browser-agent.md) — or explore the [OpenAI Agents SDK Python kit](../starter-kits.md) for building multi-step pipelines around generated code.
