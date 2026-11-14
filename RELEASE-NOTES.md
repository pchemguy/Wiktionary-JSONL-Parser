# Wiktionary JSONL Parser 0.4.0

- Import the full extracted Kaikki Russian Wiktionary JSONL directly. The importer skips standalone redirect objects.
- Entry IDs retain the positions of the original source lines. Redirects leave gaps in IDs and count toward batch totals and progress.

Download `wiktionary-jsonl-parser-python.zip` for the wheel and source distribution and verify it with `SHA256SUMS`. Use Python 3.11 or later with SQLiteICUex. See the [installation and usage guide](https://github.com/pchemguy/Wiktionary-JSONL-Parser#install).
