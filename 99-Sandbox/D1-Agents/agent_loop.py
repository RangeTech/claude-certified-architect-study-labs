"""D1 sandbox — the agent loop done right (stop_reason-driven).

    python agent_loop.py            # the CORRECT loop
    python agent_loop.py --nl       # WRONG: stop by scanning text for "done"
    python agent_loop.py --cap      # WRONG: stop on a fixed iteration cap
    python agent_loop.py --serial   # disable parallel tool use (observe serialization)

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam points:
  - Terminate on `stop_reason`, never by parsing natural language, never by using
    an iteration cap as the PRIMARY stop (a cap is only a safety backstop).
  - One response can contain MULTIPLE tool_use blocks (parallel). Execute all of
    them and return ALL tool_results in ONE user turn.
"""
import os
import sys
import anthropic

MODEL = "claude-sonnet-4-6"

TOOLS = [
    {"name": "get_weather", "description": "Get current weather for a city.",
     "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}},
    {"name": "get_population", "description": "Get the population of a city.",
     "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}},
]

FACTS = {
    ("get_weather", "Paris"): "18C, rain",
    ("get_weather", "Tokyo"): "27C, clear",
    ("get_population", "Paris"): "2.1M",
    ("get_population", "Tokyo"): "14M",
}


def run_tool(name, args):
    return FACTS.get((name, args.get("city")), "unknown")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content":
                 "Compare Paris and Tokyo on weather AND population, then say which city is bigger."}]
    tool_choice = {"type": "auto"}
    if mode == "--serial":
        tool_choice["disable_parallel_tool_use"] = True

    for i in range(1, 11):  # 10 = safety BACKSTOP, not the stop mechanism
        resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS,
                                       tool_choice=tool_choice, messages=messages)
        blocks = [b.type for b in resp.content]
        print(f"[turn {i}] stop_reason={resp.stop_reason}  blocks={blocks}")

        # ---- WRONG terminators (for contrast; enabled by flags) ----
        if mode == "--nl":
            text = "".join(b.text for b in resp.content if b.type == "text")
            if any(w in text.lower() for w in ("bigger", "done", "finished")):
                print("  NL-STOP fired — unreliable: it triggers on a word, not on real completion.")
                return
        if mode == "--cap" and i >= 2:
            print("  CAP-STOP fired at iteration 2 — cuts work short (or masks a stuck loop).")
            return

        # ---- CORRECT: drive on stop_reason ----
        if resp.stop_reason == "end_turn":
            print("  DONE:", "".join(b.text for b in resp.content if b.type == "text").strip())
            return
        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for b in resp.content:
                if b.type == "tool_use":
                    out = run_tool(b.name, b.input)
                    print(f"    exec {b.name}({b.input}) -> {out}")
                    results.append({"type": "tool_result", "tool_use_id": b.id, "content": out})
            messages.append({"role": "user", "content": results})  # ALL results, ONE turn
            continue
        print(f"  unhandled stop_reason={resp.stop_reason}")
        return

    print("  safety backstop hit (10 turns). A cap is a backstop, never the terminator.")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
