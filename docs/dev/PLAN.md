# Delivery plan

Deliver the Russian Wiktionary JSONL converter in five phases. The serial converter establishes mapping and persistence, CLI progress reports committed input bytes, and the parallel importer builds on the measured worker-and-merge design. The [specification](SPEC.md), [schema](spec/schema.sql), [mapping contract](spec/mapping.md), and [decomposition](DECOMPOSITION.md) govern the work.

## Phase 1 — JSONL-to-SQLite converter

The phase delivers a fresh import from a local UTF-8 JSONL file into a queryable SQLite database. It includes the full mapped field set, configurable batches, failure handling, and an installable CLI. The first milestone establishes a usable entry import and checks SQLiteICUex and transaction behavior before the mapping expands. The next milestone completes the database content. The third verifies distribution and use from an installed package.

| Milestone | Scope and dependency | Demonstrable result and exit evidence |
| --- | --- | --- |
| M-001 — Entry import | Establish the canonical schema and SQLiteICUex preflight. Connect the CLI, JSONL decoding, root entry mapping, and atomic batch writes. | Convert a small dump through the CLI with default and explicit output paths. Verify empty input, a shorter final batch, and the output state after an unreadable input, missing collation, destination conflict, malformed line, or write failure. Review the CLI diagnostics and batch log before expanding the mapping. |
| M-002 — Complete relational mapping | Extend the working importer to every child table and finish mapping diagnostics. Requires M-001. | Import a fixture that exercises all table families. Compare stored values, array indices, duplicate rows, missing and explicit values, transformed JSON, and sense and example keys with the mapping contract. Verify that mapping or insert failure preserves the earlier committed prefix. |
| M-003 — Installable CLI | Package the complete converter and schema. Document installation, the SQLiteICUex prerequisite, usage, output, and failure behavior. Requires M-002. | Build the wheel and source distribution from a known revision. Inspect the installed schema and CLI entry point. Run the installed CLI on a sample and compare its database with the source-tree result. Prepare the initial version, release notes, and release inventory. |
| M-004 — Phase review | Review the integrated converter after M-001 through M-003 are complete. | Complete one phase code review, regression run, and report. Resolve blocking findings and record remaining follow-ups. Verify the final candidate against the accepted system behavior and packaging checks. |

Each delivery milestone includes focused tests, review, and recorded results. The phase exit requires a successful CLI import with SQLiteICUex, with a representative local sample sufficient to establish the runtime contract. A test collation can exercise schema and transaction tests. Measure a representative import to record elapsed time, committed lines, and batch size. Throughput is baseline evidence for future tuning.

## Phase 2 — Import progress logging

Phase 2 delivers byte-based CLI progress on top of the released SQLiteICUex converter.

| Milestone | Scope | Exit evidence |
| --- | --- | --- |
| 2.1 — Progress logging | Add the importer callback and default CLI reporter with quiet mode. Update user-facing CLI guidance. | Exact byte counts after SQLite writes, no advancement on failed batches, and no progress for empty or quiet imports. Run the focused and regression checks. |
| 2.2 — Phase review | Review the complete change and build the wheel and source archive for version 0.2.0. | Verify the installed CLI, repeat the regression checks, and validate the release bundle. |

## Phase 3 — Parallel import

| Milestone | Scope and dependency | Exit evidence |
| --- | --- | --- |
| 3.1 — Run planning and worker execution | Apply bootstrap policy and byte partitioning. Deliver the independently testable worker with final ID assignment, atomic batch writes, and progress. | Policy boundaries and chunk framing pass. Worker output matches its range and key contract, using the selected edition's mapper and schema. |
| 3.2 — End-to-end parallel import | Add process supervision, staged merge and publication, then connect the CLI and library handlers. Depends on 3.1. | Installed invocation on Linux and Windows-compatible process startup, cancellation, grouped and direct output, injected failures, and result integrity are checked. Record native execution evidence separately. |
| 3.3 — Release candidate review and correction | Build the candidate, benchmark it against the recorded serial baseline, conduct comprehensive review, and fix confirmed in-scope findings. Depends on 3.2. | Pin the candidate revision and packages, publish the review and findings, and verify corrections against the rebuilt candidate. |
| 3.4 — Phase review | Verify the complete corrected delivery and coherent incorporation into the main project documents. Depends on 3.3. | Passing regression and distribution checks, platform evidence, database equivalence, candidate review disposition, and recorded release readiness. |

See the [repository layout](layout.md), [performance evidence](reports/importer-performance.md), and [Phase 3 report](features/003_24f121f-parallel-importer-redesign/PHASE-REPORT.md).

## Phase 4 — Standalone redirect handling

| Milestone | Delivery and exit evidence |
| --- | --- |
| 4.1 — Redirect handling and verification | Add the Russian edition's classification and preserve source-line accounting through the shared worker. Verify focused and regression coverage, user documentation, installed CLI and library invocation, and the parallel benchmark's source-line rate. Run the exact unfiltered Kaikki dump through the installed importer. Verify source-position IDs, row equivalence, complete progress and SQLite integrity. |
| 4.2 — Phase review | Review the verified phase, incorporate accepted behavior into the governing documents, and check the release candidate and package inventory. Publish the release from the verified default-branch integration. |

See the [Phase 4 report](features/008_984ad61-skip-redirect-records/PHASE-REPORT.md).

## Phase 5 — CLI processing time

| Milestone | Delivery and exit evidence |
| --- | --- |
| 5.1 — CLI timing and verification | Instrument the CLI around the existing synchronous import call. Verify the exact format and order, successful empty input, quiet mode, failure, interruption, and CLI help. Update usage documentation. |
| 5.2 — Phase review | Reconcile governing documents, verify regressions and installed CLI behavior, and check the package inventory. Publish patch release `0.4.1` from the verified default-branch revision. |

See the [Phase 5 report](features/009_a09aaf4-cli-processing-time/PHASE-REPORT.md).

## Integration and release

Phase 1 corresponds to `0.1.0`. Phase 2 corresponds to `0.2.0`. Phase 4 corresponds to `0.4.0`. Phase 3 corresponds to `0.3.0` and requires comprehensive candidate review, corrections, and re-verification before release. Phase 5 corresponds to `0.4.1`. Finalize the version and release notes for the verified phase, integrate the reviewed implementation into the default branch, and publish a GitHub release from that verified revision. Use `wiktionary-jsonl-parser-python.zip` as the release download. It contains the wheel and source distribution with their installable filenames. Publish `SHA256SUMS` for the uploaded bundle. Before tagging or publishing, execute the naming and checksum checks against the actual release files. Repair and rebuild any failing candidate. Verify the hosted download and checksum after publishing.
