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
