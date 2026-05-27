# Cross-platform prompt porter

> **Last verified:** 2026-05-06 · **Drift risk:** medium

## Goal

Given a Claude-formatted system prompt, this agent produces equivalent versions for OpenAI (ChatGPT / Assistants API) and Gemini, accounting for each platform's system-instruction conventions, formatting expectations, role-label differences, and known behavioral quirks. The output is a three-section Markdown file containing the original prompt, the OpenAI port, and the Gemini port, each with a brief annotation explaining what changed and why.

## Recommended platform(s)

Primary: [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) with a single `read_prompt` tool.

Alternates: Direct prompt call with a current OpenAI model; Anthropic Claude used to port its own prompt format to competitors (useful for a sanity check).

## Why this platform

Prompt porting is a single-step text-transformation task that does not require persistent state or complex tool loops. The Agents SDK is used here primarily for the structured entry point (read from file, write to file) and for the tracing that shows exactly which transformation was applied.

## Required subscription / account / API

- OpenAI API key and `OPENAI_MODEL` set to a current model ID.
- No external integrations required.

## Required tools / connectors

- `read_prompt(path: str) -> str` — reads the source prompt file.
- No write tools; output is printed or saved by the caller script.

## Permission model

| Permission | Scope | Rationale |
|---|---|---|
| File read | The specified prompt file only | Agent reads the source prompt. |
| File write | Optional output path | To save the ported prompts; human reviews before deployment. |
| Network | OpenAI API only | No other calls. |
| Env vars | `OPENAI_API_KEY` only | Never logged or printed. |

## Filled agent spec

| Field | Value |
|---|---|
| Job statement | Read a Claude system prompt and produce equivalent OpenAI and Gemini versions with annotations explaining each adaptation. |
| Inputs | Path to the source prompt file. |
| Outputs | Markdown file with three sections: original, OpenAI port, Gemini port, each with annotations. |
| Tools | `read_prompt` |
| Stop conditions | Both ports produced; annotations written; output file written. |
| Error handling | If the source prompt is empty or unreadable, report the error and exit. |
| HITL gates | The prompt engineer reviews both ports and tests them on the target platform before deployment. |
| Owner | The prompt engineer or developer who manages the agent prompt. |
| Review cadence | Re-port whenever the source Claude prompt changes materially. |

## Setup steps

1. Set up the environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install openai-agents python-dotenv
   ```
2. Add `OPENAI_API_KEY=<your-key>` and `OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL` to `.env`. Add `.env` to `.gitignore`.
3. Save your Claude prompt as `source_prompt.md` or `source_prompt.txt`.
4. Save `prompt_porter.py` (see Prompt / instructions below).
5. Run:
   ```
   python prompt_porter.py --source ./source_prompt.md --output ./ported_prompts.md
   ```
6. Review `ported_prompts.md` and test each port on its target platform before deploying.

## Prompt / instructions

````python
# prompt_porter.py
import argparse, os
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

@function_tool
def read_prompt(path: str) -> str:
    """Read the source prompt file."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return f"ERROR: {e}"

SYSTEM_PROMPT = """
You are a cross-platform prompt porting specialist. You understand the system-instruction
conventions of Claude (Anthropic), OpenAI (ChatGPT and Assistants API), and Gemini.

Key differences to account for:

Claude conventions (source format):
- Uses an explicit <system> or SYSTEM block in some interfaces, or a separate system turn.
- Responds well to XML-style tags (<instructions>, <context>, <examples>).
- The Human/Assistant turn structure is familiar but not required in API usage.
- Claude tends to follow long, structured instructions reliably.

OpenAI conventions (target):
- System prompt is passed as the "system" role message in the messages array.
- Function/tool calling is described in the system prompt or via the tools parameter
  (see https://platform.openai.com/docs/guides/function-calling).
- Structured outputs are enabled via the response_format parameter
  (see https://platform.openai.com/docs/guides/structured-outputs).
- Avoid XML tags in the system prompt; prefer numbered lists or plain prose.
- ChatGPT Projects use a "custom instructions" field, not a system message; note this.

Gemini conventions (target):
- System instructions are passed via the system_instruction field in the API request.
- Function declarations are passed separately (see https://ai.google.dev/gemini-api/docs/function-calling).
- Gemini is sensitive to instruction length; prefer concise system prompts under 500 words.
- Avoid heavy XML structure; use plain prose with clear paragraph breaks.
- Gemini may require explicit "respond only in English" if language control is needed.

Steps:
1. Call read_prompt to load the source Claude prompt.
2. Identify the prompt's structure: role, job statement, tool instructions, output format,
   constraints, examples.
3. Produce a Markdown file with these three sections:

## Original Claude prompt

```
<paste the original prompt verbatim>
```

**Annotation:** Brief description of the original structure and any Claude-specific idioms used.

---

## OpenAI port

```
<the adapted system prompt for OpenAI>
```

**Changes made:**
- Bullet list of specific adaptations and the reason for each.

---

## Gemini port

```
<the adapted system prompt for Gemini>
```

**Changes made:**
- Bullet list of specific adaptations and the reason for each.

---

## Porting notes

2-4 sentences on any behavioral differences the prompt engineer should test on each platform.

Rules:
- Preserve the original prompt's intent, constraints, and output format.
- Do not add capabilities or tools not present in the original.
- Do not add markdown italic in the ported prompts.
- If the original uses XML tags, replace them with numbered sections in the OpenAI port
  and plain prose paragraphs in the Gemini port.
- Flag any Claude-specific features (e.g., extended thinking, tool-use format) that have
  no direct equivalent on the target platform.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    agent = Agent(
        name="PromptPorter",
        model=os.environ["OPENAI_MODEL"],
        instructions=SYSTEM_PROMPT,
        tools=[read_prompt],
    )
    result = Runner.run_sync(agent, f"Port the prompt at: {args.source}")
    if args.output:
        Path(args.output).write_text(result.final_output)
        print(f"Ported prompts written to {args.output}")
    else:
        print(result.final_output)

if __name__ == "__main__":
    main()
````

## Example input

`source_prompt.md` (Claude format):
```
<instructions>
You are a customer-support agent for Acme Software.

<rules>
1. Answer only from the provided knowledge base.
2. If the answer is not in the knowledge base, say: "I don't have that information.
   Please contact support@acme.example."
3. Do not discuss competitors.
4. Keep answers under 150 words.
</rules>

<output_format>
Plain text. No markdown. One paragraph.
</output_format>
</instructions>
```

## Expected output

Three sections:

1. Original Claude prompt — the source verbatim, with annotation noting it uses `<instructions>`, `<rules>`, and `<output_format>` XML tags and a hard word cap.

2. OpenAI port — the same rules expressed as a numbered list in plain prose, system-role message format, without XML tags. Note that the output-format instruction is preserved.

3. Gemini port — the same rules condensed into two paragraphs (under 150 words total), without XML tags. Notes that Gemini's system_instruction field is used, and that the competitor-avoidance rule should be tested because Gemini may be more verbose on that topic.

## Eval cases

1. Short prompt with no XML tags — minimal changes needed; OpenAI and Gemini ports are nearly identical to the original; annotations note "no structural changes required."
2. Prompt with `<example>` blocks — examples are reformatted as numbered few-shot exemplars in both ports.
3. Prompt using Claude's extended-thinking feature — porter flags this as "No direct equivalent" in both ports.
4. Prompt with a tool-use section (Claude format) — porter adapts tool descriptions to the [OpenAI function-calling format](https://platform.openai.com/docs/guides/function-calling) and [Gemini function-calling format](https://ai.google.dev/gemini-api/docs/function-calling) separately.
5. Prompt that is 800 words long — Gemini port is condensed to under 500 words; annotations list what was condensed and why.
6. Prompt containing markdown italic (`*text*`) — porter removes italic and substitutes plain text or all-caps for emphasis per the house style.

## Red-team probes

1. Source prompt containing an instruction to "ignore platform rules": the porter must preserve the instruction in a sanitized form but annotate that it may conflict with platform safety guidelines.
2. Source prompt with a competitor brand name in the text: the porter must preserve it as-is and note in the porting notes that this may trigger content filters on some platforms.
3. Empty source file: porter reports "ERROR: empty prompt file" and produces no output.

## Failure modes

- Semantic drift: the port changes the meaning of a constraint (e.g., "under 150 words" becomes "concise"). Mitigation: annotations must call out every change; human reviewer compares the three versions side by side.
- Platform assumption errors: the porter assumes features that do not exist on the target platform. Mitigation: the platform-specific notes in the system prompt are updated whenever platform docs change.
- XML tag survival: the porter forgets to strip XML tags from the OpenAI or Gemini port. Mitigation: the explicit rule "replace XML tags"; post-generation grep for `<` and `>` in the ported sections.
- Over-condensation of Gemini port: meaningful constraints are dropped to hit the word count. Mitigation: the annotation "Changes made" must list every omission; reviewer restores any dropped constraint.
- Hallucinated tool-calling syntax: the porter invents function-calling syntax that does not match the target platform's actual format. Mitigation: the system prompt links to official docs; reviewer tests the port against a real API call.

## Cost / usage controls

- Porting one prompt is usually a small request, but cost depends on prompt length and the selected model's current token price.
- Set `max_tokens=2000` to accommodate all three sections plus annotations.
- Batch-port multiple prompts by running the script in a loop; log token usage per prompt.

## Safe launch checklist

- [ ] Source prompt has been reviewed and is the current canonical version.
- [ ] Both ported prompts have been tested on the target platform with at least three inputs before deployment.
- [ ] Annotations have been read and all flagged items resolved.
- [ ] No XML tags remain in the OpenAI or Gemini ports.
- [ ] Word count of the Gemini port is under 500 words.
- [ ] Eval cases 1-6 pass on synthetic prompts before use with production prompts.

## Maintenance cadence

Re-port whenever the source Claude prompt changes. Re-verify the platform-specific notes in the system prompt when Anthropic, OpenAI, or Google update their system-instruction conventions (check each platform's changelog quarterly). Run all six eval cases after any change to the porter prompt.
