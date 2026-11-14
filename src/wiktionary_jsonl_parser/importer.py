"""Read Wiktionary JSONL and persist source-line batches to SQLite."""

import sqlite3
from collections.abc import Callable
from contextlib import closing
from dataclasses import dataclass
from os import fstat
from pathlib import Path
from typing import BinaryIO

from .mapping import RowsByTable, append_record_rows
from .worker import (
    INSERTS,
    Chunk as Chunk,
    ImportFailure as ImportFailure,
    decode_record as decode_record,
    initialize_database as initialize_database,
    read_batches as read_batches,
    require_unicode_collation as require_unicode_collation,
    schema_sql as schema_sql,
    write_batch,
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
