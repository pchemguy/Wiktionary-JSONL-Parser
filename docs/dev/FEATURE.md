# Parallel importer redesign

Import a local, extracted Wiktionary JSONL file into one SQLite database using the worker-and-merge scheme measured in the [parallel benchmark](reports/importer-performance.md#seven-concurrent-imports-with-ids-assigned-during-insertion). The new execution path preserves the [mapping rules](spec/mapping.md), [SQLite schema](spec/schema.sql), and SQLiteICUex requirement.

## Import pipeline

Divide the input into contiguous, roughly byte-balanced chunks at complete line boundaries. Fresh Windows-compatible Python processes read their assigned ranges directly and write independent temporary SQLite databases. The worker count is `os.cpu_count() - 2`. Each worker uses **10,000 source lines per batch by default** and reports its own byte progress with its zero-based chunk ID after each successful batch commit.

Assign each entry's final ID at insertion as `10_000_000 * chunk_index + chunk_line_number`. The chunk index is zero-based and the local line number is one-based. Dependent rows use that final entry ID. Batch log IDs use the same chunk offset with the local batch number. IDs preserve source order when sorted, with gaps between chunks.

After all workers succeed, merge the schema-compatible databases in source chunk order. Use one `INSERT ... SELECT ... UNION ALL ...` per table in each merge group, keeping foreign keys enabled and inserting parent tables first. Publish the destination only after a successful merge. A worker or merge failure aborts the run, cleans up its owned temporary files, and leaves no partial destination. This replaces the current published-prefix behavior for the parallel path.

## Design decisions to resolve

- Define the public entry point and compatibility behavior for existing CLI and library callers, including quiet mode and diagnostics when only the chunk-local line number is known.
- Define behavior when Python cannot report a CPU count, reports two or fewer CPUs, or the resulting worker count exceeds the SQLite attachment limit. Define how the importer handles a chunk that would exceed its ID range.

## Campaign release gate

Implement the redesigned pipeline, then comprehensively review the exact release candidate. Review Windows-compatible process startup and cancellation, chunk framing, ID ranges and source order, transaction and merge integrity, failure cleanup and destination publication, CLI and library compatibility, throughput, documentation, and packaging. Fix confirmed in-scope findings and repeat the affected checks, regression suite, and release checks on the corrected candidate before tagging or publishing the final campaign release.
