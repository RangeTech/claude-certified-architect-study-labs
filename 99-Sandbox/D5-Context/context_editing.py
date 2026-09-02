"""D5 sandbox — context editing: clearing stale tool results (offline demo).

    python context_editing.py       # no API key needed — pure message-list mechanics

Exam points:
  - In a long agent run, old tool_results dominate the context window. Clearing the
    OLDEST tool_results (keeping the last N) reclaims space while preserving recent
    working state. The Anthropic API can do this automatically (context editing /
    clear-tool-uses); see the D5L8 answer key for the live-API version.
  - The trade: you free tokens but lose detail from cleared turns — keep enough
    recent results that the agent can still reason.

This script simulates a growing tool history and shows the size reduction from
clearing all but the last N tool_results.
"""
KEEP_LAST = 3


def approx_tokens(messages):
    # crude proxy: ~4 chars per token over the serialized content
    return sum(len(str(m.get("content", ""))) for m in messages) // 4


def build_history(n_tool_calls):
    messages = [{"role": "user", "content": "Investigate the incident using the tools."}]
    for i in range(n_tool_calls):
        messages.append({"role": "assistant",
                         "content": [{"type": "tool_use", "id": f"t{i}", "name": "read_log",
                                      "input": {"file": f"log_{i}.txt"}}]})
        messages.append({"role": "user",
                         "content": [{"type": "tool_result", "tool_use_id": f"t{i}",
                                      "content": f"LOG {i}: " + ("noise data " * 200)}]})
    return messages


def clear_old_tool_results(messages, keep_last):
    tool_turns = [i for i, m in enumerate(messages)
                  if isinstance(m.get("content"), list)
                  and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in m["content"])]
    to_clear = set(tool_turns[:-keep_last]) if keep_last else set(tool_turns)
    out = []
    for i, m in enumerate(messages):
        if i in to_clear:
            out.append({"role": m["role"], "content": "[tool result cleared to reclaim context]"})
        else:
            out.append(m)
    return out


def main():
    full = build_history(12)
    trimmed = clear_old_tool_results(full, KEEP_LAST)
    print(f"  full history:     ~{approx_tokens(full):6} tokens  ({len(full)} messages)")
    print(f"  after clearing:   ~{approx_tokens(trimmed):6} tokens  (kept last {KEEP_LAST} tool results)")
    saved = approx_tokens(full) - approx_tokens(trimmed)
    print(f"  reclaimed:        ~{saved} tokens without dropping recent working state")


if __name__ == "__main__":
    main()
