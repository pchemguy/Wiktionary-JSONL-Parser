# Wiktionary JSONL Parser 0.2.0

The CLI reports cumulative input bytes read and processed after each successful SQLite batch write. The percentage uses the opened file's size, so a preliminary line-counting pass is unnecessary. Progress is flushed to stderr. Use `--no-progress` for quiet runs.

Library callers may supply `on_progress(processed_bytes, total_bytes)` as a keyword argument. The callback runs after each successful batch write. A failed batch produces no progress update.

Download `wiktionary-jsonl-parser-python.zip` for the installable wheel and source distribution, and use `SHA256SUMS` to verify it. The [README](https://github.com/pchemguy/Wiktionary-JSONL-Parser/blob/v0.2.0/README.md) has installation and usage instructions. Python 3.11 or later and SQLiteICUex remain required.
