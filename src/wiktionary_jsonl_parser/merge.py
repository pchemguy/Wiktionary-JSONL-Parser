"""Assemble completed worker databases without changing their stored keys."""

import sqlite3
from contextlib import closing
from pathlib import Path

from .editions import Edition, initialize_database


def merge_databases(
    sources: list[Path], output: Path, group_size: int, *, edition: Edition
) -> None:
    """Copy one group at a time into the staged output database."""

    with closing(sqlite3.connect(output.as_uri(), uri=True)) as db:
        initialize_database(db, edition)
        for offset in range(0, len(sources), group_size):
            group = sources[offset : offset + group_size]
            aliases = [f"worker_{i}" for i in range(len(group))]
            for alias, source in zip(aliases, group, strict=True):
                db.execute(
                    f"ATTACH DATABASE ? AS {alias}", (source.as_uri() + "?mode=ro",)
                )
            with db:
                db.execute("BEGIN")
                for table in (*edition.inserts, "batch_log"):
                    copies = " UNION ALL ".join(
                        f"SELECT * FROM {alias}.{table}" for alias in aliases
                    )
                    db.execute(f"INSERT INTO main.{table} {copies}")
            for alias in aliases:
                db.execute(f"DETACH DATABASE {alias}")
