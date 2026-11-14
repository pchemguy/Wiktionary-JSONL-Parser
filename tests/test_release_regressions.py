import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

import pytest

from wiktionary_jsonl_parser import importer
from wiktionary_jsonl_parser.cli import main

LINE = b'{"word":"one","lang":"Russian","lang_code":"ru"}\n'


def test_fresh_worker_uses_callers_package(tmp_path: Path) -> None:
    shadow = tmp_path / "wiktionary_jsonl_parser"
    shadow.mkdir()
    (shadow / "__init__.py").write_text("raise SystemExit(29)\n", encoding="ascii")
    (tmp_path / "in.jsonl").write_bytes(LINE)
    parent_package = Path(importer.__file__).resolve().parents[1]
    subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import sys; sys.path.insert(0, sys.argv[1]); "
            "from wiktionary_jsonl_parser.importer import import_jsonl; "
            "import_jsonl('in.jsonl', 'out.sqlite')",
            str(parent_package),
        ],
        cwd=tmp_path,
        check=True,
    )
    with closing(sqlite3.connect(tmp_path / "out.sqlite")) as db:
        assert db.execute("SELECT word FROM entries").fetchall() == [("one",)]


@pytest.mark.parametrize("error", [ProcessLookupError, PermissionError])
def test_cancel_reaps_siblings_despite_termination_error(
    error: type[OSError],
) -> None:
    first = Mock()
    first.poll.return_value = None
    first.terminate.side_effect = error("injected terminate failure")
    if error is PermissionError:
        first.wait.side_effect = [subprocess.TimeoutExpired("worker", 3), 0]
    sibling = Mock()
    sibling.poll.return_value = None
    if error is PermissionError:
        with pytest.raises(ExceptionGroup, match="worker cleanup"):
            importer.cancel_workers({0: first, 1: sibling}, {})
        first.kill.assert_called_once()
    else:
        importer.cancel_workers({0: first, 1: sibling}, {})
    first.wait.assert_called()
    first.stdout.close.assert_called_once()
    sibling.terminate.assert_called_once()
    sibling.wait.assert_called_once()
    sibling.stdout.close.assert_called_once()


def test_cleanup_error_after_publication_preserves_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    single_worker: None,
) -> None:
    source = tmp_path / "source.jsonl"
    source.write_bytes(LINE)
    cleanup = TemporaryDirectory.cleanup

    def cleanup_fails(self: TemporaryDirectory[str]) -> None:
        cleanup(self)
        raise PermissionError("forced cleanup error")

    monkeypatch.setattr(TemporaryDirectory, "cleanup", cleanup_fails)
    assert main([str(source), "--no-progress"]) == 0
    assert "forced cleanup error" in capsys.readouterr().err
    with closing(sqlite3.connect(source.with_suffix(".sqlite"))) as db:
        assert db.execute("SELECT word FROM entries").fetchall() == [("one",)]


@pytest.mark.parametrize(
    ("relative_parent", "expected_parent"),
    [
        pytest.param("a/sym", "b/inside", id="symlinked-parent"),
        pytest.param(
            "a/sym/../write",
            "b/write",
            marks=pytest.mark.skipif(
                sys.platform == "win32",
                reason="this traversal regression uses POSIX symlink semantics",
            ),
            id="parent-after-symlink",
        ),
    ],
)
def test_stage_is_created_under_resolved_destination_parent(
    tmp_path: Path,
    single_worker: None,
    relative_parent: str,
    expected_parent: str,
) -> None:
    for name in ("a/write", "b/write", "b/inside"):
        (tmp_path / name).mkdir(parents=True)
    try:
        (tmp_path / "a/sym").symlink_to(tmp_path / "b/inside", target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"cannot create test symlink: {exc}")
    source = tmp_path / "in.jsonl"
    source.write_bytes(LINE)
    importer.import_jsonl(source, tmp_path / relative_parent / "out.sqlite")
    assert [p.name for p in (tmp_path / expected_parent).iterdir()] == ["out.sqlite"]
    assert list((tmp_path / "a/write").iterdir()) == []
    assert not list(tmp_path.rglob(".wiktionary-import-*"))


def test_unbounded_library_batch_size_can_process_a_small_file(
    tmp_path: Path,
    single_worker: None,
) -> None:
    source = tmp_path / "in.jsonl"
    source.write_bytes(LINE * 2)
    output = tmp_path / "out.sqlite"
    importer.import_jsonl(source, output, 10**10_000)
    with closing(sqlite3.connect(output)) as db:
        assert db.execute("SELECT batch_id, line_count FROM batch_log").fetchall() == [
            (1, 2)
        ]
