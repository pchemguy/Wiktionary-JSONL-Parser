"""Read Wiktionary JSONL and persist source-line batches to SQLite."""

import json
import sqlite3
from collections.abc import Iterator
from importlib.resources import files
from itertools import islice
from typing import BinaryIO, NoReturn


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


def read_batches(source: BinaryIO, batch_size: int) -> Iterator[list[bytes]]:
    """Read complete physical lines using LF framing."""

    while batch := list(islice(source, batch_size)):
        yield batch


def reject_json_constant(token: str) -> NoReturn:
    raise ValueError(f"invalid JSON constant {token}")


def decode_record(raw: bytes, line_number: int) -> dict[str, object]:
    """Decode one JSON object and attach its source line to decoding errors."""

    try:
        data = json.loads(
            raw.decode("utf-8-sig" if line_number == 1 else "utf-8"),
            parse_constant=reject_json_constant,
        )
    except (ValueError, RecursionError) as exc:
        raise ImportFailure(f"invalid JSONL record: {exc}", line_number) from exc
    if not isinstance(data, dict):
        raise ImportFailure("expected a JSON object", line_number)
    return data
