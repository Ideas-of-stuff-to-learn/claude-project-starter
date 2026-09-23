# claude-project-starter

A GitHub template repository with the Claude Code intelligence system pre-installed. New projects start with AGENTS.md, context skeleton, SQLite knowledge base scripts, and plugin wiring already in place — no setup from scratch.

## How to use

1. Click **"Use this template"** on GitHub to create a new repo from this one
2. Clone the new repo
3. Open it in Claude Code
4. Fill in `AGENTS.md`: replace the `[Project Name]` header and the project description
5. Update `context/gitContext.md` with your repo URL
6. Run `/build-intelligence` — the skill will fill in `context/*.md` files and populate `.ai/knowledge.db` based on your actual codebase

## What's included

| Path | Purpose |
|---|---|
| `AGENTS.md` | AI operating instructions (edit the project section at the top) |
| `CLAUDE.md` | One-line `@AGENTS.md` import for Claude Code |
| `context/*.md` | 14 context skeleton files — fill in after setup |
| `.ai/rebuild_db.py` | Rebuild SQLite knowledge base from scratch |
| `.ai/sync_context.py` | Fast incremental sync of context docs to SQLite |
| `.ai/system-config.json` | Project-specific config read by plugin hook scripts |
| `tasks/backlog.md` | Session progress log |
| `.claude/settings.json` | Plugin marketplace + enabled plugins |
| `.gitignore` | Correct §68 setup — `.claude/` tracked, local settings excluded |

## Plugin

This template references the [claude-intelligence-plugin](https://github.com/Ideas-of-stuff-to-learn/claude-intelligence-plugin), which will supply skills, hooks, and subagents once they are packaged there. Install it with:

```
/plugin marketplace add Ideas-of-stuff-to-learn/claude-intelligence-plugin
/plugin install claude-intelligence-plugin@claude-intelligence-plugin
```
