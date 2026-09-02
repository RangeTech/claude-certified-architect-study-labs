# D4-Prompting — Prompt Engineering & Structured Output (20%)

```bash
export ANTHROPIC_API_KEY=sk-...
pip install anthropic
```

## Files
- `structured_output.py` — guarantee output shape with a forced tool schema.
- `prompt_size.py` — measure the token/latency tax of a bloated system prompt.

## Experiments

### 1. Guaranteed structure
```bash
python structured_output.py
```
A tool `input_schema` + `tool_choice={"type":"tool","name":...}` forces the model to emit args matching the schema — every `required` key is present. This is the deterministic answer when a scenario says the output MUST be valid JSON of a fixed shape (vs. "ask nicely for JSON in the prompt", the honeypot).

### 2. Prompt right-sizing
```bash
python prompt_size.py
```
Same extraction, a padded vs a concise system prompt. The big one burns input tokens and latency on **every** call with no accuracy gain here. Bigger ≠ better.

## Hard incompatibilities (memorize — the exam tests these as absolutes)

| Combination | Result |
|---|---|
| citations + `output_config.format` | **400 error** |
| prefilling the assistant turn + JSON outputs | **incompatible** |
| changing `output_config.format` mid-thread | **invalidates the prompt cache** |
| JSON outputs + `strict: true` tools | **combinable in one request (OK)** |

## Enforcement ladder (low → high)
prompt wording < CLAUDE.md guidance < few-shot examples < validation/retry loop < **schema-forced tools / structured outputs / strict**. When the requirement word is MUST / ALWAYS / GUARANTEE, climb to the top.

## Self-check
1. Output MUST be valid JSON of a fixed schema — mechanism? → **forced tool schema / structured outputs**, not a prompt request.
2. Citations + a forced output format? → **400 error.**
3. Prefill + JSON outputs? → **incompatible.**
4. Does a longer system prompt improve accuracy? → **No** — it costs tokens/latency; right-size it.
5. Change `output_config.format` mid-conversation — side effect? → **cache invalidated.**
