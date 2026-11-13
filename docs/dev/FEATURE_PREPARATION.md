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
