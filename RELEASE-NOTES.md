# Wiktionary JSONL Parser 0.3.0

- Convert one local extract using fresh Python workers that write independent SQLite databases. The importer merges completed chunks within the available attachment slots and publishes the result in one operation.
- Use 10,000 source lines per worker batch by default. Progress reports committed bytes separately for each chunk. Warnings identify when the requested worker count exceeds SQLite's effective attachment capacity.
- Entry and batch IDs are allocated within each chunk and remain fixed during merge. The SQLite schema and JSON mapping are unchanged. Failed imports leave the destination unpublished.

Download `wiktionary-jsonl-parser-python.zip` for the installable wheel and source distribution. Verify the bundle with `SHA256SUMS`. Use Python 3.11 or later with SQLiteICUex. See the [installation and usage guide](https://github.com/pchemguy/Wiktionary-JSONL-Parser#install).
