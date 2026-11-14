# Release tool

`build_release.py` builds the Python source distribution and wheel from the checkout and prepares the two GitHub release downloads. Run it with Python 3.11 or later and the `build` package. Use a repository checkout with the bundled release inventory checker.

```bash
python tools/build_release.py
```

The build writes the installable distributions to `dist/` and stages `wiktionary-jsonl-parser-python.zip` and `SHA256SUMS` in `release/`. The ZIP uses the distributions' installable filenames internally. The script reads the version from `pyproject.toml` and checks the full staging inventory. It does not create a tag or upload files.

Use `--dist PATH` and `--release PATH` to select alternate directories. The staging directory must be absent or empty. To build without an isolated build environment, supply `--no-isolation` and provide Hatchling and its dependencies to the same interpreter. Verify the bundle from the staging directory with `sha256sum -c SHA256SUMS`.

## Merge pre-keyed import databases

Run `merge_databases.py` with the parser installed and [SQLiteICUex available](../docs/linux-sqlite-icuex-setup.md) in the same Python interpreter.

```text
python tools/merge_databases.py merged.sqlite part-1.sqlite part-2.sqlite part-3.sqlite
```

Pass completed importer databases in source order, using a new path for the destination. Each input must use the same importer schema. Assign disjoint `entries.id` and `batch_log.batch_id` ranges before calling the tool. Carry each entry offset through the related `entry_id` and `examples.sense_entry_id` columns. Keep child indices within each entry or sense unchanged.

The tool attaches the inputs read-only and inserts each table with a single `INSERT ... SELECT ... UNION ALL ...` statement. Foreign keys are checked with parent tables inserted first. All table inserts commit in one transaction. Its timer includes creating the destination schema, attaching and checking schemas, copying rows, and committing. Prepare IDs before timing so the reported duration measures the merge itself.

## Benchmark parallel imports

Run `benchmark_parallel_import.py` with the parser installed in Python 3.11 or later with SQLiteICUex. The command below also works in Windows CMD:

```text
python tools/benchmark_parallel_import.py ru-extract.jsonl parallel.sqlite
```

Supply an unchanged, uncompressed local Russian Wiktionary JSONL file and a new output path. This benchmark splits the file by bytes at complete line boundaries and starts `os.cpu_count() - 2` fresh Python processes. Each reads its part of the original file directly and uses the importer's worker to write a temporary SQLite database beside the destination. The SQLite attachment limit must accommodate all workers. Workers retain the 10,000-line batch size and report local progress on stderr, labeled `[chunk N]`.

Entry IDs are the one-based line number within the chunk plus `10_000_000 * chunk_index`, with a zero-based chunk index. Batch IDs use the same offset and a one-based local batch number. The mapper writes related foreign keys using the final IDs. A chunk can contain up to 10,000,000 lines. The merge copies the stored IDs in source chunk order.

A worker failure stops the run, terminates remaining workers, and discards the temporary databases. The destination appears only after all chunks and the final merge succeed. Publication uses rename on Windows and a hard link on POSIX, so the output filesystem must support the corresponding operation. The benchmark prints partition, worker wall time, merge and publication, cleanup, total time, and throughput. Input lines per second include skipped redirects, while imported entries per second count mapped entries. The timer starts after runtime and output-path preflight and creation of the temporary directory.

## Run from a Windows checkout

Use `tools\ru-extract.bat` in Windows CMD with a SQLiteICUex-enabled `python` on `PATH`. The launcher uses the checkout's `src` directory, so the package can be imported without installation.

```text
tools\ru-extract.bat "C:\Data\ru-extract.jsonl" --no-progress
```

With no arguments, the launcher reads the same-named JSONL file beside the batch file. If you copy the launcher outside the checkout, set `WIKTIONARY_JSONL_PARSER_ROOT` to the checkout path before running it. The launcher scopes its `PYTHONPATH` changes to the command and returns the parser's exit status. The parser writes the SQLite database next to the JSONL by default. Use `--output` to choose a different new destination.
