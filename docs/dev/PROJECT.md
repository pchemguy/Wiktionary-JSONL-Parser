# Wiktionary JSONL Parser

Wiktionary JSONL Parser converts the Kaikki.org extract of the Russian Wiktionary edition into a local relational SQLite database. It is intended for users who want to query and postprocess the extract with SQL.

## Initial scope

The converter reads a local UTF-8 `ru-extract.jsonl` supplied by the caller. The Russian Wiktionary edition determines the input format. Every mappable record is eligible for import, including records whose word language is other than Russian.

The importer runs in one process and reads the input in source order. It processes configurable batches measured in source lines, including a shorter final batch. SQLite persistence is the expected throughput bottleneck and the first target for measurement and tuning.

The output adopts the legacy SQL schema and mapping. It preserves mapped values and duplicates, source array order, and entry and sense relationships. The Wiktextract JSON Schema serves as a reference for interpreting fields. The importer decodes JSON and reports malformed input or mapping failures without running JSON Schema validation.

The initial scope starts with an extracted file and ends with the SQLite database. Obtaining, extracting, or streaming archives and using multiprocessing are outside this scope. Additional Russian Wiktionary datasets from Wikimedia may be integrated in a later increment.

## Proposed behavior

| Decision | Proposal |
| --- | --- |
| Invocation and output safety | Require explicit input and output paths. Refuse an existing output file by default. |
| Interrupted imports | Adapt `batch_log` to record each committed batch's actual source-line count. Commit the log row and mapped rows in one transaction. If a record cannot be decoded, mapped, or written, stop, report its source line when known, roll back the active batch, and retain prior committed batches. Defer resuming until source identity can be checked. |
| SQLite collation | Retain `UTF_CI` with the SQLiteICUex comparison semantics required by the legacy schema. The importer checks availability before creating its output. SQLite clients must register it for queries that use it. |
| Unmapped fields | Keep the legacy mapping and document omissions, including `etymology_links`, which the current source schema defines. |

## Reference inputs

- [Kaikki raw distributions](https://kaikki.org/dictionary/rawdata.html) and [Russian Wiktionary JSON Schema](https://tatuylonen.github.io/wiktextract/ru.json)
- [Legacy SQL schema](https://github.com/pchemguy/NLP_Tools/blob/890b55b35905a9195653d161ad09057a15a85238/ruwiktionary_rawdb/src/ruwiktionary_rawdb/ru.schema.sql) and [mapping implementation](https://github.com/pchemguy/NLP_Tools/blob/890b55b35905a9195653d161ad09057a15a85238/ruwiktionary_rawdb/src/ruwiktionary_rawdb/mapping.py)
- [Legacy README](https://github.com/pchemguy/NLP_Tools/blob/890b55b35905a9195653d161ad09057a15a85238/ruwiktionary_rawdb/README.md), [converter specification](https://github.com/pchemguy/NLP_Tools/blob/890b55b35905a9195653d161ad09057a15a85238/ruwiktionary_rawdb/ruwiktionary_jsonl_to_sqlite_SPEC.md), and [implementation plan](https://github.com/pchemguy/NLP_Tools/blob/890b55b35905a9195653d161ad09057a15a85238/ruwiktionary_rawdb/ruwiktionary_rawdb_IMPLEMENTATION_PLAN.md)
- [SQLiteICUex](https://github.com/pchemguy/SQLiteICUex) and [additional Russian Wiktionary dumps](https://dumps.wikimedia.org/ruwiktionary/)
