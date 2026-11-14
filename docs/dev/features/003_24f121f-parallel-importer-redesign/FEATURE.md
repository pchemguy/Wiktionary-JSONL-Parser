# Parallel importer

The importer converts a local, extracted Wiktionary JSONL file into one SQLite database. It uses the [mapping rules](../../spec/mapping.md), the [SQLite schema](../../spec/schema.sql), and SQLiteICUex.

## Development phases

Develop the single-process importer first to establish the mapping, persistence, and progress behavior. Then [benchmark](../../reports/importer-performance.md) partitioning, independent imports, and SQLite merges. The multiprocessing phase follows the measured [worker-and-merge design](../../reports/importer-performance.md#seven-concurrent-imports-with-ids-assigned-during-insertion).

## Import pipeline

Divide the input into contiguous, roughly byte-balanced chunks at complete line boundaries. Start one fresh Windows-compatible Python process per chunk. Each worker reads its range directly and writes an independent temporary SQLite database. Workers default to **10,000 source lines per batch** and report byte progress with their zero-based chunk ID after each successful batch commit.

### Worker count and attachment limit

Let `W = os.cpu_count() - 2` when Python reports more than two logical CPUs. Use one worker when the CPU count is unavailable or at most two. Whenever the worker count is one, the worker processes the whole input and writes the complete database to a staging path. After the worker succeeds and closes the database, publish that file directly. This path requires zero SQLite attachments.

At bootstrap, read `L = con.getlimit(sqlite3.SQLITE_LIMIT_ATTACHED)`. Open the staged destination as `main`, so all `L` attachment slots are available for worker databases. Warn whenever the requested worker count `W` exceeds `L`. This includes `W = 1` with `L = 0`, where the single worker proceeds directly.

For `W > 1` and `L = 0`, ask the user to confirm running with one worker after issuing the warning. On explicit confirmation, set `W = 1` and publish the completed worker database directly. If the user declines or confirmation is unavailable, abort before starting any worker.

For `W > 1` and `L >= 1`, apply these rules:

| Condition | Workers | Merge groups |
| --- | ---: | --- |
| `L >= W` | `W` | One group |
| `L < W < 1.5 * L` | `L` | One group |
| `W >= 1.5 * L` | `W` | Groups of at most `L` databases |

For `L = 1` and `W > 1`, keep all workers and merge one worker database at a time. For `L = 10`, a request for 10 workers proceeds with all 10, a request for 14 uses 10, and a request for 15 proceeds with groups of 10 and 5.

### IDs and destination

Assign each entry's ID at insertion as `10_000_000 * chunk_index + chunk_line_number`, using a zero-based chunk index and a one-based line number. Dependent rows use the assigned entry ID. Batch log IDs use the same chunk offset with the one-based local batch number. Sorting by ID preserves source order. If any worker exceeds its ID range, abort the entire run.

When multiple workers are used, wait for all to succeed and merge their databases into one staged destination in source chunk order. Use one `INSERT ... SELECT ... UNION ALL ...` per table per merge group. Keep foreign keys enabled and insert parent tables before child tables. Publish the destination only after every merge group succeeds. A worker or merge failure aborts the run, cleans up its owned temporary files, and leaves the requested destination unpublished. Identify the chunk and chunk-local line in diagnostics where available.

## Campaign release gate

Comprehensively review the exact release candidate after implementation. Cover Windows-compatible process startup and cancellation, chunk framing, worker and attachment-limit boundaries, ID ranges and source order, transaction and merge integrity, failure cleanup and destination publication, CLI and library behavior, throughput, documentation, and packaging. Fix confirmed in-scope findings and rerun the affected checks, regression suite, and release checks before tagging or publishing the final campaign release.
