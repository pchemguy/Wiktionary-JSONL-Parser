import json
import os
import sys
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer
from wiktionary_jsonl_parser.cli import main, report_progress

pytestmark = pytest.mark.usefixtures("single_worker")


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

    caller_pid = os.getpid()

    def observe(chunk: int, processed: int, total: int) -> None:
        assert not dest.exists()
        assert os.getpid() == caller_pid
        updates.append((chunk, processed, total))

    importer.import_jsonl(source, dest, 2, on_progress=observe)
    assert updates == [(0, len(first + second), len(data)), (0, len(data), len(data))]


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
        f"[chunk 0] {size * 2}/{size * 3} bytes read and processed (66.6%)",
        f"[chunk 0] {size * 3}/{size * 3} bytes read and processed (100.0%)",
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


@pytest.mark.parametrize("failure", ["decode", "mapping"])
def test_failed_batch_emits_only_prior_progress(
    failure: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source = tmp_path / "failure.jsonl"
    first = entry("ok") + b"\n"
    invalid = {"decode": b"invalid", "mapping": b"{}"}
    source.write_bytes(first + invalid[failure])
    assert main([str(source), "--batch-size", "1"]) == 1
    lines = capsys.readouterr().err.splitlines()
    assert len(lines) == 2
    assert lines[0].startswith(
        f"[chunk 0] {len(first)}/{source.stat().st_size} bytes read and processed"
    )
    assert lines[1].startswith("wiktionary-jsonl-parser: ")
    assert not source.with_suffix(".sqlite").exists()
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
    report_progress(2, 9999, 10000)
    assert stream.text == "[chunk 2] 9999/10000 bytes read and processed (99.9%)\n"
    assert stream.flushed
