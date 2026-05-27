# First Browser Agent: Extract a 7-Day Weather Forecast into JSON

> **Last verified:** 2026-05-06 · **Drift risk:** medium-high

## Use case

You want an agent to open a public weather website and extract the 7-day forecast for one city, returning a structured JSON object with days, high temperatures, low temperatures, and weather conditions. No login is required. The agent runs in a sandboxed environment and is constrained to a single allowlisted URL.

This quickstart has a higher drift risk than others in this section. Browser automation is sensitive to website layout changes, JavaScript rendering delays, and anti-bot measures. Expect to revisit this setup periodically.

Target completion time: 40–60 minutes.

---

## Best platform choice and why

**Primary: [browser-use](https://github.com/browser-use/browser-use) Python library**

`browser-use` is an open-source Python library that connects a large language model to a Playwright-controlled browser. It accepts a natural-language goal, drives the browser to accomplish it, and returns structured results. For a contained data-extraction task like this one, it is a practical choice: it is local, auditable, does not require a paid automation platform subscription, and the code is small enough to read and understand in an afternoon.

Run it inside a virtual machine or a containerized environment. Do not run browser automation agents in your primary browser profile or on a machine with active logged-in sessions to services you use for work or personal accounts.

---

## Prerequisites

- Python 3.11 or later.
- An API key for either Anthropic (`ANTHROPIC_API_KEY`) or OpenAI (`OPENAI_API_KEY`), stored as an environment variable.
- A sandbox environment: a virtual machine, a Docker container, or at minimum a dedicated Python virtual environment on a machine that does not have sensitive browser sessions active.
- `pip` and the ability to install packages.
- Playwright system dependencies (installed as part of setup below).

---

## Setup steps

1. Create and activate a fresh virtual environment:
   ```bash
   python3 -m venv browser-agent-venv
   source browser-agent-venv/bin/activate   # On Windows: browser-agent-venv\Scripts\activate
   ```

2. Install `browser-use` and the Playwright browser driver per the [browser-use README](https://github.com/browser-use/browser-use):
   ```bash
   pip install browser-use
   playwright install chromium
   ```

3. Install the LLM SDK for whichever provider you are using:
   ```bash
   # For Anthropic:
   pip install anthropic
   # For OpenAI:
   pip install openai
   ```

4. Set your API key:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   # or
   export OPENAI_API_KEY="your-key-here"
   ```

5. Create the agent script from the Copyable instructions section below. Save it as `weather_agent.py`.

6. Review the safety boundaries section before running. In particular, confirm you are not running this in a browser profile with active sessions.

7. Run the agent:
   ```bash
   python weather_agent.py
   ```

---

## Copyable instructions

### Agent script: `weather_agent.py`

```python
import asyncio
import json
import os

from browser_use import Agent
from browser_use.browser import BrowserConfig

# --- Configuration ---
TARGET_URL = "https://example.com/weather/sample-city"  # Replace with your target public URL
CITY = "Sample City"
MAX_STEPS = 15  # Hard cap on agent actions; raise if needed, but start low

# Allowlist: the agent may only navigate to URLs matching this prefix
ALLOWED_URL_PREFIX = "https://example.com/weather/"

# Set your LLM. Replace the import and instantiation for OpenAI if preferred.
from anthropic import Anthropic
# from openai import OpenAI  # Uncomment for OpenAI

# browser-use accepts any LangChain-compatible LLM.
# See https://github.com/browser-use/browser-use for supported model integrations.
from langchain_anthropic import ChatAnthropic
# from langchain_openai import ChatOpenAI  # Uncomment for OpenAI

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.environ["ANTHROPIC_API_KEY"],
)
# llm = ChatOpenAI(model=os.environ["OPENAI_MODEL"], api_key=os.environ["OPENAI_API_KEY"])


GOAL = f"""
Go to {TARGET_URL} and extract the 7-day weather forecast for {CITY}.

Return ONLY a JSON object with the following structure — no prose, no explanation:

{{
  "city": "{CITY}",
  "forecast": [
    {{
      "day": "Monday",
      "date": "2026-05-06",
      "high_f": 62,
      "low_f": 48,
      "condition": "Partly cloudy"
    }}
  ]
}}

Rules:
- Only navigate to URLs that start with {ALLOWED_URL_PREFIX}. Do not click any link 
  that would take you outside that prefix.
- Do not fill in any forms, do not click login buttons, do not accept any cookies 
  that require account creation.
- If you cannot find the 7-day forecast on the page, return a JSON object with 
  "error": "forecast not found" instead of guessing.
- Stop as soon as you have the forecast data. Do not explore the site further.
"""


async def main():
    browser_config = BrowserConfig(
        headless=True,   # Set to False to watch the browser during debugging
    )

    agent = Agent(
        task=GOAL,
        llm=llm,
        max_actions_per_step=MAX_STEPS,
        browser_config=browser_config,
    )

    result = await agent.run()

    # Extract the final message from the agent result
    final_output = result.final_result()
    print("--- Raw agent output ---")
    print(final_output)

    # Attempt to parse as JSON for validation
    try:
        parsed = json.loads(final_output)
        print("\n--- Parsed JSON ---")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"\nJSON parse error: {e}")
        print("The agent did not return valid JSON. See troubleshooting section.")


if __name__ == "__main__":
    asyncio.run(main())


```

---

## Example input

The script targets a placeholder URL: `https://example.com/weather/sample-city`. Before running, replace this with a real public weather service URL for a city of your choice. Use a service that does not require login. Some public options at time of writing include national meteorological service websites and open-data weather portals.

Replace both `TARGET_URL` and `ALLOWED_URL_PREFIX` in the configuration block at the top of the script so the allowlist matches your chosen domain.

---

## Expected output

When the agent succeeds, the terminal output should include valid JSON like this:

```json
{
  "city": "Sample City",
  "forecast": [
    {"day": "Monday",    "date": "2026-05-06", "high_f": 58, "low_f": 46, "condition": "Cloudy"},
    {"day": "Tuesday",   "date": "2026-05-07", "high_f": 55, "low_f": 44, "condition": "Rain"},
    {"day": "Wednesday", "date": "2026-05-08", "high_f": 60, "low_f": 47, "condition": "Partly cloudy"},
    {"day": "Thursday",  "date": "2026-05-09", "high_f": 63, "low_f": 49, "condition": "Mostly sunny"},
    {"day": "Friday",    "date": "2026-05-10", "high_f": 65, "low_f": 51, "condition": "Sunny"},
    {"day": "Saturday",  "date": "2026-05-11", "high_f": 61, "low_f": 48, "condition": "Partly cloudy"},
    {"day": "Sunday",    "date": "2026-05-12", "high_f": 57, "low_f": 45, "condition": "Rain"}
  ]
}
```

The exact values will reflect the live forecast on the day you run the script.

---

## Safety boundaries

These boundaries are non-negotiable for browser automation agents.

- Never run against a logged-in browser session. The `BrowserConfig` in the script uses an isolated context. Do not share your default browser profile with the agent. A logged-in session exposes cookies, saved passwords, and authenticated access to every service you use.
- Never run against payment pages, account settings, or any page that allows writes. This quickstart targets a read-only public page. If you adapt this script, audit the target page carefully before running.
- Run in a sandbox. A virtual machine or Docker container is strongly preferred. At minimum, use a dedicated virtual environment and a machine where losing access to browser state would cause no harm.
- Set a maximum step cap. The `MAX_STEPS` variable in the script limits how many actions the agent can take. Start at 15. If the agent exceeds this without completing the task, it aborts rather than wandering.
- Enforce the URL allowlist in the goal string. The goal instructs the agent not to navigate outside the allowlist prefix. This is a soft constraint (it is in the prompt, not enforced at the browser level). For stronger enforcement, add a Playwright navigation listener that raises an exception on disallowed URLs.
- Do not run on a schedule. This is a manually triggered, single-run script. Do not add a cron job, a loop, or any mechanism that runs it repeatedly without human review.
- No PHI or PII in the goal string. Do not include real names, addresses, or identifying information in the task prompt.

---

## Eval / check steps

After the agent completes:

1. **JSON validates.** The script already attempts `json.loads()` on the output. If it throws `JSONDecodeError`, the agent did not return structured data. See troubleshooting.

2. **Dates are contiguous.** Check that the `date` fields in the forecast array form a consecutive 7-day sequence starting from today. A gap or repetition suggests the agent extracted data incorrectly. You can validate this with:
   ```python
   from datetime import date, timedelta
   import json
   
   data = json.loads(open("forecast_output.json").read())
   dates = [d["date"] for d in data["forecast"]]
   expected = [(date.today() + timedelta(days=i)).isoformat() for i in range(7)]
   assert dates == expected, f"Date mismatch: got {dates}"
   ```

3. **No extra navigation.** Review the agent's action log (printed to stdout by default). Confirm that all URLs visited begin with `ALLOWED_URL_PREFIX`. Any URL outside that prefix is a safety boundary violation; investigate before running again.

---

## Troubleshooting

**The agent is blocked by a CAPTCHA.**
Some weather sites serve CAPTCHAs to headless browsers. Try setting `headless=False` in `BrowserConfig` to use a visible browser window, which is less likely to be flagged. If CAPTCHAs persist, switch to a different public weather data source. Do not attempt to automate CAPTCHA solving.

**The page is JavaScript-heavy and the forecast does not appear.**
`browser-use` uses Playwright, which executes JavaScript. However, if the forecast is loaded by a delayed async call, the agent may screenshot the page before the data is available. Add a step to the goal: "Wait for the 7-day forecast section to be fully visible before extracting data." If the problem persists, try increasing the `max_actions_per_step` to give the agent more time to interact with the page.

**The website layout changed and the agent extracts the wrong data.**
Weather sites change their layouts. This is the primary reason for the medium-high drift risk rating. Re-run with `headless=False` to watch what the agent sees, then adjust the goal string to describe the current layout (e.g., "The forecast is in a table with class `forecast-table`").

**The agent returns a JSON error field: `"error": "forecast not found"`.**
The target URL may be wrong, or the page structure changed significantly. Confirm the URL loads correctly in a real browser and that the 7-day forecast is visible without login.

**`langchain_anthropic` or `langchain_openai` is not installed.**
Install the required LangChain integration package:
```bash
pip install langchain-anthropic   # or langchain-openai
```

---

Where to go next: [First MCP Agent](./first-mcp-agent.md) — or explore the [browser-use advanced patterns kit](../starter-kits.md) for multi-step extraction workflows.
