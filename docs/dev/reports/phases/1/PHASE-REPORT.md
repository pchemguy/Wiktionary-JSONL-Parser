# Phase 1 — JSONL-to-SQLite converter

**Result — Passed.** The source tree and installed CLI implement the accepted import, mapping and batch transaction contracts.

## Evidence

| Milestone | Verified result |
| --- | --- |
| [1.1 — Entry import](1.1.md) | SQLiteICUex preflight, canonical DDL, JSONL decoding, CLI and atomic entry writes. |
| [1.2 — Complete relational mapping](1.2.md) | Every table checked, including array positions, composite sense/example keys, and parameterized writes. Mapping errors and injected child and batch-log errors preserve the committed prefix. |
| [1.3 — Installable CLI](1.3.md) | Source distribution and wheel include the exact schema. The installed CLI and the source-tree CLI created identical databases. The release inventory and checksums passed. |
| 1.4 — Phase review | Reviewed the full schema, mapper, CLI, importer and package. A regression check caught SQLite treating the literal Linux output filename `:memory:` specially. Using an absolute path for the writing connection restores ordinary file behavior. |

On Debian 13 x86-64, CPython 3.12.14 with SQLiteICUex and SQLite 3.54.1 passed 54 pytest cases. Its two standard-SQLite-only cases were run separately and both passed. Ruff lint, Ruff format, strict mypy, the schema byte comparison and distribution checks passed. Windows execution was outside this verification run.

## Kaikki sample

Read the first 32,893 complete lines from the first 16 MiB of the [Kaikki Russian dump](https://kaikki.org/dictionary/downloads/ru/ru-extract.jsonl.gz). The unmodified prefix stopped at line 1 with the required-field diagnostic and no batch log rows. The prefix contained 2,972 redirect-only records and 29,921 entries. Excluding the redirect-only records for the successful sample preserved the relative order and original bytes of the entries.

The source-tree CLI imported 106,545,145 input bytes and committed 29,921 lines in 6.252 seconds with a 5,000-line batch size. Six log rows summed to 29,921. The entries count agreed, and `PRAGMA foreign_key_check` returned zero violations. The entry sample SHA-256 was `e8ab1ccf1d1db1b3ed797fd99dcbe9af65029d3f370e119b5c47c7e317b7d1dc`.

## Open findings

No blocking implementation findings against the accepted contracts. The unfiltered dump prefix demonstrates a source-format limitation. Redirect-only records need a product decision about storage or omission before the importer can accept them directly. The README describes the entry-only input requirement. No full-dump timing was measured.
