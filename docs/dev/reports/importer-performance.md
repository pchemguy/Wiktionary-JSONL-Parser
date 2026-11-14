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
