# Official Resources Index

## Certification
- CCA-F certification page (Exam Guide PDF, T&Cs, exam policy, practice exam): https://anthropic.skilljar.com/claude-certified-architect-foundations-certification
- Exam access request: https://anthropic.skilljar.com/claude-certified-architect-foundations-access-request

## Anthropic Academy (free courses)
- Course catalog: https://anthropic.skilljar.com/
- Introduction to Model Context Protocol: https://anthropic.skilljar.com/introduction-to-model-context-protocol
- MCP: Advanced Topics: https://anthropic.skilljar.com/model-context-protocol-advanced-topics
- Introduction to Agent Skills: https://anthropic.skilljar.com/introduction-to-agent-skills
- Introduction to Subagents: https://anthropic.skilljar.com/introduction-to-subagents
- Building with the Claude API and Claude Code in Action: find both in the catalog above.

## Docs by domain

D1 Agentic Architecture & Orchestration
- Building effective agents (workflows vs agents; the five workflow patterns incl. orchestrator-workers): https://www.anthropic.com/engineering/building-effective-agents
- How we built our multi-agent research system (orchestrator-worker in production, subagent prompt completeness, checkpoints/state persistence, resume-on-error): https://www.anthropic.com/engineering/multi-agent-research-system
- Tool use overview (the agent loop, stop_reason, parallel tool use): https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
- Subagents in Claude Code (context isolation, tool restrictions, spawning): https://code.claude.com/docs/en/sub-agents
- Subagents in the Agent SDK (AgentDefinition parameters, coordinator wiring): https://code.claude.com/docs/en/agent-sdk/subagents

D2 Tool Design & MCP Integration
- Tool use overview (descriptions, tool_choice, strict): https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
- MCP in Claude Code (scopes: local/project/user, env-var expansion, /mcp, auth): https://code.claude.com/docs/en/mcp
- Model Context Protocol docs (client/server model, tools vs resources vs prompts): https://modelcontextprotocol.io/

D3 Claude Code Configuration & Workflows
- Claude Code overview: https://docs.claude.com/en/docs/claude-code/overview
- Extend Claude Code — when to use CLAUDE.md vs rules vs Skills vs subagents vs hooks vs MCP: https://code.claude.com/docs/en/features-overview
- Memory / CLAUDE.md (hierarchy, imports, `.claude/rules/` with path globs): https://code.claude.com/docs/en/memory
- Hooks: https://code.claude.com/docs/en/hooks
- Skills: https://code.claude.com/docs/en/skills
- Slash commands: https://code.claude.com/docs/en/slash-commands
- Settings and permissions: https://code.claude.com/docs/en/settings
- Permission modes (incl. plan mode): https://code.claude.com/docs/en/permission-modes
- Subagents: https://code.claude.com/docs/en/sub-agents
- MCP in Claude Code: https://code.claude.com/docs/en/mcp
- CLI reference (-p, --output-format json, --resume, --bare, --tools vs --allowedTools): https://code.claude.com/docs/en/cli-reference
- Headless / programmatic use (bare mode, JSON output, auto-approving tools): https://code.claude.com/docs/en/headless
- Tools reference (Grep vs Glob vs Read vs Bash — which tool for which job): https://code.claude.com/docs/en/tools-reference
- Common workflows (codebase exploration, plan mode, refactoring, testing): https://code.claude.com/docs/en/common-workflows
- Sessions (--continue, --resume, session scope rules): https://code.claude.com/docs/en/sessions
- Code review (automated PR review configuration): https://code.claude.com/docs/en/code-review
- GitHub Actions: https://code.claude.com/docs/en/github-actions

D4 Prompt Engineering & Structured Output
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Structured outputs (output_config.format, strict tools, incompatibilities, optional/nullable fields, enums): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Console prompting tools (generator, improver, eval): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools

D5 Context Management & Reliability
- Context editing (tool-result clearing, thinking clearing, compaction): https://platform.claude.com/docs/en/build-with-claude/context-editing
- Batch processing: https://docs.claude.com/en/docs/build-with-claude/batch-processing
- Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## Interactive / hands-on (official)
- anthropics/courses notebooks (incl. prompt engineering interactive tutorial): https://github.com/anthropics/courses
- Anthropic Cookbook: https://github.com/anthropics/anthropic-cookbook

If any code.claude.com slug moves, start from the docs index at https://code.claude.com/docs/llms.txt; it enumerates every page.
