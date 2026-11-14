# Project handoff

Phase 3 is complete and integrated into `main`. See the [current tasks](TASKS.md), [phase report](features/003_24f121f-parallel-importer-redesign/PHASE-REPORT.md), and [campaign evidence](features/003_24f121f-parallel-importer-redesign/README.md). The [architecture](ARCHITECTURE.md), [decomposition](DECOMPOSITION.md), [specification](SPEC.md), and [delivery plan](PLAN.md) describe the integrated importer.

The [v0.3.0 release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/tag/v0.3.0) is tagged at `f95015483bd8eec8c3445aa9982ff429c32458d5`. The tagged and latest release downloads matched the staged ZIP and checksums byte for byte. All Phase 3 task issues and milestones are closed.

The [performance report](reports/importer-performance.md) retains the serial baseline and early worker and merge measurements. The [batch-size revision](reviews/002_0c74da1-default-batch-size/REVISION-REPORT.md) records the 10,000-line default. The [SQLite build revision](reviews/004_1c1297a-sqlite-attachment-limit/REVISION-REPORT.md) verifies the optional 100-slot build.

## Windows test portability revision

Campaign `007_13c6351` addressed oversized pytest IDs, redundant subprocess environment setup, Windows path diagnostics, symlink semantics, and schema checkout line endings. See the [revision report](reviews/007_13c6351-windows-test-portability/REVISION-REPORT.md) for verified Linux results and the native Windows verification limit.

A-005 fixed the schema check for worktrees that already contain a CRLF copy. The [amendment results](reviews/007_13c6351-windows-test-portability/REVISION-REPORT.md#a-005--retained-crlf-after-reopening) record verification with LF, retained CRLF and a deliberate SQL mismatch.

## Phase 4 — Standalone redirect handling

Phase 4 is complete and integrated into `main`. See the [phase report](features/008_984ad61-skip-redirect-records/PHASE-REPORT.md), [full-extract verification](features/008_984ad61-skip-redirect-records/full-extract.md), and [current tasks](TASKS.md). The [v0.4.0 release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/tag/v0.4.0) is tagged at `27ef94650ff530848d6000cf785113af28ef85b7`. Tagged and latest download checksums match the staged artifacts. Phase 4 issues and milestones are closed.

## Phase 5 — CLI processing time

The feature reports total elapsed processing time on successful CLI imports. See the [phase report](features/009_a09aaf4-cli-processing-time/PHASE-REPORT.md) and [current tasks](TASKS.md). The integrated release version is 0.4.1.
