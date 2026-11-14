# Phase 3 — Parallel import

The importer now reads contiguous byte ranges through fresh Python workers. Workers assign final chunk-local keys, write staged SQLite databases, and report committed bytes. The importer merges closed worker databases within the effective SQLite attachment limit and publishes the completed output in one operation. The Russian edition owns its schema, mapper and insert order. The canonical Russian schema and mapped output were verified against both the prior parallel candidate and the serial reference.

| Verification | Result |
| --- | --- |
| Run planning, partitioning and worker writes | Attachment thresholds, zero-slot fallback, byte framing, key bounds, batch rollback and committed progress passed. [Milestone 3.1](milestone-3.1.md) |
| End-to-end import | Direct and grouped output, cancellation, failure cleanup, publication collision, callbacks and installed entry points passed. [Milestone 3.2](milestone-3.2.md) |
| Comprehensive review and corrections | Findings and corrective tests are recorded. The corrected candidate matched all 6,100,292 mapped rows from the serial reference after key translation, and matched the earlier parallel database byte for byte. [Milestone 3.3](milestone-3.3.md) |
| Final regressions | Linux SQLiteICUex passed 111 tests. The two tests specific to standard SQLite passed on that runtime. Ruff, formatting and mypy passed. |
| Final packaging | The wheel includes the edition mapper and DDL. The source archive reproduces the wheel. The installed CLI, library, both standalone tools and bundle checks passed. |

The corrected candidate processed the 729.64 MiB input at a seven-worker median of 12.803 seconds, 56.99 MiB/s, and about 23,370 lines/s. See the [correction report](../../reviews/006_d6dcd3e-phase-3-release/REVISION-REPORT.md) and [full-sample benchmark](candidate.md) for timing and comparison methodology.

The [main architecture](../../ARCHITECTURE.md), [decomposition](../../DECOMPOSITION.md), [specification](../../SPEC.md), [delivery plan](../../PLAN.md), and [tasks](../../TASKS.md) incorporate Phase 3. The archived feature sources retain preparation and implementation evidence. Windows-compatible startup and filesystem behavior were reviewed in source. Native Windows execution remains unverified.
