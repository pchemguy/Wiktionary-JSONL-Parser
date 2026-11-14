import sqlite3

import pytest

from wiktionary_jsonl_parser import importer


@pytest.mark.parametrize(
    ("cpus", "limit", "workers", "group_size", "warned"),
    [
        (None, 10, 1, 0, False),
        (1, 10, 1, 0, False),
        (2, 10, 1, 0, False),
        (3, 0, 1, 0, True),
        (6, 4, 4, 4, False),
        (6, 3, 3, 3, True),
        (8, 4, 6, 4, True),
        (7, 2, 5, 2, True),
        (4, 1, 2, 1, True),
    ],
)
def test_plan(
    cpus: int | None, limit: int, workers: int, group_size: int, warned: bool
) -> None:
    warnings: list[str] = []

    def unexpected_confirmation() -> bool:
        pytest.fail("confirmation should only be requested at a zero limit")

    plan = importer.plan_run(cpus, limit, warnings.append, unexpected_confirmation)
    assert (plan.worker_count, plan.merge_group_size) == (workers, group_size)
    requested = cpus - 2 if cpus is not None and cpus > 2 else 1
    assert warnings == (
        [f"requested {requested} workers but SQLite allows {limit} attachments"]
        if warned
        else []
    )


@pytest.mark.parametrize("answer", [None, False, True, 1])
def test_zero_limit_requires_explicit_confirmation(answer: bool | int | None) -> None:
    calls: list[str] = []

    def confirm() -> bool:
        calls.append("confirmed")
        return answer  # type: ignore[return-value]

    callback = confirm if answer is not None else None
    if answer is True:
        plan = importer.plan_run(5, 0, calls.append, callback)
        assert (plan.worker_count, plan.merge_group_size) == (1, 0)
    else:
        with pytest.raises(importer.ImportFailure, match="confirmation"):
            importer.plan_run(5, 0, calls.append, callback)
    assert calls == ["requested 3 workers but SQLite allows 0 attachments"] + (
        [] if answer is None else ["confirmed"]
    )


def test_probe_uses_effective_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    connect = sqlite3.connect

    def limited(path: str) -> sqlite3.Connection:
        db = connect(path)
        db.setlimit(sqlite3.SQLITE_LIMIT_ATTACHED, 0)
        return db

    monkeypatch.setattr(importer.sqlite3, "connect", limited)
    assert importer.probe_attachment_limit() == 0
