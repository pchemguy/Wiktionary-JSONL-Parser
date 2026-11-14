from importlib import import_module
from pathlib import Path

import pytest

from wiktionary_jsonl_parser.worker import ImportFailure


@pytest.mark.parametrize("signal_error", [ProcessLookupError, PermissionError])
def test_benchmark_reaps_siblings_and_preserves_failure(
    signal_error: type[OSError], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "tools"))
    benchmark = import_module("benchmark_parallel_import")

    class Child:
        stdout = None

        def __init__(
            self, status: int | None = None, *, fail_signal: bool = False
        ) -> None:
            self.status = status
            self.fail_signal = fail_signal
            self.terminated = False
            self.waited = False

        def poll(self) -> int | None:
            return self.status

        def terminate(self) -> None:
            self.terminated = True
            self.status = -15
            if self.fail_signal:
                raise signal_error("forced signalling error")

        def wait(self, timeout: float | None = None) -> int:
            self.waited = True
            assert self.status is not None
            return self.status

    children = [Child(1), Child(fail_signal=True), Child()]
    launches = iter(children)
    monkeypatch.setattr(benchmark.subprocess, "Popen", lambda *a, **kw: next(launches))

    with pytest.raises(ImportFailure, match="chunk 0 exited with status 1") as error:
        benchmark.run_workers(
            Path("source.jsonl"), [0, 1, 2, 3], [Path(str(i)) for i in range(3)]
        )
    assert all(child.waited for child in children)
    assert all(child.terminated for child in children[1:])
    notes = getattr(error.value, "__notes__", [])
    if signal_error is PermissionError:
        assert notes == ["worker cleanup: forced signalling error"]
    else:
        assert notes == []
