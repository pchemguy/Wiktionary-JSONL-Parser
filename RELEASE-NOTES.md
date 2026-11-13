# Wiktionary JSONL Parser 0.1.0

The initial release converts extracted Kaikki Russian Wiktionary JSONL entries into a SQLite database. It creates the database alongside the input by default. Use `--output` to choose another location and `--batch-size` to control the number of source lines per transaction.

- Imports the complete entry, linkage, form, sense, example, translation, sound, and hyphenation mappings and preserves their order and duplicates.
- Records every committed batch in `batch_log`. On a failed batch, its rows and log entry roll back together and earlier batches stay queryable.
- Requires Python 3.11 or later with SQLiteICUex's `UTF_CI` collation available to `sqlite3`.

Kaikki redirect-only records lack required entry fields and fail at the source line. Prepare an entry-only input for dumps that contain redirects.

Download `wiktionary-jsonl-parser-python.zip` for the installable wheel and source distribution. Verify the ZIP using the accompanying `SHA256SUMS`. See the [README](README.md) for installation, runtime setup, and CLI commands.
