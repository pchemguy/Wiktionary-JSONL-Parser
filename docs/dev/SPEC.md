# Importer specification

Convert one local, extracted UTF-8 Wiktionary JSONL file into one new SQLite database using Windows-compatible worker processes. The [project brief](PROJECT.md) defines the worker policy, the [architecture](ARCHITECTURE.md) defines process and publication ownership, and the [decomposition](DECOMPOSITION.md) defines the components. The public CLI and library import the Russian Wiktionary edition. The [DDL](spec/schema.sql) and [mapping rules](spec/mapping.md) govern its output. The input must remain unchanged throughout the run. Downloading, archive extraction or streaming, JSON Schema validation, and resumption are outside this import contract.

## Entry points

```text
wiktionary-jsonl-parser INPUT [--output PATH] [--batch-size N] [--no-progress]
```

Input is a readable local JSONL file. Resolve relative paths from the caller's working directory. Keep the output on a filesystem that supports no-overwrite publication via a hard link on POSIX or a rename on Windows. If output is omitted, replace a final `.jsonl` suffix with `.sqlite` in the input's directory. For other input names require an explicit output. The output parent directory must exist and the destination must be new. Batch size is a positive integer and defaults to 10,000 source lines per worker transaction. CLI status is 0 for success, 1 for import failure, and 2 for argument errors.

The library operation is `import_jsonl(input_path, output_path, batch_size=10_000, *, on_warning=None, confirm_single_worker=None, on_progress=None) -> None`. Resolve the input and output path arguments relative to the caller’s working directory. The call runs synchronously and raises an import error with the failure stage and chunk/local line where available. The callbacks run in the importing process:

| Callback | Contract |
| --- | --- |
| `on_warning(message: str) -> None` | When supplied, receives the requested worker count and effective attachment limit if the count exceeds that limit. |
| `confirm_single_worker() -> bool` | Invoked only for multiple requested workers and zero attachment capacity. Only an explicit affirmative result authorizes one worker. Without a handler or with unavailable or negative confirmation, fail before launching any worker. |
| `on_progress(chunk_index: int, processed_bytes: int, chunk_bytes: int) -> None` | When supplied, receives each worker's cumulative bytes after that worker commits a batch. |

An exception from a callback invoked before publication aborts the import. The CLI sends warnings and diagnostics to stderr and prompts for confirmation only when interactive input is available. Decline, noninteractive input, or end of input leaves the import unstarted. Stdout stays empty. `--no-progress` suppresses progress messages. Diagnostic and confirmation handling still applies.

## Bootstrap and partitioning

Before starting workers, open the input, verify destination eligibility and SQLiteICUex's `UTF_CI`, and read `L = con.getlimit(sqlite3.SQLITE_LIMIT_ATTACHED)`. Compute the requested count `W = cpu_count - 2` if the reported logical CPU count exceeds two. Otherwise request one worker. Warn when `W > L`, including the direct single-worker case with `L = 0`.

| Condition | Run plan |
| --- | --- |
| `W = 1` | Use one worker for the whole input. Publish its completed database directly. |
| `W > 1` and `L = 0` | Confirm one worker or abort before launch. |
| `1 < W <= L` | Use `W` workers and merge once. |
| `1 <= L < W` and `2 * W < 3 * L` | Use `L` workers and merge once. |
| `1 <= L < W` and `2 * W >= 3 * L` | Use `W` workers and merge consecutive groups of at most `L` databases. |

The staged merge database opens as `main`. Every attachment slot is available for a worker database. At `L = 1` and `W > 1`, use all requested workers and attach their databases one at a time.

Split the file into ordered half-open byte ranges. Place the nominal boundaries at integer divisions of the input size across workers, advancing any interior boundary to the first complete-line boundary at or beyond it. Treat the end of the file as a boundary, including when the last record has no terminator. Coincident boundaries yield empty ranges. The ranges cover the full input exactly once in source order, and workers read them directly. Only an initial UTF-8 BOM at source byte zero is accepted. LF and CRLF end records. Blank lines, invalid UTF-8, invalid JSON, bare nonfinite tokens, and non-object lines fail the import. Duplicate object keys retain the last value. A readable empty file produces the initialized schema without rows or progress updates.

## Russian record handling

After a line decodes to a JSON object, the Russian edition skips it if its top-level `redirect` is a string and none of the top-level keys `word`, `lang`, and `lang_code` is present. An empty redirect string qualifies. Nested values, `title`, and `pos` do not determine classification. An entry key is present even when its value is null. All other objects go through normal mapping and validation. Skipped objects produce no entry or child rows.

## Worker writes and publication

Use a zero-based chunk index `i` and a one-based chunk-local source line number `n`. Assign `entries.id = 10_000_000 * i + n`. Every source line, including a skipped redirect, advances the local position. Redirects leave gaps in entry IDs. Each chunk supports local line numbers 1 through 10,000,000 inclusive. An attempt to exceed that range or the SQLite integer key range fails the run. Child foreign keys use the final entry ID. Child indices preserve the [mapping rules](spec/mapping.md). Batch IDs use the same chunk offset plus the one-based local batch number. Batch-log line counts include every processed source line in a committed batch, including skipped redirects and a shorter last batch. A redirect-only batch commits its log row. A redirect-only file produces the schema and batch logs with no mapped rows.

Each worker opens its own file handle and SQLite connection. It fully decodes and maps each batch, then uses one transaction and one parameterized `executemany()` per populated table. It writes parent tables before dependents and commits the batch log with the data. Foreign keys are enforced. CLI progress reports `[chunk N] P/T bytes read and processed (X.Y%)` after each successful batch commit. `P` counts the original bytes of mapped and skipped lines processed in committed batches by that worker and `T` is the byte length of its range. Round percentages down to one decimal place, reaching 100.0% at that chunk's end. Progress is independent for each chunk. The final destination is ready after successful publication.

Wait for all worker databases to close successfully. For multiple workers, attach each merge group read-only, insert parent tables before dependents with foreign keys enabled, copy IDs directly, and release each group before the next. Use one `INSERT ... SELECT ... UNION ALL ...` per table and group, with an ordinary `INSERT ... SELECT ...` for single-source groups. One worker publishes its closed staged database directly. Publish the result with a no-overwrite file operation on the destination filesystem after all work succeeds.

On failure cancel and reap owned workers, close connections and remove owned staging files. Leave the requested destination unpublished and preserve any preexisting destination. Retain the original diagnostic if cleanup also fails. The CLI identifies the failing chunk and local line where known. Restart after a failure uses a fresh import. If staging cleanup fails after publication, keep the completed destination and send a warning through the configured handler. The import remains successful.

## Acceptance

| Scenario | Expected evidence |
| --- | --- |
| Bootstrap limits | Exact fit, reduction, equality at the 1.5 threshold, grouped merges, one-worker fallback for small or unknown CPU counts, and positive/negative/unavailable zero-limit confirmation. Warnings follow `W > L`. |
| Standalone redirects | Mixed and redirect-only input preserve original source positions, batch logs and progress. A full raw Kaikki import matches the entry-only reference after aligning keys. |
| Input framing | Byte-boundary, CRLF, beginning BOM, later BOM rejection, long line spanning multiple nominal partitions, coincident empty ranges, unterminated record, and empty file. |
| Keys and batch writes | Entries, child relationships, and batch IDs match the chunk formulas. Both ID-range edges are tested. Parent ordering and one transaction per batch hold for short and full batches. |
| Worker and merge failure | Cancel and reap children, discard staged results, and preserve the destination on decode, mapping, worker-exit, merge, or publication failure. |
| Successful publication and progress | Direct one-worker publication and grouped merge both produce the expected data. Progress follows committed batches, quiet mode suppresses progress, and every completed nonempty chunk reaches 100.0%. |
| Runtime and installation | Fresh worker startup, CLI and library operation, and the packaged schema work with SQLiteICUex. Exercise Linux and Windows-compatible process paths. Record target-native execution separately. |
