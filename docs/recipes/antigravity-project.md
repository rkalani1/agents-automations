# Antigravity project agent

> **Last verified:** 2026-05-06 · **Drift risk:** high

## Goal

This recipe walks through building a learning-oriented agent project using the [Google Antigravity codelab](https://codelabs.developers.google.com/getting-started-google-antigravity). The codelab is an experimental Google playground for exploring AI agent concepts and tooling. The agent you build follows the codelab's guided steps to demonstrate a basic agentic loop with tool use. Because the codelab is experimental and its content changes frequently, this recipe carries a high drift risk — verify the codelab URL and steps before following this recipe.

## Recommended platform(s)

Primary: Google Antigravity (as described in the [Antigravity codelab](https://codelabs.developers.google.com/getting-started-google-antigravity)).

Alternates: [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) for the core agent pattern; [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) if you want a more stable platform.

## Why this platform

The Antigravity codelab is Google's hands-on introduction to agentic AI concepts. It is primarily a learning resource rather than a production tool, which makes it well-suited for teams exploring Google's ecosystem before committing to a production platform. The codelab walks through setting up a simple agent, defining tools, and observing the model-tool loop — the same concepts that appear in all production agent recipes in this field guide.

Important caveats: Antigravity is labeled experimental by Google. The codelab URL, content, and tooling may change without notice. The drift risk for this recipe is marked high because the underlying codelab has changed multiple times since its introduction. If the codelab link is broken or the steps differ from what is described here, fall back to the [Gemini function-calling recipe](gemini-function-calling.md) in this field guide.

## Required subscription / account / API

- A Google account with access to Google Cloud or Google AI Studio.
- A Gemini API key (from [AI Studio](https://aistudio.google.com/app/apikey)) or a Google Cloud project with the relevant APIs enabled.
- Access to the Antigravity codelab environment as described at [the codelab URL](https://codelabs.developers.google.com/getting-started-google-antigravity).

## Required tools / connectors

- The codelab environment provides a web-based IDE or a Cloud Shell terminal.
- Python (provided in Cloud Shell or installable locally).
- `google-genai` Python package (or whichever package the codelab currently specifies — verify at the codelab page).
- No external connectors beyond the Gemini API.

## Permission model

| Permission | Scope | Rationale |
|---|---|---|
| Gemini API calls | The codelab project only | Agent calls the Gemini API; no other external services. |
| File read/write | Codelab workspace only | The codelab environment is sandboxed to a temporary project. |
| Cloud Shell | If used, restricted to the session | Cloud Shell sessions are ephemeral and user-scoped. |
| API key | Stored in the codelab environment's environment variable mechanism | Do not hardcode keys in codelab code samples. |

## Filled agent spec

| Field | Value |
|---|---|
| Job statement | Follow the Antigravity codelab steps to build a minimal agent with at least one tool, observe the model-tool loop, and document what you learned. |
| Inputs | The codelab exercises (web-based steps). |
| Outputs | A working codelab completion; notes on what changed from this recipe's description. |
| Tools | Whatever the codelab defines (typically a weather or search mock tool). |
| Stop conditions | Codelab marked complete; agent loop observed running end-to-end. |
| Error handling | If any codelab step fails, consult the codelab's "Help" or "Report a bug" link; fall back to the Gemini function-calling recipe. |
| HITL gates | You review the code produced by each codelab step before running it. |
| Owner | The developer following the codelab. |
| Review cadence | High drift risk: re-verify this recipe against the live codelab every 60 days. |

## Setup steps

These steps reflect the codelab structure as of the last verification date (2026-05-06). Verify each step against the [live codelab](https://codelabs.developers.google.com/getting-started-google-antigravity) before following.

1. Open the codelab at `https://codelabs.developers.google.com/getting-started-google-antigravity`.
2. Follow the "Before you begin" section to set up your Google Cloud project or AI Studio account.
3. Open Cloud Shell (or your local terminal) and install the required package:
   ```
   pip install google-genai python-dotenv
   ```
4. Set your API key as an environment variable:
   ```
   export GEMINI_API_KEY=<your-key>
   ```
   Do not hardcode the key in any code file.
5. Follow the codelab's "Define a tool" step. The codelab typically shows a mock `get_weather(city)` function. Adapt it to `read_notes(path)` from the [Gemini function-calling recipe](gemini-function-calling.md) if you want a file-based example.
6. Follow the codelab's "Run the agent loop" step. Observe the terminal output showing tool calls and model responses.
7. Complete any remaining codelab exercises.
8. Note any differences between the codelab's current content and this recipe's description — those differences are drift signals.

## Prompt / instructions

The Antigravity codelab provides its own code samples. The pattern it teaches is equivalent to the following minimal Gemini function-calling agent (see [the Gemini function-calling recipe](gemini-function-calling.md) for the full version):

```python
# Minimal Antigravity-style agent pattern
# Mirrors the codelab's core agentic loop concept
# See: https://codelabs.developers.google.com/getting-started-google-antigravity

import os
import google.genai as genai
import google.genai.types as types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.0-flash"


def get_weather(city: str) -> str:
    """Return a mock weather description for a city (codelab demo tool)."""
    # In the codelab, this is often a mock or a real weather API call.
    # Use a mock for the recipe to avoid requiring a weather API key.
    mock_data = {
        "london": "Overcast, 14C, light rain.",
        "tokyo": "Clear, 22C, low humidity.",
        "new york": "Partly cloudy, 18C.",
    }
    return mock_data.get(city.lower(), f"No data for {city}.")


TOOL_FUNCTIONS = {"get_weather": get_weather}

tools = [types.Tool(function_declarations=[
    types.FunctionDeclaration.from_function(get_weather),
])]

config = types.GenerateContentConfig(
    system_instruction="You are a helpful assistant with access to weather data. "
                       "Call get_weather when asked about conditions in a city.",
    tools=tools,
)

messages = [{"role": "user", "parts": ["What is the weather like in Tokyo and London?"]}]

for _ in range(5):
    response = client.models.generate_content(
        model=MODEL, contents=messages, config=config
    )
    candidate = response.candidates[0]
    fn_calls = [p.function_call for p in candidate.content.parts if p.function_call]
    if not fn_calls:
        print("".join(p.text for p in candidate.content.parts if p.text))
        break
    messages.append({"role": "model", "parts": candidate.content.parts})
    fn_responses = []
    for fc in fn_calls:
        result = TOOL_FUNCTIONS.get(fc.name, lambda **kw: "Unknown tool")(**dict(fc.args))
        fn_responses.append(types.Part.from_function_response(
            name=fc.name, response={"result": result}
        ))
    messages.append({"role": "user", "parts": fn_responses})
```

## Example input

User message: "What is the weather like in Tokyo and London?"

## Expected output

```
Tokyo is currently clear with a temperature of 22C and low humidity. London has
overcast skies with light rain and a temperature of 14C.
```

This output demonstrates that the agent called `get_weather` twice (once per city) and synthesized the results into a natural-language response.

## Eval cases

1. Both cities available in mock data — agent calls the tool twice; answer includes both cities.
2. City not in mock data (e.g., "Paris") — `get_weather` returns "No data for Paris."; agent surfaces this gracefully.
3. Codelab code sample copied verbatim — code runs without modification errors in the codelab environment.
4. API key not set — `os.environ["GEMINI_API_KEY"]` raises `KeyError`; agent prints a clear error message.
5. Model name changed or deprecated — the `generate_content` call fails with a model-not-found error; update `MODEL` to the current model name.
6. Codelab content has changed from this recipe's description — drift detected; note the differences for the maintenance record.

## Red-team probes

1. Request to call a non-existent tool: "Call delete_all_files." — the agent has no such tool; it responds that it cannot perform that action.
2. Mock tool returning an extremely long string: `get_weather` returns 100 000 characters — the Gemini context window handles this, but add a truncation cap in production use.
3. Codelab environment prompt injection: a codelab exercise tells you to add a line that calls an external API — review every codelab code sample before running it; never blindly copy-paste from an unfamiliar source.

## Failure modes

- Codelab content drift: the codelab's steps, tools, and model names change without notice. Mitigation: this recipe carries `Drift risk: high`; re-verify every 60 days and document differences in the maintenance log.
- Codelab URL broken: Google may retire or move the codelab. Mitigation: fall back to the [Gemini function-calling recipe](gemini-function-calling.md), which teaches the same pattern on a stable API.
- Cloud Shell session expiration: if you pause and resume the codelab in Cloud Shell, the environment variables and installed packages reset. Mitigation: keep a local copy of your `.env` file and reinstall packages at the start of each session.
- Model quota exceeded: the free tier has rate limits; the codelab may trigger multiple API calls in quick succession. Mitigation: add a `time.sleep(1)` between tool calls if you hit 429 errors.
- Key stored in codelab code file: the codelab may instruct you to paste the key directly in the code for simplicity. Mitigation: always use environment variables; delete any hardcoded keys before sharing or committing code.

## Cost / usage controls

- The Gemini free tier is sufficient for completing the codelab exercises.
- If you use a paid project, the codelab's 5-10 API calls per exercise are typically small; calculate dollar cost from the selected Gemini model's current pricing.
- Monitor the Google Cloud billing dashboard if you use a GCP project.

## Safe launch checklist

- [ ] Live codelab URL verified before starting.
- [ ] API key stored as environment variable, not hardcoded.
- [ ] Codelab environment (Cloud Shell or local) confirmed accessible.
- [ ] Each code sample reviewed before running.
- [ ] Differences between this recipe and the live codelab content are documented.
- [ ] Drift risk flag (`high`) is acknowledged; re-verification is scheduled in 60 days.

## Maintenance cadence

Re-verify this recipe every 60 days due to the high drift risk. At each check: open the [codelab URL](https://codelabs.developers.google.com/getting-started-google-antigravity), compare the current steps to this recipe, and update the Setup steps and Prompt / instructions sections to reflect any differences. If the codelab is retired, update the recipe to use the [Gemini function-calling recipe](gemini-function-calling.md) as the primary reference and mark this recipe as deprecated. Update the `google-genai` package version note when new versions are released.
