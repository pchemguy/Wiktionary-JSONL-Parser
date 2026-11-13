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

## JSONL decoding and mapping

Read UTF-8 in source order. An initial UTF-8 BOM is allowed at the beginning of the file. LF and CRLF terminate records, and EOF may terminate the final record. Each line must decode to one complete JSON object. Blank or whitespace-only lines, invalid UTF-8, malformed JSON, non-object values, and the bare tokens `NaN`, `Infinity`, and `-Infinity` fail the import. Within an object, the last value wins when a property name occurs more than once.

The importer decodes and maps every record in a batch before writing it. The [mapping contract](spec/mapping.md) defines required mapped fields, accepted value shapes, relational normalization, and JSON text storage. Apply those rules and SQLite constraints without running a JSON Schema validator. A decode or mapping failure aborts the batch without skipping the record.

## Batch persistence and errors

The importer reads up to the configured number of source lines per batch. For each nonempty batch, the importer commits all mapped rows and one `batch_log` row in one transaction. Batch IDs start at one and increase in commit order. The log records the actual number of input lines in that batch, including a shorter final batch. A readable empty file creates the schema with zero entries and zero batch log rows.

The converter stops at the first input, mapping, or persistence error. If a transaction is active, it rolls back the entire batch, including its log row. Earlier committed batches remain available. A retry requires a fresh output database. Diagnostics go to standard error and identify the error and the one-based source line where it can be determined. CLI exit status is 0 on successful completion, 1 on import failure, and 2 on command-line usage errors.

## Acceptance

| Scenario | Required result |
| --- | --- |
| Three valid lines with batch size two | Three entries in source order and two log rows with line counts 2 and 1. An omitted output path creates the expected sibling `.sqlite` file. |
| Input framing and JSON decoding | An initial BOM, CRLF, and an unterminated final record are accepted. A blank line, invalid UTF-8, malformed JSON, a non-object record, or a bare nonfinite constant fails at the offending line. |
| Related rows and duplicate data | Repeated values appear at their original indices, example keys identify the enclosing sense, linkage `sense_index` retains its supplied value, and the database has zero foreign-key violations. |
| Retained and omitted fields | `etymology_texts`, example offsets, compacted `form_of`, and sound URLs match the [mapping contract](spec/mapping.md). `etymology_links` contributes no rows or columns. Missing, explicit null, and empty values follow the contract for the field's destination. |
| Mapping failure after a committed batch | A missing required mapped field or an invalid mapped container reports the offending source line. No rows or log entry from the failed batch remain. |
| Existing destination or missing `UTF_CI` | Failure preserves the existing destination or leaves the proposed destination absent, respectively. |
| Malformed line after a committed batch | The diagnostic gives the source line, the CLI reports failure, and the database contains only the previously committed entries, children, and log rows. |
| A database write fails within a batch | The batch contributes zero data or log rows, and all earlier commits remain intact. |
| Empty input | Success produces the initialized schema with no entries or batch log rows. |
