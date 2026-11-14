"""Read Wiktionary JSONL and persist source-line batches to SQLite."""

import json
import sqlite3
from collections.abc import Callable, Iterator
from contextlib import closing
from dataclasses import dataclass
from importlib.resources import files
from itertools import islice
from os import fstat
from pathlib import Path
from sys import maxsize
from typing import BinaryIO, NoReturn

from .mapping import LINKAGES, RowsByTable, append_record_rows


class ImportFailure(Exception):
    """An import error, optionally tied to a one-based input line."""

    def __init__(self, message: str, line_number: int | None = None) -> None:
        self.line_number = line_number
        super().__init__(
            message if line_number is None else f"line {line_number}: {message}"
        )


@dataclass(frozen=True)
class RunPlan:
    worker_count: int
    merge_group_size: int


def plan_run(
    cpu_count: int | None,
    attachment_limit: int,
    on_warning: Callable[[str], None] | None,
    confirm_single_worker: Callable[[], bool] | None,
) -> RunPlan:
    """Choose the process count and number of attachments per merge group."""

    requested = cpu_count - 2 if cpu_count is not None and cpu_count > 2 else 1
    if requested > attachment_limit and on_warning is not None:
        on_warning(
            f"requested {requested} workers but SQLite allows {attachment_limit} attachments"
        )
    if requested == 1:
        return RunPlan(1, 0)
    if attachment_limit == 0:
        if confirm_single_worker is not None and confirm_single_worker() is True:
            return RunPlan(1, 0)
        raise ImportFailure("running with one worker requires explicit confirmation")
    if attachment_limit < requested and 2 * requested < 3 * attachment_limit:
        return RunPlan(attachment_limit, attachment_limit)
    return RunPlan(requested, min(requested, attachment_limit))


def probe_attachment_limit() -> int:
    with closing(sqlite3.connect(":memory:")) as probe:
        require_unicode_collation(probe)
        return probe.getlimit(sqlite3.SQLITE_LIMIT_ATTACHED)


@dataclass(frozen=True)
class Chunk:
    index: int
    start: int
    stop: int


def partition_source(source: BinaryIO, size: int, worker_count: int) -> list[Chunk]:
    """Divide the source at LF boundaries, reading each crossed line at most once."""

    chunks = []
    start = 0
    for index in range(worker_count - 1):
        stop = size * (index + 1) // worker_count
        if stop <= start:
            stop = start
        else:
            source.seek(stop - 1)
            if source.read(1) != b"\n":
                while stop < size:
                    block = source.readline(min(size - stop, 128 * 1024))
                    if not block:
                        raise ImportFailure(
                            "input ended while finding a chunk boundary"
                        )
                    stop += len(block)
                    if block.endswith(b"\n"):
                        break
        chunks.append(Chunk(index, start, stop))
        start = stop
    chunks.append(Chunk(worker_count - 1, start, size))
    return chunks


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

    while batch := list(islice(source, min(batch_size, maxsize))):
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


def import_jsonl(
    input_path: Path,
    output_path: Path,
    batch_size: int,
    *,
    on_progress: Callable[[int, int], None] | None = None,
) -> None:
    """Import a local JSONL file into a fresh SQLite database.

    After a successful batch, on_progress receives the processed raw bytes and
    initial input size. The callback runs after the database commit.
    """

    if batch_size < 1:
        raise ImportFailure("batch size must be positive")

    try:
        with input_path.open("rb") as source:
            bytes_total = (
                fstat(source.fileno()).st_size if on_progress is not None else 0
            )
            bytes_processed = 0
            probe_attachment_limit()
            # Claim the destination exclusively before SQLite opens it.
            with output_path.open("xb"):
                pass
            with closing(sqlite3.connect(output_path.absolute())) as db:
                initialize_database(db)
                line_number = 0
                for batch_id, batch in enumerate(read_batches(source, batch_size), 1):
                    rows: RowsByTable = {table: [] for table in INSERTS}
                    for raw in batch:
                        line_number += 1
                        record = decode_record(raw, line_number)
                        try:
                            append_record_rows(record, line_number, rows)
                        except ValueError as exc:
                            raise ImportFailure(
                                f"invalid mapped value: {exc}", line_number
                            ) from exc
                    rows["batch_log"].append((batch_id, len(batch)))
                    write_batch(db, rows, batch_id)
                    if on_progress is not None:
                        bytes_processed += sum(map(len, batch))
                        on_progress(bytes_processed, bytes_total)
    except (OSError, sqlite3.Error) as exc:
        raise ImportFailure(str(exc)) from exc
