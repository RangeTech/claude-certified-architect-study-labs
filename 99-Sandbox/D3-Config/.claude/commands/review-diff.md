---
description: Review the current git diff for correctness and style
---

Run `git diff` and review the staged and unstaged changes for:

- correctness bugs (logic errors, unhandled cases)
- violations of the conventions in `.claude/rules/`

Group findings by severity (blocking / non-blocking). Do NOT edit files — report only.

$ARGUMENTS

<!--
Exam point: a slash command has EXPLICIT timing — the user decides when it runs,
unlike a skill (self-triggers on description match) or a subagent (a separate
session via the Task tool, used for context isolation or parallelism). $ARGUMENTS
injects whatever the user typed after the command.
-->
