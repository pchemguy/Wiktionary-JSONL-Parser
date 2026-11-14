from io import BytesIO

import pytest

from wiktionary_jsonl_parser.importer import Chunk, partition_source


@pytest.mark.parametrize(
    ("data", "workers", "boundaries"),
    [
        (b"", 3, [0, 0, 0, 0]),
        (b"a", 4, [0, 0, 0, 0, 1]),
        (b"a\n" * 4, 4, [0, 2, 4, 6, 8]),
        (b"abc\r\ndef", 2, [0, 5, 8]),
        (b"\xef\xbb\xbf{}\r\n{}\n{}", 5, [0, 7, 7, 7, 10, 12]),
        pytest.param(
            b"a" * 300_000 + b"\nlast",
            4,
            [0, 300_001, 300_001, 300_001, 300_005],
            id="long-line-then-final-record",
        ),
        pytest.param(
            b"a" * 300_000,
            4,
            [0, 300_000, 300_000, 300_000, 300_000],
            id="long-unterminated-line",
        ),
    ],
)
def test_partition(data: bytes, workers: int, boundaries: list[int]) -> None:
    chunks = partition_source(BytesIO(data), len(data), workers)
    assert chunks == [
        Chunk(i, start, stop)
        for i, (start, stop) in enumerate(zip(boundaries, boundaries[1:], strict=False))
    ]
    assert b"".join(data[chunk.start : chunk.stop] for chunk in chunks) == data
    assert all(start in (0, len(data)) or data[start - 1] == 10 for start in boundaries)
