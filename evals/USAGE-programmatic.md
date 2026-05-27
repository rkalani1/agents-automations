# Programmatic Eval Runner

This guide explains how to run eval cases programmatically using the OpenAI Python SDK and the Google Gemini Python SDK. It includes short code stubs for each step: read JSONL, call the API, collect responses, and prepare results for human scoring.

No real API keys appear in this document. All key references use placeholder strings.

---

## Prerequisites

```bash
pip install openai google-generativeai
```

---

## Part 1: OpenAI API Runner

### 1.1 Basic Runner

```python
import json
import time
from openai import OpenAI

# Do not hardcode real keys. Use environment variables.
# export OPENAI_API_KEY=your_key_here
import os
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def run_eval_case(case: dict, model: str = "gpt-4o") -> dict:
    """
    Submits a single eval case to the OpenAI API and returns the response.
    Returns a result dict with the case ID, input, response text, and metadata.
    """
    # Build the message list
    messages = []

    # If the input is an object with a 'system' key, add it as a system message
    if isinstance(case["input"], dict) and "system" in case["input"]:
        messages.append({"role": "system", "content": case["input"]["system"]})
        user_content = {k: v for k, v in case["input"].items() if k != "system"}
        messages.append({"role": "user", "content": json.dumps(user_content)})
    elif isinstance(case["input"], str):
        messages.append({"role": "user", "content": case["input"]})
    else:
        messages.append({"role": "user", "content": json.dumps(case["input"])})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,  # Deterministic for eval purposes
    )

    return {
        "id": case["id"],
        "category": case.get("category") or case.get("attack_class"),
        "input": case["input"],
        "expected_behavior": case.get("expected_behavior") or case.get("desired_response"),
        "must_not_do": case.get("must_not_do", []),
        "agent_response": response.choices[0].message.content,
        "model": model,
        "finish_reason": response.choices[0].finish_reason,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
        },
        "scored": False,
        "score": None,
        "verdict": None,
        "justification": None,
    }


def run_eval_file(jsonl_path: str, model: str = "gpt-4o", delay_seconds: float = 1.0) -> list:
    """
    Reads a JSONL eval file and runs every case through the API.
    Returns a list of result dicts. Adds a delay between calls to respect rate limits.
    """
    results = []
    with open(jsonl_path) as f:
        cases = [json.loads(line) for line in f if line.strip()]

    for i, case in enumerate(cases):
        print(f"Running case {i+1}/{len(cases)}: {case['id']}")
        try:
            result = run_eval_case(case, model=model)
            results.append(result)
        except Exception as e:
            results.append({
                "id": case["id"],
                "error": str(e),
                "agent_response": None,
            })
        time.sleep(delay_seconds)

    return results


def save_results(results: list, output_path: str):
    """Saves results to a JSONL file for human scoring."""
    with open(output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print(f"Saved {len(results)} results to {output_path}")


# Example usage:
# results = run_eval_file("evals/golden/summarization.jsonl", model="gpt-4o")
# save_results(results, "results/summarization_gpt4o.jsonl")
```

---

## Part 2: Gemini API Runner

```python
import json
import time
import os
import google.generativeai as genai

# Do not hardcode real keys. Use environment variables.
# export GEMINI_API_KEY=your_key_here
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def run_eval_case_gemini(case: dict, model_name: str = "gemini-1.5-pro") -> dict:
    """
    Submits a single eval case to the Gemini API and returns the response.
    """
    system_instruction = None
    user_content = None

    if isinstance(case["input"], dict) and "system" in case["input"]:
        system_instruction = case["input"]["system"]
        user_content = json.dumps({k: v for k, v in case["input"].items() if k != "system"})
    elif isinstance(case["input"], str):
        user_content = case["input"]
    else:
        user_content = json.dumps(case["input"])

    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(temperature=0.0),
    )

    response = model.generate_content(user_content)

    return {
        "id": case["id"],
        "category": case.get("category") or case.get("attack_class"),
        "input": case["input"],
        "expected_behavior": case.get("expected_behavior") or case.get("desired_response"),
        "must_not_do": case.get("must_not_do", []),
        "agent_response": response.text,
        "model": model_name,
        "scored": False,
        "score": None,
        "verdict": None,
        "justification": None,
    }


def run_eval_file_gemini(jsonl_path: str, model_name: str = "gemini-1.5-pro", delay_seconds: float = 1.5) -> list:
    """
    Reads a JSONL eval file and runs every case through the Gemini API.
    """
    results = []
    with open(jsonl_path) as f:
        cases = [json.loads(line) for line in f if line.strip()]

    for i, case in enumerate(cases):
        print(f"Running case {i+1}/{len(cases)}: {case['id']}")
        try:
            result = run_eval_case_gemini(case, model_name=model_name)
            results.append(result)
        except Exception as e:
            results.append({"id": case["id"], "error": str(e), "agent_response": None})
        time.sleep(delay_seconds)

    return results


# Example usage:
# results = run_eval_file_gemini("evals/golden/extraction.jsonl", model_name="gemini-1.5-pro")
# save_results(results, "results/extraction_gemini15pro.jsonl")
```

---

## Part 3: Scoring Stub

After running the API calls, human scorers review the JSONL results file. The following stub loads a results file and prints each case for review, leaving space for the scorer to enter a score:

```python
import json

def interactive_score(results_path: str, rubric: str = "golden"):
    """
    Loads a results JSONL and prompts a human scorer for each case.
    Updates the scored, score/verdict, and justification fields.
    Saves progress after each case.
    """
    with open(results_path) as f:
        results = [json.loads(l) for l in f if l.strip()]

    for i, r in enumerate(results):
        if r.get("scored"):
            continue  # Skip already-scored cases

        print(f"\n{'='*60}")
        print(f"Case {i+1}/{len(results)}: {r['id']}")
        print(f"Expected: {r.get('expected_behavior', r.get('desired_response', ''))}")
        print(f"\nAgent response:\n{r.get('agent_response', '[ERROR]')}")
        print(f"\nmust_not_do: {r.get('must_not_do', [])}")

        if rubric == "golden":
            score_input = input("\nScore (1-5 per criterion, or 's' to skip): ").strip()
            just = input("Justification (1-2 sentences): ").strip()
            r["score"] = score_input
        else:
            verdict = input("\nVerdict (PASS/BORDERLINE/FAIL, or 's' to skip): ").strip().upper()
            just = input("Justification (1-2 sentences): ").strip()
            r["verdict"] = verdict

        r["justification"] = just
        r["scored"] = True

        # Save after each case
        with open(results_path, "w") as f:
            for row in results:
                f.write(json.dumps(row) + "\n")

    print("\nScoring complete.")


# Example usage:
# interactive_score("results/summarization_gpt4o.jsonl", rubric="golden")
# interactive_score("results/prompt-injection_gpt4o.jsonl", rubric="red-team")
```

---

## Rate Limits and Cost Estimates

Running the full golden bank (103 cases) through gpt-4o at ~500 input tokens and ~300 output tokens per case costs approximately 103 * 800 tokens = ~82,000 tokens. At current list pricing, this is under $1 USD for a single run. Adjust the delay_seconds parameter if you hit rate limits.

For Gemini 1.5 Pro, the same batch is under the free tier threshold for many use cases. Check current pricing at ai.google.dev/pricing.

Red-team cases average slightly more tokens per case due to longer inputs. A full red-team run (101 cases) is comparable in cost to the golden run.
