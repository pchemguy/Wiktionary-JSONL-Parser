"""Read Wiktionary JSONL and persist source-line batches to SQLite."""

import sqlite3
from importlib.resources import files


class ImportFailure(Exception):
    """An import error, optionally tied to a one-based input line."""

    def __init__(self, message: str, line_number: int | None = None) -> None:
        self.line_number = line_number
        super().__init__(
            message if line_number is None else f"line {line_number}: {message}"
        )


def schema_sql() -> str:
    """Read the packaged SQLite DDL."""

    return files(__package__).joinpath("schema.sql").read_text(encoding="utf-8")


def require_unicode_collation(db: sqlite3.Connection) -> None:
    """Check that the connection provides the required SQLiteICUex collation."""

    try:
        db.execute("SELECT 'a' = 'A' COLLATE UTF_CI").fetchone()
    except sqlite3.OperationalError as exc:
        raise ImportFailure("SQLiteICUex must provide the UTF_CI collation") from exc


def initialize_database(db: sqlite3.Connection) -> None:
    """Enable foreign keys and create the converter schema."""

    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(schema_sql())
