import json
import sqlite3
from collections.abc import Callable
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer
from wiktionary_jsonl_parser.cli import main

pytestmark = pytest.mark.usefixtures("single_worker")


def write_entries(path: Path, *words: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as out:
        for word in words:
            print(
                json.dumps({"word": word, "lang": "Russian", "lang_code": "ru"}),
                file=out,
            )


def rows(path: Path, query: str) -> list[tuple[object, ...]]:
    with sqlite3.connect(path) as db:
        return db.execute(query).fetchall()


def test_sibling_database_and_short_batch(tmp_path: Path) -> None:
    source = tmp_path / "ru.extract.jsonl"
    write_entries(source, "a", "b", "a")
    assert main([str(source), "--batch-size", "2"]) == 0
    db = source.with_suffix(".sqlite")
    assert rows(db, "SELECT id, word FROM entries ORDER BY id") == [
        (1, "a"),
        (2, "b"),
        (3, "a"),
    ]
    assert rows(db, "SELECT * FROM batch_log ORDER BY batch_id") == [(1, 2), (2, 1)]


def test_empty_input_and_explicit_destination(tmp_path: Path) -> None:
    source = tmp_path / "empty.txt"
    source.touch()
    dest = tmp_path / "empty.db"
    assert main([str(source), "--output", str(dest)]) == 0
    assert rows(dest, "SELECT * FROM entries") == []
    assert rows(dest, "SELECT * FROM batch_log") == []


@pytest.mark.parametrize("size", ["0", "-1", "bad"])
def test_invalid_batch_size(size: str) -> None:
    with pytest.raises(SystemExit, match="2"):
        main(["input.jsonl", "--batch-size", size])


def test_missing_default_suffix() -> None:
    with pytest.raises(SystemExit, match="2"):
        main(["input.txt"])


def test_default_batch_size(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def invoke(
        input_path: Path,
        output_path: Path,
        batch_size: int,
        *,
        on_progress: Callable[[int, int, int], None] | None,
        on_warning: Callable[[str], None],
        confirm_single_worker: Callable[[], bool],
    ) -> None:
        assert on_progress is not None
        assert input_path == tmp_path / "in.jsonl"
        assert output_path == tmp_path / "in.sqlite"
        assert batch_size == 10_000

    monkeypatch.setattr("wiktionary_jsonl_parser.cli.import_jsonl", invoke)
    assert main([str(tmp_path / "in.jsonl")]) == 0


def test_missing_input_and_existing_destination(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "in.jsonl"
    dest = source.with_suffix(".sqlite")
    assert main([str(source)]) == 1
    assert not dest.exists()
    assert str(source) in capsys.readouterr().err
    write_entries(source, "a")
    dest.write_bytes(b"existing")
    assert main([str(source)]) == 1
    assert dest.read_bytes() == b"existing"
    assert "exists" in capsys.readouterr().err


def test_missing_collation_leaves_no_destination(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with sqlite3.connect(":memory:") as db:
        if any(name == "UTF_CI" for _, name in db.execute("PRAGMA collation_list")):
            pytest.skip("run with standard SQLite to exercise missing UTF_CI")
    source = tmp_path / "in.jsonl"
    write_entries(source, "a")
    assert main([str(source)]) == 1
    assert not source.with_suffix(".sqlite").exists()
    assert "SQLiteICUex" in capsys.readouterr().err


def test_decode_failure_leaves_no_destination(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "in.jsonl"
    write_entries(source, "a", "b", "c")
    with source.open("ab") as stream:
        stream.write(b"invalid\n")
    assert main([str(source), "--batch-size", "2"]) == 1
    assert "line 4" in capsys.readouterr().err
    assert not source.with_suffix(".sqlite").exists()


def test_literal_memory_filename_is_on_disk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import os

    if os.name == "nt":
        pytest.skip("Windows filenames cannot contain a colon")
    monkeypatch.chdir(tmp_path)
    source = Path("input.jsonl")
    write_entries(source, "on disk")
    assert main([str(source), "--output", ":memory:"]) == 0
    assert rows(tmp_path / ":memory:", "SELECT word FROM entries") == [("on disk",)]


@pytest.mark.parametrize("answer", ["yes", "no", "eof", "noninteractive"])
def test_zero_limit_cli_confirmation(
    answer: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import sys
    from io import StringIO

    class Input(StringIO):
        def isatty(self) -> bool:
            return answer != "noninteractive"

    monkeypatch.setattr(importer.os, "cpu_count", lambda: 5)
    monkeypatch.setattr(importer, "probe_attachment_limit", lambda: 0)
    monkeypatch.setattr(sys, "stdin", Input("" if answer == "eof" else answer + "\n"))
    source = tmp_path / "words.jsonl"
    write_entries(source, "a")
    output = source.with_suffix(".sqlite")
    assert main([str(source), "--no-progress"]) == (0 if answer == "yes" else 1)
    assert output.exists() == (answer == "yes")
    out, err = capsys.readouterr()
    assert out == ""
    assert "requested 3 workers but SQLite allows 0 attachments" in err
    assert ("Run with one worker?" in err) == (answer != "noninteractive")
    assert "bytes read and processed" not in err
    if answer == "yes":
        assert rows(output, "SELECT id, word FROM entries") == [(1, "a")]
    else:
        assert "requires explicit confirmation" in err


@pytest.mark.parametrize("callback", ["warning", "confirmation", "progress"])
def test_library_callback_failure_aborts(
    callback: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(importer.os, "cpu_count", lambda: 5)
    monkeypatch.setattr(
        importer, "probe_attachment_limit", lambda: 0 if callback != "progress" else 10
    )
    source, destination = tmp_path / "input", tmp_path / "output"
    write_entries(source, "a", "b", "c")

    def fail(*args: object) -> None:
        raise RuntimeError("consumer failed")

    callbacks = {
        "warning": {"on_warning": fail},
        "confirmation": {"confirm_single_worker": fail},
        "progress": {"on_progress": fail},
    }
    with pytest.raises(importer.ImportFailure, match="consumer failed"):
        importer.import_jsonl(source, destination, **callbacks[callback])  # type: ignore[arg-type]
    assert not destination.exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["input"]
