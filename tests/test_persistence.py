import json
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import worker as importer

FIXTURE = Path(__file__).with_name("fixtures") / "all-tables.jsonl"


def test_all_tables_bound_and_written_in_parent_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_connect = sqlite3.connect
    calls: list[tuple[str, int, int]] = []

    class SpyConnection(sqlite3.Connection):
        def executemany(  # type: ignore[override]
            self, sql: str, parameters: list[tuple[object, ...]]
        ) -> sqlite3.Cursor:
            assert self.in_transaction
            calls.append((sql.split()[2], sql.count("?"), len(parameters)))
            return super().executemany(sql, parameters)

    def connect(path: Path | str) -> sqlite3.Connection:
        return real_connect(path, factory=SpyConnection)

    monkeypatch.setattr(importer.sqlite3, "connect", connect)
    dest = tmp_path / "all.sqlite"
    importer.run_chunk(FIXTURE, dest, importer.Chunk(0, 0, FIXTURE.stat().st_size), 2)
    expected = {
        "entries": [
            (
                1,
                "\u0451\u0436",
                "ru",
                "\u0440\u0443\u0441\u0441\u043a\u0438\u0439",
                "noun",
                "Noun",
                "\u0401",
                '[" \u0451 "]',
                '[{"z":0,"a":1}]',
                "null",
                "[]",
            ),
            (2, "plain", "en", "English", None, None, None, None, None, None, None),
            (3, "plain", "en", "English", None, None, None, None, None, None, None),
        ],
        "forms": [(1, 0, "f", '["r"]', '["t"]')],
        "senses": [(1, 0, '["g"]', '["f","f"]', "[]", '["t"]', '["r"]', "null")],
        "examples": [(1, 0, 0, "\u0451!", "", "ref", "[[1,2],[0,1]]", "null")],
        "translations": [(1, 0, "w", "L", "lc", "rom", "s", "o", '["r"]', "[]")],
        "sounds": [
            (
                1,
                0,
                "a",
                "i",
                "r",
                '["h"]',
                '{"mp3_url":null,"ogg_url":""}',
                "[]",
                '["t"]',
            )
        ],
        "hyphenations": [(1, 0, '["a","b"]', "[]", '["t"]')],
        "batch_log": [(1, 2), (2, 1)],
    }
    for name in (
        "anagrams",
        "antonyms",
        "coordinate_terms",
        "derived",
        "holonyms",
        "hypernyms",
        "hyponyms",
        "meronyms",
        "metagrams",
        "proverbs",
        "related",
        "synonyms",
        "variants",
    ):
        expected[name] = [
            (1, 0, name, "", 0, "null", "[]"),
            (1, 1, name, None, None, None, None),
        ]
    with closing(real_connect(dest)) as db:
        tables = db.execute("SELECT name FROM sqlite_schema WHERE type = 'table'")
        assert {name for (name,) in tables} == expected.keys()
        for table, rows in expected.items():
            assert db.execute(f"SELECT * FROM {table} ORDER BY 1, 2").fetchall() == rows
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    first = calls[:-2]
    assert {name for name, _, _ in first} == expected.keys()
    assert len(first) == len(expected)
    assert first[0] == ("entries", 11, 2)
    assert first[-1] == ("batch_log", 2, 1)
    assert calls[-2:] == [("entries", 11, 1), ("batch_log", 2, 1)]
    assert [name for name, _, _ in first].index("senses") < [
        name for name, _, _ in first
    ].index("examples")
    for table, bindings, _ in first:
        assert bindings == len(expected[table][0])


@pytest.mark.parametrize("failure", ["mapping", "child insert", "log insert"])
def test_failed_batch_keeps_committed_prefix(
    failure: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = importer.initialize_database

    def initialize(db: sqlite3.Connection) -> None:
        original(db)
        if failure == "child insert":
            db.execute("""CREATE TRIGGER reject_write BEFORE INSERT ON examples
                WHEN NEW.sense_entry_id = 4 BEGIN SELECT RAISE(ABORT, 'child failure'); END""")
        if failure == "log insert":
            db.execute("""CREATE TRIGGER reject_log BEFORE INSERT ON batch_log
                WHEN NEW.batch_id = 2 BEGIN SELECT RAISE(ABORT, 'log failure'); END""")

    monkeypatch.setattr(importer, "initialize_database", initialize)
    line = FIXTURE.read_bytes().splitlines()[0]
    last = (
        line
        if failure != "mapping"
        else json.dumps({"word": "missing language"}).encode()
    )
    source = tmp_path / "failing.jsonl"
    source.write_bytes(b"\n".join((line, line, line, last)))
    output = source.with_suffix(".sqlite")
    diagnostic = {
        "mapping": "line 4",
        "child insert": "batch 2.*child failure",
        "log insert": "batch 2.*log failure",
    }[failure]
    with pytest.raises(importer.ImportFailure, match=diagnostic):
        importer.run_chunk(
            source, output, importer.Chunk(0, 0, source.stat().st_size), 2
        )
    with closing(sqlite3.connect(output)) as db:
        assert db.execute("SELECT id FROM entries ORDER BY id").fetchall() == [
            (1,),
            (2,),
        ]
        assert db.execute(
            "SELECT sense_entry_id FROM examples ORDER BY 1"
        ).fetchall() == [(1,), (2,)]
        assert db.execute("SELECT * FROM batch_log").fetchall() == [(1, 2)]
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
