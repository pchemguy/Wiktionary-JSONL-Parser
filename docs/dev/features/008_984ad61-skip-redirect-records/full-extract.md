# Full-extract verification

The installed 0.4.0 candidate read the original extracted Kaikki Russian Wiktionary dump. Source archive SHA-256 is `fdcb978c76b660e0e43977bbf7487c812e6d42e965b0a73e3f5b4ba6981174c4`. Linux used CPython 3.12.14 and SQLiteICUex 3.54.1, with 7 workers and batches of 10,000 source lines.

| Measure | Result |
| --- | ---: |
| Raw input | 2,633,813,708 bytes |
| Raw source lines | 2,729,136 |
| Standalone redirects skipped | 1,002,924 |
| Imported entries | 1,726,212 |
| Mapped rows across 20 tables | 19,062,746 |
| Committed source batches | 277 |
| Result database | 2,273,820,672 bytes |
| Import wall time | 44.318 s |
| Raw input throughput | 56.68 MiB/s |
| Source lines per second | 61,581 |
| Imported entries per second | 38,951 |

An independent scan reconstructed partition boundaries, every entry ID, and each batch log ID and count from the raw source. It classified the observed `hard-redirect` records by their recorded three-key shape and verified the entry byte stream against the previously generated reference digest. All expected entry IDs and batch log rows matched. Every mapped row in all 20 data tables matched the entry-only SQLite reference after aligning entry IDs by source order. The schema matched, all seven final progress lines equalled the corresponding raw chunk sizes, SQLite integrity returned `ok`, and foreign-key verification returned no rows.

The installed library also preserved source line 2 in a one-worker mixed input. The wheel rebuilt from its source archive matched byte for byte. The verified candidate artifact hashes are:

| File | SHA-256 |
| --- | --- |
| `wiktionary_jsonl_parser-0.4.0-py3-none-any.whl` | `f0ca021eb39c183d9abc8d21b7303931d19348cab39827d4b35ff1b2c4e293e7` |
| `wiktionary_jsonl_parser-0.4.0.tar.gz` | `dff512d816a0cf4fab27ab36d5c0bc86290f734a274f7b10d866a79a13bfe0be` |
| `SHA256SUMS` | `72cdce72c593cbeb49e43bfef8c3057a3d1f5e7e721c5709c03f896822003ac8` |
| `wiktionary-jsonl-parser-python.zip` | `39a76827853ccc70014df021f6b8f220f12c6dc26d17e2202915243e4cc9197b` |
