# Swap-in settings snippets

These are *fragments* to paste into `.claude/settings.json` (merge them into the
existing `permissions` block) so you can watch each enforcement behavior change.
Run `/permissions` inside Claude Code after editing to confirm what loaded.

- `deny-secrets.json` — hard-deny reads of secrets. Ask Claude to read `.env`; watch it refuse.
- `ask-before-bash.json` — force a confirmation prompt before any Bash command.
- `allowlist-git.json` — allow a narrow set of git commands without prompting.

Exam point — the enforcement ladder (low → high):
prompt wording < CLAUDE.md guidance < few-shot examples < validation/retry loop
< **hooks / permission deny rules / strict tool use / structured outputs**.
When the requirement is MUST / NEVER / GUARANTEE (financial, safety, compliance),
the answer lives at the top of the ladder — a deterministic mechanism, never
"add a stronger instruction".
