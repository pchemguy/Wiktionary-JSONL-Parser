# Phase 3 release candidate and benchmark

Candidate product tree `83f006c87bd4afe9f5f8d49d3c551d14b89ae5d3`, based on `4eef11d63b0325f1ad35284ba83db5fc20ff8a5c` with the 0.3.0 version, README installation example, and release notes. Built the wheel and source archive with Hatchling and verified the bundled checksums, exact schema bytes in both distributions, wheel entry point, package metadata, and installation outside the checkout.

| Candidate artifact | SHA-256 |
| --- | --- |
| `wiktionary_jsonl_parser-0.3.0-py3-none-any.whl` | `94338a587c0cca623e55a3131d1fc9a9b1ded2e3bf7d9ed965f37207f16bf9d8` |
| `wiktionary_jsonl_parser-0.3.0.tar.gz` | `fa55b19b23e8dd361b0dfdc1e69fc3eca02a703d3b43fdad2a0ac2d4f95abff1` |
| `SHA256SUMS` | `7aa267a3e2527cfefd6906f98b272f1e29550da982fb48c807e27fcc40697a1c` |
| `wiktionary-jsonl-parser-python.zip` | `31c77cb9ec755c3c1462e75a2bd25b61c1ea44f9a5b41a2642c464bfcaea4a06` |

## Shared Russian Wiktionary sample

The same entry-only Kaikki sample used for the earlier bench contains 765,085,586 bytes (729.64 MiB) in 299,210 lines. Its SHA-256 is `cc47e808281d98ab17585d0b4409aded52da3f49f160c8530f81a4d5606e6557`. Both CLIs ran with progress suppressed and the default 10,000-line batch size. The fresh serial reference is `03e626a`. Each run includes process startup and completed output. Python reported nine logical CPUs and SQLiteICUex exposed 100 attachment slots, yielding seven parallel workers in one merge group. Linux used CPython 3.12.14 and SQLite 3.54.1. The run order alternated across three repetitions.

| CLI | Runs (s) | Median (s) | MiB/s | Lines/s |
| --- | --- | ---: | ---: | ---: |
| Serial | 46.293, 47.213, 46.243 | 46.293 | 15.76 | 6,463 |
| Parallel | 14.329, 12.705, 13.739 | 13.739 | 53.11 | 21,778 |

Parallel median wall time was 3.37 times faster than the same-session serial baseline. The [earlier single-process benchmark](../../reports/importer-performance.md) is historical evidence from a separate run.

After translating parallel entry IDs to source-order ordinals, all 6,100,292 rows in the 20 mapped tables matched the serial reference, including duplicate entries, child references and text values. Batch logs were verified independently against the exact chunk IDs and line counts. Both databases passed integrity and foreign-key checks. Comparison and verification time is excluded from import throughput.

## Candidate after the edition boundary amendment

T-020 reviews the refreshed product tree `d3e1ceba4b866f9f08c987b8588316e84b682074`. The tree is based on `d0f14dd30c12fd778d003e3336605ed325abfada` and includes the edition boundary implementation, tests and documentation. Candidate package hashes apply to the build before recording the resulting verification evidence and handoff.

| Refreshed candidate artifact | SHA-256 |
| --- | --- |
| `wiktionary_jsonl_parser-0.3.0-py3-none-any.whl` | `101a17b4772e68edca93b2d0b4592154da26fb05abecd918f91d9b05b45c9ade` |
| `wiktionary_jsonl_parser-0.3.0.tar.gz` | `4639a5f4802bfcd74976d158ee7c1dda84d0e0a999a5e1bd669e056905d6ebb3` |
| `SHA256SUMS` | `23e08e9b9c69b7d887e4781b2b23eaebd0756cfee6cd063042ee2674d628804a` |
| `wiktionary-jsonl-parser-python.zip` | `7f557d8d8b91b12bb6b231191f8883697c15cea2249240775eabbb11c25f8fe7` |

The benchmark used the same sample, runtime, seven workers and settings described above.

| CLI | Runs (s) | Median (s) | MiB/s | Lines/s |
| --- | --- | ---: | ---: | ---: |
| Serial | 46.541, 47.822, 47.153 | 47.153 | 15.47 | 6,346 |
| Parallel | 12.885, 12.142, 12.882 | 12.882 | 56.64 | 23,227 |

Median parallel wall time was 3.66× faster than the same-session serial run. The output matched the original parallel candidate byte for byte. After translating keys, the renewed comparison matched all 6,100,292 mapped rows against the serial reference. Both databases passed the independent batch-log, integrity and foreign-key checks. See the [amendment report](../../reports/phases/3/revisions/005_d0f14dd-edition-boundary/REVISION-REPORT.md) for regression and installed-package evidence.
