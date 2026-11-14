from io import BytesIO

import pytest

from wiktionary_jsonl_parser.mapping import append_record_rows
from wiktionary_jsonl_parser.worker import ImportFailure, decode_record, read_batches


def test_framing_order_and_mapping() -> None:
    stream = BytesIO(
        b'\xef\xbb\xbf{"word":"old","word":"first","lang":"Russian","lang_code":"ru",'
        b'"pos":null,"pos_title":"","literal_meaning":" x ","etymology_texts":["\\u0451"],'
        b'"etymology_links":3,"categories":null,"raw_tags":[],"tags":["x"]}\r\n'
        b'{"word":"second","lang":"English","lang_code":"en"}\n'
        b'{"word":"second","lang":"English","lang_code":"en"}'
    )
    batches = list(read_batches(stream, 2))
    assert [len(batch) for batch in batches] == [2, 1]
    rows = {"entries": []}
    for index, raw in enumerate(batches[0] + batches[1], 1):
        append_record_rows(decode_record(raw, index), index, rows)
    assert rows["entries"] == [
        (
            1,
            "first",
            "ru",
            "Russian",
            None,
            "",
            " x ",
            '["\u0451"]',
            "null",
            "[]",
            '["x"]',
        ),
        (2, "second", "en", "English", None, None, None, None, None, None, None),
        (3, "second", "en", "English", None, None, None, None, None, None, None),
    ]


@pytest.mark.parametrize(
    "raw",
    [
        b"\n",
        b"   \r\n",
        b"\xff",
        b"{",
        b"[]",
        b"null",
        b'{"x": NaN}',
        b'{"x": Infinity}',
        b'{"x": -Infinity}',
        b"\xef\xbb\xbf{}",
    ],
)
def test_invalid_line_reports_source_number(raw: bytes) -> None:
    with pytest.raises(ImportFailure, match="line 4") as failure:
        decode_record(raw, 4)
    assert failure.value.line_number == 4


@pytest.mark.parametrize(
    "change",
    [
        {"word": None},
        {"lang_code": False},
        {"pos": 3},
        {"tags": {}},
        {"categories": [float("inf")]},
        {"word": "\ud800"},
        {"categories": ["\ud800"]},
    ],
)
def test_invalid_mapped_entry_values(change: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        append_record_rows(
            {"word": "first", "lang_code": "ru", "lang": "Russian", **change},
            1,
            {"entries": []},
        )
