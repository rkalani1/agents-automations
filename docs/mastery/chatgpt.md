> **Last verified:** 2026-05-06 · **Drift risk:** medium · **Plan annotations:** Free / Sub / Team / Ent / API

# ChatGPT mastery

ChatGPT is OpenAI's flagship AI assistant, available as a web app, mobile app, desktop app, and a family of APIs and SDKs. This page walks you from your very first conversation to building multi-agent Python programs. Work through the sections in order, or jump to the level that matches where you are today.

---

## 1. Beginner: your first conversation

### What you are looking at

Open [chatgpt.com](https://chatgpt.com) in any browser. You do not need an account to try the Free tier, though some features require a login. The main screen shows a large text input at the bottom and, if you are logged in, a sidebar on the left listing your past conversations.

At the top of the input area you may see a model picker — a dropdown or row of buttons showing model names like "GPT-4o" or "o1." The default model for Free accounts is GPT-4o mini or GPT-4o depending on traffic. You do not need to change it to follow this section.

### Starting a conversation

1. Click inside the text box (it usually says "Ask anything").
2. Type a question or paste text you want help with — for example: "What is the difference between a virus and a bacterium?"
3. Press Enter or click the send button (an upward arrow or paper-plane icon).
4. ChatGPT's reply appears in the main window. Each exchange is a "turn."

### The GPT picker `Sub / Team / Ent`

If you see a "Explore GPTs" link or a model menu, you can switch to a Custom GPT — a version of ChatGPT pre-configured for a specific task (writing, coding, data analysis, etc.). For now, leave the default. Custom GPTs are covered in section 3.

### Voice and canvas `Sub / Team / Ent`

- Voice mode: tap the microphone icon in the mobile app or (where available) the web app to speak your message and hear a spoken reply.
- Canvas: a split-screen mode where ChatGPT writes on the left and you can edit on the right, useful for document drafting. Trigger it by asking "Open a canvas" or by clicking the canvas icon if visible.

### How to tell whether it worked

If the reply answers your question clearly, it worked. If the reply is off-target:

- Add detail: "I am a high-school student. Explain it simply."
- Ask for a different format: "Give me a bullet list."
- Ask for revision: "That was too technical. Simplify the last paragraph."

These follow-up messages are called "follow-up prompts." You can send as many as you like in the same conversation.

---

## 2. Intermediate: Custom Instructions, memory, Projects, and file uploads

### Custom Instructions `Free / Sub / Team / Ent`

Custom Instructions are standing preferences ChatGPT applies to every conversation. They answer two questions:

- "What would you like ChatGPT to know about you?" — Your role, background, context. Example: "I am a product manager at a B2B SaaS company. Most of my questions relate to roadmap planning and stakeholder communication."
- "How would you like ChatGPT to respond?" — Style, length, format. Example: "Keep answers concise. Use plain English. Avoid bullet lists unless I ask for them."

To set them: click your profile picture or name in the lower-left corner → "Settings" → "Personalization" → "Custom Instructions." Paste your two answers, then toggle "Enable for new chats" on.

Custom Instructions apply globally, not to a single conversation. They are the simplest form of persistent personalisation on the platform.

### Memory `Sub / Team / Ent (where enabled)`

Memory lets ChatGPT save facts about you across conversations. When memory is on, ChatGPT may say "I've noted that you prefer concise answers." You can view saved memories in Settings → "Personalization" → "Manage memories" and delete any item at any time.

Memory is separate from Custom Instructions. Instructions are static text you write once; memory is dynamic and ChatGPT updates it during conversations.

Memory availability varies by region and plan. If it is not visible in your Settings, your account or region is not yet enabled.

### ChatGPT Projects `Sub / Team / Ent`

A Project is a named workspace that groups related conversations and stores shared context. It is the right tool when a topic or client recurs week after week and you do not want to re-explain background each time.

To create a Project:

1. In the left sidebar, click "New project" (or the "+" icon next to "Projects").
2. Give the project a name — for example, "Meeting prep."
3. You are now inside the project. You can upload files and set project-level instructions that apply to every conversation started here.

See [ChatGPT Projects help](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) for full documentation.

A conversation started from the top-level "New chat" button is outside any project and does not inherit project context. Always click "New chat" from inside your project to keep context loaded.

### Attaching files `Sub / Team / Ent`

Click the paperclip icon (or the "+" icon) in the message bar to attach:

- PDFs, Word documents, spreadsheets, text files — ChatGPT reads the content.
- Images — ChatGPT can describe, label, or analyse them.
- CSV or Excel files — with Code Interpreter enabled, ChatGPT can run Python to analyse them.

File uploads are per-conversation by default, or per-project when used inside a project.

---

## 3. Advanced: Custom GPTs, Actions, Tasks, and agent modes

### Custom GPTs end-to-end `Sub / Team / Ent`

A Custom GPT is a configured version of ChatGPT that you package, name, and optionally share. It is the platform's no-code/low-code way to publish a specialist assistant. Full documentation: [Creating and editing GPTs](https://help.openai.com/en/articles/8554397).

To build one:

1. Click your profile picture → "My GPTs" → "Create a GPT."
2. You see two tabs: "Create" (a guided conversation that writes the configuration for you) and "Configure" (direct editing). Switch to Configure for full control.

**The Configure tab fields:**

- **Name:** What users see in the GPT picker. Keep it short and descriptive.
- **Description:** One sentence shown in the GPT store or your workspace.
- **Instructions:** The system prompt. This is the most important field — write detailed role, goal, constraints, and output format here.
- **Conversation starters:** Up to four suggested prompts shown on the welcome screen. Use these to guide users toward the GPT's main tasks.
- **Knowledge files:** Upload reference documents the GPT uses for retrieval. PDFs, text files, and spreadsheets work well. The GPT quotes from these when relevant.
- **Capabilities:**
  - Web search — the GPT can query the web for current information. `Sub / Team / Ent`
  - Canvas — enables the split-screen document editor inside this GPT. `Sub / Team / Ent`
  - DALL-E image generation — the GPT can generate images on request. `Sub / Team / Ent`
  - Code Interpreter — the GPT can run Python to analyse data, create charts, and process files. `Sub / Team / Ent`
- **Actions:** Connect the GPT to external services via an OpenAPI schema. See below.

**Sharing options:**

- Only me (private) — only you can use it. `Sub / Team / Ent`
- Anyone with the link — share the URL with specific people. `Sub / Team / Ent`
- Public (GPT store) — listed in the OpenAI GPT store. `Sub / Team / Ent (with verification)`

### Actions: connecting a Custom GPT to an API `Sub / Team / Ent`

An Action lets your GPT call an external HTTP API — your own server, a third-party service, or a database endpoint — during a conversation. You provide an OpenAPI 3.1 schema; ChatGPT generates the UI for calling it.

Example minimal OpenAPI schema for a note-search action:

```yaml
openapi: "3.1.0"
info:
  title: Note store API
  version: "1.0"
servers:
  - url: https://your-server.example.com
paths:
  /notes/search:
    get:
      operationId: searchNotes
      summary: Search the note store by keyword
      parameters:
        - name: q
          in: query
          required: true
          schema:
            type: string
      responses:
        "200":
          description: List of matching notes
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id: {type: string}
                    title: {type: string}
                    snippet: {type: string}
```

Paste this schema into the Actions editor and ChatGPT can call `searchNotes` on demand.

### ChatGPT Tasks `Sub (where available, drift risk: high)`

Tasks let you schedule a one-off or recurring instruction — for example, "Every Monday morning, produce a summary of the topics I asked about last week." The feature is in limited rollout. Treat any documentation about specific scheduling UI as high-drift: interface and availability change frequently. When Tasks are available, you find them in the sidebar or via the "+ New task" button.

### Agent, coworker, and browser modes `Sub / Team / Ent (drift risk: high)`

OpenAI is iterating rapidly on agentic features inside ChatGPT — capabilities marketed at various times as "agent mode," "coworker mode," or "Atlas." These allow ChatGPT to take multi-step autonomous actions (web browsing, file editing, running code). The specific feature names, availability, and interface change with product releases. This guide marks this area as high-drift. Check the [OpenAI help centre](https://help.openai.com) for current names and availability before building any workflow that depends on these features.

---

## 4. Expert: OpenAI Agents SDK, tool calling, structured outputs, and Codex

### When to use the API vs the app

The app is right for: one-off tasks, exploration, workflows where a human is in the loop at each step.

The API is right for: automation, integration with other systems, evals, workflows that run without a human present, anything where you need programmatic control over inputs and outputs.

### OpenAI Agents SDK `API`

The [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (Python and TypeScript) is a framework for building multi-agent workflows. Key concepts:

- **Agent:** an LLM with a system prompt and a set of tools.
- **Tool:** a Python function the agent can call to take an action or retrieve data.
- **Handoff:** an agent passes control to another agent.
- **Guardrail:** a check run before or after an agent call to validate inputs or outputs.
- **Tracing:** the SDK logs every step; you can view traces in the OpenAI dashboard.

Install:

```bash
pip install openai-agents
export OPENAI_API_KEY=sk-REPLACE_ME
export OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL
```

Minimal agent:

```python
import asyncio
import os
from agents import Agent, Runner

model = os.environ["OPENAI_MODEL"]

meeting_prep_agent = Agent(
    name="Meeting prep",
    instructions="""You are a meeting preparation assistant.
Given a calendar entry and context notes, write a concise one-paragraph brief
covering: the purpose of the meeting, key participants, open questions, and suggested next steps.""",
    model=model,
)

async def main():
    result = await Runner.run(
        meeting_prep_agent,
        "Meeting: 2026-05-10 14:00 — Q2 roadmap review with product and engineering leads.\n"
        "Context: Last week the team shipped the new search feature. Stakeholders want to discuss prioritisation for Q3."
    )
    print(result.final_output)

asyncio.run(main())
```

For current model identifiers, always check [`../model-freshness.md`](../model-freshness.md) — do not hard-code model names in production code.

### Tool calling `API`

Tool calling (also called function calling) lets an LLM request that your code run a function and return the result. The model does not call the function directly — it outputs a structured request, your code handles it, and you return the result. Full documentation: [OpenAI — function calling](https://platform.openai.com/docs/guides/function-calling).

```python
import json
import os
import openai

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
model = os.environ["OPENAI_MODEL"]

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search the meeting notes store by keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "Search term"}
                },
                "required": ["keyword"]
            }
        }
    }
]

messages = [{"role": "user", "content": "Find any notes about the Q2 roadmap."}]
response = client.chat.completions.create(model=model, messages=messages, tools=tools)

tool_call = response.choices[0].message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)

# Your application handles the actual search here.
search_result = f"Found: Q2 roadmap discussion notes from 2026-04-15."

messages.append(response.choices[0].message)
messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": search_result})

final_response = client.chat.completions.create(model=model, messages=messages)
print(final_response.choices[0].message.content)
```

### Structured outputs `API`

Structured outputs constrain the model toward a JSON schema you provide and remove most fragile string parsing. Production code should still validate the returned object before downstream use. Full documentation: [OpenAI — structured outputs](https://platform.openai.com/docs/guides/structured-outputs).

Use the `pydantic` library to define your schema:

```python
import os
import openai
from pydantic import BaseModel

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
model = os.environ["OPENAI_MODEL"]

class MeetingBrief(BaseModel):
    purpose: str
    key_participants: list[str]
    open_questions: list[str]
    suggested_next_steps: list[str]

completion = client.beta.chat.completions.parse(
    model=model,
    messages=[
        {"role": "system", "content": "Extract a structured meeting brief from the input."},
        {"role": "user", "content": "Q2 roadmap review. Attendees: Alice (PM), Bob (Eng lead). "
         "Open question: should feature X ship before the conference? Next step: Alice to write decision doc."}
    ],
    response_format=MeetingBrief,
)

brief = completion.choices[0].message.parsed
print(brief.purpose)
print(brief.open_questions)
```

The `MeetingBrief` object is fully typed — no JSON parsing, no key errors.

### Guardrails and handoffs

In the Agents SDK, guardrails are functions that run before an agent processes input or after it produces output. Use them to enforce content policies, validate formats, or block unsafe requests:

```python
from agents import Agent, GuardrailFunctionOutput, input_guardrail

@input_guardrail
async def block_pii(ctx, agent, input):
    if "@" in str(input) or "SSN" in str(input):
        return GuardrailFunctionOutput(
            output_info="Blocked: PII detected.",
            tripwire_triggered=True
        )

agent_with_guard = Agent(
    name="Safe meeting prep",
    instructions="Prepare meeting briefs.",
    input_guardrails=[block_pii],
)
```

Handoffs let a specialist agent take over from a general one:

```python
from agents import Agent

note_search_agent = Agent(name="Note searcher", instructions="Search meeting notes on request.")
meeting_prep_agent = Agent(
    name="Meeting prep",
    instructions="Prepare meeting briefs. Hand off to the note searcher when the user asks for archived notes.",
    handoffs=[note_search_agent],
)
```

### Tracing

The Agents SDK instruments every agent run automatically. By default it sends traces to OpenAI's tracing service (visible in your OpenAI dashboard). In production, review traces regularly to spot unexpected tool calls, token spikes, and loops.

### Codex CLI vs Codex cloud `API / Sub`

- Codex CLI: a command-line coding assistant for local development. Documentation: [OpenAI Codex CLI](https://developers.openai.com/codex/cli). Install with `npm install -g @openai/codex`. It reads your local file tree and can edit files, run tests, and explain code. Requires an API key.
- Codex cloud (inside ChatGPT): a web-based version accessible from the ChatGPT interface under a "Codex" or "coding agent" entry point. It spins up a sandboxed cloud environment rather than operating on your local files.

Use the CLI when you are working in a local repository. Use the cloud version when you want a zero-setup coding agent in the browser.

### Eval and red-team practices

Before deploying any GPT or agent to other users:

1. Build a small eval set (10–50 examples) covering the main tasks and known edge cases.
2. Run the eval against your current configuration and record pass/fail rates.
3. Red-team the system prompt: try to make the model ignore its instructions, reveal its prompt, or produce harmful output. Document what works so you can patch it.
4. Re-run the eval after every significant change to the system prompt, tools, or model version.
5. For Custom GPTs, test "prompt injection" via knowledge files: upload a file containing adversarial instructions and verify the GPT does not follow them.

### MCP usage `API (where available)`

OpenAI is adding support for MCP (Model Context Protocol) as a standardised way to connect agents to external tools and data sources. When available in the Agents SDK, you register MCP servers the same way you register tools. Check the [OpenAI Agents SDK repository](https://github.com/openai/openai-agents-python) for the current MCP integration status — this is an actively evolving area.

---

## 5. Level up this workflow

A numbered ladder from casual chat to production agent:

1. Open [chatgpt.com](https://chatgpt.com), send a question, read the reply.
2. Write a follow-up message to refine the answer.
3. Fill in Custom Instructions (Settings → Personalization) with your role and response preferences.
4. Enable memory and watch how ChatGPT adapts to you over several conversations.
5. Create a ChatGPT Project for a recurring topic (client, research area, project).
6. Attach a context file to a Project conversation and ask ChatGPT to apply it.
7. Build a Custom GPT with a name, system prompt, and knowledge file.
8. Add one Action to the Custom GPT using a minimal OpenAPI schema.
9. Call the OpenAI chat completions API from Python; use structured outputs to get typed data back.
10. Build a two-agent Agents SDK program with tool calling, a guardrail, and a handoff.

---

## 6. Guided exercise: meeting prep Project to Custom GPT to Agents SDK

This exercise takes 10–20 minutes per stage. Stop at whatever stage matches your current needs or available time.

### What you need

- A ChatGPT account. Stages 1–2 need a Sub plan. Stage 3 needs an API key.
- A synthetic calendar entry and context notes (provided below).

### Synthetic inputs

```
Calendar entry:
Title: Q3 planning kickoff
Date/time: 2026-05-15 10:00–11:00
Attendees: Jordan (VP Product), Sam (Engineering lead), Riley (Design lead), Alex (PMM)
Location: Zoom (link in invite)

Context notes:
- Last quarter's big win: launched real-time search. 20% DAU lift.
- Tension point: engineering wants to reduce scope for Q3 to pay down tech debt.
- Jordan has flagged that the board wants a monetisation feature by Q4.
- Riley's team is under-resourced; they joined two headcount short.
```

### Stage 1 — ChatGPT Project

1. In [chatgpt.com](https://chatgpt.com), click "New project" in the left sidebar.
2. Name it "Meeting prep."
3. Start a new chat inside the project.
4. Paste the calendar entry and context notes. Then ask: "Write a one-paragraph meeting brief for me to read in the two minutes before this call."
5. Review the output. Follow up: "Add a 'watch out' line about any interpersonal or resourcing tensions I should be aware of."

A good output should cover: the purpose of the meeting, who matters and why, the key decision to be made, and any known friction points.

### Stage 2 — Custom GPT

1. Click your profile → "My GPTs" → "Create a GPT."
2. Switch to the Configure tab.
3. Fill in:
   - Name: Meeting brief generator
   - Description: Takes a calendar entry and context notes, returns a one-paragraph pre-meeting brief.
   - Instructions:
   ```
   You are a professional executive assistant.
   When the user provides a calendar entry and context notes, produce a single-paragraph
   meeting brief (100–150 words) covering: purpose, key attendees and their stakes,
   the central decision or tension, and one thing the user should watch for.
   Do not add preamble. Output only the brief.
   ```
   - Conversation starters: "Prepare a brief for my 10am meeting."
4. Add an Action with the note-search OpenAPI schema from section 3 (substitute a real or mock URL).
5. Save and test: paste the synthetic inputs and verify the GPT returns a brief without preamble.

### Stage 3 — Agents SDK (developer mode)

Install and configure:

```bash
pip install openai-agents pydantic
export OPENAI_API_KEY=sk-REPLACE_ME
export OPENAI_MODEL=REPLACE_WITH_CURRENT_MODEL
```

Build the program:

```python
import asyncio
import os
from agents import Agent, Runner, function_tool
from pydantic import BaseModel

model = os.environ["OPENAI_MODEL"]

# Tool: mock note search
@function_tool
def search_notes(keyword: str) -> str:
    """Search the meeting notes store by keyword."""
    # Replace with a real database query in production.
    mock_notes = {
        "monetisation": "Board memo 2026-04-01: monetisation feature required by Q4.",
        "tech debt": "Eng retro 2026-04-28: estimated 6 weeks of debt reduction needed.",
        "headcount": "Design team onboarding delayed; two roles still open as of 2026-05-01.",
    }
    for k, v in mock_notes.items():
        if keyword.lower() in k:
            return v
    return "No matching notes found."

# Structured output
class MeetingBrief(BaseModel):
    brief: str
    watch_out: str

meeting_prep_agent = Agent(
    name="Meeting prep",
    instructions="""You are an executive assistant.
Given a calendar entry and context notes, produce:
1. A 100-150 word meeting brief covering purpose, key attendees, and central tension.
2. A one-sentence 'watch out' about the most significant risk or interpersonal issue.
Use the search_notes tool if you need additional background on any topic.
Return your answer as a MeetingBrief object.""",
    tools=[search_notes],
    output_type=MeetingBrief,
    model=model,
)

CALENDAR_ENTRY = """
Title: Q3 planning kickoff
Date/time: 2026-05-15 10:00-11:00
Attendees: Jordan (VP Product), Sam (Engineering lead), Riley (Design lead), Alex (PMM)
"""
CONTEXT = """
Last quarter launched real-time search (20% DAU lift).
Engineering wants Q3 scope reduction for tech debt.
Board wants monetisation feature by Q4.
Design team is two headcount short.
"""

async def main():
    result = await Runner.run(meeting_prep_agent, CALENDAR_ENTRY + "\n" + CONTEXT)
    brief: MeetingBrief = result.final_output
    print("Brief:")
    print(brief.brief)
    print("\nWatch out:")
    print(brief.watch_out)

asyncio.run(main())
```

Run it: `python meeting_prep_agent.py`

The agent will search for notes on "tech debt," "monetisation," and "headcount" before writing the brief. The output is a typed `MeetingBrief` object — no string parsing needed.

Stop here if this is enough. The next logical step would be to add a second agent (a calendar-fetching agent that retrieves the entry from a live calendar API) and implement a handoff.

---

## 7. Plan availability table

| Capability | Free | Sub | Team | Ent | API |
|---|---|---|---|---|---|
| Plain chat (chatgpt.com) | Yes | Yes | Yes | Yes | — |
| Custom Instructions | Yes | Yes | Yes | Yes | — |
| Memory | No | Partial | Yes | Yes | — |
| Projects | No | Yes | Yes | Yes | — |
| File uploads | Partial | Yes | Yes | Yes | — |
| Custom GPTs (create) | No | Yes | Yes | Yes | — |
| Actions (in Custom GPTs) | No | Yes | Yes | Yes | — |
| Tasks (scheduled) | No | Partial | Partial | Partial | — |
| Agent / browser mode | No | Partial | Partial | Yes | — |
| Codex cloud (in ChatGPT) | No | Partial | Yes | Yes | — |
| OpenAI API (chat completions) | — | — | — | — | Yes |
| Agents SDK | — | — | — | — | Yes |
| MCP (via Agents SDK) | — | — | — | — | Partial |

"Partial" means the feature exists but has rate limits, regional restrictions, or is in limited beta. Always check the [OpenAI pricing page](https://openai.com/pricing) and [help centre](https://help.openai.com) for the current plan matrix.

---

## 8. Fallback: what to do when a feature is missing on your plan

**No Projects:**
Use Custom Instructions to carry your most important context. Start each conversation by pasting a short "context block" — three to five sentences that re-establish the background. Keep this block in a snippet manager so you can paste it in seconds.

**No Custom Instructions:**
Paste a standing context paragraph as the first message in every new conversation. Example: "I am a product manager. I will ask you questions about roadmap planning. Keep answers concise and use plain language." This is slower but functionally equivalent.

**No Memory:**
Maintain a short "facts about me" text file. Paste the relevant facts at the start of conversations where they matter. Review and update the file monthly.

**No Custom GPTs:**
Write your GPT's system prompt as a long saved prompt. Paste it at the top of a new conversation each time you need that specialist assistant. The behaviour is identical; the activation method is manual.

**No Actions (in Custom GPTs):**
Before the conversation, open the external service, copy the relevant data, and paste it into the chat. If you do this frequently, write a short script that fetches the data and formats it for pasting.

**No Tasks:**
Set a calendar reminder to manually run the prompt on schedule. If you need lightweight automation, write a Python script that calls the OpenAI API on a schedule you manage (for example, via cron on a server you control).

**No agent / browser mode:**
Perform web tasks manually. For structured research tasks, provide ChatGPT with the raw content (copied from the browser) and ask it to reason over it.

**No API access:**
All API capabilities can be approximated in the chat interface — more slowly and manually, but feasibly. The key constraint is programmatic integration: if you need ChatGPT output to flow directly into another system without human copy-paste, you need the API.

**No Agents SDK:**
Use the raw chat completions API with tool calling. The Agents SDK is a convenience layer; everything it does can be replicated with direct API calls, more code, and a hand-rolled loop that processes tool call responses. Start here to understand what the SDK abstracts before choosing to use it.
