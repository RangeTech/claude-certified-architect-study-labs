# D1-Agents — Agentic Architecture & Orchestration (27%)

Free-play sandbox for the highest-weight domain. Runs on macOS with Python.

```bash
export ANTHROPIC_API_KEY=sk-...
pip install anthropic
```

## Files
- `agent_loop.py` — the canonical `stop_reason`-driven loop, with flags that switch in the two **wrong-answer tells** so you can watch them misbehave.
- `orchestrator_workers.py` — orchestrator spawns isolated workers, collects `{finding, source, confidence}`, and **quarantines** a no-evidence worker.

## Experiments (predict before running)

### 1. The loop, done right
```bash
python agent_loop.py
```
Watch it drive purely on `stop_reason`: `tool_use` → execute → append `tool_result` → loop, then break on `end_turn`. A parallel comparison ("weather AND population") should emit **multiple `tool_use` blocks in one turn** — all their results go back in **one** user turn.

### 2. The two honeypots
```bash
python agent_loop.py --nl     # stops when it sees the word "bigger"/"done"
python agent_loop.py --cap    # stops at iteration 2 regardless of real progress
```
**Why they're wrong:** NL-parsing fires on a word, not on completion; a hard cap either cuts work short or hides a stuck loop. On the exam, "terminate when the text says done" and "cap iterations to stop" are auto-suspicion answers.

### 3. Parallel vs serial tool use
```bash
python agent_loop.py --serial
```
`disable_parallel_tool_use` forces one tool call per turn — compare the turn count against the default run.

### 4. Isolation, provenance, quarantine
```bash
python orchestrator_workers.py
```
The `timeline` worker gets **no** evidence (subagents don't inherit context) and self-reports confidence 0 → it's quarantined and kept out of synthesis. Trusted findings still carry `source` + `confidence`.

## Self-check
1. What terminates the loop? → **`stop_reason` (`end_turn`)**, never NL text, never a cap.
2. Two `tool_use` blocks in one response — how many user turns of results? → **one** (all `tool_result`s together).
3. A worker returns garbage/empty — drop it silently? → **No: quarantine with provenance.**
4. Do subagents inherit the orchestrator's context? → **No — pass what they need explicitly.**
5. Independent subtasks vs dependent stages vs one contested answer? → **parallel workers / sequential pipeline / voting.**
6. Iteration cap's real role? → **safety backstop only**, not the stop mechanism.
