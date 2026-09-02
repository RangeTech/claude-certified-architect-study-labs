#!/usr/bin/env bash
# PostToolUse hook (macOS / bash) — runs AFTER a successful Edit/Write.
#
# Exam point: PreToolUse gates (can block); PostToolUse normalizes (formatters,
# linters, logging) after the fact. Returning additionalContext feeds a system
# reminder back to Claude so a later Read of the file isn't confused by changes
# the model didn't make itself.
set -euo pipefail

INPUT="$(cat)"
LOG="$(dirname "$0")/hook-activity.log"
TS="$(date '+%Y-%m-%d %H:%M:%S')"

FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')"

case "$FILE" in
  *.py)
    if command -v black >/dev/null 2>&1; then
      OUT="$(black "$FILE" 2>&1 || true)"
      echo "[$TS] black ran on $FILE :: $OUT" >> "$LOG"
      jq -n --arg f "$FILE" --arg o "$OUT" '{
        hookSpecificOutput: {
          hookEventName: "PostToolUse",
          additionalContext: ("Black reformatted " + $f + " after your edit. " + $o)
        }
      }'
    else
      echo "[$TS] black not installed; skipped $FILE (pip install black)" >> "$LOG"
    fi
    ;;
  *)
    echo "[$TS] PostToolUse no formatter for $FILE" >> "$LOG"
    ;;
esac
exit 0
