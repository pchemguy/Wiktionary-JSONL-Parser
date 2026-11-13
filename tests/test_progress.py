import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer
from wiktionary_jsonl_parser.cli import main, report_progress


def entry(word: str) -> bytes:
    return json.dumps(
        {"word": word, "lang": "Russian", "lang_code": "ru"}, ensure_ascii=False
    ).encode("utf-8")


def test_raw_counts_after_visible_writes(tmp_path: Path) -> None:
    source = tmp_path / "words.jsonl"
    first = b"\xef\xbb\xbf" + entry("\u0451\u0436") + b"\r\n"
    second = entry("second") + b"\n"
    third = entry("last")
    data = first + second + third
    source.write_bytes(data)
    dest = source.with_suffix(".sqlite")
    updates = []

    def observe(processed: int, total: int) -> None:
        with closing(sqlite3.connect(dest)) as db:
            records = db.execute("SELECT sum(line_count) FROM batch_log").fetchone()
        updates.append((processed, total, records[0]))

    importer.import_jsonl(source, dest, 2, on_progress=observe)
    assert updates == [(len(first + second), len(data), 2), (len(data), len(data), 3)]


def test_cli_progress_and_quiet(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "words.jsonl"
    line = entry("\u0410") + b"\n"
    size = len(line)
    source.write_bytes(line * 3)
    args = [str(source), "--batch-size", "2"]
    assert main(args) == 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err.splitlines() == [
        f"{size * 2}/{size * 3} bytes read and processed (66.6%)",
        f"{size * 3}/{size * 3} bytes read and processed (100.0%)",
    ]
    assert main([*args, "--output", str(tmp_path / "quiet.db"), "--no-progress"]) == 0
    assert capsys.readouterr() == ("", "")


def test_empty_import_is_silent(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "empty.jsonl"
    source.touch()
    assert main([str(source)]) == 0
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("failure", ["decode", "mapping", "write"])
def test_failed_batch_emits_only_prior_progress(
    failure: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "failure.jsonl"
    first = entry("ok") + b"\n"
    invalid = {"decode": b"invalid", "mapping": b"{}", "write": entry("reject")}
    source.write_bytes(first + invalid[failure])
    if failure == "write":
        initialize = importer.initialize_database

        def add_trigger(db: sqlite3.Connection) -> None:
            initialize(db)
            db.execute("""CREATE TRIGGER reject_log BEFORE INSERT ON batch_log
                WHEN NEW.batch_id = 2 BEGIN SELECT RAISE(ABORT, 'forced batch failure'); END""")

        monkeypatch.setattr(importer, "initialize_database", add_trigger)
    assert main([str(source), "--batch-size", "1"]) == 1
    lines = capsys.readouterr().err.splitlines()
    assert len(lines) == 2
    assert lines[0].startswith(
        f"{len(first)}/{source.stat().st_size} bytes read and processed"
    )
    assert lines[1].startswith("wiktionary-jsonl-parser: ")
    with closing(sqlite3.connect(source.with_suffix(".sqlite"))) as db:
        assert db.execute("SELECT * FROM batch_log").fetchall() == [(1, 1)]
    assert (
        main(
            [
                str(source),
                "--output",
                str(tmp_path / "quiet.db"),
                "--no-progress",
                "--batch-size",
                "1",
            ]
        )
        == 1
    )
    assert capsys.readouterr().err.splitlines() == [lines[1]]


def test_callback_defaults_to_silent(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "words.jsonl"
    source.write_bytes(entry("quiet"))
    importer.import_jsonl(source, source.with_suffix(".sqlite"), 1)
    assert capsys.readouterr() == ("", "")


def test_progress_output_is_flushed(monkeypatch: pytest.MonkeyPatch) -> None:
    class Stream:
        def __init__(self) -> None:
            self.flushed = False
            self.text = ""

        def write(self, data: str) -> int:
            self.text += data
            return len(data)

        def flush(self) -> None:
            self.flushed = True

    stream = Stream()
    monkeypatch.setattr(sys, "stderr", stream)
    report_progress(9999, 10000)
    assert stream.text == "9999/10000 bytes read and processed (99.9%)\n"
    assert stream.flushed
