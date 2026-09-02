"""D5 sandbox — max_tokens truncation: detect and recover correctly.

    python stop_reason_recovery.py

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam points:
  - stop_reason == "max_tokens" means the output was TRUNCATED. Never parse the
    partial as if it were complete.
  - Recover by continuing, OR — for a large structured result that keeps
    truncating — SPLIT into smaller scoped calls and merge. Cranking max_tokens
    ever higher is the trap answer.
"""
import os
import sys
import anthropic

MODEL = "claude-sonnet-4-6"


def once(client, max_tokens, prompt):
    r = client.messages.create(model=MODEL, max_tokens=max_tokens,
                               messages=[{"role": "user", "content": prompt}])
    txt = "".join(b.text for b in r.content if b.type == "text")
    print(f"  max_tokens={max_tokens:<4} stop_reason={r.stop_reason:<11} chars={len(txt)}")
    return r.stop_reason, txt


def main():
    c = anthropic.Anthropic()
    print("Deliberately starve the budget:")
    sr, _ = once(c, 20, "List the numbers 1 to 200, comma separated.")
    if sr == "max_tokens":
        print("  -> TRUNCATED. Do NOT trust this partial. Continue, or split into scoped calls.")
    print("\nRecover by SPLITTING into two scoped calls and merging:")
    _, a = once(c, 300, "List the numbers 1 to 100, comma separated. Numbers only.")
    _, b = once(c, 300, "List the numbers 101 to 200, comma separated. Numbers only.")
    merged = (a.strip().rstrip(",") + ", " + b.strip())
    print(f"  merged length = {len(merged)} chars (both halves complete)")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
