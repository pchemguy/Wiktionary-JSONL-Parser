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
