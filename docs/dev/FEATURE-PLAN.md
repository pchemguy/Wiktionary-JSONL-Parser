# Redirect-skipping delivery plan

## Phase 4 — Standalone redirect handling

| Milestone | Delivery and exit evidence |
| --- | --- |
| 4.1 — Redirect handling and verification | Add the Russian edition's classification and preserve source-line accounting through the shared worker. Verify focused and regression coverage, user documentation, installed CLI and library invocation, and the parallel benchmark's source-line rate. Run the exact unfiltered Kaikki dump through the installed importer. Verify source-position IDs, row equivalence, complete progress and SQLite integrity. |
| 4.2 — Phase review | Review the verified phase, incorporate accepted behavior into the governing documents, and check the release candidate and package inventory. Publish the release from the verified default-branch integration. |

For the full verification run, use the archive and entry-only reference identified in the [preparation record](FEATURE_PREPARATION.md). Stream the raw source using actual run chunk boundaries and independently calculate expected entry IDs and per-batch source counts. Verify every entry ID and the committed source totals. Align entries by source order when comparing all mapped tables with the entry-only reference. Record elapsed time, source MiB/s, source lines/s, and imported entries/s separately. Record any native platform limits.

## File ownership

| Path | Responsibility |
| --- | --- |
| `src/wiktionary_jsonl_parser/editions/__init__.py` and `editions/ru/` | Edition predicate contract and Russian redirect classification. |
| `src/wiktionary_jsonl_parser/worker.py` | Skip mapping after decoding and retain original line and batch accounting. |
| `tests/` | Classification, worker and applicable CLI or installation checks. |
| `tools/benchmark_parallel_import.py` and `tools/README.md` | Report and document source-line throughput with redirect-containing input. |
| `README.md` and `docs/dev/` | Document direct full-extract import and incorporate accepted source-accounting behavior. |

Build the wheel and source distribution under the existing release process. Verify the package contents and release inventory before publication and compare the hosted release files against the staged checksums.
