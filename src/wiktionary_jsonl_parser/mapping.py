"""Map decoded entry objects to ordered SQLite parameter tuples."""

import json
from typing import TypeAlias

Row: TypeAlias = tuple[str | int | None, ...]
RowsByTable: TypeAlias = dict[str, list[Row]]


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
    """Append an entry row using the packaged schema's column order."""

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
