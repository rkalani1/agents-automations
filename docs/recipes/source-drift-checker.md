# Source-drift checker agent

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Goal

This agent reads a local `docs/source-map.md` file that lists URLs referenced in a documentation site, fetches the live title and meta-description for each URL, compares them against the recorded values in the source map, and produces a drift report listing which URLs appear to have changed content or moved. The user runs this manually to catch stale citations before publishing. No scheduling in this recipe.

## Recommended platform(s)

Primary: [Codex CLI](https://developers.openai.com/codex/cli) with a custom `fetch_url_meta` tool (Python helper).

Alternates: [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) with an HTTP fetch tool; browser-use library for JavaScript-rendered pages.

## Why this platform

Codex CLI integrates naturally with local file reads and small Python helper scripts, making it easy to combine the source-map parsing step with a live URL check step in a single command. For pages that require JavaScript rendering (e.g., SPAs), the browser-use library can replace the simple `requests`-based fetch without changing the rest of the recipe structure. MANUAL-ONLY: this recipe is designed to be run on demand, not on a schedule.

## Required subscription / account / API

- OpenAI API key (for Codex CLI) or an Anthropic API key (for Claude Code).
- No special credentials; the agent only fetches public URLs via standard HTTP GET.

## Required tools / connectors

- `read_source_map(path: str) -> list[dict]` — parses `source-map.md` and returns a list of `{url, recorded_title, recorded_description, context}` objects.
- `fetch_url_meta(url: str) -> dict` — performs an HTTP GET, extracts the page `<title>` and `<meta name="description">` tag, returns `{url, live_title, live_description, status_code, error}`.
- No write tools; the source map is read-only.

## Permission model

| Permission | Scope | Rationale |
|---|---|---|
| File read | `docs/source-map.md` only | Agent reads the source map; no other file system access needed. |
| File write | Optional output report path | To save the drift report; human reviews before acting. |
| Network | Outbound HTTP GET to listed URLs only | Fetches public page metadata; no authenticated requests. |
| Env vars | `OPENAI_API_KEY` only | Never logged or printed. |

The agent should not follow redirects beyond one hop, to avoid fetching unexpected destinations. Set a 10-second timeout on each request.

## Filled agent spec

| Field | Value |
|---|---|
| Job statement | Read source-map.md, fetch live metadata for each URL, compare to recorded values, and report drift suspects. |
| Inputs | Path to `docs/source-map.md`; optional tolerance level (exact-match vs. fuzzy). |
| Outputs | Markdown drift report listing URLs that appear changed, moved, or unreachable. |
| Tools | `read_source_map`, `fetch_url_meta` |
| Stop conditions | All URLs checked; report produced. |
| Error handling | If a URL returns a non-200 status or times out, record it as "Unreachable" in the report; continue to the next URL. |
| HITL gates | Technical writer or doc maintainer reviews the drift report and decides which citations to update. |
| Owner | The documentation maintainer who ran the command. |
| Review cadence | Run before any doc release; run monthly during active development. |

## Setup steps

1. Set up the environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install openai-agents requests beautifulsoup4 python-dotenv
   ```
2. Add `OPENAI_API_KEY=<your-key>` and `OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL` to `.env`. Add `.env` to `.gitignore`.
3. Ensure `docs/source-map.md` exists and follows the format below.
4. Save `drift_checker.py` (see Prompt / instructions below).
5. Run manually:
   ```
   python drift_checker.py --source-map ./docs/source-map.md --output ./drift_report.md
   ```
6. Review `drift_report.md` and update stale citations.

`docs/source-map.md` format:
```markdown
## Source map

| URL | Recorded title | Recorded description | Context |
|---|---|---|---|
| https://example.com/docs/api | Example API Docs | Reference for all endpoints | Recipe: api-agent.md |
```

## Prompt / instructions

```python
# drift_checker.py
import argparse, os, re
from pathlib import Path
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from agents import Agent, Runner, function_tool

load_dotenv()

def parse_source_map_table(text: str) -> list:
    """Parse a Markdown table from source-map.md into a list of dicts."""
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not line.startswith("| URL") and "---" not in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 4:
                rows.append({
                    "url": parts[0],
                    "recorded_title": parts[1],
                    "recorded_description": parts[2],
                    "context": parts[3],
                })
    return rows

@function_tool
def read_source_map(path: str) -> list:
    """Read and parse the source-map Markdown file."""
    try:
        text = Path(path).read_text(encoding="utf-8")
        return parse_source_map_table(text)
    except Exception as e:
        return [{"error": str(e)}]

@function_tool
def fetch_url_meta(url: str) -> dict:
    """Fetch live <title> and meta description from a URL."""
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True,
                            headers={"User-Agent": "DriftCheckerBot/1.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string.strip() if soup.title else ""
        meta_desc_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc_tag["content"].strip() if meta_desc_tag else ""
        return {
            "url": url,
            "status_code": resp.status_code,
            "live_title": title,
            "live_description": meta_desc,
        }
    except Exception as e:
        return {"url": url, "status_code": 0, "error": str(e)}

SYSTEM_PROMPT = """
You are a source-drift checker. Your job is to compare recorded URL metadata in a
source map against live page metadata and report which URLs appear to have drifted.

Steps:
1. Call read_source_map to get the list of URLs and their recorded metadata.
2. For each entry, call fetch_url_meta to get the live title and description.
3. Compare live values to recorded values. Mark a URL as a drift suspect if:
   - The live title differs substantially from the recorded title (not just whitespace/case).
   - The live description is missing or completely different.
   - The status code is not 200 (record as "Unreachable" or "Redirect").
4. Produce a Markdown drift report:

## Source drift report

**Source map:** <path>
**URLs checked:** <count>
**Drift suspects:** <count>
**Run date:** <today>

### Drift suspects

| URL | Recorded title | Live title | Status | Context |
|---|---|---|---|---|

### Unreachable URLs

| URL | Status code | Error | Context |
|---|---|---|---|

### No drift detected

List URLs that appear unchanged.

Rules:
- Do not modify source-map.md.
- Do not follow more than one redirect per URL.
- If a URL returns a 404, mark it "Page not found."
- Be conservative: flag as a suspect only when the difference is substantive.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-map", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    agent = Agent(
        name="DriftCheckerAgent",
        model=os.environ["OPENAI_MODEL"],
        instructions=SYSTEM_PROMPT,
        tools=[read_source_map, fetch_url_meta],
    )
    result = Runner.run_sync(agent, f"Check drift for source map: {args.source_map}")
    if args.output:
        Path(args.output).write_text(result.final_output)
        print(f"Drift report written to {args.output}")
    else:
        print(result.final_output)

if __name__ == "__main__":
    main()
```

## Example input

`docs/source-map.md`:
```markdown
| URL | Recorded title | Recorded description | Context |
|---|---|---|---|
| https://github.com/openai/openai-agents-python | openai/openai-agents-python | Python SDK for OpenAI Agents | Recipe: openai-agents-sdk-tool-calling.md |
| https://platform.openai.com/docs/guides/function-calling | Function calling | Guide to tool use | Recipe: multiple |
```

## Expected output

A drift report listing GitHub and OpenAI pages as "No drift detected" (assuming titles match) or as drift suspects if the pages have changed. Any unreachable URL is called out separately. The report includes the run date and the count of URLs checked.

## Eval cases

1. All URLs return 200 with matching titles — all listed under "No drift detected."
2. One URL returns 404 — listed under "Unreachable URLs" with status code 404.
3. One URL's title changed slightly (e.g., added " | OpenAI") — agent should judge whether this is substantive; document the expected behavior (minor suffix change = not a suspect).
4. Source map with 50 URLs — report is produced without hitting rate limits; add a `time.sleep(0.5)` between fetches.
5. URL that redirects permanently — agent marks it as a redirect suspect and notes the final URL.
6. Source map file not found — agent reports the error and exits cleanly.

## Red-team probes

1. URL in the source map pointing to a private internal IP (e.g., `http://192.168.1.1`) — add an allowlist check: only fetch URLs with `http://` or `https://` schemes and non-private IP ranges.
2. URL response containing a very large HTML page (10 MB) — add a `stream=True` + content-length cap in the fetch function to avoid memory exhaustion.
3. Source map entry with a URL containing shell metacharacters — the URL is passed as a string argument to `requests.get`, never to a shell; confirm no `subprocess` call is made.

## Failure modes

- False-positive drift on dynamic titles: some pages have session-specific or personalized titles. Mitigation: the "be conservative" rule; consider comparing only the first N words of the title.
- Rate limiting by target sites: rapid-fire GET requests may trigger 429 responses. Mitigation: add a configurable delay between fetches (default 500 ms).
- JavaScript-rendered pages: `requests` + BeautifulSoup cannot parse SPA content. Mitigation: swap `fetch_url_meta` for a browser-use or Playwright-based implementation for those URLs.
- Source map parse failure: non-standard Markdown table formatting breaks the parser. Mitigation: add a schema validation step and report malformed rows clearly.
- Redirect loop: a URL redirects to itself or in a loop. Mitigation: set `max_redirects=1` in the requests call.

## Cost / usage controls

- The LLM step is usually small; the main cost is network I/O time plus the selected model's current token price.
- Limit to 100 URLs per run to keep runtime under 2 minutes.
- Log the number of requests made per run.

## Safe launch checklist

- [ ] Source map does not contain internal-IP or authenticated URLs.
- [ ] Fetch function has a timeout and content-length cap.
- [ ] Delay between requests is configured (default 500 ms).
- [ ] Output report is reviewed by a human before any citations are updated.
- [ ] Agent has been tested on a synthetic source map with known-good and known-changed URLs.
- [ ] No write tools are in the agent's tool list.

## Maintenance cadence

Run this recipe before every documentation release. Re-verify the parsing logic whenever the source-map table format changes. Check that `requests` and `beautifulsoup4` are up to date quarterly. Run all six eval cases after any change to the fetch logic or the prompt.
