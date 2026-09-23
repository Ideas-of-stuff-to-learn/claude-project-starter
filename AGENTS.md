# [Project Name] — AI Operating Instructions

> **Setup:** Replace this header with your project name, fill in the one-paragraph description below,
> then delete this callout block. Run `/build-intelligence` in fill-in mode on first session.

[One-paragraph project description: what it does, tech stack, primary use case.]

---

## Persistent Knowledge System

This repository uses a persistent intelligence system. Do not reconstruct project understanding from scratch by scanning the whole repo — use the knowledge system instead.

### Keep the Context Window Light

Query SQLite for exactly what the current task needs — do not load everything upfront, and do not accumulate knowledge in the context window just because it is convenient. This applies continuously throughout every session, not only at the start.

### Entry Point

**SQLite database:** `.ai/knowledge.db`

Query it to find what you need:
```sql
-- Recover project context (start here in any new session)
SELECT * FROM realignment WHERE id = 1;

-- Find context docs by topic
SELECT name, path, description FROM context_documents WHERE tags LIKE '%auth%';

-- Find key files by area
SELECT path, description FROM files WHERE tags LIKE '%api%';

-- Find what depends on a file
SELECT * FROM dependencies WHERE target LIKE '%service%';

-- Check constraints before modifying anything
SELECT title, description FROM constraints WHERE severity = 'hard';

-- Check if approach has been tried and failed
SELECT title, lesson FROM failed_solutions WHERE area = 'backend';
```

### Context Documents (`context/`)

| File | Purpose |
|---|---|
| `context/realignment.md` | **Start here** — recovery map, what to load and in what order |
| `context/overview.md` | Project purpose, subsystems, tech stack |
| `context/architecture.md` | Layers, data flows, component responsibilities |
| `context/constraints.md` | Hard invariants that must not be violated |
| `context/current-task.md` | Active task, recent state |
| `context/dependencies.md` | File-to-file dependencies, call chains |
| `context/decisions.md` | Engineering decisions with rationale |
| `context/known-problems.md` | Known bugs, debt, fragile areas |
| `context/failed-solutions.md` | Previously attempted approaches that failed |
| `context/verification.md` | Build, dev server, and manual verification procedures |
| `context/handoff.md` | Recent changes, open work, notes for next session |
| `context/gitContext.md` | Git repo URL, workflow rules, CI/CD |

---

## Context Degradation Recovery

If you are in a new session, have lost context, are unsure about architecture, or are continuing work from another session:

1. Read `context/realignment.md` — it tells you exactly what to load and in what order
2. Query `.ai/knowledge.db` realignment record for pointers
3. Do NOT scan the entire repository — retrieve only what you need for the task

---

## Updating Durable Knowledge

When you discover something that should persist:

| Discovery | Update |
|---|---|
| Architecture finding | `context/architecture.md` |
| New dependency relationship | `context/dependencies.md` |
| Design decision | `context/decisions.md` |
| Hard constraint | `context/constraints.md` |
| New bug or debt | `context/known-problems.md` |
| Failed approach | `context/failed-solutions.md` |
| Active task state | `context/current-task.md` |
| Session state / recent changes | `context/handoff.md` |
| Intelligence system usage | `context/savings-log.md` |
| Revert safe-points | `context/revert-state.md` |

**Ghost test / local verification cleanup:** any temporary files generated during a ghost test or local verification (scratch scripts, test outputs, debug files) must be fully deleted before the task is considered complete. Never commit or leave them in the working directory.

**Before touching any code**, record the current commit hash in `context/revert-state.md`:
```bash
git rev-parse HEAD
```
Format: `YYYY-MM-DD | task: <description> | safe-point: <hash> | status: in-progress`
Update status to `complete` or `reverted` when done.

At the end of every session, append one line to `context/savings-log.md`:
```
YYYY-MM-DD | task: <what was done> | SQLite queries: <N> | context docs loaded: <N> | full repo scan avoided: yes/no | notes
```

After updating Markdown, sync to SQLite:
```bash
python .ai/sync_context.py   # fast — only re-syncs changed context/*.md docs
python .ai/rebuild_db.py     # full rebuild — use when file index/deps/constraints change
```

---

## Git Workflow

- **Trigger word:** `"ship"` — when the owner says this, commit and push current work
- Direct to `main` by default (no PR unless owner requests one)
- Never auto-merge
- Branch workflow (`ai/<desc>`) only when owner explicitly requests a PR
- `git pull --rebase` before pushing if behind origin; `git stash -u` first if uncommitted changes exist
- Commit attribution: end all commit messages with `Co-Authored-By: Claude <noreply@anthropic.com>`

---

## Progress Updates

After each meaningful sub-step of any task — reading context, finishing a file edit, completing a sync, hitting a decision point — write a one-to-two line **visible text message to the user** with a rough overall completion percentage.

```
✓ <what was just done> [~X% complete]
→ <what's next / current step> [~X% complete]
```

---

## Hard Constraints (Quick Reference)

> **Fill this in** after running `/build-intelligence`. List the invariants that must never be violated in this project.

- _(none yet — add as you discover them)_
