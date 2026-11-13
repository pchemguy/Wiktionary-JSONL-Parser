"""Map decoded entry objects to ordered SQLite parameter tuples."""

import json
from collections.abc import Iterator
from typing import TypeAlias, cast

Row: TypeAlias = tuple[str | int | None, ...]
RowsByTable: TypeAlias = dict[str, list[Row]]

LINKAGES = (
    "anagrams",
    "antonyms",
    "coordinate_terms",
    "derived",
    "holonyms",
    "hypernyms",
    "hyponyms",
    "meronyms",
    "metagrams",
    "proverbs",
    "related",
    "synonyms",
    "variants",
)


def array_items(value: object) -> Iterator[tuple[int, dict[str, object]]]:
    if not isinstance(value, list):
        raise ValueError("expected an array of objects")
    for idx, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"item {idx} must be an object")
        yield idx, cast(dict[str, object], item)


def sense_index(record: dict[str, object]) -> int | None:
    value = record.get("sense_index")
    if value is None:
        return None
    if type(value) is not int or not 0 <= value < 2**63:
        raise ValueError("sense_index must be a nonnegative SQLite integer")
    return value


def tags(record: dict[str, object]) -> tuple[str | None, str | None]:
    return retained_array(record, "raw_tags"), retained_array(record, "tags")


def text(
    record: dict[str, object], field: str, *, required: bool = False
) -> str | None:
    value = record.get(field)
    if value is None and not required:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{field} contains invalid Unicode") from exc
    return value


def json_text(value: object, field: str) -> str:
    try:
        result = json.dumps(
            value, ensure_ascii=False, allow_nan=False, separators=(",", ":")
        )
        result.encode("utf-8")
    except (ValueError, RecursionError) as exc:
        raise ValueError(f"{field} cannot be stored as UTF-8 JSON: {exc}") from exc
    return result


def retained_array(record: dict[str, object], field: str) -> str | None:
    if field not in record:
        return None
    value = record[field]
    if value is not None and not isinstance(value, list):
        raise ValueError(f"{field} must be an array or null")
    return json_text(value, field)


def append_record_rows(
    record: dict[str, object], entry_id: int, rows_by_table: RowsByTable
) -> None:
    """Append ordered entry and child tuples in the packaged schema's column order."""

    rows_by_table["entries"].append(
        (
            entry_id,
            text(record, "word", required=True),
            text(record, "lang_code", required=True),
            text(record, "lang", required=True),
            text(record, "pos"),
            text(record, "pos_title"),
            text(record, "literal_meaning"),
            retained_array(record, "etymology_texts"),
            retained_array(record, "categories"),
            retained_array(record, "raw_tags"),
            retained_array(record, "tags"),
        )
    )

    for key in (*LINKAGES, "forms", "translations", "hyphenations"):
        if key not in record:
            continue
        try:
            for idx, item in array_items(record[key]):
                rows_by_table[key].append(
                    (entry_id, idx, *flat_child_values(key, item))
                )
        except ValueError as exc:
            raise ValueError(f"{key}: {exc}") from exc


def flat_child_values(table: str, item: dict[str, object]) -> Row:
    if table == "forms":
        return (text(item, "form", required=True), *tags(item))
    if table == "translations":
        return (
            text(item, "word", required=True),
            text(item, "lang", required=True),
            text(item, "lang_code"),
            text(item, "roman"),
            text(item, "sense"),
            text(item, "other"),
            *tags(item),
        )
    if table == "hyphenations":
        return (retained_array(item, "parts"), *tags(item))
    return (text(item, "word"), text(item, "sense"), sense_index(item), *tags(item))
