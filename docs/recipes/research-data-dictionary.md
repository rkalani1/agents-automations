# Research data dictionary agent

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Goal

Given a folder of CSV files, this agent inspects each file, infers column data types, computes cardinality (unique-value count), measures missingness (null/empty-string rate), and produces a single Markdown data dictionary that a data analyst or data engineer can immediately attach to a project wiki. The agent reads files locally, sends column-level summaries to the language model, and writes one output file — it does not modify source data.

## Recommended platform(s)

Primary: [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (Python, local execution).

Alternates: Gemini API with function calling; Claude via the Anthropic Python SDK with tool use.

## Why this platform

The OpenAI Agents SDK provides a clean tool-calling loop that maps naturally to the "read a file, compute stats, accumulate results" pattern. The structured-outputs feature ([OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs)) lets you enforce a typed `ColumnEntry` schema so the agent cannot silently omit required fields. The SDK's built-in tracing makes it easy to audit which files were processed and in what order without standing up extra infrastructure.

## Required subscription / account / API

- OpenAI API key and `OPENAI_MODEL` set to a current model ID.
- No third-party connectors required.

## Required tools / connectors

- `list_csv_files(folder_path: str) -> list[str]` — returns relative paths of all `.csv` files under the given folder.
- `read_csv_sample(file_path: str, max_rows: int) -> dict` — reads up to `max_rows` rows and returns column names, dtypes, null counts, unique counts, and five sample values per column.
- No network access needed; all I/O is local.

Both tools are implemented as plain Python functions decorated with `@function_tool` from the Agents SDK.

## Permission model

| Permission | Scope | Rationale |
|---|---|---|
| File read | Input folder only | Agent must read CSVs; no other directory access needed. |
| File write | Single output path | Writes the finished Markdown dictionary; no other write access. |
| Network | None | All processing is local; no external calls required. |
| Env vars | `OPENAI_API_KEY` only | Scoped to the agent process via `.env`; never logged. |

Run the agent as a non-root user. Pass the input folder as an argument, not as an environment variable, so it appears in the process invocation log.

## Filled agent spec

| Field | Value |
|---|---|
| Job statement | Read all CSVs in a given folder, produce a Markdown data dictionary with type, cardinality, missingness, and five sample values for every column. |
| Inputs | Folder path (string); optional `max_rows` cap (default 500). |
| Outputs | `data_dictionary.md` written to a caller-specified output path. |
| Tools | `list_csv_files`, `read_csv_sample` |
| Stop conditions | All CSV files processed; output file written; no unresolved tool errors. |
| Error handling | If a file cannot be parsed (encoding errors, binary content), log a warning row in the dictionary and continue. |
| HITL gates | Human reviews the finished Markdown before committing it to the project wiki. |
| Owner | Data engineer or analyst who triggered the run. |
| Review cadence | Re-run whenever the source data schema changes; compare output against previous version. |

## Setup steps

1. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install openai-agents pandas python-dotenv
   ```
2. Create a `.env` file with `OPENAI_API_KEY=<your-key>` and `OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL`. Add `.env` to `.gitignore`.
3. Create `data_dict_agent.py` (see Prompt / instructions section below).
4. Place your CSV files in a folder, for example `./sample_data/`.
5. Run:
   ```
   python data_dict_agent.py --input ./sample_data --output ./data_dictionary.md
   ```
6. Open `data_dictionary.md` in your editor or wiki and review.

## Prompt / instructions

```python
# data_dict_agent.py
import argparse, os, json, pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

@function_tool
def list_csv_files(folder_path: str) -> list:
    """Return all .csv file paths inside folder_path."""
    p = Path(folder_path)
    return [str(f) for f in p.rglob("*.csv")]

@function_tool
def read_csv_sample(file_path: str, max_rows: int = 500) -> dict:
    """Read up to max_rows rows of a CSV and return column statistics."""
    try:
        df = pd.read_csv(file_path, nrows=max_rows, low_memory=False)
    except Exception as e:
        return {"error": str(e), "file": file_path}
    stats = {}
    for col in df.columns:
        series = df[col]
        stats[col] = {
            "dtype": str(series.dtype),
            "null_count": int(series.isna().sum()),
            "null_pct": round(series.isna().mean() * 100, 2),
            "unique_count": int(series.nunique()),
            "sample_values": series.dropna().astype(str).unique()[:5].tolist(),
        }
    return {"file": file_path, "row_count": len(df), "columns": stats}

SYSTEM_PROMPT = """
You are a data-documentation agent. Your job is to produce a complete Markdown data
dictionary from a folder of CSV files.

Steps:
1. Call list_csv_files to get all CSV paths.
2. For each path, call read_csv_sample.
3. For each file, emit a level-2 heading with the filename.
4. Under each heading, emit a Markdown table with columns:
   Column | Type | Null % | Cardinality | Sample values
5. After all files, emit a brief "Coverage notes" section noting any files that
   could not be parsed.
6. Do not invent data. Only report what the tools return.
7. Respond with the complete Markdown text and nothing else.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data_dictionary.md")
    args = parser.parse_args()

    agent = Agent(
        name="DataDictAgent",
        model=os.environ["OPENAI_MODEL"],
        instructions=SYSTEM_PROMPT,
        tools=[list_csv_files, read_csv_sample],
    )
    result = Runner.run_sync(agent, f"Process all CSVs in: {args.input}")
    Path(args.output).write_text(result.final_output)
    print(f"Written to {args.output}")

if __name__ == "__main__":
    main()
```

## Example input

```
sample_data/
  customers.csv      # 1 200 rows: id, name, email, signup_date, plan
  orders.csv         # 8 400 rows: order_id, customer_id, amount, status, created_at
  products.csv       # 340 rows:  sku, name, category, price, stock_qty
```

## Expected output

A `data_dictionary.md` file containing three level-2 sections. Each section holds a table listing every column, its inferred dtype (`int64`, `object`, `float64`, etc.), null percentage, unique-value count, and up to five sample values. A "Coverage notes" section at the end confirms all three files were processed with no errors.

## Eval cases

1. Single-column CSV with no nulls — expects a table with one row and `null_pct = 0.0`.
2. CSV with all-null column — expects `null_pct = 100.0` and `unique_count = 0`.
3. Folder with zero CSV files — agent should return an empty dictionary with a note "No CSV files found."
4. CSV with mixed-type column (integers and strings) — agent must report `dtype = object`, not crash.
5. CSV with 50 000 rows — `max_rows = 500` cap must apply; agent must note "sampled 500 of 50 000 rows."
6. CSV with non-UTF-8 encoding — agent logs a warning row in "Coverage notes" instead of crashing.
7. Nested folder with CSVs in subdirectories — `list_csv_files` uses `rglob`; all files must appear.

## Red-team probes

1. Path traversal: pass `--input ../../etc/` — the `list_csv_files` tool must validate that the resolved path stays inside the intended working directory; if it does not, the recipe implementation should add an explicit allowlist check.
2. Oversized file: provide a 500 MB CSV — the `max_rows` cap should prevent memory exhaustion; confirm the tool returns within 60 seconds.
3. Malformed tool response injection: manually return a dict with a `columns` key containing SQL injection strings — the agent must render them as plain text in the Markdown output, not execute them.

## Failure modes

- Schema-mismatch hallucination: the model invents column names not returned by the tool. Mitigation: prompt says "Only report what the tools return"; add a post-processing check that every column name in the output exists in the tool response.
- Missing file warning omitted: if a file errors and the model silently skips it, the dictionary looks complete but has gaps. Mitigation: assert that the output contains one section per file returned by `list_csv_files`.
- Token-limit overflow: a CSV with hundreds of columns may produce a tool response that exceeds the context window. Mitigation: set a `max_columns` cap (e.g., 100) in `read_csv_sample` and note "truncated" in the output.
- Dtype mis-inference: pandas infers a date column as `object` if formats are mixed. Mitigation: include a note in the Coverage section when `unique_count / row_count < 0.05` for an object column (likely a category).
- Silent encoding fallback: `pd.read_csv` may silently replace bad bytes. Mitigation: use `encoding_errors="strict"` and catch the exception explicitly.

## Cost / usage controls

- Use a cheaper/current small model for routine runs; reserve a stronger current model for dictionaries with more than 50 tables.
- Set `max_tokens=4096` on the completion request to cap per-run spend.
- A 10-file, 50-column dataset is usually a moderate request; calculate dollar cost from token count and the selected model's current pricing.
- Log token usage from `result.usage` after each run.

## Safe launch checklist

- [ ] `.env` is in `.gitignore`; no key appears in source code.
- [ ] Input folder path is validated against an allowlist or clamped to a known working directory.
- [ ] `read_csv_sample` has a `max_rows` cap and a `max_columns` cap.
- [ ] Output path is reviewed by a human before the file is committed to a wiki or shared repo.
- [ ] Agent tracing is enabled; trace logs are stored for 30 days.
- [ ] A test run on synthetic data produces correct output before running on real data.

## Maintenance cadence

Re-verify this recipe when: the OpenAI Agents SDK releases a new major version (check [the SDK changelog](https://github.com/openai/openai-agents-python)); pandas releases a breaking dtype-inference change; or the source data schema changes significantly. At each check, run the seven eval cases above and confirm all pass. Confirm that your selected `OPENAI_MODEL` is still available and appropriate.
