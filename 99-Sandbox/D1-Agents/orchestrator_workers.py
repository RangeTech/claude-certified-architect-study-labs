"""D1 sandbox — orchestrator/worker: isolation, provenance, quarantine.

    python orchestrator_workers.py

Requires ANTHROPIC_API_KEY and `pip install anthropic`.

Exam points:
  - Each worker is a SEPARATE messages.create conversation. Subagents do NOT
    inherit the parent's context — you pass exactly what each needs in its prompt.
  - Findings carry provenance: {finding, source, confidence}.
  - A failed / no-evidence worker is QUARANTINED (tagged, kept out of synthesis),
    never silently dropped and never allowed to poison the final answer.
"""
import os
import sys
import json
import anthropic

MODEL = "claude-sonnet-4-6"

EVIDENCE = {
    "logs": "03:14:02Z host=db-7 disk_usage=100% writes_rejected; ingest latency 12ms -> 4200ms over 8 min.",
    "config": "commit a1b2c3 (21 days ago): log_rotation enabled -> removed. No rotation policy since.",
    "timeline": "",  # deliberately empty -> this worker must self-report low confidence -> quarantine
}
TASKS = {
    "logs": "Identify the anomaly and the exact time it started.",
    "config": "Identify the configuration change most likely to fill a disk.",
    "timeline": "Identify when the change deployed relative to the incident.",
}


def worker(client, key):
    """A subagent — a fresh conversation that sees ONLY what we pass in."""
    ev = EVIDENCE[key]
    prompt = TASKS[key]
    prompt += f"\n\nEVIDENCE:\n{ev}" if ev else "\n\n(No evidence was provided to you.)"
    prompt += ('\n\nReturn ONLY JSON: {"finding": str, "source": str, "confidence": 0.0-1.0}. '
               'If you lack evidence, set confidence 0 and finding "INSUFFICIENT_EVIDENCE".')
    r = client.messages.create(model=MODEL, max_tokens=300,
                               messages=[{"role": "user", "content": prompt}])
    txt = "".join(b.text for b in r.content if b.type == "text")
    try:
        return json.loads(txt[txt.find("{"):txt.rfind("}") + 1])
    except Exception:
        return {"finding": "PARSE_ERROR", "source": key, "confidence": 0.0}


def main():
    client = anthropic.Anthropic()
    findings = {k: worker(client, k) for k in TASKS}

    print("=== per-worker findings (provenance preserved) ===")
    for k, v in findings.items():
        print(f"  {k}: {v}")

    good = {k: v for k, v in findings.items()
            if v.get("confidence", 0) > 0 and "INSUFFICIENT" not in v.get("finding", "")}
    quarantined = [k for k in findings if k not in good]
    print(f"\n=== QUARANTINED (kept OUT of synthesis): {quarantined} ===")

    print("\n=== synthesis input (only trusted findings, still carrying source + confidence) ===")
    for v in good.values():
        print(f"  - {v['finding']}  (source={v['source']}, confidence={v['confidence']})")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY first")
    main()
