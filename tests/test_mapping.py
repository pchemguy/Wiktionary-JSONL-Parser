import pytest

from wiktionary_jsonl_parser.mapping import RowsByTable, append_record_rows

ROOT = {"word": "word", "lang_code": "en", "lang": "English"}


def test_linkage_and_flat_children() -> None:
    data = {
        **ROOT,
        "synonyms": [
            {"word": "", "sense": None, "sense_index": 0, "raw_tags": [], "tags": None},
            {"word": "same"},
            {"word": "same"},
        ],
        "forms": [{"form": "same"}, {"form": "same", "tags": ["t"]}],
        "translations": [
            {
                "word": "x",
                "lang": "Russian",
                "lang_code": "ru",
                "roman": "",
                "sense": "meaning",
                "other": "info",
                "raw_tags": None,
                "tags": [],
            },
        ],
        "hyphenations": [{"parts": ["a", "b"]}, {"parts": []}, {}],
    }
    rows: RowsByTable = {
        table: []
        for table in ("entries", "synonyms", "forms", "translations", "hyphenations")
    }
    append_record_rows(data, 12, rows)
    assert rows["synonyms"] == [
        (12, 0, "", None, 0, "[]", "null"),
        (12, 1, "same", None, None, None, None),
        (12, 2, "same", None, None, None, None),
    ]
    assert rows["forms"] == [
        (12, 0, "same", None, None),
        (12, 1, "same", None, '["t"]'),
    ]
    assert rows["translations"] == [
        (12, 0, "x", "Russian", "ru", "", "meaning", "info", "null", "[]"),
    ]
    assert rows["hyphenations"] == [
        (12, 0, '["a","b"]', None, None),
        (12, 1, "[]", None, None),
        (12, 2, None, None, None),
    ]


@pytest.mark.parametrize(
    "field,value,diagnostic",
    [
        ("anagrams", None, "anagrams"),
        ("related", ["word"], "related"),
        ("forms", [{}], "forms.*form"),
        ("hyponym_unused", None, ""),
        ("synonyms", [{"sense_index": True}], "synonyms.*sense_index"),
        ("synonyms", [{"sense_index": -1}], "synonyms.*sense_index"),
        ("synonyms", [{"sense_index": 2**63}], "synonyms.*sense_index"),
        ("translations", [{"word": "x"}], "translations.*lang"),
        ("hyphenations", [{"parts": ""}], "hyphenations.*parts"),
    ],
)
def test_flat_child_value_shapes(field: str, value: object, diagnostic: str) -> None:
    rows: RowsByTable = {"entries": [], field: []}
    if diagnostic:
        with pytest.raises(ValueError, match=diagnostic):
            append_record_rows({**ROOT, field: value}, 1, rows)
    else:
        append_record_rows({**ROOT, field: value}, 1, rows)
        assert not rows[field]
