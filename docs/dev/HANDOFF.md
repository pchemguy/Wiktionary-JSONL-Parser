# Project handoff

Checkpoint — Import progress released and importer profiled.

T-011 and T-012 are complete. Campaign `001_83e7d6a` is integrated into `main`. The [v0.2.0 release](https://github.com/pchemguy/Wiktionary-JSONL-Parser/releases/tag/v0.2.0) is tagged at `febb34006911b5c4bea39084fb79ef9aa3b4666c`. The published bundle and checksums match their staged bytes at both the tagged and latest URLs. The preparation, implementation and phase review milestones are closed.

See the [current tasks](TASKS.md), [archived feature evidence](features/001_83e7d6a-import-progress/README.md), and [benchmark and pipeline profile](reports/importer-performance.md). The full authorized feature and measurement work is complete.

Revision `002_0c74da1` set the default batch size to 10,000 source lines. The [revision report](reviews/002_0c74da1-default-batch-size/REVISION-REPORT.md) records the verified change.

## Active feature preparation

Campaign `003_24f121f` opens the parallel importer redesign from `main` at `24f121f3f328aa575d52121acaf079f83d5a7a5c`. Preparation runs on `design-docs/003_24f121f-parallel-importer-redesign` and returns to `main`. See the [preparation record](FEATURE_PREPARATION.md), [checklist](FEATURE_DOCS_TASKS.md), and [GitHub milestone](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/9). The user accepted the [feature brief](FEATURE.md). The user accepted the [feature architecture](FEATURE_ARCHITECTURE.md). The [feature decomposition](FEATURE_DECOMPOSITION.md) is accepted under the user's preapproval. The [specification](FEATURE-SPEC.md), [delivery plan](FEATURE-PLAN.md), and [tasks T-013 through T-022](FEATURE-TASKS.md) are ready. The [feature package review](FEATURE-QC-REPORT.md) passed. Integrate the approved preparation branch into the default branch. The checked preparation package defines the next implementation range, T-013 through T-022.

Nested revision `004_1c1297a` documented and verified the optional build setting for 100 SQLite attachments. See the [revision report](reviews/004_1c1297a-sqlite-attachment-limit/REVISION-REPORT.md). The attachment-limit build note is available for feature design.
