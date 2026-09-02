# D3-Config — Claude Code config playground (CCA-F Domain 3)

A throwaway space to *touch* every configuration mechanism the exam tests in
**Domain 3 — Claude Code Configuration & Workflows (20%)**. The official
`_AnswerKeys/D3/` artifacts are PowerShell/Windows; this sandbox is macOS/bash so
you can actually run it locally. Nothing here is graded — break it, tweak it, undo it.
(This is one of the five domain sandboxes under `99-Sandbox/`.)

> This is a sandbox, not a lab. Do the real labs (`03-Hands-On-Labs/D3/`) for the
> guided version with success criteria. Come here to experiment freely.

## What's inside

```
99-Sandbox/D3-Config/
├── CLAUDE.md                     project memory (marker: SANDBOX-PROJECT) + @import
├── shared-conventions.md         imported into CLAUDE.md via @import
├── sub/CLAUDE.md                 subdirectory memory (marker: SANDBOX-SUBDIR, loads on demand)
├── src/example.py                deliberately unformatted → PostToolUse formatter target
├── infra/prod/config.yaml        PROTECTED (deny rule + PreToolUse hook block)
├── infra/staging/config.yaml     unprotected (the "safe" target)
├── headless/generate-then-review.sh   two-stage isolated-session CI pipeline
└── .claude/
    ├── settings.json             permissions (allow/ask/deny) + hook wiring
    ├── settings-examples/        swap-in permission fragments to observe each behavior
    ├── hooks/                    pre-tool-block.sh (PreToolUse), post-tool-format.sh (PostToolUse)
    ├── rules/python-style.md     scoped rule (paths: glob) — loads only for src/**/*.py
    ├── skills/release-runbook/   a skill that self-triggers on its description
    └── commands/review-diff.md   a /review-diff slash command (explicit timing)
```

## Setup (one time)

```bash
chmod +x .claude/hooks/*.sh headless/*.sh   # already done if you cloned after setup
# Prereqs used by the demos: jq (hooks), and optionally black (formatter demo)
brew install jq
pip install black        # optional, for the PostToolUse demo
```

### Important: how to actually load these settings

Claude Code resolves the *project root* from the git repository root. Because this
sandbox is nested inside the study repo, running `claude` from the repo root will
**not** pick up `99-Sandbox/D3-Config/.claude/settings.json` or the hooks. Two ways to run it:

- **Recommended — make it its own project:**
  ```bash
  cp -R 99-Sandbox/D3-Config ~/cca-sandbox && cd ~/cca-sandbox && git init && claude
  ```
- **In place:** `cd 99-Sandbox/D3-Config && claude` still loads `CLAUDE.md`/`sub/CLAUDE.md`
  hierarchy and `/memory`, but project `settings.json` + hooks may not activate
  unless this folder is the git/project root. When in doubt, use the copy above.

Inside Claude Code, `/memory` shows loaded memory files and `/permissions` shows
active allow/ask/deny rules — use them to verify each experiment.

## Guided experiments

Each maps to an exam objective. Predict the outcome *before* you run it.

### 1. Memory hierarchy + @import  (objective: CLAUDE.md hierarchy)
Ask Claude: **"Which markers do you see?"** At the sandbox root you should see
`SANDBOX-PROJECT` (repo root) and the imported `snake_case` convention, but **not**
`SANDBOX-SUBDIR`. Then ask it to work on a file in `sub/` and ask again — the
subdirectory marker now loads on demand. (A `~/.claude/CLAUDE.md` USER marker, if
you have one, always loads.)
**Predict:** which markers are in context at the root vs inside `sub/`?

### 2. PreToolUse hook = hard guardrail  (objective: hooks vs prompt rules)
Ask Claude to **edit `infra/prod/config.yaml`** (e.g. "set replicas to 9"). The
PreToolUse hook denies it deterministically and suggests `infra/staging/`. Now try
`infra/staging/config.yaml` — it succeeds. Tail `.claude/hooks/hook-activity.log`
to see ALLOWED/BLOCKED lines.
**Why it matters:** a CLAUDE.md "please never edit prod" is guidance a model can
rationalize past; the hook cannot be. This is the MUST/NEVER → deterministic answer.

### 3. PostToolUse hook = normalization  (objective: PreToolUse vs PostToolUse)
Ask Claude to **edit `src/example.py`** (any change). If `black` is installed, the
PostToolUse hook reformats it afterward and reports back via `additionalContext`.
**Predict:** does the hook run before or after the edit lands? Could it *block* the
edit? (No — that's PreToolUse's job.)

### 4. Permission deny/ask/allow  (objective: settings enforcement)
Run `/permissions`. Then merge a fragment from `settings-examples/` into
`settings.json` and re-check: `deny-secrets.json` (ask Claude to read `.env` → refused),
`ask-before-bash.json` (every Bash prompts first), `allowlist-git.json` (whitelisted
git runs without a prompt).
**Predict:** which wins when the same path is in both `allow` and `deny`? (deny)

### 5. Scoped rule vs always-on memory  (objective: rules/ paths glob)
`rules/python-style.md` has `paths: ["src/**/*.py"]`. Ask Claude to edit a `.py` in
`src/` and it should honor snake_case / f-strings; editing a YAML file it won't pull
the rule in. Contrast with CLAUDE.md, which is always loaded.
**Predict:** why scope a rule instead of putting it in CLAUDE.md? (keeps
file-type-specific guidance out of every unrelated conversation)

### 6. Skill self-triggering  (objective: skills & progressive disclosure)
Ask something like **"help me cut a release"** — the `release-runbook` skill should
fire off its *description* match without you naming it. Now weaken the description
(edit the frontmatter to something vague) and watch it stop triggering.
**Lesson:** fix triggering by fixing the description, not by prompting louder.

### 7. Slash command vs skill vs subagent  (objective: invocation mechanisms)
Run **`/review-diff`** — explicit, user-timed. Compare mentally: a skill loads
itself on a description match; a subagent (Task tool) is a separate session for
isolation/parallelism.

### 8. Headless isolated-session review  (objective: CI workflows, review architecture)
```bash
cd ~/cca-sandbox   # wherever you copied it; needs ANTHROPIC_API_KEY
./headless/generate-then-review.sh
```
Stage 1 generates `src/generated.py`; Stage 2 reviews it in a **fresh** session with
none of the generator's context, then a CI gate branches on `VERDICT: PASS/FAIL`.
**Why:** an independent reviewer beats same-session self-review (the generator is
anchored to its own choices). `--output-format json` makes the result machine-parseable.

## Self-check (answers are the exam's discriminators)

1. A rule "MUST never touch prod" — CLAUDE.md line, or hook/deny rule? → **hook / deny (deterministic).**
2. A skill isn't triggering. Fix? → **sharpen its `description`**, not louder prompts.
3. PreToolUse vs PostToolUse? → **Pre can block (gate); Post normalizes after (formatters/logging).**
4. Same path in `allow` and `deny`? → **deny wins.**
5. Guidance only relevant to `*.py` files? → **`.claude/rules/*.md` with a `paths:` glob**, not CLAUDE.md.
6. Better review: same-session self-review or a fresh isolated session? → **isolated session.**
7. `@import` in CLAUDE.md does what? → pulls a shared file into project memory.
8. Subdirectory CLAUDE.md loads when? → **on demand**, when Claude works in that subdir.

## Reset

```bash
git checkout 99-Sandbox/D3-Config && git clean -fd 99-Sandbox/D3-Config   # from the repo root
```
Ignored runtime files (`hook-activity.log`, `gen-*.json`, `review-*.json`,
`src/generated.py`) are already listed in `.gitignore`.
