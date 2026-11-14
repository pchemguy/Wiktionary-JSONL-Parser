# Parallel importer delivery plan

The single-process importer established mapping, persistence, and progress. The [benchmarks](reports/importer-performance.md) measured partitioning, independent worker writes, and database merging. Phase 3 delivers the production multiprocessing path specified in the [feature specification](FEATURE-SPEC.md), building on the benchmarked design.

## Phase 3 — Parallel import

| Milestone | Scope and dependency | Exit evidence |
| --- | --- | --- |
| 3.1 — Run planning and worker execution | Apply bootstrap policy and byte partitioning. Deliver the independently testable worker with final ID assignment, atomic batch writes, and progress. | Policy boundaries and chunk framing pass. Worker output matches its range and key contract, using the selected edition's mapper and schema. |
| 3.2 — End-to-end parallel import | Add process supervision, staged merge and publication, then connect the CLI and library handlers. Depends on 3.1. | Installed invocation on Linux and Windows-compatible process startup, cancellation, grouped and direct output, injected failures, and result integrity are checked. Record native execution evidence separately. |
| 3.3 — Release candidate review and correction | Build the candidate, benchmark it against the recorded serial baseline, conduct comprehensive review, and fix confirmed in-scope findings. Depends on 3.2. | Pin the candidate revision and packages, publish the review and findings, and verify corrections against the rebuilt candidate. |
| 3.4 — Phase review | Verify the complete corrected delivery and coherent incorporation into the main project documents. Depends on 3.3. | Passing regression and distribution checks, platform evidence, database equivalence, candidate review disposition, and recorded release readiness. |

## File ownership

| Path | Responsibility |
| --- | --- |
| `src/wiktionary_jsonl_parser/cli.py` | CLI argument parsing, callbacks for confirmation, warnings and progress, diagnostic display, public command. |
| `src/wiktionary_jsonl_parser/importer.py` | Public import call, coordination, SQLite bootstrap, worker supervision, stage lifetime, and publication. |
| `src/wiktionary_jsonl_parser/worker.py` | Assigned byte-range reader, fresh worker entry point, batch loop and writes. |
| `src/wiktionary_jsonl_parser/merge.py` | One-destination merger and read-only grouped attachment lifecycle. |
| `src/wiktionary_jsonl_parser/editions/` | Edition definition, lookup, and database initialization with the shared batch log. |
| `src/wiktionary_jsonl_parser/editions/ru/` | Russian mapper, parent-first insert statements, and mapped-table schema resource. |
| `tests/` | Focused planning, worker, merge, and CLI tests plus full pipeline, platform and installed-package checks. |
| `tools/` and `docs/dev/reports/importer-performance.md` | Benchmark harnesses and measured comparisons. |
| `docs/dev/features/003_24f121f-parallel-importer-redesign/` | Feature delivery and phase evidence. Place the comprehensive review and correction records in the campaign's review directory. |

## Final campaign release

Comprehensively review the exact candidate across accepted design and scope, worker and merge implementation, test and platform evidence, public usage and build instructions, workflows, and actual distribution contents. Record blocking findings against the pinned source and package hashes. Fix confirmed in-scope findings and rebuild. Repeat affected checks, regression tests, and distribution verification against the corrected candidate. Integrate the verified phase into the default branch, rebuild and verify assets from the release revision, and publish only after the review, fixes, and re-verification pass.
