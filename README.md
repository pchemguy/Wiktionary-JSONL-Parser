# Wiktionary JSONL Parser

Convert an extracted Kaikki.org Russian Wiktionary JSONL file into a relational SQLite database. The import preserves mapped values, duplicate entries, source array order, and relationships between entries, senses, and examples. It includes records for other word languages found in the Russian edition.

## Install

Use Python 3.11 or later with [SQLiteICUex](https://github.com/pchemguy/SQLiteICUex) available to Python's `sqlite3` module. The importer requires the `UTF_CI` collation on new connections. See [Build Python with SQLiteICUex on Linux](docs/linux-sqlite-icuex-setup.md) for a verified Debian setup.

Download `wiktionary-jsonl-parser-python.zip` from the [latest release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/latest) and extract its wheel and source distribution. Set `python_icu` to your SQLiteICUex-enabled Python executable. From the directory containing the extracted wheel, install it with pip:

```bash
"$python_icu" -m pip install ./wiktionary_jsonl_parser-0.4.2-py3-none-any.whl
```

If your private interpreter has no pip, use `uv pip install --python "$python_icu" ./wiktionary_jsonl_parser-0.4.2-py3-none-any.whl`.

## Convert

Supply an already extracted, local UTF-8 JSONL file. The first command writes `data/ru-extract.sqlite`. The second selects an explicit destination and uses batches of at most 5,000 source lines.

```bash
"$python_icu" -m wiktionary_jsonl_parser.cli data/ru-extract.jsonl
"$python_icu" -m wiktionary_jsonl_parser.cli data/ru-extract.jsonl --output data/words.db --batch-size 5000
```

The installed `wiktionary-jsonl-parser` command accepts the same arguments. Workers read separate byte ranges from the input and write their own SQLite databases. The default batch size is 10,000 source lines per worker. After each batch commit, the CLI reports `[chunk N] P/T bytes read and processed (X.Y%)` on stderr, based on that worker's assigned byte range. After a successful import, the CLI reports total processing time on stderr, including merge and publication. Use `--no-progress` to suppress both messages while retaining warnings and diagnostics. Supply `--output` when the input name lacks a final `.jsonl` suffix. The destination's parent directory must exist, and the destination must be new. Publication uses a hard link on POSIX and a rename on Windows.

The importer requests the logical CPU count minus two workers, with one worker when that calculation would be less than one or the CPU count is unknown. It warns when the requested count exceeds SQLite's attachment limit and adjusts the worker count or merges in groups. If the limit is zero and multiple workers were requested, an interactive CLI caller must explicitly confirm a one-worker import. Keep the input file unchanged while the import runs.

Import the extracted Kaikki dump directly. The Russian edition skips objects with a top-level string `redirect` and none of the keys `word`, `lang`, or `lang_code`. Skipped lines still count toward source-position IDs, batch line counts, and byte progress. Entry IDs therefore have gaps where redirects appeared. Other records go through normal decoding and mapping.

## Query and inspect failures

Open the output with a SQLite client that provides `UTF_CI` for queries using that collation. For example, use the same Python interpreter to inspect the imported entries and committed batches:

```bash
"$python_icu" - data/words.db <<'PY'
import sqlite3
import sys
from contextlib import closing

with closing(sqlite3.connect(sys.argv[1])) as db:
    print(db.execute("SELECT id, word, lang_code FROM entries ORDER BY id LIMIT 10").fetchall())
    print(db.execute("SELECT batch_id, line_count FROM batch_log ORDER BY batch_id").fetchall())
PY
```

Each batch commits all its mapped rows and one `batch_log` row together. Entry and batch IDs equal 10,000,000 times the zero-based chunk index plus the one-based local line or batch number. Each chunk can contain up to 10,000,000 lines. A failure discards the import staging files and leaves the destination unpublished. Diagnostics identify the stage and, where available, the chunk and its one-based local line. Exit status is 0 on success, 1 on import failure, or 2 on command-line usage errors.

## Library usage

```python
from wiktionary_jsonl_parser.importer import import_jsonl

import_jsonl("data/ru-extract.jsonl", "data/words.db", batch_size=10_000)
```

Optional keyword-only callbacks report warnings (`on_warning(message)`) and progress (`on_progress(chunk_index, processed_bytes, chunk_bytes)`). Supply `confirm_single_worker()` to authorize the zero-attachment fallback by returning `True`. The callbacks run synchronously in the calling process. Import failures raise `ImportFailure` from the same module.

See the [mapping contract](docs/dev/spec/mapping.md), [schema](docs/dev/spec/schema.sql), and [import specification](docs/dev/SPEC.md) for the stored columns and value rules.

> [!IMPORTANT]
>
> This project is developed with generative AI assistance under human direction. See [AI_DISCLOSURE.md](AI_DISCLOSURE.md) for details.

The development workflow is documented in [SDD-MANAGER.md](SDD-MANAGER.md).
