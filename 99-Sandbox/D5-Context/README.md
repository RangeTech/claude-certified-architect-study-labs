# D5-Context — Context Management & Reliability (15%)

```bash
export ANTHROPIC_API_KEY=sk-...   # needed for cache_forensics.py + stop_reason_recovery.py
pip install anthropic
```
(`context_editing.py` runs offline — no key needed.)

## Files
- `cache_forensics.py` — read the prompt-caching signals in `usage`.
- `stop_reason_recovery.py` — detect `max_tokens` truncation and recover the right way.
- `context_editing.py` — clear stale tool results to reclaim the window (offline mechanics).

## Experiments

### 1. Caching signatures
```bash
python cache_forensics.py            # call 1 CREATE, call 2 READ (prefix unchanged)
python cache_forensics.py --mutate   # prefix changed -> cache_read collapses to 0
```
**Read the tells:** `cache_read` → 0 right after a change = you mutated the prefix; gradual misses over time = TTL expiry. Design: stable content first, volatile last, `cache_control` on the boundary.

### 2. Truncation recovery
```bash
python stop_reason_recovery.py
```
A starved budget yields `stop_reason == "max_tokens"` — the partial is **not** complete, never parse it as final. The correct recovery for large output is to **split into scoped calls and merge**; endlessly raising `max_tokens` is the trap.

### 3. Context editing
```bash
python context_editing.py
```
Simulates a 12-tool-call history and clears all but the last 3 tool results, showing the token reclaim. The live API can do this automatically (context editing / clear-tool-uses) — see `03-Hands-On-Labs/_AnswerKeys/D5/D5L8/`.

## Compaction contract (what a summary MUST preserve)
task overview · current state · important discoveries (**including rejected/failed approaches**) · next steps · user constraints. If compaction loses a decision, fix the **summary contract**, not the schedule.

## Reliability grab-bag (exam favorites)
- Long/multi-agent pipelines **checkpoint** findings + decisions to durable storage; on restart, **resume from the last completed step** (don't rerun the whole pipeline). Retry logic complements checkpointing, never replaces it.
- Structured errors `{category, retryable, partial_results, attempted}` beat a generic string; a swallowed error returned as success is always wrong.

## Self-check
1. `cache_read` drops to 0 right after an edit — cause? → **prefix mutation.**
2. Gradual cache misses over time? → **TTL expiry.**
3. `stop_reason == "max_tokens"` — is the output complete? → **No, truncated; don't parse as final.**
4. Big output keeps truncating — best fix? → **split into scoped calls + merge**, not ever-higher max_tokens.
5. Compaction dropped a rejected approach and the agent retried it — fix? → **the summary contract**, not the schedule.
6. Pipeline crashes at step 7 of 10 on restart? → **resume from checkpoint**, don't rerun 1–6.
