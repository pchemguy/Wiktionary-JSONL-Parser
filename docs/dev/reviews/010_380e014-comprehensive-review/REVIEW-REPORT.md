# Comprehensive review report

Campaign `010_380e014` reviews `380e014b5118ab34c7a292c43be0fc3120440abc` under the [review plan](REVIEW-PLAN.md). Checks use Linux x86-64 with CPython 3.12 and the 100-attachment SQLiteICUex build, plus standard SQLite for the negative runtime checks.

## U-001 — Converter and test coverage

Reviewed the current design and mapping against the edition, schema, importer, worker, merge and test sources. Verified LF framing, source-order ranges, final ID allocation, redirect gaps, mapping and table order, transactional writes, grouped read-only attachments, cancellation, and no-overwrite publication. Tests exercise both run-plan and ID edges, mapped-value failures, partial batch rollback, worker cancellation, and destination collision. No correction identified in the exercised converter paths.

- The SQLiteICUex suite passed 132 tests. Both standard SQLite negative checks passed separately.
- In 3,000 seeded comparisons across six worker counts, partitioned readers produced the same physical lines as sequential iteration.
- The full local Russian extract imported with seven workers and the default 10,000-line batch in 45.916 seconds. SQLite contained 1,726,212 entries and the batch log totaled 2,729,136 source lines. The difference of 1,002,924 matches the independently counted standalone redirects. Every nonempty chunk reached 100.0%, stdout was empty, `quick_check` returned `ok`, and `foreign_key_check` found zero violations.
- Native Windows execution and instrumented coverage were unavailable. The exercise used source inspection and the declared pytest checks.

## U-002 — Consumer interfaces, tools and documentation

Executed the module CLI and README queries on a fixture. Ran the seven-worker benchmark and a three-input merge with disjoint keys. The merge returned 111 rows and zero foreign-key violations. A duplicate key produced the expected failure and no output. Ruff lint, format, and mypy passed. All 72 maintained relative path references resolved. The current Linux setup recipe was inspected and its deployed runtime used for the checks.

### R-001 — The Windows launcher embeds a workstation path

Medium priority, confirmed by source inspection. `tools/ru-extract.bat` sets `REPO` to `H:\GitHub\Wiktionary-JSONL-Parser` and changes the caller's `PYTHONPATH`. A checkout at another location cannot rely on the launcher to select its own parser sources. Derive the source path from the launcher's location, scope environment changes, and document its default and explicit input forms. Check command construction and available platform evidence.

### R-002 — The manual merge exposes an unfinished output

Medium priority, reproduced with an instrumented schema initializer. `tools/merge_databases.py` creates the destination before attaching sources or writing data. A separate read-only connection observed zero schema objects at that path, and the path disappeared after a forced failure. Stage on the destination filesystem and reuse the importer's no-overwrite publication. Recheck success, invalid input or duplicate keys, and a competing destination.

### R-003 — A benchmark cleanup error can strand other workers

Medium priority, reproduced with controlled child-process doubles. In `tools/benchmark_parallel_import.py`, a termination error stops the cleanup loops, masks an already detected failing chunk, and leaves another child unterminated and unreaped. Reuse the importer's cancellation logic and preserve the primary diagnostic. Recheck a simulated signalling race and a real malformed-input run.
