"""D2 sandbox — tool design: descriptions, tool_choice, strict.

    python tool_design.py

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam points:
  - A tool's `description` (and per-field descriptions) is the model's ONLY guide
    to WHEN and HOW to call it. Vague descriptions -> wrong tool / missing args.
  - tool_choice: {"type":"auto"} model decides; {"type":"any"} must call some tool;
    {"type":"tool","name":X} force one; {"type":"none"} forbid tools.
"""
import os
import sys
import anthropic

MODEL = "claude-sonnet-4-6"

VAGUE = [{"name": "lookup", "description": "look stuff up",
          "input_schema": {"type": "object",
                           "properties": {"q": {"type": "string"}}, "required": ["q"]}}]

PRECISE = [{"name": "get_order_status",
            "description": ("Return the shipping status for a customer order given its numeric "
                            "order_id. Use when the user asks where their order is or wants a "
                            "tracking update."),
            "input_schema": {"type": "object",
                             "properties": {"order_id": {"type": "integer",
                                                         "description": "numeric order id, e.g. 40321"}},
                             "required": ["order_id"]}}]

PROMPT = "Where is my order 40321?"


def ask(client, tools, choice, label):
    r = client.messages.create(model=MODEL, max_tokens=400, tools=tools,
                               tool_choice=choice, messages=[{"role": "user", "content": PROMPT}])
    calls = [(b.name, b.input) for b in r.content if b.type == "tool_use"]
    print(f"  {label:42} stop={r.stop_reason:10} calls={calls}")


def main():
    c = anthropic.Anthropic()
    ask(c, VAGUE, {"type": "auto"}, "VAGUE desc, auto")
    ask(c, PRECISE, {"type": "auto"}, "PRECISE desc, auto")
    ask(c, PRECISE, {"type": "tool", "name": "get_order_status"}, "PRECISE, forced tool")
    ask(c, PRECISE, {"type": "none"}, "PRECISE, tool_choice=none")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
