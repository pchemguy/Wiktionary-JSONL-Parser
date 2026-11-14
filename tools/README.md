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
