"""Merge importer databases with globally unique IDs using SQLite UNION ALL."""

import argparse
import os
import sqlite3
from collections.abc import Sequence
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

from wiktionary_jsonl_parser.editions import initialize_database
from wiktionary_jsonl_parser.editions.ru import RUSSIAN_EDITION
from wiktionary_jsonl_parser.importer import publish_database
from wiktionary_jsonl_parser.worker import ImportFailure, require_unicode_collation


def schema_signature(db: sqlite3.Connection, schema: str) -> list[tuple[str, str, str]]:
    """Read the schema definition, excluding SQLite's internal objects."""
    return db.execute(
        f"SELECT type, name, sql FROM {schema}.sqlite_schema "
        "WHERE name NOT GLOB 'sqlite_*' ORDER BY type, name"
    ).fetchall()


def merge_databases(output: Path, sources: Sequence[Path]) -> dict[str, int]:
    """Copy importer databases with already-disjoint entry and batch IDs."""

    source_uris = [path.resolve(strict=True).as_uri() + "?mode=ro" for path in sources]
    if not source_uris:
        raise ValueError("at least one source database is required")
    if len(set(source_uris)) != len(source_uris):
        raise ValueError("source database paths must be distinct")

    with closing(sqlite3.connect(":memory:")) as probe:
        require_unicode_collation(probe)
    if os.path.lexists(output):
        raise FileExistsError(f"output already exists: {output}")
    destination = output.parent.resolve(strict=True) / output.name
    with TemporaryDirectory(
        prefix=".wiktionary-merge-", dir=destination.parent
    ) as directory:
        staged = Path(directory) / "merged.sqlite"
        with closing(sqlite3.connect(staged.as_uri(), uri=True)) as db:
            initialize_database(db, RUSSIAN_EDITION)
            expected_schema = schema_signature(db, "main")
            attachments = []
            for index, uri in enumerate(source_uris, start=1):
                name = f"source_{index}"
                db.execute(f"ATTACH DATABASE ? AS {name}", (uri,))
                if schema_signature(db, name) != expected_schema:
                    raise ValueError(f"schema mismatch: {sources[index - 1]}")
                attachments.append(name)

            counts = {}
            with db:
                db.execute("BEGIN")
                # The importer table order puts all parent rows before dependents.
                for table in (*RUSSIAN_EDITION.inserts, "batch_log"):
                    columns = ", ".join(
                        f'"{column[1]}"'
                        for column in db.execute(f'PRAGMA main.table_info("{table}")')
                    )
                    union = " UNION ALL ".join(
                        f'SELECT {columns} FROM {name}."{table}"'
                        for name in attachments
                    )
                    cursor = db.execute(
                        f'INSERT INTO main."{table}" ({columns}) {union}'
                    )
                    counts[table] = cursor.rowcount
        publish_database(staged, destination)
    return counts


def main(argv: Sequence[str] | None = None) -> int:
    """Run a timed merge into a new SQLite file."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new destination database")
    parser.add_argument(
        "sources", type=Path, nargs="+", help="pre-keyed input databases"
    )
    args = parser.parse_args(argv)
    start = perf_counter()
    try:
        counts = merge_databases(args.output, args.sources)
    except (ImportFailure, OSError, ValueError, sqlite3.Error) as exc:
        parser.exit(1, f"{parser.prog}: {exc}\n")
    elapsed = perf_counter() - start
    print(f"Merged {sum(counts.values()):,} rows in {elapsed:.3f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
