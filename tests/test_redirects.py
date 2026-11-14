import json
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer, worker
from wiktionary_jsonl_parser.editions.ru import RUSSIAN_EDITION

REDIRECT = b'{"title":"old","redirect":"new","pos":"hard-redirect"}\n'
ENTRY = b'{"word":"new","lang":"Russian","lang_code":"ru","forms":[{"form":"new"}]}\n'


@pytest.mark.parametrize(
    ("record", "skips"),
    [
        ({"redirect": "target"}, True),
        ({"redirect": "", "title": None, "pos": 9}, True),
        ({"redirect": None}, False),
        ({"redirect": 42}, False),
        ({"metadata": {"redirect": "nested"}}, False),
        ({"redirect": "target", "word": None}, False),
        ({"redirect": "target", "lang": None}, False),
        ({"redirect": "target", "lang_code": None}, False),
    ],
)
def test_russian_redirect_classification(
    record: dict[str, object], skips: bool
) -> None:
    assert RUSSIAN_EDITION.skip_record is not None
    assert RUSSIAN_EDITION.skip_record(record) is skips


def test_redirects_preserve_source_ids_batches_and_progress(tmp_path: Path) -> None:
    source = tmp_path / "mixed.jsonl"
    mixed_entry = json.loads(ENTRY)
    mixed_entry["redirect"] = "still an entry"
    mixed_record = json.dumps(mixed_entry).encode()
    lines = [
        REDIRECT,
        REDIRECT,
        ENTRY,
        REDIRECT,
        mixed_record + b"\r\n",
        REDIRECT.rstrip(b"\n"),
    ]
    source.write_bytes(b"".join(lines))
    target = tmp_path / "mixed.sqlite"
    total = source.stat().st_size
    progress = []
    worker.run_chunk(
        source,
        target,
        worker.Chunk(2, 0, total),
        2,
        lambda *info: progress.append(info),
        edition=RUSSIAN_EDITION,
    )
    assert progress == [
        (2, sum(len(line) for line in lines[:end]), total) for end in (2, 4, 6)
    ]
    with closing(sqlite3.connect(target)) as db:
        assert db.execute("SELECT id FROM entries ORDER BY id").fetchall() == [
            (20_000_003,),
            (20_000_005,),
        ]
        assert db.execute(
            "SELECT entry_id FROM forms ORDER BY entry_id"
        ).fetchall() == [(20_000_003,), (20_000_005,)]
        assert db.execute("SELECT * FROM batch_log ORDER BY batch_id").fetchall() == [
            (20_000_001, 2),
            (20_000_002, 2),
            (20_000_003, 2),
        ]


@pytest.mark.parametrize("cpu_count", [3, 5])
def test_redirect_only_input_publishes_empty_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cpu_count: int
) -> None:
    monkeypatch.setattr(importer.os, "cpu_count", lambda: cpu_count)
    source = tmp_path / "redirects.jsonl"
    source.write_bytes(REDIRECT * 8)
    target = tmp_path / "redirects.sqlite"
    progress = []
    importer.import_jsonl(
        source, target, batch_size=3, on_progress=lambda *info: progress.append(info)
    )
    totals = {chunk: (processed, total) for chunk, processed, total in progress}
    assert len(totals) == cpu_count - 2
    assert sum(total for _, total in totals.values()) == source.stat().st_size
    assert all(processed == total for processed, total in totals.values())
    with closing(sqlite3.connect(target)) as db:
        assert db.execute("SELECT count(*) FROM entries").fetchone() == (0,)
        assert db.execute("SELECT sum(line_count) FROM batch_log").fetchone() == (8,)


@pytest.mark.parametrize(
    "invalid",
    [b"{", b"[]", b"\xff", b'{"redirect":"target","word":null}', b'{"redirect":null}'],
)
def test_bad_line_after_redirect_leaves_no_database(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, invalid: bytes
) -> None:
    monkeypatch.setattr(importer.os, "cpu_count", lambda: 3)
    source = tmp_path / "bad.jsonl"
    target = tmp_path / "bad.sqlite"
    source.write_bytes(REDIRECT + invalid)
    with pytest.raises(importer.ImportFailure, match=r"chunk 0: line 2:"):
        importer.import_jsonl(source, target)
    assert not target.exists()


def test_redirects_count_toward_chunk_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(worker, "ID_RANGE", 2)
    source = tmp_path / "limit.jsonl"
    source.write_bytes(REDIRECT * 3)
    with pytest.raises(worker.ImportFailure, match=r"line 3: chunk exceeds its range"):
        worker.run_chunk(
            source,
            tmp_path / "limit.sqlite",
            worker.Chunk(0, 0, source.stat().st_size),
            1,
            edition=RUSSIAN_EDITION,
        )
