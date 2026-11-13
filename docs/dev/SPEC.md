# Importer specification

The converter imports the Kaikki Russian Wiktionary extract from a local UTF-8 JSONL file into a fresh SQLite database. It reads in source order and processes all supported records regardless of `lang_code`. Downloading, archive extraction, JSON Schema validation, multiprocessing, and resumption are outside the importer scope. See the [project brief](PROJECT.md), [architecture](ARCHITECTURE.md), and [decomposition](DECOMPOSITION.md).

## Command line and output

```text
wiktionary-jsonl-parser INPUT [--output PATH] [--batch-size N]
```

| Argument | Behavior |
| --- | --- |
| `INPUT` | Required path to a readable local UTF-8 JSONL file. |
| `--output PATH` | Optional destination database path. When omitted, replace the final `.jsonl` suffix with `.sqlite` in the input path and keep the parent directory. For example, `data/ru-extract.jsonl` yields `data/ru-extract.sqlite`. If the input name has no final `.jsonl` suffix, supply an explicit output path. |
| `--batch-size N` | Positive integer maximum number of source lines per batch. Defaults to 25,000. |

Relative paths are interpreted from the working directory. The destination parent directory must exist. The converter refuses an existing destination without modifying it. It checks that the input can be opened and that SQLiteICUex's `UTF_CI` collation is available before creating the output. It initializes the output with the [SQLite schema](spec/schema.sql) and enforces foreign keys on the writing connection.

## Reading and mapping

Each source line must contain one JSON object. LF and CRLF terminate records, and a final record may end at EOF. Empty or whitespace-only lines, malformed JSON, invalid UTF-8, nonfinite numeric constants, and non-object top-level values fail the import. The importer applies mapping rules and SQLite constraints without running a JSON Schema validator.

Every decoded and mappable record yields one `entries` row. Entry IDs are unique and increase in source order. Entry and child IDs associate rows with their source entry or sense. Child indices start at zero within their immediate source arrays. Preserve duplicate entries, duplicate array elements, and array order. The schema defines the tables, columns, keys, and collations.

| Source | SQLite representation |
| --- | --- |
| Entry fields | `word`, `lang_code`, and `lang` are required. `pos`, `pos_title`, and `literal_meaning` map to the same-named columns. Store `etymology_texts`, `categories`, `raw_tags`, and `tags` as JSON text. Ignore `etymology_links`. |
| Linkage arrays | Expand `anagrams`, `antonyms`, `coordinate_terms`, `derived`, `holonyms`, `hypernyms`, `hyponyms`, `meronyms`, `metagrams`, `proverbs`, `related`, `synonyms`, and `variants` into same-named tables. Preserve a supplied `sense_index` as a source value. The sense foreign key used by examples comes from the zero-based sense position. |
| `forms`, `senses`, `translations`, `sounds`, and `hyphenations` | Expand each array into its same-named table. Store declared JSON-valued columns as JSON text. Transform `senses[].form_of` into an ordered JSON array of the objects' `word` values. |
| `senses[].examples` | Expand into `examples` rows keyed by the entry ID, sense index, and example index within the sense. Store the two offset arrays as JSON text. |
| Sound URLs | Store supplied `flac_url`, `mp3_url`, `oga_url`, `ogg_url`, `opus_url`, and `wav_url` fields in `sounds.urls` as a JSON object in this key order. Use SQL `NULL` when all are absent. |

Mapped text preserves its source value. JSON text uses compact serialization with literal non-ASCII characters, preserving array order. Missing optional columns use SQL `NULL`, while explicit empty strings and retained empty arrays are stored as `''` and `[]`, respectively. A missing or empty array expanded into a table yields zero child rows. Ignore other unmapped properties and leave missing values unfilled by schema defaults. Missing required values and values that cannot be mapped fail the current batch.

## Batch persistence and errors

The importer reads up to the configured number of source lines and decodes and maps them before writing. For each nonempty batch, the importer commits all mapped rows and one `batch_log` row in one transaction. Batch IDs start at one and increase in commit order. The log records the actual number of input lines in that batch, including a shorter final batch. A readable empty file creates the schema with zero entries and zero batch log rows.

The converter stops at the first input, mapping, or persistence error. If a transaction is active, it rolls back the entire batch, including its log row. Earlier committed batches remain available. A retry requires a fresh output database. Diagnostics go to standard error and identify the error and the one-based source line where it can be determined. CLI exit status is 0 on successful completion, 1 on import failure, and 2 on command-line usage errors.

## Acceptance

| Scenario | Required result |
| --- | --- |
| Three valid lines with batch size two | Three entries in source order and two log rows with line counts 2 and 1. An omitted output path creates the expected sibling `.sqlite` file. |
| Related rows and duplicate data | Repeated values appear at their original indices, example keys identify the enclosing sense, and the database has zero foreign-key violations. |
| Retained and omitted fields | `etymology_texts` is preserved, `etymology_links` is ignored, and `form_of` and sound URLs match the mapped forms above. Missing optional fields differ from explicit empty values as specified. |
| Existing destination or missing `UTF_CI` | Failure preserves the existing destination or leaves the proposed destination absent, respectively. |
| Malformed line after a committed batch | The diagnostic gives the source line, the CLI reports failure, and the database contains only the previously committed entries, children, and log rows. |
| A database write fails within a batch | The batch contributes zero data or log rows, and all earlier commits remain intact. |
| Empty input | Success produces the initialized schema with no entries or batch log rows. |
