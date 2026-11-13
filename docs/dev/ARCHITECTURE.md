# Architecture

The converter is a single-process Python pipeline for local Wiktextract JSONL. Its input, output, and scope are defined in the [project brief](PROJECT.md).

## Pipeline

| Block | Responsibility |
| --- | --- |
| Command-line interface | Accept the input path, output path, and batch size. Hand the request to the import coordinator and present its progress, result, or error. |
| Import coordinator | Run the conversion in source order. Set batch boundaries by source-line count, pass each numbered line through decoding and mapping, and request commit at a full batch or a nonempty final batch. |
| JSONL reader and decoder | Read the local UTF-8 file sequentially and track physical line numbers. Decode one JSON object per line and identify the source line when decoding fails. |
| Relational mapper | Translate decoded objects into entry data and dependent rows. Preserve source order within arrays, retain duplicates, and associate examples with their enclosing senses. The mapping rules and their outputs are independent of file and database access. |
| SQLite writer | Own the database schema, connection, foreign-key enforcement, generated entry identifiers, inserts, and transaction lifecycle. Write entry, sense, and dependent rows in dependency order. |

The CLI calls the coordinator. The coordinator calls the reader and decoder, mapper, and writer. The writer consumes mapped values and resolves database identifiers. Each source record is processed within the active batch, so a batch can be committed without buffering its entire decoded or mapped content. The importer does not require a preliminary file scan.

## Persistence and failure boundaries

The SQLite writer opens one output connection after the importer checks that SQLiteICUex supplies `UTF_CI`. The caller supplies an SQLite runtime with SQLiteICUex available to Python. Queries in downstream SQLite clients that use `UTF_CI` also require that collation on their own connections. The runtime check occurs before output creation.

Each nonempty batch is one SQLite transaction. The coordinator supplies the actual batch line count, and the writer commits one `batch_log` row with the mapped rows. A failed batch is rolled back. Earlier committed batches remain available, and the CLI reports the import failure with the source line when known. Successful completion requires reaching end of input and committing any final batch. A retry starts a fresh import.

SQLite persistence is the expected bottleneck. A single writer and configurable transaction size keep the write path measurable without introducing concurrency. Any later write optimization must preserve source ordering, referential integrity, and the batch commit boundary.

A future Wikimedia input can have its own reader and mapping. Sharing the writer would depend on whether its mapped data fits the SQLite schema and transaction model.
