# Architecture

The command-line interface invokes a single-process importer for local UTF-8 JSONL. The importer reads source lines in order in configurable batches, then decodes and maps each batch to related SQLite rows. See the [project brief](PROJECT.md) for the import scope.

The importer writes through one SQLite connection and requires SQLiteICUex for the `UTF_CI` collation. Each batch and its `batch_log` row commit in one transaction, with referential integrity enforced. If a batch fails, none of its rows are committed and earlier commits remain intact.
