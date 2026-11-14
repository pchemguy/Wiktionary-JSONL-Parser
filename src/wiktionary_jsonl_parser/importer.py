"""Read Wiktionary JSONL and persist source-line batches to SQLite."""

import json
import os
import sqlite3
import subprocess
import sys
from collections.abc import Callable
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from tempfile import TemporaryDirectory
from threading import Thread
from typing import BinaryIO

from .editions import get_edition
from .merge import merge_databases
from .worker import (
    Chunk,
    ImportFailure as ImportFailure,
    Progress,
    require_unicode_collation,
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


WorkerEvents = Queue[tuple[int, str | int | ImportFailure]]


def drain_worker(
    index: int, child: subprocess.Popen[str], events: WorkerEvents
) -> None:
    """Forward child output while the importing thread handles callbacks."""

    assert child.stdout is not None
    try:
        with child.stdout:
            for line in child.stdout:
                events.put((index, line))
        events.put((index, child.wait()))
    except Exception as exc:
        events.put((index, ImportFailure(str(exc), stage="worker", chunk_index=index)))


def cancel_workers(
    children: dict[int, subprocess.Popen[str]], readers: list[Thread]
) -> None:
    for child in children.values():
        if child.poll() is None:
            child.terminate()
    for child in children.values():
        try:
            child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
    for reader in readers:
        reader.join()
    for child in children.values():
        if child.stdout is not None:
            child.stdout.close()


def run_workers(
    source: Path,
    outputs: list[Path],
    chunks: list[Chunk],
    batch_size: int,
    on_progress: Progress | None,
    *,
    edition_id: str,
) -> None:
    """Start fresh Python interpreters and reap them before returning."""

    children: dict[int, subprocess.Popen[str]] = {}
    readers: list[Thread] = []
    events: WorkerEvents = Queue()
    try:
        for chunk, output in zip(chunks, outputs, strict=True):
            try:
                child = subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "wiktionary_jsonl_parser.worker",
                        str(source),
                        str(output),
                        str(chunk.index),
                        str(chunk.start),
                        str(chunk.stop),
                        str(batch_size),
                        edition_id,
                        "1" if on_progress is not None else "0",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    errors="replace",
                )
                children[chunk.index] = child
                reader = Thread(target=drain_worker, args=(chunk.index, child, events))
                reader.start()
                readers.append(reader)
            except (OSError, RuntimeError) as exc:
                raise ImportFailure(
                    f"cannot start worker: {exc}",
                    stage="worker",
                    chunk_index=chunk.index,
                ) from exc

        remaining = len(children)
        diagnostics: dict[int, str] = {}
        while remaining:
            index, event = events.get()
            if isinstance(event, ImportFailure):
                raise event
            if isinstance(event, int):
                if event:
                    details = diagnostics.get(index)
                    message = f"exited with status {event}"
                    if details:
                        message += f": {details}"
                    raise ImportFailure(message, stage="worker", chunk_index=index)
                remaining -= 1
                continue
            try:
                message = json.loads(event)
            except (ValueError, RecursionError):
                diagnostics[index] = event.strip()[-1000:]
                continue
            match message:
                case ["progress", int(processed), int(total)]:
                    if on_progress is not None:
                        on_progress(index, processed, total)
                case ["failure", str(detail), line]:
                    raise ImportFailure(detail, line, stage="worker", chunk_index=index)
                case _:
                    diagnostics[index] = event.strip()[-1000:]
    except BaseException as exc:
        try:
            cancel_workers(children, readers)
        except Exception as cleanup:
            exc.add_note(f"worker cleanup: {cleanup}")
        raise
    else:
        for reader in readers:
            reader.join()


def import_jsonl(
    input_path: str | Path,
    output_path: str | Path,
    batch_size: int = 10_000,
    *,
    on_warning: Callable[[str], None] | None = None,
    confirm_single_worker: Callable[[], bool] | None = None,
    on_progress: Progress | None = None,
) -> None:
    """Import local JSONL through staged worker databases into a new file."""

    if (
        not isinstance(batch_size, int)
        or isinstance(batch_size, bool)
        or batch_size < 1
    ):
        raise ImportFailure("batch size must be a positive integer", stage="bootstrap")
    stage = "bootstrap"
    staging: TemporaryDirectory[str] | None = None
    try:
        edition = get_edition("ru")
        source_path = Path(input_path).absolute()
        destination = Path(output_path).absolute()
        with source_path.open("rb") as source:
            if os.path.lexists(destination):
                raise FileExistsError(f"output already exists: {destination}")
            if not destination.parent.is_dir():
                raise NotADirectoryError(
                    f"output directory does not exist: {destination.parent}"
                )
            limit = probe_attachment_limit()
            plan = plan_run(os.cpu_count(), limit, on_warning, confirm_single_worker)
            stage = "partition"
            chunks = partition_source(
                source, os.fstat(source.fileno()).st_size, plan.worker_count
            )
        stage = "staging"
        staging = TemporaryDirectory(
            prefix=".wiktionary-import-", dir=destination.parent
        )
        root = Path(staging.name)
        outputs = [root / f"worker-{chunk.index}.sqlite" for chunk in chunks]

        stage = "workers"
        run_workers(
            source_path,
            outputs,
            chunks,
            batch_size,
            on_progress,
            edition_id=edition.identifier,
        )

        staged_output = outputs[0]
        if plan.worker_count > 1:
            stage = "merge"
            staged_output = root / "merged.sqlite"
            merge_databases(
                outputs, staged_output, plan.merge_group_size, edition=edition
            )

        stage = "publication"
        publish_database(staged_output, destination)
    except BaseException as exc:
        if staging is not None:
            try:
                staging.cleanup()
            except OSError as cleanup:
                exc.add_note(f"staging cleanup: {cleanup}")
        if isinstance(exc, ImportFailure) and exc.stage is not None:
            raise
        if isinstance(exc, Exception):
            failure = ImportFailure(str(exc), stage=stage)
            for note in getattr(exc, "__notes__", ()):
                failure.add_note(note)
            raise failure from exc
        raise
    else:
        assert staging is not None
        staging.cleanup()


def publish_database(staged: Path, destination: Path) -> None:
    """Make a closed database visible atomically without replacing a destination."""

    if os.name == "nt":
        os.rename(staged, destination)
    else:
        os.link(staged, destination)
