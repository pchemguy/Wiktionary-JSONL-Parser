# Import progress logging preparation

## Identity and request

- Campaign `001_83e7d6a`, baseline `83e7d6a5052649cc6accb7d23af6e2d3f765620c`, preparation branch `design-docs/001_83e7d6a-import-progress`, creation parent and integration target `main`. The intended implementation branch is `feature/001_83e7d6a-import-progress` after preparation integration.
- Open a feature campaign for progress update logging based on input bytes. Avoid a pass to count input lines. Measure bytes read and processed, and emit the update after the batch write.
- The [released phase](reports/phases/1/PHASE-REPORT.md), [specification](SPEC.md), and [decomposition](DECOMPOSITION.md) establish the baseline. The relevant code is in [the importer](../../src/wiktionary_jsonl_parser/importer.py) and [CLI](../../src/wiktionary_jsonl_parser/cli.py).

## Current control

Interactive, one pass, with strict delivery. The user approved all feature checkpoints and authorized complete implementation. The range covers preparation, implementation, integration, and release. [Milestone 6](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/6) and its nine campaign issue associations were read back before branch or document writes. The integrated manual provenance scaffolding is present and reused.

## Decisions and evidence

- User direction establishes the progress unit and reporting point. The proposal counts the actual raw bytes read and processed for each completed batch and reports them after the batch write returns. The input file size supplies the denominator.
- The approved CLI defaults are one flushed progress line per batch on stderr and `--no-progress` to suppress updates.
- FDOCS-001 is complete and [issue #20](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/20) was verified closed. FDOCS-002 presents [the feature brief](FEATURE.md), blob `24f4d40a1512fc472034f802b5e0ca8e8442e1e1`, for review. The proposal matches the directed unit and reporting point and preserves the existing import and failure contract. The user accepted the brief and preapproved subsequent feature checkpoints.
- FDOCS-002: Accepted FEATURE blob 24f4d40a1512fc472034f802b5e0ca8e8442e1e1 under the user’s explicit approval.
- FDOCS-003: The single-process pipeline and existing CLI-to-importer boundary apply. Progress observes the completion of an existing batch write and does not introduce another component or connection.
- FDOCS-004: The [decomposition delta](FEATURE_DECOMPOSITION.md) at blob 3a0c33938666ccc3335cdd88cc0180fdc90c5e2c defines importer measurement and CLI presentation.
- FDOCS-005: The [specification](FEATURE-SPEC.md) at blob c543768ede458db8eaccffc9adcb8896c244b6ab and [review](FEATURE-SPEC-REVIEW-REPORT.md) are ready under the explicit preapproval.
- FDOCS-006: The [delivery plan](FEATURE-PLAN.md) at blob 10cfeb42948b4b412dad2e6bda0251d62d0950d5 defines one delivery milestone and a final phase review.
- FDOCS-007: Reuse the [repository layout](layout.md) for importer, CLI, tests and README. The [combined plan and layout review](FEATURE-PLAN-REVIEW-REPORT.md) confirms placement.
- FDOCS-008: The [task list](FEATURE-TASKS.md) at blob 52816e06441620fc3e51ec97a0dffddbaa966124 selects T-011 and T-012. The [task review](FEATURE-TASKS-REVIEW-REPORT.md) passed.
- FDOCS-009: The [package review](FEATURE-QC-REPORT.md) verified the final delta, local references, unique task IDs and readiness. Preparation integration follows.
