"""Decode and write one byte range into a worker SQLite database."""

import json
import sqlite3
from collections.abc import Callable, Iterable, Iterator
from contextlib import closing
from dataclasses import dataclass
from importlib.resources import files
from itertools import islice
from pathlib import Path
from sys import maxsize
from typing import BinaryIO, NoReturn

from .mapping import LINKAGES, RowsByTable, append_record_rows


class ImportFailure(Exception):
    """An import error with optional stage, chunk index, and chunk-local line."""

    def __init__(
        self,
        message: str,
        line_number: int | None = None,
        *,
        stage: str | None = None,
        chunk_index: int | None = None,
    ) -> None:
        self.detail = message
        self.stage = stage
        self.chunk_index = chunk_index
        self.line_number = line_number
        labels = []
        if stage is not None:
            labels.append(stage)
        if chunk_index is not None:
            labels.append(f"chunk {chunk_index}")
        if line_number is not None:
            labels.append(f"line {line_number}")
        super().__init__(": ".join([*labels, message]))


@dataclass(frozen=True)
class Chunk:
    index: int
    start: int
    stop: int


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


def read_batches(source: Iterable[bytes], batch_size: int) -> Iterator[list[bytes]]:
    """Read complete physical lines using LF framing."""

    lines = iter(source)
    while batch := list(islice(lines, min(batch_size, maxsize))):
        yield batch


def reject_json_constant(token: str) -> NoReturn:
    raise ValueError(f"invalid JSON constant {token}")


def decode_record(
    raw: bytes, line_number: int, *, bom_allowed: bool = True
) -> dict[str, object]:
    """Decode one JSON object and attach its source line to decoding errors."""

    try:
        data = json.loads(
            raw.decode("utf-8-sig" if bom_allowed and line_number == 1 else "utf-8"),
            parse_constant=reject_json_constant,
        )
    except (ValueError, RecursionError) as exc:
        raise ImportFailure(f"invalid JSONL record: {exc}", line_number) from exc
    if not isinstance(data, dict):
        raise ImportFailure("expected a JSON object", line_number)
    return data


INSERTS = {
    "entries": (
        "INSERT INTO entries (id, word, lang_code, lang, pos, pos_title, literal_meaning, "
        "etymology_texts, categories, raw_tags, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    **{
        table: f"INSERT INTO {table} (entry_id, idx, word, sense, sense_index, raw_tags, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
        for table in LINKAGES
    },
    "forms": "INSERT INTO forms (entry_id, idx, form, raw_tags, tags) VALUES (?, ?, ?, ?, ?)",
    "translations": (
        "INSERT INTO translations (entry_id, idx, word, lang, lang_code, roman, sense, other, "
        "raw_tags, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "hyphenations": (
        "INSERT INTO hyphenations (entry_id, idx, parts, raw_tags, tags) VALUES (?, ?, ?, ?, ?)"
    ),
    "senses": (
        "INSERT INTO senses (entry_id, idx, glosses, form_of, categories, topics, raw_tags, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "examples": (
        "INSERT INTO examples (sense_entry_id, sense_idx, idx, text, translation, ref, "
        "bold_text_offsets, bold_translation_offsets) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "sounds": (
        "INSERT INTO sounds (entry_id, idx, audio, ipa, rhymes, homophones, urls, raw_tags, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "batch_log": "INSERT INTO batch_log (batch_id, line_count) VALUES (?, ?)",
}


def write_batch(
    db: sqlite3.Connection, rows_by_table: RowsByTable, batch_id: int
) -> None:
    """Commit one batch atomically, including its log row."""

    try:
        db.execute("BEGIN")
        for table, sql in INSERTS.items():
            if rows_by_table[table]:
                db.executemany(sql, rows_by_table[table])
        db.commit()
    except sqlite3.Error as exc:
        if db.in_transaction:
            db.rollback()
        raise ImportFailure(f"cannot write batch {batch_id}: {exc}") from exc


ID_RANGE = 10_000_000
SQLITE_MAX_INTEGER = (1 << 63) - 1
Progress = Callable[[int, int, int], None]


def chunk_key(index: int, local_number: int) -> int:
    if local_number > ID_RANGE:
        raise ImportFailure(
            f"chunk exceeds its range of {ID_RANGE:,} IDs", local_number
        )
    key = index * ID_RANGE + local_number
    if key > SQLITE_MAX_INTEGER:
        raise ImportFailure("ID exceeds SQLite integer range", local_number)
    return key


def read_chunk(source: BinaryIO, chunk: Chunk) -> Iterator[bytes]:
    source.seek(chunk.start)
    remaining = chunk.stop - chunk.start
    while remaining:
        raw = source.readline(remaining)
        if not raw:
            raise ImportFailure("input ended inside the assigned range")
        remaining -= len(raw)
        yield raw


def run_chunk(
    input_path: Path,
    output_path: Path,
    chunk: Chunk,
    batch_size: int,
    on_progress: Progress | None = None,
) -> None:
    """Write a staged worker database and report only committed byte counts."""

    try:
        with (
            input_path.open("rb") as source,
            closing(sqlite3.connect(output_path)) as db,
        ):
            initialize_database(db)
            line_number = 0
            processed = 0
            batches = read_batches(read_chunk(source, chunk), batch_size)
            for batch_number, batch in enumerate(batches, 1):
                rows: RowsByTable = {table: [] for table in INSERTS}
                for raw in batch:
                    line_number += 1
                    entry_id = chunk_key(chunk.index, line_number)
                    record = decode_record(
                        raw, line_number, bom_allowed=chunk.start == 0
                    )
                    try:
                        append_record_rows(record, entry_id, rows)
                    except ValueError as exc:
                        raise ImportFailure(
                            f"invalid mapped value: {exc}", line_number
                        ) from exc
                batch_id = chunk_key(chunk.index, batch_number)
                rows["batch_log"].append((batch_id, len(batch)))
                write_batch(db, rows, batch_id)
                if on_progress is not None:
                    processed += sum(map(len, batch))
                    on_progress(chunk.index, processed, chunk.stop - chunk.start)
    except ImportFailure as exc:
        raise ImportFailure(
            exc.detail, exc.line_number, stage="worker", chunk_index=chunk.index
        ) from exc
    except (OSError, sqlite3.Error) as exc:
        raise ImportFailure(str(exc), stage="worker", chunk_index=chunk.index) from exc
