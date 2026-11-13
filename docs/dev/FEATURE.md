# Import progress logging

The Wiktionary JSONL CLI reports progress for large local input files without a preliminary line-counting pass. After each successful batch write, it reports the cumulative input bytes read and processed and their percentage of the input file's size.

## Progress measure

The importer reads binary lines in source-line batches. Measure the raw bytes belonging to each completed batch, including any UTF-8 BOM, line terminators, and an unterminated final record. Use the size of the opened input file as the total. Observe progress after the batch write completes, including for a short final batch. A failed batch produces no progress update for those bytes. A clean import of an unchanged, nonempty file reaches the file's full byte size. Empty input completes without a percentage update.

## CLI behavior

The CLI emits one flushed line to stderr per batch by default. For example:

```text
52428800/209715200 bytes read and processed (25.0%)
```

Use `--no-progress` for scripts that need stderr to contain diagnostics only. Library calls remain silent by default.

The [existing failure and batch guarantees](SPEC.md#batch-persistence-and-errors) govern the import. A progress line describes the current invocation. It adds no state to the output database.
