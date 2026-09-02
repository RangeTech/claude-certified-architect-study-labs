---
description: Python style conventions, scoped to source files only
paths:
  - "src/**/*.py"
---

# Python style (loads only when Claude touches src/**/*.py)

- Use snake_case for functions and variables.
- Prefer f-strings over `.format()` and `%` formatting.
- Every public function gets a one-line docstring.

Exam point: a `.claude/rules/*.md` file with a `paths:` glob is *scoped* guidance —
it is pulled in only when Claude works on a matching file, unlike CLAUDE.md which
is always loaded. Pick rules over CLAUDE.md when the guidance is file-type specific
and would otherwise be dead weight in every conversation.
