#!/usr/bin/env bash
# Two-stage headless pipeline (macOS / bash) — generate in one session, then
# review in a SEPARATE, isolated session.
#
# Exam point: an independent reviewer with none of the generator's reasoning
# context catches more than same-session self-review (the generator is anchored
# to its own choices). `claude -p` = non-interactive; `--output-format json` =
# machine-parseable so a CI gate can branch on the result.
set -euo pipefail

SPEC="${1:-Write a Python function process_batch(records) that filters active records and returns count + average score. Save it to src/generated.py}"
TS="$(date '+%H%M%S')"

echo "=== STAGE 1: generate (session A) ==="
claude -p "$SPEC" --output-format json > "gen-$TS.json"
if [ "$(jq -r '.is_error' "gen-$TS.json")" = "true" ]; then
  echo "generation failed:" >&2
  jq -r '.result' "gen-$TS.json" >&2
  exit 1
fi

echo "=== STAGE 2: review in a FRESH session (session B, no gen context) ==="
claude -p "Review src/generated.py for correctness bugs and style. Print BLOCKING first, then non-blocking. End with the literal line VERDICT: PASS or VERDICT: FAIL." \
  --output-format json > "review-$TS.json"

VERDICT="$(jq -r '.result' "review-$TS.json" | grep -Eo 'VERDICT: (PASS|FAIL)' | tail -1 || true)"
echo "Reviewer said: ${VERDICT:-<none>}"
[ "$VERDICT" = "VERDICT: PASS" ] || { echo "gate: blocking findings, exit 1" >&2; exit 1; }
echo "gate: passed"
