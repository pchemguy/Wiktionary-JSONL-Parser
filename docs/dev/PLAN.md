# Delivery plan

Deliver the single-process Russian Wiktionary JSONL converter and its CLI progress updates. Each delivery milestone runs through the CLI and writes to SQLite. The [specification](SPEC.md), [schema](spec/schema.sql), [mapping contract](spec/mapping.md), and [decomposition](DECOMPOSITION.md) govern the work.

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

## Integration and release

Phase 1 corresponds to `0.1.0`. Phase 2 corresponds to `0.2.0`. Finalize the version and release notes for the verified phase, integrate the reviewed implementation into the default branch, and publish a GitHub release from that verified revision. Use `wiktionary-jsonl-parser-python.zip` as the release download. It contains the wheel and source distribution with their installable filenames. Publish `SHA256SUMS` for the uploaded bundle. Before tagging or publishing, execute the naming and checksum checks against the actual release files. Repair and rebuild any failing candidate. Verify the hosted download and checksum after publishing.
