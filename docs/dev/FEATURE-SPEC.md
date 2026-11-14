# Skip standalone redirect records specification

The [import specification](SPEC.md) governs framing, decoding, mapping, and failure behavior. These requirements add standalone redirect handling for the Russian Wiktionary edition.

## Record classification

After a source line has decoded to a JSON object under the existing decoder, skip its mapping if the object has a top-level string-valued `redirect` and none of the top-level keys `word`, `lang`, and `lang_code`. An empty string qualifies. `title` and `pos` do not participate in classification. A nested redirect field has no effect. An entry key is present even when its value is null or otherwise invalid. Every object outside the skip rule goes through ordinary mapping and validation. Invalid JSON, invalid UTF-8, and non-object JSON remain errors.

A skipped redirect creates no entry row, child row, or redirect row. Skipping is automatic for the Russian edition through the CLI and library.

## Accounting and output

- Every source line counts toward the existing chunk-local position, chunk line limit, and source-line batch size. Entry IDs use the original formula `10_000_000 * chunk_index + chunk_local_source_line`. Redirects leave gaps at their source positions. Diagnostics retain the original chunk-local positions.
- On a successful batch transaction, `batch_log.line_count` includes mapped records and skipped redirects. A redirect-only batch commits a log row. Progress includes the original bytes of both kinds of records after the batch commits. A redirect-only file produces the SQLite schema and batch log with empty entry and child tables. Empty input retains its existing behavior.
- A failure in a batch or worker follows the existing cancellation and unpublished-output contract. One-worker publication and grouped merging preserve the same IDs and log counts. Keep the default batch size at 10,000 source lines and use the existing CLI and library signatures and SQL schema.
- The benchmark reports input lines per second from committed source-line counts, including skipped redirects. A count of mapped entries represents imported entries.

## Acceptance

| Scenario | Expected result |
| --- | --- |
| Leading, consecutive, and trailing redirects among entries | Entries preserve their exact source-position IDs. Child foreign keys reference those IDs. Committed line and byte totals cover the entire input. |
| All-redirect batch, chunk, or file | There are no rows for redirects. Existing batch boundaries, committed log rows, and complete chunk progress are visible. |
| String, empty string, missing and non-string redirect values, nested fields, and objects containing entry keys | Only objects satisfying the top-level predicate are skipped. Mixed records retain ordinary mapping and validation. |
| Malformed input and range overflow after skips | The importer reports the original source position, fails, and leaves the destination unpublished. Redirects still count at the chunk limit. |
| Full raw extract | The known archive yields 1,726,212 entries from 2,729,136 lines, with 1,002,924 redirects skipped. Verify IDs against the unfiltered source and compare mapped data with the entry-only reference after aligning IDs. Verify integrity, foreign keys, and completed progress. |
