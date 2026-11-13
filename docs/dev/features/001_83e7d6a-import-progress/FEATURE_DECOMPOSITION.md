# Import progress decomposition

> Historical feature record. The [main documents](README.md) own the current behavior and tasks.

The importer owns measurement. When called with an optional keyword-only `on_progress` callback, it captures the byte size from the opened input descriptor. After each successful batch write, it accumulates the lengths of the batch's original byte strings and calls `on_progress(processed_bytes, total_bytes)` synchronously. Each successful update follows transaction commit. Calls without a callback retain their silent library behavior and skip progress-specific work.

The CLI supplies the reporter by default and suppresses it with `--no-progress`. The reporter owns percentage formatting, stderr, and flushing. The mapper, batch reader, and database schema retain their existing contracts.
