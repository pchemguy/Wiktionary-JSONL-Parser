# JSON-to-SQLite mapping

## Relational normalization

Create one `entries` row per record. The importer assigns unique entry IDs in source order before insertion. Each element of an expanded array creates one child row. Use the element's zero-based position in its immediate array as `idx`. Preserve duplicate entries, duplicate array elements, and array order. Copy mapped strings without trimming, case folding, Unicode normalization, or transliteration. Use the [SQLite schema](schema.sql) for column types, keys, and collations.

Child tables use the enclosing entry's ID. An example uses the enclosing sense's `entry_id` and `idx` as `sense_entry_id` and `sense_idx`. Its own `idx` is its position within that sense's `examples` array.

## Field mapping

The table lists the source fields consumed for each destination. Copy fields to same-named columns unless a transformation is specified. Required text fields must be present as JSON strings. Ignore unmapped properties, including `etymology_links`.

| Source → destination | Required text | Optional scalars | Retained JSON text |
| --- | --- | --- | --- |
| Root object → `entries` | `word`, `lang_code`, `lang` | `pos`, `pos_title`, `literal_meaning` | `etymology_texts`, `categories`, `raw_tags`, `tags` |
| Linkage arrays → same-named tables | — | `word`, `sense`, `sense_index` | `raw_tags`, `tags` |
| `forms[]` → `forms` | `form` | — | `raw_tags`, `tags` |
| `senses[]` → `senses` | — | — | `glosses`, `form_of`, `categories`, `topics`, `raw_tags`, `tags` |
| `senses[].examples[]` → `examples` | `text` | `translation`, `ref` | `bold_text_offsets`, `bold_translation_offsets` |
| `translations[]` → `translations` | `word`, `lang` | `lang_code`, `roman`, `sense`, `other` | `raw_tags`, `tags` |
| `sounds[]` → `sounds` | — | `audio`, `ipa`, `rhymes` | `homophones`, `raw_tags`, `tags`, generated `urls` |
| `hyphenations[]` → `hyphenations` | — | — | `parts`, `raw_tags`, `tags` |

The linkage arrays are `anagrams`, `antonyms`, `coordinate_terms`, `derived`, `holonyms`, `hypernyms`, `hyponyms`, `meronyms`, `metagrams`, `proverbs`, `related`, `synonyms`, and `variants`. Copy `sense_index` unchanged as an optional nonnegative integer, including zero when explicitly supplied. It is a source definition number. Only the sense position supplies the example foreign key.

## Missing, null, and empty values

| Source value | Stored result |
| --- | --- |
| Missing optional scalar or explicit JSON `null` for an optional scalar | SQL `NULL` |
| Explicit empty string in a text field | Empty SQL text |
| Missing retained array | SQL `NULL` |
| Explicit JSON `null` in a directly retained JSON field | JSON text `null` |
| Explicit empty retained array, including `form_of` | JSON text `[]` |
| Missing or empty array expanded into a table | Zero child rows |

The importer leaves absent properties unfilled by source-schema defaults. A supplied expanded array must be an array of objects. A directly retained array must be an array or JSON `null`. Optional non-null scalars must have their mapped type. A missing required field or an incompatible mapped value fails the batch. The importer checks the shapes consumed by these rules and preserves the contents of directly retained arrays as supplied.

## JSON text and transformations

Store retained or generated JSON text without insignificant whitespace and with non-ASCII characters written literally. Preserve array order and the decoded member order of objects within directly retained arrays. Store finite numbers using the JSON serializer's standard representation. Reject values that cannot be serialized as valid UTF-8 JSON. In particular, preserve example offset arrays as supplied, including the order of each `[start, end]` pair. The converter stores the original offsets and text without recalculating offsets.

- **`senses[].form_of`** takes an array of objects with required string `word` fields and stores an array of those strings in source order. For example, `[{"word":"слово"},{"word":"слово"}]` becomes `["слово","слово"]`. A missing field yields SQL `NULL`. A supplied value, including explicit JSON `null`, must meet this array contract.
- **`sounds.urls`** contains the supplied URL properties in this key order: `flac_url`, `mp3_url`, `oga_url`, `ogg_url`, `opus_url`, `wav_url`. A present property contains a string or JSON `null`. Missing properties contribute no keys. Retain present empty strings and null values. For example, a sound with `ogg_url` set to an empty string and `mp3_url` set to `"https://example.test/audio.mp3"` yields `{"mp3_url":"https://example.test/audio.mp3","ogg_url":""}`. When all six properties are absent, store SQL `NULL`.
