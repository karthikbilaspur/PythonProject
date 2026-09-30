"""SQLite connection and schema."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT NOT NULL,
    author       TEXT NOT NULL,
    isbn         TEXT NOT NULL UNIQUE,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 1),
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS members (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id     INTEGER NOT NULL REFERENCES books(id),
    member_id   INTEGER NOT NULL REFERENCES members(id),
    borrowed_on TEXT NOT NULL,
    due_on      TEXT NOT NULL,
    returned_on TEXT,
    fine        REAL NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_loans_active ON loans(book_id, returned_on);
CREATE INDEX IF NOT EXISTS idx_loans_member ON loans(member_id, returned_on);
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    # isolation_level=None -> we control transactions explicitly (see service._tx)
    conn = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn
