> **Last verified:** 2026-05-06 · **Drift risk:** medium-high · **Plan annotations:** Free / Sub / Team / Ent / API

# Gemini mastery

Gemini is Google's family of multimodal language models, delivered through a consumer chat product at [gemini.google.com](https://gemini.google.com), a developer playground at [Google AI Studio](https://ai.google.dev/aistudio), and a programmatic interface through the [Gemini API](https://ai.google.dev/gemini-api/docs). This page walks you from your first conversation to running production agents, step by step.

Cross-reference [../model-freshness.md](../model-freshness.md) before relying on any model identifier — Google regularly promotes new model versions and retires older ones.

---

## 1. Beginner: first conversation, model picker, voice

### Opening the chat

Go to [gemini.google.com](https://gemini.google.com) in any modern browser. Sign in with a Google account — a personal Gmail account qualifies. You land on a clean chat interface with a text box at the bottom. Type any message and press Enter or click the send button (arrow icon). The model responds in the main panel.

**How to tell whether it worked:** you see a reply stream in, character by character. If the page shows a loading spinner that never resolves, reload the tab and try again.

**Plan annotation:** The base interface is **Free** with a Google account. Rate limits apply; if you hit them the page will display a message asking you to wait or upgrade.

### Choosing a model

In the top-left corner of the chat panel, look for a dropdown that currently shows the active model name (something like "Gemini 2.0 Flash" or "Gemini 1.5 Pro"). Click it to open the model picker. You will see a list of available models. Descriptions next to each model indicate speed, capability tier, and context window. Select the model that fits your task:

- Flash models: fast, lower cost, good for most everyday tasks. **Free** and **Sub**.
- Pro models: deeper reasoning, longer context. **Sub** (Gemini Advanced) and **API**.
- Experimental or preview models: cutting-edge, may be unstable. **Sub** and **API**. Mark any workflow depending on these as drift risk: high.

After selecting a model, your next message uses it. The picker resets to default if you start a new conversation.

### Using voice input

On the text box, look for a microphone icon. Click it, allow microphone access in your browser when prompted, and speak your message. The system transcribes your speech into the text box. Review the transcription, then send. There is no always-on voice agent in the base web app; each interaction is push-to-talk.

On mobile (Android or iOS), the Gemini app offers a richer voice experience with spoken responses. The web app at gemini.google.com does not auto-speak responses by default.

**Plan annotation:** Voice input is **Free**.

### The "Saved info" and personalization area

Click your profile picture or avatar in the top-right corner, then choose **Settings** (or look for a "Personalization" entry in the left sidebar, depending on the current UI layout — this area drifts frequently). Inside, find **Saved info** or **Personalization**. Here you can enter facts about yourself — your profession, preferred response style, topics you care about — and Gemini will incorporate them into future responses. Think of it as a standing context block that prepends to every conversation.

What to paste: short declarative facts. Example: `I am a software engineer. Respond at an intermediate technical level. Prefer concise bullet points over long paragraphs.`

**Plan annotation:** Saved info is **Free** for personal Google accounts. Enterprise management of system-level instructions belongs to the Workspace tier (**Team / Ent**).

---

## 2. Intermediate: Drive integration, file uploads, memory, image generation

### Attaching files and context

In the chat text box, click the **+** or paperclip icon to open the attachment menu. You can upload files from your local machine (PDFs, text files, images, spreadsheets) or connect to Google Drive. The Drive option — where you can reference a specific Google Doc, Sheet, or Slide — requires a Google account with Drive access. When you attach a Drive file, Gemini reads its content as context for the conversation without you having to copy-paste.

What to click: text box → paperclip → **Upload from Drive** → navigate to your file → **Insert**. You will see a chip (a small tag) appear in the text box indicating the file is attached. Send your message; the model answers with that file's content in context.

Large files consume context window. Watch for a warning that the file is too large; if one appears, try a condensed version or extract the relevant section first.

**Plan annotation:** Local file uploads are **Free**. Drive integration requires a Google account and is **Free** for personal accounts. Deeper Workspace integrations (company Drive, Shared Drives, admin-controlled policies) require **Team / Ent**.

### Saved info as the closest thing to memory

Gemini does not currently maintain persistent memory across conversations the way some other tools do. The "Saved info" block (described in section 1) is the primary mechanism for personalization. Each new conversation starts fresh unless you rely on:

1. The Saved info block.
2. Manually pasting previous context into a new chat.
3. A Gem (see section 3) with a Knowledge file.

If you need genuine persistent memory across sessions, building on the Gemini API with your own storage layer is the right path. See section 4.

### Uploading files for analysis

Beyond Drive attachments, you can drag and drop local files directly into the chat area, or use the paperclip upload path. Supported types include PDFs, images (JPEG, PNG, WEBP, GIF), text files, and common document formats. After uploading, ask the model anything about the content: summarize this PDF, extract the table from this image, compare these two documents.

**Plan annotation:** File uploads are **Free** with limits on file size and number per session. Higher limits and larger files are available under **Sub** (Gemini Advanced).

### Image generation flows

Gemini supports image generation inline in the chat. Type a prompt like "Generate an image of a futuristic city skyline at dusk" and send it. If the model and your plan support image generation, you will see an image appear in the response. Look for a download icon beneath the image to save it locally.

Image generation quality and availability depend on which model is active. Some models in the picker do not support image generation; if yours does not, the response will be text-only. Switch to a model labeled with image generation capability if needed.

**Plan annotation:** Image generation is **Sub** (Gemini Advanced) for higher quality and higher volume. Limited image generation may be available **Free** depending on Google's current rollout.

---

## 3. Advanced: Gems, Deep Research, code capabilities, Agent mode

### Gems end-to-end

A Gem is a saved, reusable custom assistant. You configure it with instructions and optional knowledge files, then invoke it any time you want that specific behavior without re-prompting. To create one:

1. Open [gemini.google.com](https://gemini.google.com). In the left sidebar, find the **Gems** section and click **New Gem** (or the **+** icon next to "Gems"). If you do not see this sidebar item, look for Gems under the hamburger menu. Refer to [Gems help](https://support.google.com/gemini/answer/15235603?hl=en) for the current UI path.
2. Give the Gem a name and optional description.
3. In the **Instructions** field, write the system-level behavior you want. Be specific: state the role, the output format, the tone, any constraints. Example: `You are a research summarizer. When given scientific abstracts, extract: (1) research question, (2) method, (3) key finding, (4) limitation. Always output in a four-field structured list. Do not editorialize.`
4. In the **Knowledge** section, click **Upload files** to attach reference documents. These become persistent context for every conversation with this Gem.
5. Click **Save**. The Gem now appears in your sidebar.

To use it: click the Gem name in the sidebar and start chatting. The instructions and knowledge files are active.

**Plan annotation:** Gems are **Sub** (Gemini Advanced). The number of Gems you can create and the size of knowledge files may be limited; check current limits in [Gems help](https://support.google.com/gemini/answer/15235603?hl=en).

### Sharing Gems

After saving a Gem, open it and look for a **Share** option (a link icon or share button). You can generate a link that lets others use — but not edit — your Gem. This is useful for team rollouts. Editing access stays with the creator.

**Plan annotation:** Sharing is **Sub**. Enterprise-managed sharing belongs to **Team / Ent**.

### Deep Research

Deep Research is a Gemini feature that, when given a question or topic, breaks the task into a multi-step research plan, searches the web, synthesizes findings, and returns a structured long-form report. To trigger it:

1. Start a new chat.
2. In the model picker, select a model labeled **Deep Research** (the exact label may vary).
3. Type your research query and send.
4. Gemini will first show a research plan. You can review and adjust it before it runs.
5. The system then executes searches and returns a report, often with inline citations.

Deep Research is not an always-on agent; it runs one research cycle per invocation. You cannot leave it running unattended. For fully autonomous research loops, use the Gemini API with agentic orchestration (see section 4).

**Plan annotation:** Deep Research is **Sub** (Gemini Advanced). Availability and model selection drift; verify in-app.

### Agent mode and Cowork (drift risk: high)

Google has experimented with "Agent mode" and a "Cowork" collaborative-canvas surface inside Gemini. Availability of these features changes frequently based on region, account type, and rollout phase. If you see an "Agent" tab or a canvas option in your sidebar, these represent Gemini's ability to operate on multi-step tasks using browser or tool access. Mark any workflow that depends on these as **drift risk: high** and verify that the feature is still present before building on it.

**Plan annotation:** Agent and Cowork features, where available, are **Sub** or **Ent**.

### Code-related capabilities

In any Gemini chat, you can paste code and ask questions about it: explain this function, find the bug, refactor for readability, translate from Python to TypeScript. The response includes formatted code blocks with syntax highlighting. A copy icon sits at the top-right of each code block.

For longer coding sessions, the inline editor experience inside AI Studio (section 4) is more capable than the consumer chat. Inside the consumer chat, code capabilities are primarily read-and-explain rather than execute-and-iterate.

**Plan annotation:** Code assistance in chat is **Free** and **Sub**.

---

## 4. Expert: Gemini API, AI Studio, Gemini CLI, Vertex AI

### Google AI Studio

[Google AI Studio](https://ai.google.dev/aistudio) is Google's browser-based developer environment for the Gemini API. It is the fastest path from zero to a working API call. Go to [ai.google.dev/aistudio](https://ai.google.dev/aistudio), sign in with a Google account, and you land on a prompt playground. Here you can:

- Write and test prompts with adjustable parameters (temperature, top-p, max output tokens).
- Switch between Gemini model versions without writing code.
- Add system instructions to a prompt to simulate a custom assistant.
- Upload files directly into the prompt context.
- View the raw API request and response in a side panel.

To get an API key: in AI Studio, click **Get API key** in the left sidebar, or go directly to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey). Create a new key and copy it. Store it in an environment variable:

```bash
export GEMINI_API_KEY="YOUR_KEY_HERE"
```

Never paste a real key into source code. Use `GEMINI_API_KEY` as the variable name by convention.

**Plan annotation:** AI Studio is **Free** for development with usage-based rate limits. Higher rate limits and production SLAs require the **API** billing tier.

### Calling the Gemini API from Python

Install the current SDK. Google has published the `google-genai` package as the newer unified client (check [ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs) for the current recommended package, as the naming has shifted between `google-generativeai` and `google-genai`):

```bash
pip install google-genai
```

Basic generation call:

```python
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

response = client.models.generate_content(
    model=model,
    contents="Explain the difference between precision and recall in two sentences.",
)
print(response.text)
```

Read the model identifier from the `GEMINI_MODEL` environment variable so that upgrading to a newer model requires only an environment change, not a code change. See [../model-freshness.md](../model-freshness.md) for how to track model lifecycle.

### Function calling

Function calling lets the model request that your code execute a function and return results, enabling tool-augmented agents. The model does not call functions directly; it outputs a structured call descriptor that your code interprets, runs, and feeds back. Full reference: [Gemini function calling docs](https://ai.google.dev/gemini-api/docs/function-calling).

```python
import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

def get_weather(location: str) -> dict:
    # Replace with a real weather API call in production
    return {"location": location, "temperature_c": 22, "condition": "partly cloudy"}

weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Returns current weather for a location.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "location": types.Schema(type=types.Type.STRING, description="City name"),
                },
                required=["location"],
            ),
        )
    ]
)

response = client.models.generate_content(
    model=model,
    contents="What is the weather in Berlin right now?",
    config=types.GenerateContentConfig(tools=[weather_tool]),
)

# Check whether the model issued a function call
candidate = response.candidates[0]
part = candidate.content.parts[0]
if part.function_call:
    call = part.function_call
    result = get_weather(**dict(call.args))
    print("Function result:", json.dumps(result))
```

For multi-turn agentic loops, feed the function result back to the model in a follow-up `generate_content` call. The [function calling docs](https://ai.google.dev/gemini-api/docs/function-calling) show the full turn structure.

**Plan annotation:** Function calling is **API** (billed per token). Available in AI Studio for testing at **Free** rate limits.

### Structured output

Structured output constrains the model's response to a specific JSON schema, which is essential for agent pipelines that parse model output programmatically. Reference: [Gemini structured output docs](https://ai.google.dev/gemini-api/docs/structured-output).

```python
import os
from google import genai
from google.genai import types
import typing

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

class ResearchSummary(typing.TypedDict):
    research_question: str
    method: str
    key_finding: str
    limitation: str

response = client.models.generate_content(
    model=model,
    contents="Abstract: This study examined the effect of sleep duration on working memory in adults aged 25-40. We used a randomized crossover design with 60 participants. Short sleep (5h) significantly reduced working memory capacity compared to normal sleep (8h). A limitation is the small sample size.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ResearchSummary,
    ),
)

import json
summary = json.loads(response.text)
print(summary)
```

The `response_mime_type="application/json"` and `response_schema` combination forces output that validates against your schema. If parsing fails, inspect `response.text` for the raw string.

**Plan annotation:** Structured output is **API**. Free-tier rate limits in AI Studio apply.

### Gemini CLI

The [Gemini CLI](https://github.com/google-gemini/gemini-cli) is an open-source command-line interface for Gemini. Install it with Node.js:

```bash
npm install -g @google/gemini-cli
```

Authenticate either with your Google account (OAuth flow, no API key needed for personal use) or with an API key:

```bash
gemini auth login          # browser-based Google account OAuth
# or
export GEMINI_API_KEY="YOUR_KEY_HERE"
```

Basic usage:

```bash
gemini "Summarize the file README.md" < README.md
```

The CLI can pipe files into prompts, making it useful for scripting Gemini into shell workflows. Check the [repository](https://github.com/google-gemini/gemini-cli) for the current command reference, as the CLI is actively developed and commands drift.

**Plan annotation:** CLI with personal Google account OAuth is **Free** within usage limits. Using an API key bills against your **API** quota.

### Antigravity (drift risk: high)

[Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity) is Google's agent-first IDE experiment. It integrates Gemini deeply into a coding environment, enabling multi-step code generation, automated test running, and iterative refinement. Because this project is in active development, treat any Antigravity-specific workflow as **drift risk: high**. Verify the codelab is still active and follow its current instructions rather than assuming this page's description is current.

**Plan annotation:** Antigravity availability and pricing are experimental. Check the [codelab](https://codelabs.developers.google.com/getting-started-google-antigravity) for current status.

### Vertex AI (brief mention)

For production enterprise deployments, [Vertex AI](https://cloud.google.com/vertex-ai) is Google Cloud's managed ML platform that hosts Gemini models alongside other Google and open-source models. Vertex AI adds enterprise features: VPC service controls, private endpoints, audit logging, fine-tuning, model evaluation pipelines, and committed-use pricing. The Gemini API and Vertex AI use similar SDK calls; the main difference is authentication (service accounts instead of API keys) and endpoint configuration. For a field-guide agent builder, start with the Gemini API directly; graduate to Vertex AI when you need enterprise controls.

**Plan annotation:** Vertex AI is **Ent** / GCP billing.

---

## 5. Level up this workflow

1. **Visit [gemini.google.com](https://gemini.google.com), send your first message.** Confirm the response arrives and note which model was active. (Free)
2. **Explore the model picker.** Try the same prompt on Flash vs. Pro and compare quality vs. speed. (Free / Sub)
3. **Fill in Saved info.** Write 3–5 facts about yourself and your preferred output style. Notice how subsequent responses adapt. (Free)
4. **Upload a file.** Attach a PDF or text file and ask the model to summarize it. (Free)
5. **Create your first Gem.** Write focused instructions, attach one knowledge file, save, and verify the Gem follows your instructions. (Sub)
6. **Run a Deep Research query.** Review the research plan before approving it; compare output quality to a plain chat answer. (Sub)
7. **Open AI Studio.** Reproduce your best Gem prompt in the playground, adjust temperature and system instructions, and inspect the raw API call in the side panel. (Free with rate limits)
8. **Get an API key and make your first Python call.** Run the basic generation example from section 4 with your own prompt. (API)
9. **Add function calling.** Extend your script to expose one tool to the model and handle the function-call response. (API)
10. **Add structured output.** Define a schema for your use case and validate that the model's output consistently conforms. (API)
11. **Install and use the Gemini CLI.** Pipe a local file into the CLI and script a one-liner that saves output to a file. (Free / API)
12. **Design an agentic loop.** Combine function calling, structured output, and a simple retry/eval loop in Python. Use `GEMINI_MODEL` from the environment. (API)

---

## 6. Guided exercise: build a "research summary Gem"

**Goal:** Create a Gem that accepts scientific abstracts and returns a structured one-page summary. Then promote the same workflow to the Gemini API with structured output.

### Part A: Gem in the consumer UI

**Step 1 — Prepare three synthetic abstracts.** Create a text file with three short, made-up research abstracts. Example:

```
Abstract 1:
This study investigated the impact of ambient noise on reading comprehension among university students. A within-subjects design was used with 80 participants exposed to silence, 50 dB background noise, and 70 dB noise. Reading comprehension scores declined significantly at 70 dB. The study was limited to a single university setting.

Abstract 2:
We examined whether spaced-repetition flashcard software improves vocabulary retention compared to massed practice. Forty adult learners of Mandarin were randomly assigned to conditions over six weeks. The spaced-repetition group retained 22% more words at follow-up. Self-selection of study times was not controlled.

Abstract 3:
This paper reports on a pilot program that offered coding bootcamps to unemployed adults over 12 weeks. Employment rates at 6-month follow-up were compared against a waitlist control group. Participants in the bootcamp were 2.3x more likely to report tech-sector employment. The study lacked randomization.
```

**Step 2 — Create the Gem.** In the left sidebar, click **Gems** → **New Gem**. Name it "Research Summarizer".

**Step 3 — Write Gem instructions.** In the Instructions field, paste:

```
You are a scientific literature assistant. For every abstract the user submits, extract and return exactly four fields in a numbered list:
1. Research question: one sentence stating what the study asked.
2. Method: one sentence describing the study design and sample.
3. Key finding: one sentence stating the main result with any reported number.
4. Limitation: one sentence naming the primary constraint acknowledged by the authors.
Do not add commentary, caveats, or introductory text. Output only the four-field list.
```

**Step 4 — Add a knowledge file.** Upload the three-abstract text file you created in Step 1.

**Step 5 — Save and test.** Click **Save**. Then open the Gem and type: "Summarize the three abstracts in the knowledge file." Verify the response is a clean four-field list for each abstract.

**Expected output:** Three blocks, each with exactly the four numbered fields, no extra prose.

### Part B: promote to Gemini API with structured output

**Step 6 — Reproduce in AI Studio.** Go to [ai.google.dev/aistudio](https://ai.google.dev/aistudio). Create a new prompt. Paste your Gem instructions as the System instructions. Paste Abstract 1 as the user message. Confirm it returns the four fields.

**Step 7 — Enable structured output in AI Studio.** In the right panel, find **Output format** or **Response schema** settings. Define a JSON schema with four string fields: `research_question`, `method`, `key_finding`, `limitation`. Run the prompt and confirm the output is valid JSON.

**Step 8 — Port to Python.** Use the structured output code example from section 4, replacing the contents with Abstract 1. Run the script and assert that `json.loads(response.text)` succeeds and returns all four keys.

**Step 9 — Process all three abstracts in a loop.** Wrap the API call in a for-loop over a list of abstract strings and print structured results for each.

**Completion check:** You have a reusable Gem for quick in-browser use and a Python script that batch-processes abstracts and returns machine-parseable JSON. Both use the same instructions; the API version adds schema enforcement.

---

## 7. Plan availability table

| Feature | Free | Sub (Gemini Advanced) | Team / Ent | API |
|---|---|---|---|---|
| Basic chat at gemini.google.com | Yes | Yes | Yes | — |
| Model picker (Flash models) | Yes | Yes | Yes | Yes |
| Model picker (Pro / experimental models) | Limited | Yes | Yes | Yes |
| Voice input (web) | Yes | Yes | Yes | — |
| Saved info / personalization | Yes | Yes | Admin-managed | — |
| File uploads (local) | Yes, size-limited | Yes, higher limits | Yes | Yes |
| Google Drive attachment | Yes | Yes | Yes (Workspace) | — |
| Image generation in chat | Limited rollout | Yes | Yes | Yes |
| Gems (create and use) | No | Yes | Yes | — |
| Gems (share) | No | Yes | Yes | — |
| Deep Research | No | Yes | Yes | — |
| Agent / Cowork modes | No | Limited (drift high) | Limited (drift high) | — |
| AI Studio playground | Yes (rate-limited) | Yes | Yes | Yes |
| Gemini API key | Yes (free tier) | — | — | Yes (billed) |
| Function calling | No (consumer) | No (consumer) | No (consumer) | Yes |
| Structured output | No (consumer) | No (consumer) | No (consumer) | Yes |
| Gemini CLI | Yes (OAuth, free limits) | — | — | Yes (API key) |
| Antigravity IDE | Experimental | Experimental | Experimental | Experimental |
| Vertex AI (enterprise) | No | No | No | Ent / GCP billing |

---

## 8. Fallback

Use this table when a feature is unavailable on your current plan or the feature has drifted.

| Feature | If unavailable in Gemini | Fallback |
|---|---|---|
| Gems (Sub required) | No Gem builder on Free plan | Use the "Saved info" block plus a well-structured preamble in each chat; or switch to a free custom assistant in Claude (Projects) or ChatGPT (GPT builder with free-tier limit) |
| Deep Research (Sub required) | Not available on Free | Use the Gemini API with a multi-turn search loop; or use Perplexity's research mode (free tier available) |
| Persistent memory across sessions | Not available in consumer chat | Store context in a text file and paste the relevant portion at the start of each session; or build a memory layer with the API + a vector store |
| Function calling / structured output (API only) | Not available in consumer chat | Use AI Studio structured output UI for manual testing; promote to API for automation |
| Agent / Cowork mode (drift high) | Feature may have been removed or renamed | Check [gemini.google.com](https://gemini.google.com) for current feature listing; use the Gemini API with an orchestration library (LangChain, LlamaIndex) as a stable alternative |
| Gemini CLI (Node.js required) | Node not available in environment | Use the Python SDK directly or call the REST API with `curl` |
| Image generation in chat | Not available on Free or current model | Switch to a Pro/Advanced model in the model picker; or use the Gemini API's image generation endpoint; or use an external image generation service |
| Antigravity IDE | Experimental, may be offline | Use AI Studio with the code execution capability; or use GitHub Copilot / Cursor as a stable alternative |
| Vertex AI | GCP account / billing required | Continue with the Gemini API direct endpoint; consult your organization's GCP admin if enterprise controls are needed |
