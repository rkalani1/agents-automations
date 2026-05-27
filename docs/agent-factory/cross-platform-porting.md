> **Last verified:** 2026-05-06 · **Drift risk:** low

# Cross-platform porting

A prompt pack written for one platform rarely runs correctly on another without adaptation. Each platform has its own conventions for where system instructions live, how tools are defined, how structured output is specified, and how refusals are expressed. This page documents those conventions for the four platforms most commonly used by field guide readers: Claude (Project + Code), OpenAI (Agents SDK + Custom GPT + Codex), Gemini (Gems + API), and GitHub Copilot.

## What porting does and does not change

Porting adapts the delivery mechanism, not the intent. The job statement, stop conditions, and constraint list from the spec should survive the port unchanged. What changes is how those constraints are expressed in the syntax and idioms each platform expects. A constraint written as "do not access external URLs" is the same constraint whether it appears in a Claude project instruction, an OpenAI system message, a Gemini system instruction, or a Copilot agent description — the location and formatting differ, but the meaning does not.

## Claude: Project instructions and Claude Code

In Claude Projects, the system instruction is set in the project's instruction field, which persists across all conversations in that project. This is the canonical location for the agent's role definition, scope, constraint list, and output format instructions. Individual conversation turns should not re-state constraints already in the project instruction.

For tool use, Claude accepts a tools array in the API request. Each tool is defined with a name, description, and JSON Schema for its input parameters. The description field is important: Claude uses it to decide when to call the tool, so a vague description leads to incorrect tool selection.

For refusal idioms, Claude's default behavior is to produce a verbose, apologetic refusal. In most agent contexts this is undesirable. The system instruction should explicitly specify the refusal style: "When declining a request, give a one-sentence explanation and do not apologize." This reduces output verbosity and keeps the agent's tone consistent.

Claude Code operates as a coding agent in the terminal. Instructions are provided via the `CLAUDE.md` file in the project root, which is automatically loaded as context. See the [Claude Code setup documentation](https://code.claude.com/docs/en/setup) for how `CLAUDE.md` interacts with project-level and directory-level instructions. When porting a code-related agent to Claude Code, the `CLAUDE.md` file is the primary location for the system instruction.

## OpenAI: Agents SDK, Custom GPT, and Codex

### Agents SDK

The [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) provides a Python-native way to define agents with explicit tool lists, handoff logic, and guardrails. The system prompt is passed as the `instructions` parameter when constructing an `Agent` object. Tool definitions are Python functions decorated with the SDK's tool decorator; docstrings serve as tool descriptions and are passed to the model automatically.

For structured output, the Agents SDK supports passing a Pydantic model as the `output_type` parameter on the `Agent` constructor. This triggers [OpenAI's structured outputs](https://platform.openai.com/docs/guides/structured-outputs) mode, which constrains the model to produce JSON that validates against the schema. When porting an agent with a JSON output requirement, this is the most reliable approach: define a Pydantic model matching the schema, pass it as `output_type`, and remove explicit format instructions from the system prompt — the schema constraint replaces them.

Refusal behavior in the Agents SDK can be handled with input and output guardrails. An input guardrail is a function that runs before the agent processes a turn and can return a guardrail result that terminates the turn with a specific message. This is more reliable than relying on the system prompt alone for hard constraints.

### Custom GPT

In the Custom GPT interface, the system instruction is the "Instructions" field. Tool definitions use OpenAPI schema format for Actions. Structured output is not configurable directly in the Custom GPT interface — it depends on the underlying model's default behavior. For format-sensitive agents, the system prompt must carry explicit schema instructions and the eval suite must check format compliance carefully.

### Codex CLI

The [Codex CLI](https://developers.openai.com/codex/cli) runs as a coding assistant in the terminal. The system prompt is passed via the `--system-prompt` flag or set in a configuration file. Porting a coding agent to Codex CLI requires ensuring that all tool calls are within the set of shell commands Codex is permitted to run, and that the constraint list explicitly addresses any dangerous shell operations (e.g., "do not run commands that delete files").

## Gemini: Gems and API

### Gems

Gemini Gems are the equivalent of Custom GPTs. The system instruction is the "Instructions" field in the Gem configuration. Tool definitions are not directly configurable for most Gem users; Gems rely on Google's built-in tools (Search, code execution, etc.) rather than custom tool schemas.

### Gemini API with function calling

The Gemini API supports [function calling](https://ai.google.dev/gemini-api/docs/function-calling) via a tools array in the request. Each tool is defined with a `FunctionDeclaration` that includes name, description, and parameters in JSON Schema format. The structure is similar to OpenAI's tool definition format but uses slightly different field names — `parameters` rather than `input_schema`, and `properties` at the top level of the schema.

For structured output, Gemini supports a `response_schema` parameter in the generation config and `response_mime_type: "application/json"`. This constrains the model to produce JSON matching the schema, similar to OpenAI's structured outputs mode. When porting, map the Pydantic model or JSON Schema from the OpenAI spec to Gemini's `response_schema` field.

Refusal idioms in Gemini default to safety-filter blocks at the API level. For agents where the refusal behavior needs to be customized, the system instruction should specify the desired refusal style, and the eval suite should verify that the instruction-level refusal takes precedence over generic refusal language.

## GitHub Copilot cloud agent

The [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) operates in the context of a GitHub repository and responds to issues and pull request comments. The agent's behavior is not controlled by a system prompt in the traditional sense; instead, it is shaped by a `copilot-instructions.md` file in the `.github` directory of the repository.

Key porting considerations for Copilot:

- System instruction location: `.github/copilot-instructions.md`. This file should contain the agent's scope, constraint list, and any output format requirements.
- Tool scope: the Copilot agent has access to the repository contents and can open pull requests; it does not have access to arbitrary external APIs unless explicitly integrated.
- Structured output: not applicable in the same way as API-based platforms; output is natural-language code and explanations in PR comments. Format compliance is enforced by code review, not schema validation.
- Refusal idioms: the agent should be instructed to leave a comment explaining why it cannot fulfill a request rather than silently not responding.

## Porting checklist

When porting a prompt pack to a new platform, verify each of the following:

- [ ] The system instruction is in the correct location for the platform.
- [ ] All tools from the original spec are available on the target platform, or substitutes are documented.
- [ ] Structured output constraints are implemented using the platform's native mechanism, not only via system prompt instructions.
- [ ] The refusal style matches the agent's tone specification.
- [ ] At least 5 golden cases from the original eval suite pass on the ported version before the port is considered complete.
- [ ] Any platform-specific limitations (e.g., Gem's lack of custom tools) are documented in the porting note and communicated to the owner.
