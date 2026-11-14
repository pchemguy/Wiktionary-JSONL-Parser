"""Make the source checkout importable in fresh Python interpreters during tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def child_import_path(monkeypatch: pytest.MonkeyPatch) -> None:
    src = str(Path(__file__).resolve().parents[1] / "src")
    monkeypatch.setenv("PYTHONPATH", src, prepend=os.pathsep)


@pytest.fixture
def single_worker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(os, "cpu_count", lambda: 3)
