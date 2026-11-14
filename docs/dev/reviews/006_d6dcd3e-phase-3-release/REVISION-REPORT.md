# Phase 3 candidate corrections

[Review findings](REVIEW-REPORT.md)

| ID | Correction and recheck |
| --- | --- |
| R-001 | A fresh, isolated interpreter loads the caller's package root. An installed CLI and a library caller with a same-named package in the working directory both imported successfully. |
| R-002 | Cancellation handles an exit race and attempts termination and reaping independently for every child. Fault injection verified sibling termination, waits, pipe closure, and preservation of the error detail. |
| R-003 | Publication determines success. A later staging cleanup failure keeps the database and reports a warning. The injected CLI check verified status 0 and the complete published data. |
| R-004 | Staging uses the resolved destination directory. The symlink and parent-traversal regression verified the correct destination and no leftover staging. |
| R-005 | Clamp the internal batch argument to the maximum chunk length. A library batch size with ten thousand digits imported the small fixture as one batch. |
| R-006 | README identifies the publication operation on each platform. T-022 incorporates the canonical documents. |
| R-007 | A read-only attachment test uses names containing spaces, hashes and percent signs, which exercise URI escaping in filenames valid on Windows. Linux executed the check. |

The six new regression cases all failed against the reviewed source and passed after correction. The full Linux SQLiteICUex suite passed 111 tests with two standard-SQLite-specific skips. Both skipped tests passed separately using standard SQLite. Type, formatting and lint checks passed. The installed console entry point and both standalone tools passed their smoke tests. The 0.3.0 candidate was rebuilt and its inventory and checksums passed.

On the same 729.64 MiB sample, the corrected seven-worker CLI took 12.803, 13.246, 12.759 seconds. Median time was 12.803 seconds (56.99 MiB/s, 23,370 lines/s). All three outputs matched the prior seven-worker output byte for byte. The prior sample comparison to the serial reference therefore applies to the corrected output.

| Artifact | Candidate SHA-256 |
| --- | --- |
| `wiktionary_jsonl_parser-0.3.0-py3-none-any.whl` | `3c3bb39d39603b3f535ba757e7c90805b0fdde109b7ac18558c312b5ad41b21b` |
| `wiktionary_jsonl_parser-0.3.0.tar.gz` | `3f1139b759d2de90299d8dc6c1e8f09c279de85296453467b91983bbd3fc1e70` |
| `SHA256SUMS` | `a3e9e6bf06666dbe8fd4068215ff06aaf11d42d4f6003cb895aa5f653fdd2aea` |
| `wiktionary-jsonl-parser-python.zip` | `507f272762aa956b0c58626bf82533f5a5cf80bf11927729fc07e0ba20b3dd19` |
