import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer, merge, worker
from wiktionary_jsonl_parser.editions import Edition
from wiktionary_jsonl_parser.editions.ru import RUSSIAN_EDITION

FIXTURE = Path(__file__).with_name("fixtures") / "all-tables.jsonl"


@pytest.mark.parametrize(("workers", "limit"), [(1, 0), (2, 1), (2, 2)])
def test_assemble(
    workers: int, limit: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(importer.os, "cpu_count", lambda: workers + 2)
    monkeypatch.setattr(importer, "probe_attachment_limit", lambda: limit)
    line = FIXTURE.read_bytes().splitlines()[0] + b"\n"
    source, output = tmp_path / "source", tmp_path / "output"
    source.write_bytes(line * 4)
    merge_calls = []
    attach = importer.merge_databases

    def observe(paths: list[Path], dest: Path, group: int, *, edition: Edition) -> None:
        merge_calls.append(group)
        assert edition is RUSSIAN_EDITION
        attach(paths, dest, group, edition=edition)

    monkeypatch.setattr(importer, "merge_databases", observe)
    importer.import_jsonl(source, output, 2)
    assert merge_calls == ([] if workers == 1 else [limit])
    with closing(sqlite3.connect(output)) as db:
        keys = [1, 2, 3, 4] if workers == 1 else [1, 2, 10_000_001, 10_000_002]
        assert [
            row[0] for row in db.execute("SELECT id FROM entries ORDER BY id")
        ] == keys
        assert [
            row[0]
            for row in db.execute("SELECT sense_entry_id FROM examples ORDER BY 1")
        ] == keys
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    assert sorted(path.name for path in tmp_path.iterdir()) == ["output", "source"]


def test_merge_uses_read_only_attachments_and_switches_groups(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.write_bytes(FIXTURE.read_bytes())
    size = source.stat().st_size
    paths = [tmp_path / f"source #%{i}.sqlite" for i in range(3)]
    for i, path in enumerate(paths):
        worker.run_chunk(
            source, path, worker.Chunk(i, 0, size), 2, edition=RUSSIAN_EDITION
        )
    before = [(p.stat().st_mtime_ns, p.read_bytes()) for p in paths]
    with closing(sqlite3.connect((tmp_path / "probe").as_uri(), uri=True)) as db:
        db.execute("ATTACH DATABASE ? AS source", (paths[0].as_uri() + "?mode=ro",))
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            db.execute("DELETE FROM source.entries")
    output = tmp_path / "merged"
    merge.merge_databases(paths, output, 2, edition=RUSSIAN_EDITION)
    assert before == [(p.stat().st_mtime_ns, p.read_bytes()) for p in paths]
    with closing(sqlite3.connect(output)) as db:
        assert db.execute("SELECT count(*) FROM entries").fetchone() == (9,)
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("failure", ["worker", "merge", "publication", "collision"])
def test_discard_staging_on_failure(
    failure: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(importer.os, "cpu_count", lambda: 4)
    source, output = tmp_path / "source", tmp_path / "output"
    data = FIXTURE.read_bytes()
    source.write_bytes(data if failure != "worker" else data + b"\ninvalid")

    def fail_merge(
        paths: list[Path], destination: Path, group: int, *, edition: Edition
    ) -> None:
        raise sqlite3.OperationalError("forced merge failure")

    def fail_link(staged: Path, destination: Path) -> None:
        if failure == "collision":
            destination.write_bytes(b"concurrent output")
            os_link(staged, destination)
        else:
            raise OSError("forced publication failure")

    os_link = importer.publish_database
    if failure == "merge":
        monkeypatch.setattr(importer, "merge_databases", fail_merge)
    if failure in {"publication", "collision"}:
        monkeypatch.setattr(importer, "publish_database", fail_link)
    stage = "publication" if failure == "collision" else failure
    with pytest.raises(importer.ImportFailure, match=stage):
        importer.import_jsonl(source, output, 2)
    if failure == "collision":
        assert output.read_bytes() == b"concurrent output"
    else:
        assert not output.exists()
    assert not list(tmp_path.glob(".wiktionary-import-*"))
