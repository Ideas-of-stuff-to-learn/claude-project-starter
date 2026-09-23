"""Rebuild .ai/knowledge.db from scratch. Run from repo root: python .ai/rebuild_db.py"""
import sqlite3, os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS context_documents (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    path        TEXT NOT NULL,
    description TEXT,
    tags        TEXT,
    updated_at  TEXT
);
CREATE TABLE IF NOT EXISTS files (
    id          INTEGER PRIMARY KEY,
    path        TEXT NOT NULL UNIQUE,
    language    TEXT,
    description TEXT,
    tags        TEXT
);
CREATE TABLE IF NOT EXISTS dependencies (
    id           INTEGER PRIMARY KEY,
    source       TEXT NOT NULL,
    relationship TEXT NOT NULL,
    target       TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS constraints (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    severity    TEXT DEFAULT 'hard'
);
CREATE TABLE IF NOT EXISTS decisions (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL UNIQUE,
    description TEXT,
    area        TEXT
);
CREATE TABLE IF NOT EXISTS known_problems (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL UNIQUE,
    description TEXT,
    area        TEXT,
    severity    TEXT DEFAULT 'medium'
);
CREATE TABLE IF NOT EXISTS failed_solutions (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL UNIQUE,
    description TEXT,
    area        TEXT,
    lesson      TEXT
);
CREATE TABLE IF NOT EXISTS realignment (
    id                   INTEGER PRIMARY KEY,
    realignment_doc      TEXT,
    overview_doc         TEXT,
    architecture_doc     TEXT,
    constraints_doc      TEXT,
    current_task_doc     TEXT,
    dependencies_doc     TEXT,
    decisions_doc        TEXT,
    known_problems_doc   TEXT,
    failed_solutions_doc TEXT,
    handoff_doc          TEXT,
    git_doc              TEXT,
    notes                TEXT
);
DROP TABLE IF EXISTS git_configuration;
CREATE TABLE git_configuration (
    id            INTEGER PRIMARY KEY,
    upstream      TEXT,
    base_branch   TEXT,
    auto_merge    INTEGER DEFAULT 0,
    branch_prefix TEXT,
    trigger_word  TEXT,
    workflow      TEXT,
    notes         TEXT
);
""")

# ── Context Documents ─────────────────────────────────────────────────────────
context_docs = [
    ("overview",         "context/overview.md",         "Project purpose, subsystems, tech stack",                             "overview,intro,stack"),
    ("architecture",     "context/architecture.md",     "Layers, data flows, component responsibilities",                      "architecture,layers,flow"),
    ("dependencies",     "context/dependencies.md",     "File-to-file dependencies, call chains",                              "dependencies,imports,calls"),
    ("decisions",        "context/decisions.md",        "Engineering decisions with rationale",                                "decisions,rationale,design"),
    ("constraints",      "context/constraints.md",      "Hard invariants, behavioral constraints, security rules",             "constraints,invariants,rules"),
    ("known-problems",   "context/known-problems.md",   "Known bugs, technical debt, fragile areas",                          "bugs,debt,problems"),
    ("failed-solutions", "context/failed-solutions.md", "Previously attempted approaches that failed",                        "failed,history,lessons"),
    ("current-task",     "context/current-task.md",     "Currently active task, state, next steps",                           "task,current,status"),
    ("verification",     "context/verification.md",     "Build, dev server, manual verification procedures",                  "verification,build"),
    ("handoff",          "context/handoff.md",          "Session handoff: recent changes, open work, notes",                  "handoff,session"),
    ("realignment",      "context/realignment.md",      "Recovery map: how to reconstruct project understanding",             "realignment,recovery"),
    ("gitContext",       "context/gitContext.md",        "Git repo URL, workflow rules, CI/CD",                               "git,workflow,ci"),
    ("revert-state",     "context/revert-state.md",     "Safe-point commit hashes recorded before each task",                 "git,revert,safety"),
    ("savings-log",      "context/savings-log.md",      "Running log of sessions using the intelligence system",              "meta,savings,log"),
]
c.executemany(
    "INSERT OR REPLACE INTO context_documents (name, path, description, tags, updated_at) VALUES (?, ?, ?, ?, date('now'))",
    [(name, path, desc, tags) for name, path, desc, tags in context_docs]
)

# ── Source Files ──────────────────────────────────────────────────────────────
# Add your project's key files here after running /build-intelligence
files = []
c.executemany(
    "INSERT OR REPLACE INTO files (path, language, description, tags) VALUES (?, ?, ?, ?)",
    files
)

# ── Dependencies ──────────────────────────────────────────────────────────────
deps = []
c.executemany(
    "INSERT OR REPLACE INTO dependencies (source, relationship, target) VALUES (?, ?, ?)",
    deps
)

# ── Constraints ───────────────────────────────────────────────────────────────
constraints_data = []
c.executemany(
    "INSERT OR REPLACE INTO constraints (title, description, severity) VALUES (?, ?, ?)",
    constraints_data
)

# ── Known Problems ────────────────────────────────────────────────────────────
problems = []
c.executemany(
    "INSERT OR REPLACE INTO known_problems (title, description, area, severity) VALUES (?, ?, ?, ?)",
    problems
)

# ── Failed Solutions ──────────────────────────────────────────────────────────
failures = []
c.executemany(
    "INSERT OR REPLACE INTO failed_solutions (title, description, area, lesson) VALUES (?, ?, ?, ?)",
    failures
)

# ── Git Config ────────────────────────────────────────────────────────────────
# Update upstream to your repo URL after setup
c.execute("""
INSERT OR REPLACE INTO git_configuration (id, upstream, base_branch, auto_merge, branch_prefix, trigger_word, workflow, notes)
VALUES (
    1,
    'https://github.com/owner/repo.git',
    'main',
    0,
    'ai/',
    'ship',
    'implement locally → owner says "ship" → git add → commit → git pull --rebase → git push origin main.',
    'Never auto-merge. Branch workflow (ai/<desc>) only when owner explicitly requests a PR.'
)
""")

# ── Realignment Record ────────────────────────────────────────────────────────
c.execute("""
INSERT OR REPLACE INTO realignment (
    id, realignment_doc, overview_doc, architecture_doc, constraints_doc,
    current_task_doc, dependencies_doc, decisions_doc, known_problems_doc,
    failed_solutions_doc, handoff_doc, git_doc, notes
) VALUES (
    1, 'context/realignment.md', 'context/overview.md', 'context/architecture.md',
    'context/constraints.md', 'context/current-task.md', 'context/dependencies.md',
    'context/decisions.md', 'context/known-problems.md', 'context/failed-solutions.md',
    'context/handoff.md', 'context/gitContext.md',
    'Load realignment.md first. Then overview→architecture→constraints→current-task. Others only as needed.'
)
""")

conn.commit()
conn.close()
print("knowledge.db rebuilt successfully.")

conn2 = sqlite3.connect(db_path)
c2 = conn2.cursor()
for table in ["context_documents","files","dependencies","constraints","known_problems","failed_solutions"]:
    n = c2.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {n} rows")
conn2.close()
