import sqlite3
from pathlib import Path

import pytest

from wiktionary_jsonl_parser import importer


def test_schema_matches_contract() -> None:
    specified = Path(__file__).resolve().parents[1] / "docs/dev/spec/schema.sql"
    assert importer.schema_sql().encode("utf-8") == specified.read_bytes()


def test_initialize_schema_from_any_working_directory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    with sqlite3.connect(":memory:") as db:
        db.create_collation(
            "UTF_CI", lambda left, right: (left > right) - (left < right)
        )
        importer.initialize_database(db)
        assert db.execute("PRAGMA foreign_keys").fetchone() == (1,)
        assert db.execute(
            "SELECT count(*) FROM sqlite_schema WHERE type = 'table'"
        ).fetchone() == (21,)


def test_preflight_rejects_missing_collation(tmp_path: Path) -> None:
    destination = tmp_path / "result.sqlite"
    with sqlite3.connect(":memory:") as db:
        db.create_collation("UTF_CI", None)
        with pytest.raises(importer.ImportFailure, match="SQLiteICUex.*UTF_CI"):
            importer.require_unicode_collation(db)
    assert not destination.exists()


def test_preflight_accepts_installed_collation() -> None:
    with sqlite3.connect(":memory:") as db:
        if not any(name == "UTF_CI" for _, name in db.execute("PRAGMA collation_list")):
            pytest.skip("SQLiteICUex runtime unavailable")
        importer.require_unicode_collation(db)
