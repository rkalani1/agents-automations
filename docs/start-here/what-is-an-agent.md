# What is an agent?

> **Last verified:** 2026-05-06 · **Drift risk:** low

## Working definition

An agent is a system that combines four things:

- **A model** — the language model that reasons, plans, and produces text or structured output.
- **Tools** — capabilities the model can invoke: web search, code execution, file reads/writes, API calls, browser control, or anything else you expose.
- **A loop** — the model runs repeatedly, inspecting tool results and deciding what to do next, rather than producing one response and stopping.
- **A stop condition** — a rule (or set of rules) that ends the loop: task complete, error threshold hit, maximum steps reached, or a human says stop.

Remove the loop and you have ordinary chat. Remove the tools and you have a text transformer. Remove the stop condition and you have an infinite loop. All four parts matter.

## One-shot chat vs. agentic loop

| | One-shot chat | Agent |
|---|---|---|
| Turns | 1 prompt → 1 response | Many model calls, interleaved with tool use |
| State | None between turns | Accumulates in context window or external memory |
| Side effects | None | Files written, APIs called, forms submitted |
| Failure modes | Hallucination, refusal | All of the above, plus runaway actions, stuck loops |
| When to use | Q&A, summarization, drafting | Multi-step workflows with external data or actions |

## Minimal mental model

```
while not done:
    thought = model(context)
    if thought.calls_tool:
        result = run_tool(thought.tool, thought.args)
        context.append(result)
    else:
        return thought.final_answer
```

The model never "runs" on its own — your code (or the platform's runtime) drives the loop. The model only decides: which tool to call next, with what arguments, and whether it is finished. Everything else is infrastructure.

## Tool-calling terminology across vendors

The underlying mechanism is the same everywhere, but vendors use different names:

| Vendor | Term in docs |
|--------|-------------|
| OpenAI | [Function calling](https://platform.openai.com/docs/guides/function-calling) / tool use |
| Anthropic | [Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) |
| Google | Function calling / tool use |
| MCP spec | [Tool](https://modelcontextprotocol.io/specification/2025-06-18) (a named callable with a JSON schema) |

"Function calling" and "tool use" mean the same thing at the protocol level. The model emits a structured call; the host executes it; the result goes back into context.

## What counts as a tool?

Anything you can describe with a name, a parameter schema, and a return type. Common examples:

- Read or write a file
- Run a shell command
- Query a database or REST API
- Search the web
- Click a button in a browser ([Anthropic computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use))
- Call another model or sub-agent

!!! note
    A tool is not magic. It is a function your code defines and exposes. The model cannot access tools you have not explicitly registered.

## MCP: a standard tool protocol

The [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18) defines a vendor-neutral wire format for tools, resources, and prompts. An MCP server exposes tools; an MCP client (a model host) calls them. This lets you write a tool once and use it from Claude Desktop, Gemini CLI, or your own agent runtime.

The rest of this guide assumes you understand the four-part definition above. When a later section says "the agent called a tool," it means the model emitted a structured request, your runtime executed it, and the result was appended to context.
