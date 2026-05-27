> **Last verified:** 2026-05-06 · **Drift risk:** high
> **Official sources:** [Anthropic computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [OpenAI computer use](https://developers.openai.com/api/docs/guides/tools-computer-use), [browser-use repo](https://github.com/browser-use/browser-use), [OpenAI CUA announcement](https://openai.com/index/computer-using-agent/)

# Comparison: Browser and Computer Use Approaches

This page compares the four main approaches an agent builder might choose. Drift risk is marked high because all four providers are iterating rapidly: model capabilities, action APIs, pricing, and safety policies change with each major release.

## Quick comparison table

| Dimension | Anthropic computer use | OpenAI computer use | browser-use (library) | Hosted browser agents |
|-----------|----------------------|-------------------|----------------------|----------------------|
| Interface type | Full desktop + browser | Full desktop + browser | Browser only | Browser only (typically) |
| Action model | Single action per turn (older) / batched actions | Batched `actions[]` array per turn | Goal-driven, library manages loop | Goal-driven, provider manages loop |
| Screenshot input | Required each turn | Required each turn | Managed internally | Managed internally |
| Models supported | Claude 4.x, Sonnet 3.7+ | gpt-5.5 / gpt-5.4 with the built-in `computer` tool; `computer-use-preview` is legacy | Any LangChain-compatible model | Provider-specific |
| Self-hosting required | Yes (sandbox required) | Yes (sandbox required) | Yes (Playwright + Python env) | No |
| Cost model | API tokens + input image tokens | API tokens + input image tokens | API tokens for the LLM + your infra | Subscription or per-minute billing |
| Open source | No | No | Yes (MIT) | No |
| Coordinate scaling | Required for pre-4.7 models | Not required (1:1 at `detail: original`) | Handled by library | Handled by provider |
| DOM access | No (vision only) | No (vision only, plus code-exec harness option) | Yes (DOM + vision hybrid) | Varies |

## Anthropic computer use

Anthropic introduced computer use in [October 2024](https://www.anthropic.com/news/3-5-models-and-computer-use) as a beta capability. The current interface is the `computer_20251124` tool type, supported by Claude Opus 4.7 and later models.

Strengths:
- Full desktop automation (not just browser). Can control any GUI application running in the sandbox.
- The zoom action (`computer_20251124` only, requires `enable_zoom: true`) lets the model inspect high-density UI elements at full resolution.
- Mature reference implementation available (Docker-based sandbox with Xvfb display server).

Weaknesses:
- Every turn requires a screenshot round-trip to the API. Latency accumulates on multi-step tasks.
- Coordinate scaling is required for models before Claude Opus 4.7 — the API downsamples images and Claude returns coordinates in the downsampled space, which must be scaled back to screen space before executing clicks.
- Sandbox setup (Docker + X virtual framebuffer + window manager) is non-trivial to configure for first-timers.
- The beta flag and tool type version string change with new model releases, requiring code updates.

## OpenAI computer use

OpenAI announced the Computer-Using Agent in [January 2025](https://openai.com/index/computer-using-agent/) and shipped it in the Responses API. The current production model is `gpt-5.5` with tool type `computer`.

Strengths:
- Batched actions: the model can return multiple actions (click, then type) in a single `computer_call`, reducing round trips.
- `detail: "original"` on screenshot inputs preserves full resolution up to 10.24 megapixels without manual coordinate scaling.
- Three integration paths: built-in `computer` tool, custom harness over Playwright/Selenium, or a code-execution harness for DOM workflows.
- `previous_response_id` lets you build the conversation history through response chaining rather than managing message arrays manually.

Weaknesses:
- Newer than Anthropic's offering; older `computer-use-preview` integrations need code changes to use the current `computer` tool with current models.
- Full desktop automation capability is the same as Anthropic's in principle, but real-world reliability on non-browser desktop apps is less documented.
- Code-execution harness (the third path) blurs the line between computer use and code execution, which may require a different mental model for builders used to screenshot-driven loops.

## browser-use (Python library)

[browser-use](https://github.com/browser-use/browser-use) is an open-source library that provides a high-level `Agent` class. You give it a task string and an LLM; it handles the automation loop internally.

Strengths:
- Highest abstraction level among the four approaches: you write `agent.run()` and get results.
- DOM-aware: the library can extract structured DOM information in addition to visual screenshots, making it more reliable on data-heavy web pages than pure vision approaches.
- Works with any LangChain-compatible model, including current OpenAI, Claude, Gemini, and open-source models exposed through LangChain adapters.
- Active development; MCP integration was added (the `MCPClient` class lets agents use MCP servers alongside browser actions).
- Docker image available (`browseruse/browseruse`) for containerized deployment.

Weaknesses:
- Browser-only. Cannot automate desktop GUI applications.
- The LLM manages reasoning; you get less visibility into intermediate steps than you do with a raw action loop.
- The library's internals evolve quickly. Breaking changes across minor versions are common; pin versions for production use.
- Requires a local Playwright-controlled browser, which has its own headless/headful configuration surface.
- As of 2025, browser-use migrated from Playwright to a direct Chrome DevTools Protocol (CDP) implementation for lower-level control. Code written against older versions may need updates.

## Hosted browser agents

Several providers (including cloud offerings from browser-use and others) host the browser sandbox and agent loop for you. You send a task, they return a result or a live session URL.

Strengths:
- Zero infrastructure. No Docker, no Playwright, no display server.
- Scales horizontally without you managing capacity.

Weaknesses:
- Data sovereignty: every URL visited and every page rendered passes through the provider's infrastructure.
- Less control over the agent loop, timeouts, and retry behavior.
- Vendor lock-in.
- Not suitable for tasks involving internal systems that cannot be accessed from external IP ranges.

## Choosing an approach

Use Anthropic or OpenAI computer use when you need full desktop automation or when you want tight control over the action loop and are comfortable managing a sandbox VM. Use browser-use when you want a quick start with browser-only tasks and your LLM provider is flexible. Use a hosted agent when the task involves public web browsing, the data involved is not sensitive, and you want to skip infrastructure management entirely.

In all cases, read [Operating boundaries](boundaries.md) before deploying anything that touches real accounts.
