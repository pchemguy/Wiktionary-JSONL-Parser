# Import progress specification

The `wiktionary-jsonl-parser INPUT [--output PATH] [--batch-size N] [--no-progress]` CLI writes one flushed progress line to stderr after each successful batch write. A progress update reports the cumulative bytes read, decoded, and mapped for batches whose SQLite write is complete. The numerator counts the original bytes, including a BOM, CRLF, LF, and a final line without a terminator. The denominator is the byte size of the opened input file captured at the start. Progress requires no preliminary scan.

For a positive total, use the format `52428800/209715200 bytes read and processed (25.0%)`. Round down to one decimal place so that 100.0% is reached at the full size for an unchanged file. If the initial size is zero but data is encountered, report just the byte count. Percentage semantics assume the input file stays unchanged during import. Empty input emits no progress line.

Decode, mapping, or persistence failure leaves the last reported count at the preceding successful batch and emits the existing diagnostic. `--no-progress` suppresses only progress lines. Stdout stays empty. Library imports remain silent unless the caller supplies a keyword-only `on_progress` callback accepting two integers.

Acceptance covers a raw binary fixture with a BOM, CRLF, multibyte text and an unterminated final line, a short final batch, a writable progress stream, default and suppressed CLI progress, empty input, and failure after an earlier successful batch. Observe the written database from a separate connection during the callback to prove the update follows the batch transaction.
