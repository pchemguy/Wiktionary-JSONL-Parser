"""Decode and write one byte range into a worker SQLite database."""

import json
import sqlite3
from collections.abc import Callable, Iterable, Iterator
from contextlib import closing
from dataclasses import dataclass
from itertools import islice
from pathlib import Path
from sys import maxsize
from typing import BinaryIO, NoReturn

from .editions import (
    BATCH_LOG_INSERT,
    Edition,
    RowsByTable,
    get_edition,
    initialize_database,
)


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


def require_unicode_collation(db: sqlite3.Connection) -> None:
    """Check that the connection provides the required SQLiteICUex collation."""

    try:
        db.execute("SELECT 'a' = 'A' COLLATE UTF_CI").fetchone()
    except sqlite3.OperationalError as exc:
        raise ImportFailure("SQLiteICUex must provide the UTF_CI collation") from exc


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


def write_batch(
    db: sqlite3.Connection,
    edition: Edition,
    rows_by_table: RowsByTable,
    batch_id: int,
    line_count: int,
) -> None:
    """Commit one batch atomically, including its log row."""

    try:
        db.execute("BEGIN")
        for table, sql in edition.inserts.items():
            if rows_by_table[table]:
                db.executemany(sql, rows_by_table[table])
        db.executemany(BATCH_LOG_INSERT, [(batch_id, line_count)])
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
    *,
    edition: Edition,
) -> None:
    """Write a staged worker database and report only committed byte counts."""

    try:
        with (
            input_path.open("rb") as source,
            closing(sqlite3.connect(output_path)) as db,
        ):
            initialize_database(db, edition)
            line_number = 0
            processed = 0
            skip_record = edition.skip_record
            batches = read_batches(read_chunk(source, chunk), batch_size)
            for batch_number, batch in enumerate(batches, 1):
                rows: RowsByTable = {table: [] for table in edition.inserts}
                for raw in batch:
                    line_number += 1
                    entry_id = chunk_key(chunk.index, line_number)
                    record = decode_record(
                        raw, line_number, bom_allowed=chunk.start == 0
                    )
                    if skip_record is not None and skip_record(record):
                        continue
                    try:
                        edition.map_record(record, entry_id, rows)
                    except ValueError as exc:
                        raise ImportFailure(
                            f"invalid mapped value: {exc}", line_number
                        ) from exc
                batch_id = chunk_key(chunk.index, batch_number)
                write_batch(db, edition, rows, batch_id, len(batch))
                if on_progress is not None:
                    processed += sum(map(len, batch))
                    on_progress(chunk.index, processed, chunk.stop - chunk.start)
    except ImportFailure as exc:
        raise ImportFailure(
            exc.detail, exc.line_number, stage="worker", chunk_index=chunk.index
        ) from exc
    except (OSError, sqlite3.Error) as exc:
        raise ImportFailure(str(exc), stage="worker", chunk_index=chunk.index) from exc


def main() -> int:
    """Run the private child-process entry point."""

    import sys

    source, output, index, start, stop, batch_size, identifier, progress = sys.argv[1:]
    chunk = Chunk(int(index), int(start), int(stop))

    def report(chunk_index: int, processed: int, total: int) -> None:
        print(json.dumps(["progress", processed, total]), flush=True)

    try:
        run_chunk(
            Path(source),
            Path(output),
            chunk,
            int(batch_size),
            report if progress == "1" else None,
            edition=get_edition(identifier),
        )
    except ImportFailure as exc:
        print(json.dumps(["failure", exc.detail, exc.line_number]), flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
