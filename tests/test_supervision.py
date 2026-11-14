import sqlite3
import subprocess
import sys
import threading
from contextlib import closing
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer

LINE = b'{"word":"a","lang":"Russian","lang_code":"ru"}\n'


def test_fresh_workers_report_progress_to_the_importing_thread(tmp_path: Path) -> None:
    source = tmp_path / "input"
    source.write_bytes(LINE * 4)
    paths = [tmp_path / "db0", tmp_path / "db1"]
    chunk_size = len(LINE) * 2
    chunks = [
        importer.Chunk(0, 0, chunk_size),
        importer.Chunk(1, chunk_size, 2 * chunk_size),
    ]
    updates = []
    owner = threading.get_ident()

    def progress(chunk: int, done: int, total: int) -> None:
        assert threading.get_ident() == owner
        updates.append((chunk, done, total))

    importer.run_workers(source, paths, chunks, 1, progress, edition_id="ru")
    assert sorted(updates) == [
        (i, done, chunk_size) for i in range(2) for done in (len(LINE), chunk_size)
    ]
    for i, path in enumerate(paths):
        with closing(sqlite3.connect(path)) as db:
            assert db.execute("SELECT id FROM entries ORDER BY id").fetchall() == [
                (i * 10_000_000 + 1,),
                (i * 10_000_000 + 2,),
            ]


@pytest.mark.parametrize("unexpected", [False, True])
def test_failed_worker_stops_and_reaps_sibling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, unexpected: bool
) -> None:
    source = tmp_path / "input"
    source.write_bytes(b"bad\n" + LINE)
    paths = [tmp_path / "bad", tmp_path / "slow"]
    chunks = [importer.Chunk(0, 0, 4), importer.Chunk(1, 4, 4 + len(LINE))]
    launch = subprocess.Popen
    started: list[subprocess.Popen[str]] = []

    def inject(args: list[str], **kwargs: object) -> subprocess.Popen[str]:
        assert args[-2] == "ru"
        if args[-1] == "1":
            pytest.fail("progress must be disabled for this supervision test")
        if len(started) == 1:
            args = [sys.executable, "-c", "import time; time.sleep(30)"]
        elif unexpected:
            args = [sys.executable, "-c", "raise SystemExit(15)"]
        process = launch(args, **kwargs)  # type: ignore[arg-type,call-overload]
        started.append(process)
        return process

    monkeypatch.setattr(importer.subprocess, "Popen", inject)
    match = "chunk 0.*status 15" if unexpected else "chunk 0.*line 1.*JSONL"
    with pytest.raises(importer.ImportFailure, match=match):
        importer.run_workers(source, paths, chunks, 2, None, edition_id="ru")
    assert len(started) == 2
    assert all(
        p.returncode is not None and p.stdout and p.stdout.closed for p in started
    )
