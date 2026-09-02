#!/usr/bin/env bash
# PreToolUse hook (macOS / bash) — deterministically BLOCKS Edit/Write to infra/prod/.
#
# Exam point: this is a *hard guardrail*. Unlike a CLAUDE.md rule or a loud prompt,
# a PreToolUse hook cannot be talked out of it — even if the user or the model
# "really wants to" edit the file. That determinism is why the honeypot answer
# ("add a stronger instruction to CLAUDE.md") loses to "add a hook / deny rule"
# whenever the requirement word is MUST / NEVER / GUARANTEE.
#
# Contract: hook payload arrives as JSON on stdin; we emit a JSON permission
# decision on stdout. Requires `jq`.
set -euo pipefail

INPUT="$(cat)"
LOG="$(dirname "$0")/hook-activity.log"
TS="$(date '+%Y-%m-%d %H:%M:%S')"

TOOL="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')"
FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')"

echo "[$TS] PreToolUse tool=$TOOL path=$FILE" >> "$LOG"

if printf '%s' "$FILE" | grep -q 'infra/prod/'; then
  echo "[$TS] BLOCKED $TOOL on $FILE" >> "$LOG"
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Edits to infra/prod/ are prohibited by a PreToolUse hook. This is a hardcoded guardrail, not a prompt rule.",
      additionalContext: "Route changes to infra/staging/ instead, or ask the user to apply infra/prod/ changes manually."
    }
  }'
  exit 0
fi

echo "[$TS] ALLOWED $TOOL on $FILE" >> "$LOG"
exit 0
