# Architecture

The command-line interface passes the input path, output path, and batch size to a single-process importer. The importer checks that SQLiteICUex provides `UTF_CI` before creating the output, then uses one SQLite connection with foreign keys enabled. See the [project brief](PROJECT.md) for the input and output scope.

## Import loop

1. Read up to the configured number of UTF-8 source lines into a batch. Preserve source order and process a shorter final batch at end of input.
2. Decode the batch and map its records to related SQLite rows.
3. Write the entire batch in one SQLite transaction, including a `batch_log` row with the actual source-line count.

A read, decode, mapping, or database error stops the import. Roll back any active transaction and report the source line when known. Earlier committed batches remain in the database. A retry starts a fresh import.
