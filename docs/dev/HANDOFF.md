# Project handoff

Phase 3 is complete and integrated into `main`. See the [current tasks](TASKS.md), [phase report](features/003_24f121f-parallel-importer-redesign/PHASE-REPORT.md), and [campaign evidence](features/003_24f121f-parallel-importer-redesign/README.md). The [architecture](ARCHITECTURE.md), [decomposition](DECOMPOSITION.md), [specification](SPEC.md), and [delivery plan](PLAN.md) describe the integrated importer.

The [v0.3.0 release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/tag/v0.3.0) is tagged at `f95015483bd8eec8c3445aa9982ff429c32458d5`. The tagged and latest release downloads matched the staged ZIP and checksums byte for byte. All Phase 3 task issues and milestones are closed.

The [performance report](reports/importer-performance.md) retains the serial baseline and early worker and merge measurements. The [batch-size revision](reviews/002_0c74da1-default-batch-size/REVISION-REPORT.md) records the 10,000-line default. The [SQLite build revision](reviews/004_1c1297a-sqlite-attachment-limit/REVISION-REPORT.md) verifies the optional 100-slot build.
