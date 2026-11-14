import pytest

from wiktionary_jsonl_parser.editions.ru.mapping import RowsByTable, append_record_rows

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


def test_nested_senses_examples_and_sounds() -> None:
    data = {
        **ROOT,
        "senses": [
            {"glosses": [], "categories": None},
            {
                "glosses": [" x "],
                "form_of": [{"word": "\u0451"}, {"word": "\u0451"}],
                "topics": [{"z": 1, "a": 2}],
                "raw_tags": [],
                "tags": None,
                "examples": [
                    {"text": "\u0451!", "bold_text_offsets": [[1, 2], [0, 1]]},
                    {
                        "text": "",
                        "translation": None,
                        "ref": "",
                        "bold_translation_offsets": None,
                    },
                ],
            },
            {"form_of": []},
        ],
        "sounds": [
            {
                "ogg_url": "",
                "mp3_url": "m",
                "flac_url": None,
                "wav_url": "w",
                "opus_url": "o",
                "oga_url": "g",
                "audio": "a",
                "ipa": "i",
                "rhymes": "",
                "homophones": [],
                "raw_tags": None,
                "tags": ["t"],
            },
            {},
        ],
    }
    rows: RowsByTable = {
        table: [] for table in ("entries", "senses", "examples", "sounds")
    }
    append_record_rows(data, 8, rows)
    assert rows["senses"] == [
        (8, 0, "[]", None, "null", None, None, None),
        (8, 1, '[" x "]', '["\u0451","\u0451"]', None, '[{"z":1,"a":2}]', "[]", "null"),
        (8, 2, None, "[]", None, None, None, None),
    ]
    assert rows["examples"] == [
        (8, 1, 0, "\u0451!", None, None, "[[1,2],[0,1]]", None),
        (8, 1, 1, "", None, "", None, "null"),
    ]
    assert rows["sounds"] == [
        (
            8,
            0,
            "a",
            "i",
            "",
            "[]",
            '{"flac_url":null,"mp3_url":"m","oga_url":"g","ogg_url":"","opus_url":"o","wav_url":"w"}',
            "null",
            '["t"]',
        ),
        (8, 1, None, None, None, None, None, None, None),
    ]


@pytest.mark.parametrize(
    "field,value,diagnostic",
    [
        ("senses", [{"form_of": None}], "senses.*form_of"),
        ("senses", [{"form_of": [{"word": None}]}], "senses.*form_of.*word"),
        ("senses", [{"examples": None}], "senses.*examples"),
        ("senses", [{"examples": [{}]}], "senses.*examples.*text"),
        (
            "senses",
            [{"examples": [{"text": "x", "bold_text_offsets": {}}]}],
            "bold_text_offsets",
        ),
        ("sounds", [], ""),
        ("sounds", [{"wav_url": 8}], "sounds.*wav_url"),
    ],
)
def test_nested_child_value_shapes(field: str, value: object, diagnostic: str) -> None:
    rows: RowsByTable = {
        table: [] for table in ("entries", "senses", "examples", "sounds")
    }
    if diagnostic:
        with pytest.raises(ValueError, match=diagnostic):
            append_record_rows({**ROOT, field: value}, 1, rows)
    else:
        append_record_rows({**ROOT, field: value}, 1, rows)
        assert not rows[field]
