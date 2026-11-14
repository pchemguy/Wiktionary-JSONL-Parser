"""Database definitions for supported Wiktionary editions."""

import sqlite3
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeAlias

Row: TypeAlias = tuple[str | int | None, ...]
RowsByTable: TypeAlias = dict[str, list[Row]]


@dataclass(frozen=True)
class Edition:
    """The mapped schema and parent-first write order for one edition."""

    identifier: str
    schema_sql: Callable[[], str]
    map_record: Callable[[dict[str, object], int, RowsByTable], None]
    inserts: Mapping[str, str]
    skip_record: Callable[[dict[str, object]], bool] | None = None


def get_edition(identifier: str) -> Edition:
    if identifier == "ru":
        from .ru import RUSSIAN_EDITION

        return RUSSIAN_EDITION
    raise ValueError(f"unsupported Wiktionary edition: {identifier}")


BATCH_LOG_SCHEMA = """CREATE TABLE batch_log (
    batch_id            INTEGER PRIMARY KEY,
    line_count          INTEGER NOT NULL
);

"""
BATCH_LOG_INSERT = "INSERT INTO batch_log (batch_id, line_count) VALUES (?, ?)"


def initialize_database(db: sqlite3.Connection, edition: Edition) -> None:
    """Enable foreign keys and create the shared log and edition tables."""

    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(BATCH_LOG_SCHEMA + edition.schema_sql())
