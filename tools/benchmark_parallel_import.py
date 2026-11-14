"""Benchmark independent SQLite importer workers on one local JSONL file."""

import argparse
import os
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter, sleep

from merge_databases import merge_databases

from wiktionary_jsonl_parser.cli import report_progress
from wiktionary_jsonl_parser.editions.ru import RUSSIAN_EDITION
from wiktionary_jsonl_parser.worker import (
    Chunk,
    ImportFailure,
    require_unicode_collation,
    run_chunk,
)

BATCH_SIZE = 10_000


def chunk_bounds(path: Path, workers: int) -> list[int]:
    """Find contiguous ranges that begin and end at JSONL line boundaries."""
    with path.open("rb") as source:
        size = os.fstat(source.fileno()).st_size
        bounds = [0]
        for index in range(1, workers):
            boundary = size * index // workers
            if boundary > bounds[-1]:
                source.seek(boundary - 1)
                if source.read(1) != b"\n":
                    source.readline()
                bounds.append(source.tell())
            else:
                bounds.append(bounds[-1])
        return [*bounds, size]


def run_workers(source: Path, bounds: list[int], outputs: list[Path]) -> None:
    """Start independent workers and terminate any that remain after failure."""
    running: dict[int, subprocess.Popen[bytes]] = {}
    try:
        for index, output in enumerate(outputs):
            running[index] = subprocess.Popen(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--worker",
                    str(source),
                    str(output),
                    str(index),
                    str(bounds[index]),
                    str(bounds[index + 1]),
                ]
            )
        while running:
            for index, process in list(running.items()):
                status = process.poll()
                if status is None:
                    continue
                if status:
                    raise ImportFailure(f"chunk {index} exited with status {status}")
                del running[index]
            if running:
                sleep(0.01)
    finally:
        for process in running.values():
            if process.poll() is None:
                process.terminate()
        for process in running.values():
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def benchmark(source: Path, output: Path) -> None:
    """Time partitioning, workers, and publication of one merged output."""
    cpu_count = os.cpu_count()
    if cpu_count is None or cpu_count <= 2:
        raise ValueError("benchmark requires more than two logical CPUs")
    workers = cpu_count - 2
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    source = source.resolve(strict=True)
    with closing(sqlite3.connect(":memory:")) as db:
        require_unicode_collation(db)
        if workers > db.getlimit(sqlite3.SQLITE_LIMIT_ATTACHED):
            raise ValueError(
                "worker count exceeds this SQLite build's attachment limit"
            )

    with TemporaryDirectory(prefix="parallel-import-", dir=output.parent) as directory:
        started = perf_counter()
        bounds = chunk_bounds(source, workers)
        paths = [Path(directory) / f"chunk-{i}.sqlite" for i in range(workers)]
        partitioned = perf_counter()
        run_workers(source, bounds, paths)
        imported = perf_counter()
        staged = Path(directory) / "merged.sqlite"
        counts = merge_databases(staged, paths)
        if os.name == "nt":
            # Windows rename refuses to replace an existing destination.
            staged.rename(output)
        else:
            os.link(staged, output)
        merged = perf_counter()

    finished = perf_counter()
    elapsed = finished - started
    print(f"Workers: {workers}")
    print(f"Chunk bytes: {[b - a for a, b in zip(bounds, bounds[1:], strict=False)]}")
    print(f"Partition: {partitioned - started:.6f} s")
    print(f"Worker import wall time: {imported - partitioned:.6f} s")
    print(f"Merge and publication: {merged - imported:.6f} s")
    print(f"Cleanup: {finished - merged:.6f} s")
    print(f"Total: {elapsed:.6f} s")
    print(f"Input MiB/s: {bounds[-1] / 2**20 / elapsed:.3f}")
    print(f"Input lines/s: {counts['entries'] / elapsed:.2f}")
    print(f"Merged rows: {sum(counts.values())}")


def main() -> int:
    """Execute the benchmark or one internal worker invocation."""
    if sys.argv[1:2] == ["--worker"]:
        _, _, source, output, index, first, stop = sys.argv
        try:
            run_chunk(
                Path(source),
                Path(output),
                Chunk(int(index), int(first), int(stop)),
                BATCH_SIZE,
                report_progress,
                edition=RUSSIAN_EDITION,
            )
        except (ImportFailure, OSError, sqlite3.Error) as exc:
            print(exc, file=sys.stderr, flush=True)
            return 1
        return 0

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="local uncompressed entry-only JSONL")
    parser.add_argument("output", type=Path, help="new destination SQLite database")
    args = parser.parse_args()
    try:
        benchmark(args.source, args.output)
    except (ImportFailure, OSError, sqlite3.Error, ValueError) as exc:
        parser.exit(1, f"{parser.prog}: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
