---
name: release-runbook
description: Use when preparing, tagging, or documenting a software release; covers changelog, version bump, git tag, and deploy checklist
---

## Release Runbook

1. Update CHANGELOG.md with all changes since the last release.
2. Bump the version in pyproject.toml / package.json.
3. `git tag -a v{version} -m "Release v{version}"`.
4. `git push origin v{version}`.
5. Deploy via the CI pipeline.
6. Announce in #releases.

<!--
Exam point: a skill loads ITSELF when its frontmatter `description` matches the
task — you do not invoke it by name. If a skill "won't trigger", the fix is a
sharper description (the trigger surface), NOT louder prompting. Progressive
disclosure: only this description sits in context until the skill fires.
Frontmatter extras worth knowing: `disable-model-invocation: true` makes it
user-invoke-only (a slash command); `context: fork` runs it in an isolated
subagent context with no conversation history.
-->
