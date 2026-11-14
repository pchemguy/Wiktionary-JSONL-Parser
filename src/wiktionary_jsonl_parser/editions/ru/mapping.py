"""Map decoded entry objects to ordered SQLite parameter tuples."""

import json
from collections.abc import Iterator
from typing import cast

from .. import Row, RowsByTable

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

    for key in (*LINKAGES, "forms", "translations", "hyphenations", "sounds"):
        if key not in record:
            continue
        try:
            for idx, item in array_items(record[key]):
                rows_by_table[key].append(
                    (entry_id, idx, *flat_child_values(key, item))
                )
        except ValueError as exc:
            raise ValueError(f"{key}: {exc}") from exc

    if "senses" in record:
        try:
            for idx, sense in array_items(record["senses"]):
                append_sense_rows(sense, entry_id, idx, rows_by_table)
        except ValueError as exc:
            raise ValueError(f"senses: {exc}") from exc


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
    if table == "sounds":
        return (
            text(item, "audio"),
            text(item, "ipa"),
            text(item, "rhymes"),
            retained_array(item, "homophones"),
            sound_urls(item),
            *tags(item),
        )
    if table == "hyphenations":
        return (retained_array(item, "parts"), *tags(item))
    return (text(item, "word"), text(item, "sense"), sense_index(item), *tags(item))


def sound_urls(item: dict[str, object]) -> str | None:
    urls = {
        key: text(item, key)
        for key in ("flac_url", "mp3_url", "oga_url", "ogg_url", "opus_url", "wav_url")
        if key in item
    }
    return json_text(urls, "urls") if urls else None


def form_of(sense: dict[str, object]) -> str | None:
    if "form_of" not in sense:
        return None
    try:
        words = [
            text(form, "word", required=True)
            for _, form in array_items(sense["form_of"])
        ]
        return json_text(words, "form_of")
    except ValueError as exc:
        raise ValueError(f"form_of: {exc}") from exc


def append_sense_rows(
    sense: dict[str, object], entry_id: int, sense_idx: int, rows_by_table: RowsByTable
) -> None:
    rows_by_table["senses"].append(
        (
            entry_id,
            sense_idx,
            retained_array(sense, "glosses"),
            form_of(sense),
            retained_array(sense, "categories"),
            retained_array(sense, "topics"),
            *tags(sense),
        )
    )
    if "examples" not in sense:
        return
    try:
        for idx, example in array_items(sense["examples"]):
            rows_by_table["examples"].append(
                (
                    entry_id,
                    sense_idx,
                    idx,
                    text(example, "text", required=True),
                    text(example, "translation"),
                    text(example, "ref"),
                    retained_array(example, "bold_text_offsets"),
                    retained_array(example, "bold_translation_offsets"),
                )
            )
    except ValueError as exc:
        raise ValueError(f"sense {sense_idx} examples: {exc}") from exc
