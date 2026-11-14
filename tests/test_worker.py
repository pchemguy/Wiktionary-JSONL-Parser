import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import worker
from wiktionary_jsonl_parser.editions import Edition
from wiktionary_jsonl_parser.editions.ru import RUSSIAN_EDITION

FIXTURE = Path(__file__).with_name("fixtures") / "all-tables.jsonl"
RECORD = b'{"word":"duplicate","lang":"Russian","lang_code":"ru"}'


def test_worker_keys_and_committed_progress(tmp_path: Path) -> None:
    source = tmp_path / "source"
    first = FIXTURE.read_bytes().splitlines()[0] + b"\r\n"
    second = RECORD + b"\n"
    prefix = b"another chunk\n"
    data = first + second + RECORD
    source.write_bytes(prefix + data + b"\nother chunk\n")
    db = tmp_path / "worker"
    updates = []

    def progress(chunk: int, done: int, total: int) -> None:
        with closing(sqlite3.connect(db)) as connection:
            lines = connection.execute("SELECT sum(line_count) FROM batch_log")
            updates.append((chunk, done, total, lines.fetchone()[0]))

    worker.run_chunk(
        source,
        db,
        worker.Chunk(2, len(prefix), len(prefix + data)),
        2,
        progress,
        edition=RUSSIAN_EDITION,
    )
    assert updates == [
        (2, len(first + second), len(data), 2),
        (2, len(data), len(data), 3),
    ]
    with closing(sqlite3.connect(db)) as connection:
        assert connection.execute("SELECT id FROM entries ORDER BY id").fetchall() == [
            (20_000_001,),
            (20_000_002,),
            (20_000_003,),
        ]
        assert connection.execute(
            "SELECT count(*) FROM entries WHERE word='duplicate'"
        ).fetchone() == (2,)
        assert connection.execute("SELECT sense_entry_id FROM examples").fetchall() == [
            (20_000_001,)
        ]
        assert connection.execute("SELECT * FROM batch_log ORDER BY 1").fetchall() == [
            (20_000_001, 2),
            (20_000_002, 1),
        ]
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []


def test_noninitial_bom_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "source"
    records = RECORD + b"\n" + b"\xef\xbb\xbf" + RECORD
    source.write_bytes(records)
    start = len(RECORD) + 1
    with pytest.raises(worker.ImportFailure, match="chunk 1.*line 1.*JSONL"):
        worker.run_chunk(
            source,
            tmp_path / "db",
            worker.Chunk(1, start, len(records)),
            2,
            edition=RUSSIAN_EDITION,
        )


def test_worker_id_boundaries() -> None:
    assert worker.chunk_key(1, 10_000_000) == 20_000_000
    with pytest.raises(worker.ImportFailure, match="10000000|10,000,000"):
        worker.chunk_key(1, 10_000_001)
    limit = (1 << 63) - 1
    index, line = divmod(limit, 10_000_000)
    assert worker.chunk_key(index, line) == limit
    with pytest.raises(worker.ImportFailure, match="SQLite integer"):
        worker.chunk_key(index, line + 1)


def test_worker_rolls_back_and_suppresses_failed_progress(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    setup = worker.initialize_database

    def reject_last_log(db: sqlite3.Connection, edition: Edition) -> None:
        setup(db, edition)
        db.execute("""CREATE TRIGGER reject_log BEFORE INSERT ON batch_log
            WHEN NEW.batch_id = 10000002 BEGIN SELECT RAISE(ABORT, 'forced'); END""")

    monkeypatch.setattr(worker, "initialize_database", reject_last_log)
    source, output = tmp_path / "source", tmp_path / "out"
    source.write_bytes((RECORD + b"\n") * 2)
    size = source.stat().st_size
    updates = []
    with pytest.raises(worker.ImportFailure, match="chunk 1.*batch 10000002.*forced"):
        worker.run_chunk(
            source,
            output,
            worker.Chunk(1, 0, size),
            1,
            lambda chunk, done, total: updates.append((chunk, done, total)),
            edition=RUSSIAN_EDITION,
        )
    assert updates == [(1, size // 2, size)]
    with closing(sqlite3.connect(output)) as db:
        assert db.execute("SELECT id FROM entries").fetchall() == [(10_000_001,)]
        assert db.execute("SELECT * FROM batch_log").fetchall() == [(10_000_001, 1)]
