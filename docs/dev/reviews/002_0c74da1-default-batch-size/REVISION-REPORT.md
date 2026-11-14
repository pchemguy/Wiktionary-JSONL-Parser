# Default batch size revision report

Campaign `002_0c74da1` started from `main` at `0c74da116be8a6014c05835ad8aa6ecd508f80b7`. The [plan](REVISION-PLAN.md) opened in commit `37546fb23150b2a41a497be74bc7075f204db00b`.

Action A-001 sets the CLI default to 10,000 source lines and derives the help text from the argument default. The README, current specification, and default-value test use the same number.

The updated default test failed against the previous value and passed with the new default. The SQLiteICUex pytest run passed 62 tests and skipped two cases specific to standard SQLite. Those two cases passed separately on standard SQLite. Ruff lint and format, strict mypy, and the CLI help check passed.

The CLI imported the project's 29,921-entry Kaikki sample with the batch-size flag omitted. The batch log recorded 10,000, 10,000, and 9,921 lines. The output contained 29,921 entries, the foreign-key check returned zero violations, and the final progress update reached 100.0%. Checks ran on Debian 13 with CPython 3.12.14 and SQLite 3.54.1 with SQLiteICUex.
