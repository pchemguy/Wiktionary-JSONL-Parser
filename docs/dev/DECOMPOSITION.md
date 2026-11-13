# Decomposition

The [architecture](ARCHITECTURE.md) uses one import loop and one output SQLite connection. The CLI invokes the importer. The importer owns batch processing and the connection, calls the mapper, and writes the mapped rows.

| Unit | Interface and ownership |
| --- | --- |
| CLI | `main(argv: Sequence[str] \| None = None) -> int` parses the command line, resolves the output path, and calls `import_jsonl` with the input path, resolved output path, and batch size in source lines. When the output path is omitted, the CLI keeps the input directory and replaces the final `.jsonl` suffix with `.sqlite`. It formats and flushes progress to stderr unless quiet mode is selected, emits diagnostics, and returns the process status. |
| Importer | `import_jsonl(input_path: Path, output_path: Path, batch_size: int, *, on_progress: Callable[[int, int], None] \| None = None) -> None` runs a fresh import. It owns the input file, source line counter, entry ID allocation, current batch, and the output connection. It completes normally on success and raises an import error on failure, carrying the source line when known. |
| Mapping function | `append_record_rows(record, entry_id, rows_by_table) -> None` maps one decoded JSON object into the current batch. It appends parameter tuples in the fixed column order for each table. Its inputs are the decoded object, the assigned integer entry ID, and the batch's row lists. |

## Batch data

The importer reads up to `batch_size` complete lines in source order, then decodes each as UTF-8 JSON and passes its object to the mapping function. The batch holds row lists keyed by destination table. Tuples in each list follow source order, including the order of repeated values. The mapping function stores `etymology_texts` and leaves `etymology_links` out of the output.

The importer assigns entry IDs in source order before insertion so that dependent rows can use their parent keys when tuples are built. An entry owns its senses. A sense is identified by its entry ID and its position within the entry, and an example carries that sense key. The database schema defines the remaining table relationships.

## Progress reporting

When progress is requested, the importer reads the initial size from the opened input descriptor. After each successful write, it adds the original lengths of the batch's binary lines to the running count and calls `on_progress(processed_bytes, total_bytes)`. The CLI owns formatting and output.

## SQLite writes

The importer checks for SQLiteICUex's `UTF_CI` collation before creating the output. On the output connection, it enables foreign-key enforcement before starting any batch transaction.

For each batch, the importer adds the `batch_log` tuple with the actual number of source lines. It opens one transaction and makes exactly one `executemany()` call for each populated table, including `batch_log`. Each table uses a fixed parameterized `INSERT` statement with all tuple values bound. Parent tables precede dependent tables, including senses before examples. The importer commits once after all inserts succeed and rolls back an active transaction on failure.

Mapping can be checked with decoded objects and empty row lists. The write path can be checked with multiple table lists and an induced insert failure to verify that the batch data and its log entry share a transaction.
