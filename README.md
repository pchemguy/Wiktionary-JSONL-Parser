# Wiktionary JSONL Parser

Convert an extracted Kaikki.org Russian Wiktionary JSONL file into a relational SQLite database. The import preserves mapped values, duplicate entries, source array order, and relationships between entries, senses, and examples. It includes records for other word languages found in the Russian edition.

## Install

Use Python 3.11 or later with [SQLiteICUex](https://github.com/pchemguy/SQLiteICUex) available to Python's `sqlite3` module. The importer requires the `UTF_CI` collation on new connections. See [Build Python with SQLiteICUex on Linux](docs/linux-sqlite-icuex-setup.md) for a verified Debian setup.

Download `wiktionary-jsonl-parser-python.zip` from the [latest release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/latest) and extract its wheel and source distribution. Set `python_icu` to your SQLiteICUex-enabled Python executable. From the directory containing the extracted wheel, install it with pip:

```bash
"$python_icu" -m pip install ./wiktionary_jsonl_parser-0.2.0-py3-none-any.whl
```

If your private interpreter has no pip, use `uv pip install --python "$python_icu" ./wiktionary_jsonl_parser-0.2.0-py3-none-any.whl`.

## Convert

Supply an already extracted, local UTF-8 JSONL file. The first command writes `data/ru-extract.sqlite`. The second selects an explicit destination and uses batches of at most 5,000 source lines.

```bash
"$python_icu" -m wiktionary_jsonl_parser.cli data/ru-extract.jsonl
"$python_icu" -m wiktionary_jsonl_parser.cli data/ru-extract.jsonl --output data/words.db --batch-size 5000
```

The installed `wiktionary-jsonl-parser` command accepts the same arguments. The default batch size is 10,000 source lines. After each successful batch write, the CLI prints the cumulative input bytes read and processed and their percentage of the input file size on stderr. Use `--no-progress` to suppress updates while retaining error diagnostics. Supply `--output` when the input name lacks a final `.jsonl` suffix. The destination's parent directory must exist, and the destination must be new.

Every input line must contain a mappable entry. In particular, a Kaikki redirect record containing `title` and `redirect` but lacking the required entry fields fails at its source line. Prepare an entry-only JSONL file before import if your dump includes those records.

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

Each batch commits all of its mapped rows and one `batch_log` row together. On failure, the command writes a diagnostic to standard error and reports the one-based source line when available. Earlier committed batches remain queryable. To retry, use a fresh output path. Exit status is 0 on success, 1 on import failure, or 2 on command-line usage errors.

See the [mapping contract](docs/dev/spec/mapping.md), [schema](docs/dev/spec/schema.sql), and [import specification](docs/dev/SPEC.md) for the stored columns and value rules.

> [!IMPORTANT]
>
> This project is developed with generative AI assistance under human direction. See [AI_DISCLOSURE.md](AI_DISCLOSURE.md) for details.

The development workflow is documented in [SDD-MANAGER.md](SDD-MANAGER.md).
