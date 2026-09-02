"""D2 sandbox — scoped tool distribution beats a kitchen-sink toolbox.

    python scoped_tools.py

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam point: handing one agent every tool bloats context (every schema is tokens)
and degrades selection accuracy. Scope each agent to the tools its job needs.
Here we measure input_tokens for a 2-tool agent vs a 12-tool agent on the same
request, and confirm both still pick the right tool.
"""
import os
import sys
import anthropic

MODEL = "claude-sonnet-4-6"


def tool(n):
    return {"name": f"op_{n}",
            "description": f"Perform operation {n} on the widget subsystem with detailed options.",
            "input_schema": {"type": "object",
                             "properties": {"target": {"type": "string"}}, "required": ["target"]}}


SCOPED = [tool(1), tool(2)]
KITCHEN = [tool(i) for i in range(1, 13)]
PROMPT = "Use operation 1 on widget A."


def measure(client, tools, label):
    r = client.messages.create(model=MODEL, max_tokens=60, tools=tools,
                               messages=[{"role": "user", "content": PROMPT}])
    chosen = [b.name for b in r.content if b.type == "tool_use"]
    print(f"  {label:22} input_tokens={r.usage.input_tokens:5}  chosen={chosen}")


def main():
    c = anthropic.Anthropic()
    measure(c, SCOPED, "scoped (2 tools)")
    measure(c, KITCHEN, "kitchen-sink (12)")
    print("  -> the token gap is pure overhead; it grows with every tool you don't need.")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
