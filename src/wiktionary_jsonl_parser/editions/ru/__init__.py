"""Database contract for the Russian Wiktionary extract."""

from importlib.resources import files

from .. import Edition
from .mapping import LINKAGES, append_record_rows


def schema_sql() -> str:
    return files(__package__).joinpath("schema.sql").read_text(encoding="utf-8")


INSERTS = {
    "entries": (
        "INSERT INTO entries (id, word, lang_code, lang, pos, pos_title, literal_meaning, "
        "etymology_texts, categories, raw_tags, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    **{
        table: f"INSERT INTO {table} (entry_id, idx, word, sense, sense_index, raw_tags, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
        for table in LINKAGES
    },
    "forms": "INSERT INTO forms (entry_id, idx, form, raw_tags, tags) VALUES (?, ?, ?, ?, ?)",
    "translations": (
        "INSERT INTO translations (entry_id, idx, word, lang, lang_code, roman, sense, other, "
        "raw_tags, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "hyphenations": (
        "INSERT INTO hyphenations (entry_id, idx, parts, raw_tags, tags) VALUES (?, ?, ?, ?, ?)"
    ),
    "senses": (
        "INSERT INTO senses (entry_id, idx, glosses, form_of, categories, topics, raw_tags, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "examples": (
        "INSERT INTO examples (sense_entry_id, sense_idx, idx, text, translation, ref, "
        "bold_text_offsets, bold_translation_offsets) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    ),
    "sounds": (
        "INSERT INTO sounds (entry_id, idx, audio, ipa, rhymes, homophones, urls, raw_tags, tags) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ),
}


def is_standalone_redirect(record: dict[str, object]) -> bool:
    """Recognize a redirect object without any of the required entry keys."""

    return isinstance(record.get("redirect"), str) and not (
        "word" in record or "lang" in record or "lang_code" in record
    )


RUSSIAN_EDITION = Edition(
    "ru", schema_sql, append_record_rows, INSERTS, skip_record=is_standalone_redirect
)
