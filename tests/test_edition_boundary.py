import sqlite3
from contextlib import closing
from pathlib import Path

from wiktionary_jsonl_parser.editions import Edition, get_edition
from wiktionary_jsonl_parser.merge import merge_databases
from wiktionary_jsonl_parser.worker import Chunk, run_chunk


def test_edition_supplies_schema_mapping_and_order(tmp_path: Path) -> None:
    def map_record(
        record: dict[str, object],
        key: int,
        rows: dict[str, list[tuple[str | int | None, ...]]],
    ) -> None:
        rows["headwords"].append((key, str(record["spelling"])))
        rows["notes"].append((key, "example"))

    edition = Edition(
        identifier="test",
        schema_sql=lambda: (
            "CREATE TABLE headwords (id INTEGER PRIMARY KEY, spelling TEXT);\n"
            "CREATE TABLE notes (headword_id INTEGER REFERENCES headwords(id), "
            "note TEXT);\n"
        ),
        map_record=map_record,
        inserts={
            "headwords": "INSERT INTO headwords (id, spelling) VALUES (?, ?)",
            "notes": "INSERT INTO notes (headword_id, note) VALUES (?, ?)",
        },
    )
    first, second = b'{"spelling":"one"}\n', b'{"spelling":"two"}'
    source = tmp_path / "input.jsonl"
    source.write_bytes(first + second)
    shards = [tmp_path / "one.db", tmp_path / "two.db"]
    run_chunk(source, shards[0], Chunk(0, 0, len(first)), 1, edition=edition)
    run_chunk(
        source,
        shards[1],
        Chunk(1, len(first), len(first + second)),
        1,
        edition=edition,
    )
    destination = tmp_path / "merged.db"
    merge_databases(shards, destination, 2, edition=edition)
    with closing(sqlite3.connect(destination)) as db:
        assert db.execute("SELECT * FROM headwords ORDER BY id").fetchall() == [
            (1, "one"),
            (10_000_001, "two"),
        ]
        assert db.execute("SELECT * FROM notes ORDER BY headword_id").fetchall() == [
            (1, "example"),
            (10_000_001, "example"),
        ]
        assert db.execute("SELECT * FROM batch_log ORDER BY batch_id").fetchall() == [
            (1, 1),
            (10_000_001, 1),
        ]
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []


def test_russian_definition_has_edition_tables_only() -> None:
    edition = get_edition("ru")
    assert edition.identifier == "ru"
    assert "batch_log" not in edition.inserts
    assert tuple(edition.inserts).index("senses") < tuple(edition.inserts).index(
        "examples"
    )
