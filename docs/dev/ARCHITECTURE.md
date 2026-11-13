# Architecture

The command-line interface passes the input path, output path, and batch size to a single-process importer. The importer checks that SQLiteICUex provides `UTF_CI` before creating the output, then uses one SQLite connection with foreign keys enabled. See the [project brief](PROJECT.md) for the input and output scope.

## Import loop

1. Read the UTF-8 input in source order, tracking the source line number. Decode each line, apply the project's field mapping, and insert the entry and its related rows.
2. At the configured line count or the end of a nonempty final batch, insert a `batch_log` row with the actual batch line count and commit it in the same transaction as the data.
3. On a read, decode, mapping, or database error, stop and roll back any active batch. Report the source line when known. Previously committed batches remain in the database. A retry starts a fresh import.

The loop holds one record's decoded and mapped data at a time. The mapping rules determine which values go into which rows. SQLite assigns entry IDs and enforces relationships between rows.
