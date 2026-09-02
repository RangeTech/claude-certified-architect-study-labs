# 99-Sandbox — hands-on playgrounds for all five CCA-F domains

Free-play spaces to *touch* the behavior the exam tests. Unlike `03-Hands-On-Labs/`
(guided, with success criteria), these are for poking, breaking, and re-running.
Nothing here is graded. macOS/bash + Python throughout (the official D3 answer keys
are PowerShell; this rebuilds them cross-platform).

## The five sandboxes

| Folder | Domain (weight) | Language | Highlights |
|---|---|---|---|
| `D1-Agents/` | Agentic Architecture & Orchestration (27%) | Python | `stop_reason` loop + wrong-answer toggles, orchestrator/worker isolation & quarantine |
| `D2-Tools-MCP/` | Tool Design & MCP Integration (18%) | Python | descriptions/`tool_choice`, scoped vs kitchen-sink tools, a real MCP server |
| `D3-Config/` | Claude Code Configuration & Workflows (20%) | bash + CLI | settings/permissions, Pre/PostToolUse hooks, memory hierarchy, skills, headless CI |
| `D4-Prompting/` | Prompt Engineering & Structured Output (20%) | Python | schema-forced output, prompt right-sizing, incompatibility table |
| `D5-Context/` | Context Management & Reliability (15%) | Python | cache forensics, truncation recovery, context editing |

Each folder has its own `README.md` with experiments (predict-before-you-run) and a self-check whose answers are the exam's discriminators.

## Setup

```bash
export ANTHROPIC_API_KEY=sk-...        # D1, D2, D4, most of D5
pip install anthropic
pip install pydantic "mcp[cli]"        # pydantic optional; mcp only for D2's server
brew install jq                        # D3 hooks
pip install black                      # optional, D3 PostToolUse formatter demo
```
Python scripts make small, real API calls (outputs vary run to run). `context_editing.py` (D5) runs offline.

## Running the D3 config sandbox

D3 loads project `settings.json` + hooks, which Claude Code resolves from the git
project root. Because these sandboxes are nested in the study repo, copy the D3
folder out and make it its own project:
```bash
cp -R 99-Sandbox/D3-Config ~/cca-sandbox && cd ~/cca-sandbox && git init && claude
```
The Python sandboxes (D1/D2/D4/D5) just run directly with `python <script>.py`.

## Suggested order
Follow exam weight: **D1 → D3/D4 → D2 → D5**. For each, read that folder's README,
predict each experiment's outcome, run it, then take the self-check cold the next day.

> These sandboxes encode behavior against the live docs as of this writing. When a
> sandbox and the current Anthropic docs disagree, **the docs win** — the exam is
> written against the docs.
