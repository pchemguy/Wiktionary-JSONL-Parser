# Importer benchmark and profile

Measured the [v0.2.0 release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/tag/v0.2.0) at `febb34006911b5c4bea39084fb79ef9aa3b4666c` on Debian 13 x86-64 with CPython 3.12.14 and SQLite 3.54.1 with SQLiteICUex. The runner reported an AMD EPYC 9V74 CPU and an overlayfs workspace.

The workload was the 29,921-entry, 106,545,145-byte Kaikki sample described in the [Phase 1 report](phases/1/PHASE-REPORT.md#kaikki-sample). Its SHA-256 is `e8ab1ccf1d1db1b3ed797fd99dcbe9af65029d3f370e119b5c47c7e317b7d1dc`. The input excludes redirect-only records from the original prefix.

## End-to-end benchmark

Ran the CLI in a new Python process three times per batch size, with progress enabled and stderr captured. Every run wrote to a new on-disk database. Timing includes process startup and exit. Entry counts, batch log totals, the final progress line and foreign-key integrity were verified outside the timed interval. The input had been read for checksum verification before timing, so these runs represent warm-input behavior.

| Batch size, lines | Transactions | Trials, s | Median, s | Input MiB/s | Entries/s |
| ---: | ---: | --- | ---: | ---: | ---: |
| 25,000 | 2 | 7.077, 5.961, 6.469 | 6.469 | 15.71 | 4,625 |
| 5,000 | 6 | 6.041, 5.782, 6.155 | 6.041 | 16.82 | 4,953 |

The trial times overlap. The small median difference is specific to this sample and environment.

## Pipeline profile

After benchmarking, measured the existing CLI stages using monotonic wall-clock timers on a new database at 25,000 lines per batch. The top-level stages below are mutually exclusive. The profile ran in-process, with timer overhead included. SQLite child timings are included in the SQLite row.

| Stage | Seconds | Share of instrumented wall time |
| --- | ---: | ---: |
| Mapping and serialization | 2.775 | 44.7% |
| SQLite batch writes | 1.955 | 31.5% |
| UTF-8 and JSON decoding | 0.987 | 15.9% |
| Binary batch reads | 0.184 | 3.0% |
| Schema initialization | 0.037 | 0.6% |
| Other import work and timer overhead | 0.275 | 4.4% |
| **Total** | **6.213** | **100.0%** |

Mapping and serialization took the most time. A separate `cProfile` run identified flat child mapping, retained JSON serialization, and text field validation within that stage. It observed 620,197 calls to `json.dumps()`, with 2.406 seconds of cumulative time in the profiler run. That cumulative time includes descendants and is separate from the stage timings above.

SQLite took 1.955 seconds. Its 40 `executemany()` calls accounted for 1.913 seconds, and two commits accounted for 0.041 seconds. The two progress output calls together took roughly 0.11 ms. These measurements identify the bottleneck for this entry sample and runner. Full-dump, cold-storage, and Windows performance remain unmeasured.

## Larger sample at the 10,000-line default

Benchmarked [commit `a3311d4`](https://github.com/pchemguy/Wiktionary-JSONL-Parser/commit/a3311d48addf6556be3a16a58e97f81bb87f0d3b) using the same Debian 13, CPython 3.12.14, SQLite 3.54.1 with SQLiteICUex, and overlayfs setup.

The sample contains the first 299,210 entries from the [Kaikki Russian extract](https://kaikki.org/dictionary/downloads/ru/ru-extract.jsonl.gz), in source order with the original bytes preserved. It excludes 7,454 redirect-only records from the selected prefix. The download ETag was `"6ae5037e-1269eeb2"`. The first 29,921 entries match the smaller sample byte for byte. The larger input is 765,085,586 bytes (729.64 MiB), ten times the lines and 7.18 times the bytes. Its SHA-256 is `cc47e808281d98ab17585d0b4409aded52da3f49f160c8530f81a4d5606e6557`.

Each trial started a fresh CLI process and wrote a new on-disk database. The CLI used its default batch size and progress logging. Total time includes CLI startup, progress output, and database writes, with input preparation and database verification outside timing. The input was prepared on the same host immediately before the runs. No cache flush was performed.

| Run | Total time (s) | Input throughput (MiB/s) | Lines/s |
| --- | ---: | ---: | ---: |
| 1 | 42.831 | 17.035 | 6,986 |
| 2 | 43.577 | 16.744 | 6,866 |
| 3 | 42.549 | 17.148 | 7,032 |
| **Median** | **42.831** | **17.035** | **6,986** |

All three runs had 299,210 database entries, 29 batches of 10,000 lines and one of 9,210 lines, zero foreign-key violations, and a final progress update of 100.0%. Throughput uses the uncompressed JSONL input size and the number of imported lines.

## Three pre-keyed databases merged with UNION ALL

Split the 299,210-entry sample above into contiguous chunks at the first complete line at or beyond each byte boundary. Each chunk was imported separately with the 10,000-line default, in sequence on the same Debian 13 and SQLiteICUex runtime. Import times cover separate CLI invocations and exclude splitting and verification.

| Chunk | Input MiB | Lines | Import time (s) | Prepared entry IDs | Prepared batch IDs |
| --- | ---: | ---: | ---: | --- | --- |
| 1 | 243.22 | 168,183 | 14.910 | 1–168,183 | 1–17 |
| 2 | 243.21 | 73,149 | 14.581 | 168,184–241,332 | 18–25 |
| 3 | 243.21 | 57,878 | 15.041 | 241,333–299,210 | 26–31 |

The sequential imports took 44.532 seconds in total. Before timing the merge, assigned globally disjoint ranges by adding cumulative prior entry and batch counts to each later source database. Applied the same entry offset to dependent `entry_id` and `examples.sense_entry_id` columns, leaving child indices unchanged. Preparation of chunks 2 and 3 took 4.548 and 4.502 seconds, including a foreign-key check and each database's update transaction. Chunk 1 retained its original IDs.

[The merge utility](../../../tools/merge_databases.py) created a fresh destination for each trial, attached the three databases read-only, and ran one `INSERT ... SELECT ... UNION ALL ...` per table inside one transaction with foreign keys enabled. The timer includes schema creation, attachment and schema checks, inserts, and commit. It excludes pre-keying and post-merge verification. The prepared source databases totaled 641.31 MiB. No cache flush was performed.

| Run | Merge time (s) | Source DB MiB/s | DB rows/s |
| --- | ---: | ---: | ---: |
| 1 | 4.879 | 131.44 | 1,250,322 |
| 2 | 4.660 | 137.62 | 1,309,082 |
| 3 | 4.398 | 145.82 | 1,387,068 |
| **Median** | **4.660** | **137.62** | **1,309,082** |

Each destination held 6,100,323 rows across 21 tables and was 640.94 MiB. A key-based comparison with binary text comparison found identical rows in all 20 data tables from a single import of the same sample. The merged `batch_log` preserved the 31 chunk-level batch rows in order. Each merged database passed the foreign-key check.

## Ten pre-keyed databases merged with UNION ALL

Repeated the experiment at commit `b70f078174b6c73e078bcb85d8046a2923fb81e3` with the same 299,210-entry sample and runtime. Split at the first complete line at or beyond each tenth of the input bytes. The ten imports ran sequentially with the 10,000-line default.

| Chunk | Input MiB | Lines | Import time (s) | ID preparation (s) | Entry IDs | Batch IDs |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 72.967 | 20,383 | 4.448 | 0.000 | 1–20,383 | 1–3 |
| 2 | 72.962 | 62,314 | 4.128 | 2.626 | 20,384–82,697 | 4–10 |
| 3 | 72.964 | 76,994 | 4.499 | 1.103 | 82,698–159,691 | 11–18 |
| 4 | 72.964 | 26,171 | 4.091 | 1.283 | 159,692–185,862 | 19–21 |
| 5 | 72.965 | 20,457 | 4.234 | 1.199 | 185,863–206,319 | 22–24 |
| 6 | 72.979 | 20,392 | 4.658 | 1.180 | 206,320–226,711 | 25–27 |
| 7 | 72.967 | 22,178 | 4.644 | 1.127 | 226,712–248,889 | 28–30 |
| 8 | 72.951 | 20,052 | 5.245 | 1.252 | 248,890–268,941 | 31–33 |
| 9 | 72.962 | 14,545 | 5.046 | 1.278 | 268,942–283,486 | 34–35 |
| 10 | 72.962 | 15,724 | 4.759 | 1.134 | 283,487–299,210 | 36–37 |

The imports took 45.751 seconds in total. Disjoint ID preparation took 12.183 seconds separately, including the per-database foreign-key checks. Chunk 2's new key ranges overlapped its local ranges, so its keys passed through unused negative values inside the preparation transaction. Other shifted chunks used one update per table. Prepared database files totaled 687.27 MiB.

The same merge script attached all ten input databases read-only, the runtime's attachment limit. It wrote a fresh destination in each run with one `INSERT ... SELECT ... UNION ALL ...` per table. The same timing boundaries apply as in the three-chunk experiment.

| Run | Merge time (s) | Source DB MiB/s | DB rows/s |
| --- | ---: | ---: | ---: |
| 1 | 4.840 | 142.00 | 1,260,399 |
| 2 | 4.193 | 163.91 | 1,454,884 |
| 3 | 4.785 | 143.63 | 1,274,886 |
| **Median** | **4.785** | **143.63** | **1,274,886** |

Each run copied 6,100,329 rows and produced a 640.94 MiB database. All 20 data tables matched the single-import reference, the original 37 chunk batch rows were preserved, and all three foreign-key checks passed.

The ten-chunk median was 0.125 seconds above the three-chunk median, with overlapping trial times. The two runs used different chunk boundaries and different amounts of ID preparation.

## Seven concurrent imports with IDs assigned during insertion

Used the same 299,210-entry, 729.64 MiB sample and Debian 13 SQLiteICUex runtime. Python saw nine logical CPUs, so `os.cpu_count() - 2` started seven fresh processes. The [benchmark harness](../../../tools/benchmark_parallel_import.py) located byte-range boundaries at line breaks. Workers read their ranges directly from the source file. The chunks were about 104.24 MiB each and contained 32,499, 121,975, 38,197, 28,193, 31,451, 24,411, and 22,484 lines, respectively.

Each worker assigned final entry IDs from its one-based chunk line numbers plus `10_000_000 * chunk_index`. Batch IDs used the same chunk offset with a local batch number. Each worker wrote a separate SQLite database, emitted independently labeled progress after each batch commit, and kept the 10,000-line default. The existing merge utility copied the stored IDs directly. No separate ID preparation pass was needed.

| Run | Partition (s) | Concurrent imports (s) | Merge and publish (s) | Total (s) | Input MiB/s | Lines/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.002 | 7.752 | 4.481 | 12.268 | 59.475 | 24,389 |
| 2 | <0.001 | 7.572 | 4.611 | 12.218 | 59.721 | 24,490 |
| 3 | <0.001 | 7.111 | 4.918 | 12.069 | 60.458 | 24,792 |

The total includes worker startup, progress output captured to a file, merge, publication, and temporary database cleanup. Harness preflight and post-run verification are outside the timer. No cache flush was performed. The median was 12.218 seconds, about 3.51 times faster than the earlier 42.831-second serial median on the same sample. The merge and publication took 4.611 seconds in the median-total run, about 38% of that run.

Verified all seven progress streams, exact entry IDs, 34 batch-log rows, and zero foreign-key violations in all three outputs. All 20 data tables matched the serial reference after translating IDs for comparison. An invalid-input test stopped the run, left no child workers or temporary databases, and published no destination. The harness uses fresh subprocesses with no fork dependency. Windows execution was unavailable for this benchmark.

## Batch-size sweep with seven concurrent workers

Used commit `232c7d335c6106fba2f6a9a3d50a8e9b80bcc299` and the same 299,210-line, 729.64 MiB sample, chunk boundaries, ID allocation, and SQLiteICUex environment as the seven-worker benchmark above. Each local harness copy changed only the worker `BATCH_SIZE` constant. Three trials per setting were interleaved in rotating order, each writing a fresh database with progress enabled. Sample hashing and output verification were outside the timed interval. No cache flush was performed. The earlier 10,000-line runs are shown for reference.

| Batch size (lines) | Batch log rows | Total trials (s) | Median worker time (s) | Median merge and publish (s) | Median total (s) | Input MiB/s | Lines/s |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 303 | 13.867, 13.516, 13.503 | 7.622 | 5.853 | 13.516 | 53.99 | 22,138 |
| 2,000 | 154 | 13.076, 13.165, 12.505 | 7.654 | 5.465 | 13.076 | 55.80 | 22,882 |
| 5,000 | 63 | 12.082, 12.522, 13.549 | 7.848 | 4.638 | 12.522 | 58.27 | 23,894 |
| 10,000 | 34 | 12.268, 12.218, 12.069 | 7.572 | 4.611 | 12.218 | 59.72 | 24,490 |

Worker and merge medians are calculated independently. Throughput uses the median total time per setting. The 5,000-line runs had the fastest median of the new settings, 12.522 seconds, and overlapped the earlier 10,000-line runs. Most of the median difference between the 1,000-line and 5,000-line settings appeared in merge and publication time. The timings establish no cause for that difference.

Each trial preserved the expected chunk IDs, independent progress streams, and batch log. All nine databases matched the serial reference across all 20 data tables after ID translation and had zero foreign-key violations.
