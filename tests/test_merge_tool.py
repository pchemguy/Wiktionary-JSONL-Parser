import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from tools import merge_databases as tool

from wiktionary_jsonl_parser.editions import Edition
from wiktionary_jsonl_parser.editions.ru import RUSSIAN_EDITION
from wiktionary_jsonl_parser.worker import Chunk, run_chunk

SOURCE = Path(__file__).with_name("fixtures") / "all-tables.jsonl"


@pytest.mark.parametrize("failure", [None, "duplicate", "collision"])
def test_manual_merge_publishes_only_the_completed_output(
    failure: str | None, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "merged.sqlite"
    inputs = [tmp_path / f"part-{i}.sqlite" for i in range(2)]
    for i, part in enumerate(inputs):
        chunk = Chunk(0 if failure == "duplicate" else i, 0, SOURCE.stat().st_size)
        run_chunk(SOURCE, part, chunk, 2, edition=RUSSIAN_EDITION)
    originals = [part.read_bytes() for part in inputs]

    initialize = tool.initialize_database

    def during_merge(db: sqlite3.Connection, edition: Edition) -> None:
        assert not destination.exists(), "destination exposed during schema creation"
        initialize(db, edition)
        if failure == "collision":
            destination.write_bytes(b"concurrent output")

    monkeypatch.setattr(tool, "initialize_database", during_merge)
    if failure == "duplicate":
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE constraint failed"):
            tool.merge_databases(destination, inputs)
        assert not destination.exists()
    elif failure == "collision":
        with pytest.raises(FileExistsError):
            tool.merge_databases(destination, inputs)
        assert destination.read_bytes() == b"concurrent output"
    else:
        counts = tool.merge_databases(destination, inputs)
        assert counts["entries"] == 6
        with closing(sqlite3.connect(destination)) as db:
            assert db.execute("SELECT id FROM entries ORDER BY id").fetchall() == [
                (1,),
                (2,),
                (3,),
                (10_000_001,),
                (10_000_002,),
                (10_000_003,),
            ]
            assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    assert [part.read_bytes() for part in inputs] == originals
    assert sorted(tmp_path.iterdir()) == sorted(
        [*inputs, destination] if failure != "duplicate" else inputs
    )
