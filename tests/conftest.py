import os

import pytest


@pytest.fixture
def single_worker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(os, "cpu_count", lambda: 3)
