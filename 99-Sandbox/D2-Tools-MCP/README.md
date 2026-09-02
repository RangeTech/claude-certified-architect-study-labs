# D2-Tools-MCP — Tool Design & MCP Integration (18%)

```bash
export ANTHROPIC_API_KEY=sk-...
pip install anthropic
pip install "mcp[cli]"   # only for the MCP server
```

## Files
- `tool_design.py` — how the `description` and `tool_choice` change which tool fires.
- `scoped_tools.py` — token cost of a kitchen-sink toolbox vs a scoped one.
- `mcp_server.py` + `.mcp.json` — a minimal MCP server you can attach to Claude Code.

## Experiments

### 1. Descriptions and tool_choice
```bash
python tool_design.py
```
The **vague** tool often mis-fires or fills args poorly; the **precise** one calls `get_order_status(order_id=40321)` cleanly. Then watch `tool_choice`: `auto` (model decides), forced `{"type":"tool","name":...}` (always calls it), `none` (must answer without tools).
**Lesson:** if a tool is called wrongly, sharpen its description before touching the prompt.

### 2. Scope beats kitchen-sink
```bash
python scoped_tools.py
```
Same request, 2 tools vs 12. Note the `input_tokens` gap — every unused tool schema is dead weight, and more tools also blur selection. Scope each agent to its job.

### 3. Attach a real MCP server to Claude Code
The `.mcp.json` here is **project scope** (committed, shared via git). From this folder:
```bash
cd ~/cca-sandbox/D2-Tools-MCP   # wherever you copied the sandbox as its own project
claude
```
Inside Claude Code: `/mcp` lists servers; approve `cca-sandbox`, then ask *"add 2 and 40"* or *"echo hello"* and watch it call the MCP tools. `claude mcp list` shows configured servers and scopes.
> Scopes recap: **local** = this machine only; **project** = `.mcp.json` in the repo (team-shared); **user** = all your projects. Untrusted servers are a real risk surface — only attach ones you trust.

## Self-check
1. A tool keeps getting called with wrong args. First fix? → **improve the tool/field `description`** (+ consider `strict`).
2. `tool_choice` values? → **auto / any / tool(name) / none.**
3. Why not give every agent all tools? → **token bloat + worse selection; scope to the job.**
4. `.mcp.json` committed to the repo = which scope? → **project (shared via git).**
5. Force exactly one specific tool? → **`{"type":"tool","name":X}`.**
