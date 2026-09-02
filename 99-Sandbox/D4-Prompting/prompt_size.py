"""D4 sandbox — bloated vs concise system prompt: measure tokens + latency.

    python prompt_size.py

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam point: more instructions is NOT more accuracy. An over-long system prompt
costs input tokens and latency on every call and can dilute the signal. Right-size
the prompt to the task. Same extraction, two prompts — watch input_tokens/latency.
"""
import os
import sys
import time
import anthropic

MODEL = "claude-sonnet-4-6"

BIG = ("You are an expert enterprise invoice data extraction assistant. " +
       ("Follow every accounting, tax, multi-currency, VAT, GST and HST convention meticulously "
        "and normalize all fields exhaustively. ") * 60)

SMALL = "Extract invoice_number, vendor, due_date (ISO 8601) and total. Reply as JSON only."

INVOICE = "Invoice #12345 from Acme Corp, Due 2024-01-15, Total $500.00"


def run(client, system, label):
    t = time.time()
    r = client.messages.create(model=MODEL, max_tokens=200, system=system,
                               messages=[{"role": "user", "content": INVOICE}])
    dt = time.time() - t
    print(f"  {label:14} input_tokens={r.usage.input_tokens:5}  output={r.usage.output_tokens:4}  {dt:.2f}s")


def main():
    c = anthropic.Anthropic()
    run(c, BIG, "BIG system")
    run(c, SMALL, "SMALL system")
    print("  -> the BIG prompt pays its token/latency tax on EVERY request, for no accuracy gain here.")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
