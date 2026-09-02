"""D4 sandbox — reliable structured output via a forced tool schema.

    python structured_output.py

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam point: the most reliable way to GUARANTEE shape is to define a schema and
force it — here a tool with an input_schema plus tool_choice forcing that tool.
The model must emit args matching the schema. (See README for the hard
incompatibilities the exam loves: citations + output format, prefill + JSON, etc.)
"""
import os
import sys
import json
import anthropic

MODEL = "claude-sonnet-4-6"

INVOICE = "Invoice #12345 from Acme Corp, Due 2024-01-15, Total $500.00"

SCHEMA = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string"},
        "vendor": {"type": "string"},
        "due_date": {"type": "string", "description": "ISO 8601 (YYYY-MM-DD)"},
        "total": {"type": "number"},
    },
    "required": ["invoice_number", "vendor", "due_date", "total"],
}

TOOL = [{"name": "emit_invoice",
         "description": "Return the extracted invoice fields.",
         "input_schema": SCHEMA}]


def main():
    c = anthropic.Anthropic()
    r = c.messages.create(model=MODEL, max_tokens=300, tools=TOOL,
                          tool_choice={"type": "tool", "name": "emit_invoice"},
                          messages=[{"role": "user", "content": f"Extract the fields:\n{INVOICE}"}])
    data = next(b.input for b in r.content if b.type == "tool_use")
    print("Structured result (schema-guaranteed shape):")
    print(json.dumps(data, indent=2))
    # every required key is present because the schema forced it
    missing = [k for k in SCHEMA["required"] if k not in data]
    print("missing required keys:", missing or "none")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
