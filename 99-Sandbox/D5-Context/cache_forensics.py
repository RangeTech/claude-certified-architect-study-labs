"""D5 sandbox — prompt caching signatures.

    python cache_forensics.py           # 1st call CREATES cache, 2nd READS it
    python cache_forensics.py --mutate  # change the STABLE prefix -> read drops to 0

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam points:
  - Caching is PREFIX-based. Put STABLE content first, VOLATILE content last, and
    mark the boundary with cache_control.
  - cache_read dropping to ~0 immediately after a change  = you mutated the prefix.
  - gradual misses over time                              = TTL expiry.
"""
import os
import sys
import anthropic

MODEL = "claude-sonnet-4-6"

# a big, stable prefix so it clears the minimum-cacheable-size bar
STABLE = "You are a customer support agent. " + ("Company policy detail. " * 600)


def call(client, prefix, user_suffix, tag):
    r = client.messages.create(
        model=MODEL, max_tokens=20,
        system=[{"type": "text", "text": prefix, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": "Reply with OK. " + user_suffix}],
    )
    u = r.usage
    created = getattr(u, "cache_creation_input_tokens", 0)
    read = getattr(u, "cache_read_input_tokens", 0)
    print(f"  {tag:34} cache_create={created:5}  cache_read={read:5}  input={u.input_tokens}")


def main():
    mutate = len(sys.argv) > 1 and sys.argv[1] == "--mutate"
    c = anthropic.Anthropic()
    call(c, STABLE, "one", "1st call (expect CREATE)")
    prefix2 = (STABLE + " EXTRA") if mutate else STABLE
    tag = "2nd call, prefix MUTATED (read->0)" if mutate else "2nd call, prefix same (expect READ)"
    call(c, prefix2, "two", tag)


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
