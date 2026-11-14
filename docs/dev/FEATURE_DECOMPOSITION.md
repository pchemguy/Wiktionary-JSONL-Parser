# Parallel importer decomposition

The [architecture](FEATURE_ARCHITECTURE.md) separates the caller-facing import operation, the worker's batch loop, and assembly of the final database. The importer owns the lifetime of the run. The decoder, mapper, and SQLite schema are shared by all workers.

## Component interfaces

| Component | Responsibility and interface |
| --- | --- |
| CLI | `main(argv) -> int` parses source, destination, batch size, and quiet mode. It invokes the importer, supplies warning, confirmation, and progress handlers, and renders diagnostics. |
| Importer | `import_jsonl(input_path, output_path, batch_size=10_000, *, on_warning=None, confirm_single_worker=None, on_progress=None) -> None` runs one import. It owns bootstrap, staging, worker supervision, selection of the database to publish, and publication. It reports import failures to the caller. |
| Run planning | Accepts the input size, reported CPU count, effective SQLite attachment limit, and any required confirmation. Produces the number of workers and maximum merge group size by applying the [accepted policy](FEATURE.md#worker-count-and-attachment-limit). Partitioning then produces the ordered input ranges. |
| Worker | Receives a chunk descriptor, input and temporary output paths, and the batch size. Opens its own input and SQLite connection, reads its assigned range, maps records, commits batches, and sends progress or failure information to the importer. |
| Mapper | `append_record_rows(record, entry_id, rows_by_table) -> None` consumes the decoded record and its assigned final entry ID. It appends tuples in the shared schema's column order according to the [mapping rules](spec/mapping.md). |
| Merger | Receives completed worker database paths in chunk order, a staged destination, and the merge group size. It opens the staged database as `main`, attaches read-only sources for each group, inserts their rows, and releases the attachments before the next group. |

The importer calls `on_warning(message)` when a warning applies. It calls `confirm_single_worker() -> bool` only when multiple workers are requested and the attachment limit is zero. An unavailable confirmation handler ends the run at that decision. When supplied, `on_progress(chunk_index, processed_bytes, chunk_bytes)` receives each worker's progress in the importing process. The CLI writes independently labeled updates to stderr. Quiet mode suppresses progress, while warnings, confirmation, and diagnostics remain visible.

## Worker inputs and lifecycle

A chunk descriptor contains its zero-based index and a half-open byte range `[start, stop)`. The planner finds boundaries on complete lines and assigns descriptors in source order. Workers start as fresh Python processes through a Windows-compatible entry point. Each process receives only its paths, descriptor, and options. Workers return status, diagnostics, and progress. The importer receives mapped data through their completed SQLite files.

The importer starts and reaps every worker it owns. A failed process, including an unexpected exit, stops the run. The importer terminates and waits for other running workers before removing staged files. A worker's diagnostic includes the chunk index and local line number where available.

## Batch and merge operations

Each worker reads at most the configured source-line count into a batch, decodes the lines, and builds parameter tuples. Its one-based local line number and chunk index determine the final entry ID. The worker checks the reserved ID range before inserting and gives the mapper the final ID for use in dependent rows. Batch-log IDs use the same chunk offset and a one-based local batch number.

A worker enables foreign keys. For each batch it uses one transaction and exactly one parameterized `executemany()` per populated table, with parent rows before dependent rows. It commits the batch log in that transaction and emits byte progress after the commit. A failed batch causes the worker to fail.

The merger starts after all worker databases are closed. For each group it runs one `INSERT ... SELECT ... UNION ALL ...` per table, with a single-source group using the corresponding `INSERT ... SELECT ...`. It copies stored keys directly and writes parent tables first with foreign keys enabled. After every group succeeds and the staged destination closes, the importer publishes it. With one worker, the importer publishes that worker's completed database directly.

## Verification seams

Test planning with supplied CPU and attachment limits, partitioning with small files and known line boundaries, workers with chosen chunks and expected IDs, and the merger with small staged databases. Exercise the full importer for cancellation, cleanup, and final publication. Measure progress at committed batch boundaries and check that an error leaves the destination unpublished.
