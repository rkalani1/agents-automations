> **Last verified:** 2026-05-06 · **Drift risk:** medium · **Plan annotations:** Free / Sub / Team / Ent / API

# Perplexity mastery

Perplexity is an AI-powered answer engine that combines a large language model with live web retrieval. Every answer it produces is grounded in real-time search results and annotated with clickable source citations. This page takes you from opening the product for the first time through building programmatic, search-grounded pipelines with the Sonar API.

---

## 1. Beginner: ask a question and verify the answer

### What you are looking at

Go to [perplexity.ai](https://www.perplexity.ai). The interface is a single search bar in the centre of the screen. There is no setup required for free use. If you want to save your history, create a free account with an email address or a Google or Apple login.

Type a question in plain language — for example: `What are the main causes of inflation?` — and press Enter or click the arrow button. Within a few seconds you will see:

- A prose answer in the main panel.
- Numbered superscript citations inline with the text (for example `[1]`).
- A source list on the right side (desktop) or below the answer (mobile) showing the title and domain of each cited page.
- A row of follow-up question suggestions at the bottom.

### How to tell whether it worked

A correct Perplexity response has at least two characteristics: the answer makes grammatical sense given your question, and every factual claim links to a source you can visit. Click any citation number. Your browser opens the original page. Read the relevant passage. If the page says what Perplexity claims, the citation checks out. If the passage is missing or says something different, the citation is stale or wrong — treat that claim with extra scrutiny.

Perplexity can and does hallucinate. It is not a substitute for reading primary sources on high-stakes topics. Treat it as a fast first-pass synthesiser, not a final authority.

### Focus modes

By default Perplexity searches the open web. You can narrow or change the source pool using focus modes. In the current interface, click the **+** (plus) icon or the "connectors and sources" control near the search bar to access these options:

| Mode | What it searches | Best for |
|---|---|---|
| Web | Broad open web | General research, current events, product comparisons |
| Academic | Scholarly databases and journals | Peer-reviewed evidence, literature reviews |
| Social | Forums, Reddit, social platforms | Sentiment, community experience, emerging discussion |
| Video | YouTube and video platforms | Summarising talks, finding walkthroughs |
| Writing | Generates text without additional search | Drafting, brainstorming |
| Math | Wolfram Alpha-backed computation | Equations, numerical problem-solving |

You can combine Web, Academic, and Social simultaneously. Selecting only what you need reduces noise and keeps the model focused. [Perplexity focus mode UI, YouTube guide, 2026](https://www.youtube.com/watch?v=9zjCl7c9s7U)

### Follow-up questions

After the initial answer, you can type a follow-up in the same thread. Perplexity carries the context forward. This is useful for drilling down: `Explain the demand-pull factor in more detail` or `Show only sources from 2024 or later`. Each follow-up is a new search grounded in the thread context.

### Saving and sharing

Click the share icon (top-right of a thread) to copy a shareable link. Anyone with the link can read the thread without an account. To export as a PDF: open the Library tab in the left sidebar, find the thread, click the three-dot menu, and select **Export as PDF** ([Guideflow export guide](https://www.guideflow.com/tutorial/how-to-export-a-thread-as-a-pdf-in-perplexity)).

---

## 2. Intermediate: Spaces, system prompts, and files

### What Spaces are

A Space is a persistent project container inside Perplexity. It holds a system prompt that applies to every thread you run inside it, a set of uploaded files and source URLs, and an optional sharing configuration for collaborators. Think of it as a personalised research assistant that already knows your topic before you ask anything.

**Plan note:** Spaces are available to Pro subscribers and above. [Perplexity Spaces guide, PerplexityAI Magazine, 2026](https://perplexityaimagazine.com/perplexity-hub/perplexity-ai-spaces-guide-2026/)

### Creating a Space

1. In the left sidebar, click the **Spaces** icon (third icon from the top in the current interface).
2. Click **Create a Space** or **New Space**.
3. Enter a name that describes your project — for example, `Weekly Competitive Intelligence`.
4. (Optional) Add a short description. This metadata helps the model understand the broader context of your queries.
5. In the **Custom Instructions** field, type the standing instructions that should apply to every query. For example: `Always cite only sources published in the last 90 days. Summarise findings in three bullet points before elaborating. Flag any claims that rely on a single source.`
6. Click **Save**.

Your Space is now listed in the sidebar. Every new thread you open from within the Space inherits the system prompt automatically.

### Adding sources and files

Inside a Space, click **Add Sources** (or the sources panel, depending on the interface version):

- **URL sources:** Paste specific web addresses. Perplexity will treat these pages as preferred references when composing answers inside the Space.
- **File uploads:** Upload PDFs, CSVs, and text documents. Pro accounts can upload up to 50 files per Space (25 MB per file). Enterprise accounts can upload up to 500 files. Uploaded files are co-queried alongside the live web, giving you answers that cite your own documents alongside public sources. [Perplexity Spaces guide, 2026](https://perplexityaimagazine.com/perplexity-hub/perplexity-ai-spaces-guide-2026/)

### Profile and personalisation

In your account settings (click your avatar or profile icon → **Settings**), you can set preferences for:

- Default language and tone.
- Whether AI-generated images appear in answers.
- Whether Perplexity uses your search history to personalise future results.

These settings apply globally, not per Space. Per-Space behaviour is controlled by the Space's custom instructions.

### Sharing a Space

Inside the Space, click **Invite** (top-left area of the Space view). You can share:

- With specific collaborators by email.
- With everyone in your organisation (Enterprise accounts).
- With anyone who has the link.

By default, a Space is private to the creator.

### Pages — research converted to articles

Pages take a completed research thread and convert it into a structured, formatted, shareable article. The workflow as of early 2026 is: run your research thread, then use the **Convert to Page** option (found in the Library tab or the thread's menu). Perplexity restructures the thread into sections with headings, inline citations, and optional images.

**Drift risk: high.** The standalone "Create a Page" button was temporarily retired in early 2026 while the feature is being rebuilt. The conversion path via existing threads remains available. Export options remain limited: Pages are hosted on Perplexity's servers and shared via a public URL. As of early 2026, there is no direct PDF export, Markdown download, or API for extracting Page content. The workaround is to copy the generated text and citations into a document editor immediately after creating the Page. [Perplexity Pages status, 2026](https://www.perplexity.ai/help-center/en/articles/10352968-perplexity-pages)

---

## 3. Advanced: quality controls, Deep Research, and sharing

### Deep Research mode

Deep Research is an agent-style mode available from the main search bar. Click the **Research** option or the relevant toggle (the UI label varies; look for "Deep Research" or a similar multi-step research label). When activated, Perplexity runs dozens of searches, reads hundreds of sources, and composes a long-form synthesised report. A Deep Research session typically takes 2–5 minutes.

The output can be exported as a PDF or converted to a Page. Deep Research is rate-limited on the free tier and consumes "Pro Search" credits. [Introducing Perplexity Deep Research, Perplexity Blog](https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research)

### Reading citations critically

Not all citations are equal. Before treating a Perplexity answer as reliable:

1. Click every citation that underpins a key claim.
2. Check the publication date. Perplexity may cite content that is months or years old without flagging it.
3. Check the source's authority. A Wikipedia article, a personal blog, and a peer-reviewed journal each carry different epistemic weight.
4. Look for single-source claims. If only one citation supports a surprising assertion, find a second source independently.
5. For academic work, switch to Academic focus mode and verify the DOI of any cited paper.

### When Perplexity is and is not a research substitute

Perplexity is useful for: rapid orientation on unfamiliar topics, drafting literature reviews for later manual verification, monitoring news across domains, and gathering informal community opinion (Social mode). It is not a substitute for: primary source reading in high-stakes decisions, systematic literature reviews that require documented search methodology, legal or medical advice, or any context where source provenance must be auditable.

### Comet — AI-native browser

> **Drift risk: high.** This feature is in active development.

Comet is a Chromium-based browser from Perplexity. It adds an always-on AI assistant that can summarise any page, answer questions about highlighted text, and (as of early 2026) operate a "Control browser" mode in which it performs multi-step browsing tasks on your behalf. Comet is a separate download from [perplexity.ai/comet](https://www.perplexity.ai/comet/). It requires a Pro or Max subscription for the agentic features. [Introducing Comet, Perplexity Blog](https://www.perplexity.ai/hub/blog/introducing-comet)

### Importing and exporting research

| Format | Method |
|---|---|
| Thread to PDF | Library → thread → three-dot menu → Export as PDF |
| Thread to Page | Library → thread → Convert to Page |
| Page to document | Copy text manually; no native export as of 2026 |
| Space files | Upload and download through the Space's sources panel |

---

## 4. Expert: the Perplexity API

### Overview

The [Perplexity API](https://docs.perplexity.ai) provides programmatic access to search-grounded language model completions. It is OpenAI-compatible, meaning you can use the OpenAI Python or TypeScript SDK by changing two parameters: the `base_url` and the `api_key`. This makes it easy to slot Perplexity into any existing LLM pipeline.

The API exposes three primary surfaces:

- **Sonar API** — chat completions with live web search grounding.
- **Search API** — raw, ranked web search results without a language model layer.
- **Agent API** — a multi-provider orchestration layer that supports tool use, structured outputs, and reasoning control.

### The sonar model family

As of May 2026, the Sonar model family includes ([Perplexity Sonar models](https://docs.perplexity.ai/docs/sonar/models.md)):

| Model | Category | Best for |
|---|---|---|
| `sonar` | Search | Fast, cost-effective factual queries and topic summaries |
| `sonar-pro` | Search | Complex queries and multi-turn follow-ups requiring higher quality |
| `sonar-reasoning-pro` | Reasoning | Step-by-step analyses, chain-of-thought tasks, logical synthesis |
| `sonar-deep-research` | Research | Exhaustive multi-source reports, market analyses, literature reviews |

For most retrieval-augmented generation (RAG) pipelines where you need live web citations, `sonar-pro` is the practical default. For deep autonomous research tasks, `sonar-deep-research` is appropriate but is slower and more expensive.

### Pinning a model with an environment variable

Do not hard-code model names in production code. Use an environment variable so you can swap models without touching source code:

```bash
# Shell (macOS / Linux)
export PERPLEXITY_API_KEY="your-key-here"
export PERPLEXITY_MODEL="sonar-pro"
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai",
)

model = os.environ.get("PERPLEXITY_MODEL", "sonar-pro")

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "What are the main AI regulatory developments this week?",
        }
    ],
)

print(response.choices[0].message.content)
# Citations are in: response.citations (Perplexity extension to the standard response)
```

Never put your API key in source code or commit it to version control. Use environment variables or a secrets manager.

### Reading citations from the API response

The Perplexity API returns a `citations` field (or a `search_results` field in some endpoints) alongside the standard OpenAI-format `choices` array. Always parse URLs from this field, not from the model's generated text. The model may hallucinate URLs if prompted to include links in the response body. The `search_results` field contains accurate source titles, URLs, and publication dates. ([Perplexity Prompt Guide](https://docs.perplexity.ai/docs/agent-api/prompt-guide))

### When to choose Perplexity API over OpenAI or Gemini API

Use the Perplexity Sonar API when:

- Your application needs citations from live web sources and you want those citations to be verifiable.
- You are building a news monitor, market-intelligence feed, or any tool where information freshness matters.
- You need to reduce the burden of building your own search + retrieval pipeline.

Use a standard LLM API (OpenAI, Anthropic, Gemini) when:

- You are working with your own private documents and need document-level control over what is retrieved.
- You need structured outputs, function calling, or fine-tuning that the Sonar API does not expose.
- Latency is critical and you can tolerate an older knowledge cutoff.

### The pplx CLI

Inside this field guide, the `pplx` command-line tool is used by guide authors and automation agents to perform research while writing. It is a build-time tool for the guide, not a product recommended for end users. End users interacting with Perplexity should use the web interface or the official API directly.

---

## 5. Level up ladder

1. Ask a question at perplexity.ai and click at least three citations to verify them.
2. Run a follow-up question in the same thread; observe how context carries over.
3. Switch to Academic focus mode and repeat a research query; compare source quality.
4. Create a free account and open the Library tab; review saved threads.
5. (Sub) Create your first Space with a meaningful system prompt.
6. (Sub) Add two source URLs and one uploaded PDF to the Space; run a query that references the document.
7. (Sub) Share a Space with a collaborator and observe permission settings.
8. (Sub) Convert a research thread to a Page; note export limitations.
9. (API) Generate an API key at console.perplexity.ai; make a `curl` request using `sonar`.
10. (API) Write a Python script that reads `PERPLEXITY_API_KEY` and `PERPLEXITY_MODEL` from environment variables and parses `search_results` citations from the response.

---

## 6. Guided exercise: build a weekly news brief Space

This exercise takes 20–30 minutes and requires a Pro subscription for the Space features. The API portion requires an API key.

### Part A: the Space (manual, weekly run)

**Goal:** A Space that delivers a concise competitive-intelligence brief when you paste in a weekly question template.

1. Create a new Space named `Weekly News Brief`.

2. Set the custom instructions to:
   ```
   You are a research assistant compiling a weekly news brief for an AI product team.
   For every claim, cite the source with its publication date.
   Prioritise sources from the last 7 days.
   Structure every response as: (a) top 3 headlines with one-sentence summaries, (b) one emerging trend to watch, (c) one counterpoint or contrarian view.
   ```

3. Add source URLs relevant to your domain — for example, the homepage URLs of three industry publications or analyst sites you trust. These become preferred references.

4. Each week, open the Space and paste this template question, filling in the blanks:
   ```
   Week of [DATE]. Topic: [YOUR DOMAIN]. What happened this week that an AI product team should know about?
   ```

5. Review the output. Click citations. Copy the content into your notes tool.

6. Optionally convert the thread to a Page and share the link with your team.

### Part B: developer mode — port to the Perplexity API

Once you are comfortable with the manual Space, recreate the behaviour programmatically.

```bash
export PERPLEXITY_API_KEY="your-key-here"
export PERPLEXITY_MODEL="sonar-pro"
```

```python
import os
import datetime
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai",
)

model = os.environ.get("PERPLEXITY_MODEL", "sonar-pro")

SYSTEM_PROMPT = """You are a research assistant compiling a weekly news brief for an AI product team.
For every claim, cite the source with its publication date.
Prioritise sources from the last 7 days.
Structure every response as:
(a) top 3 headlines with one-sentence summaries,
(b) one emerging trend to watch,
(c) one counterpoint or contrarian view."""

week_of = datetime.date.today().strftime("%Y-%m-%d")
domain = "AI developer tooling"  # change to your domain

user_message = (
    f"Week of {week_of}. Topic: {domain}. "
    "What happened this week that an AI product team should know about?"
)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ],
)

print(response.choices[0].message.content)

# Print source citations
if hasattr(response, "citations"):
    print("\n--- Sources ---")
    for i, url in enumerate(response.citations, 1):
        print(f"[{i}] {url}")
```

Run this script manually each week. Do not schedule it as an automated job — review the output yourself before distributing it.

---

## 7. Plan availability table

| Feature | Free | Sub (Pro) | Team | Ent | API |
|---|---|---|---|---|---|
| Ask questions (web search) | Yes | Yes | Yes | Yes | Via Sonar API |
| Focus modes (Web, Academic, Social, Video, Writing, Math) | Yes | Yes | Yes | Yes | Via search filters |
| Spaces | No | Yes | Yes | Yes | System prompt equivalent via API `system` field |
| Pages (Convert to Page) | No | Yes | Yes | Yes | Not available — export manually |
| File upload in Spaces | No | Yes (50 files/Space) | Yes | Yes (500 files/Space) | Not directly — use embeddings API |
| Profile / personalisation settings | Partial | Yes | Yes | Yes | Not applicable |
| Deep Research mode | Limited | Yes | Yes | Yes | `sonar-deep-research` model |
| Comet browser | No | Yes (basic) | — | — | Not applicable |
| Comet "Control browser" agentic mode | No | Yes (Pro) | — | — | Not applicable |
| API access (Sonar, Search, Agent) | No | No | No | No | API key required — separate billing |

**Drift risk notes:** Comet features are in active development. The "Control browser" mode was noted as Pro/Max as of early 2026 but the feature boundaries may shift. Pages is being rebuilt; check [perplexity.ai/help-center](https://www.perplexity.ai/help-center/en/articles/10352968-perplexity-pages) for current status.

---

## 8. Fallback

If a feature listed above is unavailable on your plan or has changed since this page was last verified, these alternatives apply:

| Feature | Fallback |
|---|---|
| Spaces (Sub only) | Create a shared document with your system prompt text; paste it at the start of every new Perplexity thread manually. |
| File upload | Upload the document to a public URL or a pastebin service, then add the URL as a source in a Space, or paste relevant excerpts into your thread. |
| Pages (unavailable/rebuilding) | Copy the thread text into Notion, Google Docs, or a Markdown file. Paste citations manually. |
| Deep Research (rate-limited) | Run three to five sequential threads with narrower focused queries; combine the outputs manually. |
| Perplexity API | Use OpenAI or Anthropic API with a web-search tool attached, or integrate a search engine API (e.g., Brave Search, Tavily) as a retrieval step before your LLM call. |
| Comet browser | Use the Perplexity web interface for research and a standard browser for everything else. There is no equivalent free-tier browser agent from Perplexity. |

---

For API reference documentation, see [docs.perplexity.ai](https://docs.perplexity.ai). For Sonar model details, see [docs.perplexity.ai/docs/sonar/models.md](https://docs.perplexity.ai/docs/sonar/models.md). For Spaces and Pages help, see [perplexity.ai/help-center](https://www.perplexity.ai/help-center).
