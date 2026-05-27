# Antigravity Project Layout

Last verified: 2026-05-06
Drift risk: high

Reference: https://codelabs.developers.google.com/getting-started-google-antigravity

## Overview

An Antigravity project is a structured workspace that organizes the files, tools, and agent configuration for a single bounded task or team. Each project has a root directory, a configuration manifest, and one or more agent definitions.

## Typical Directory Structure

```
my-antigravity-project/
  antigravity.yaml          # Project manifest: agent definitions, tool permissions, HITL config
  agents/
    summarizer.yaml         # Agent definition: model, tools, prompt reference
  prompts/
    summarizer_system.txt   # System prompt for the summarizer agent
  data/
    notes/                  # Input notes directory (read-only for the agent)
    outputs/                # Agent output directory
  evals/
    golden_cases.jsonl      # Evaluation cases
  docs/
    PROJECT_README.md       # This file
```

## Key Configuration Files

### antigravity.yaml

The project manifest defines which agents are active, what tools they may use, and what HITL gates are required. A minimal example structure:

```yaml
# antigravity.yaml (example structure — verify field names against current API)
project_name: "my-summarizer-project"
agents:
  - name: summarizer
    definition: agents/summarizer.yaml
    hitl:
      require_approval_for: ["file_write", "external_call"]
tool_permissions:
  read_file:
    scope: "data/notes/"
  write_file:
    scope: "data/outputs/"
    requires_hitl: true
```

### agents/summarizer.yaml

The agent definition specifies the model, prompt, and tool subset for a specific agent:

```yaml
# agents/summarizer.yaml (example structure — verify field names against current API)
name: summarizer
model: gemini-pro  # or the current recommended Gemini variant
prompt: prompts/summarizer_system.txt
tools:
  - read_file
max_context_files: 50
stop_on_errors: 3
```

## Data Flow

1. A human invokes the agent with a target notes directory.
2. The agent reads files under `data/notes/` using the `read_file` tool.
3. The agent produces a summary and writes it to `data/outputs/` (if write permission is granted via HITL).
4. Logs are written to the project's log stream for audit and cost tracking.

## Tool Scoping in Antigravity

Antigravity supports per-agent tool scoping in the project manifest. Use this to restrict `read_file` to the `data/notes/` subdirectory and `write_file` to `data/outputs/`. Never grant project-wide filesystem access if the agent only needs a subdirectory.

## Notes on Platform Evolution

Antigravity's configuration schema and available tools are updated frequently. Always validate this file's YAML examples against the current documentation before deploying:
https://codelabs.developers.google.com/getting-started-google-antigravity
