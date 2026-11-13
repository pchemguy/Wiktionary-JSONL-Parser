# Wiktionary JSONL Parser

Wiktionary JSONL Parser converts the Kaikki.org extract of the Russian Wiktionary edition into a local relational SQLite database. It is intended for users who want to query and postprocess the extract with SQL.

## Initial scope

The converter reads a local UTF-8 `ru-extract.jsonl` supplied by the caller. The Russian Wiktionary edition determines the input format. Every mappable record is eligible for import, including records whose word language is other than Russian.

The importer runs in one process and reads the input in source order. It processes configurable batches measured in source lines, including a shorter final batch. SQLite persistence is the expected throughput bottleneck and the first target for measurement and tuning.

The SQLite output preserves mapped values, duplicate records, source array order, and the relationships between entries, senses, and examples. The Wiktextract JSON Schema serves as a reference for interpreting fields. The importer decodes JSON and reports malformed input or mapping failures without running JSON Schema validation.

The initial scope starts with an extracted file and ends with the SQLite database. Obtaining, extracting, or streaming archives and using multiprocessing are outside this scope. Additional Russian Wiktionary datasets from Wikimedia may be integrated in a later increment.

## Import behavior

The converter supports fresh imports only. Each batch's mapped rows and a `batch_log` row recording its actual source-line count commit together. If decoding, mapping, or writing fails, the importer stops, reports the source line when known, rolls back the active batch, and retains prior committed batches. To retry, start a fresh import.

SQLiteICUex is required to provide the `UTF_CI` collation. The importer checks that `UTF_CI` is available before creating the output database. SQLite clients also need the collation for queries that use it.

The mapper stores `etymology_texts` and ignores `etymology_links`. The presence of `etymology_links` does not cause a record to be rejected.

The command-line interface requires an input path and accepts an optional output path. By default, it creates the database next to the input file, replacing the final `.jsonl` suffix with `.sqlite`. The converter refuses an existing output file by default.

## Reference inputs

- [Kaikki raw distributions](https://kaikki.org/dictionary/rawdata.html) and [Russian Wiktionary JSON Schema](https://tatuylonen.github.io/wiktextract/ru.json)
- [SQLiteICUex](https://github.com/pchemguy/SQLiteICUex) and [additional Russian Wiktionary dumps](https://dumps.wikimedia.org/ruwiktionary/)
