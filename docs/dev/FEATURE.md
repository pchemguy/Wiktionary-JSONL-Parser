# Skip standalone Russian Wiktionary redirects

Import the full Kaikki Russian Wiktionary JSONL extract directly. Skip standalone redirect records during import by default. Redirect targets and metadata are outside the SQLite output.

## Record handling

After decoding a source line as a JSON object, skip it if its top-level `redirect` value is a string and the object has none of the top-level entry keys `word`, `lang`, or `lang_code`. The decision uses the object structure. It does not depend on a particular `pos` or `title`. A record with any of the entry keys continues through ordinary entry mapping and validation even if it also has a `redirect` field. Malformed JSON and unsupported entry records retain the existing failure behavior.

## Source positions and batches

Keep the existing entry ID formula, `10_000_000 * chunk_index + chunk_local_source_line`. Count every source line, including skipped redirects. Redirect lines leave gaps in entry IDs and count toward the per-chunk line limit. Failure diagnostics use the same chunk-local source positions.

Use the current source-line batch boundaries and record all successfully processed source lines in `batch_log.line_count`, including redirects. A redirect-only batch writes its batch-log row. Include skipped bytes in progress after the batch commits, so each processed nonempty chunk reaches 100%. An input containing only redirects produces the schema and batch log with no entries or related rows.

The CLI, library and SQLite schema require no additional options or fields. The 10,000-source-line default and the existing worker, merge and publication behavior apply.
