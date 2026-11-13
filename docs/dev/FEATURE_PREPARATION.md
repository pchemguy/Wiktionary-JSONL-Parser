# Import progress logging preparation

## Identity and request

- Campaign `001_83e7d6a`, baseline `83e7d6a5052649cc6accb7d23af6e2d3f765620c`, preparation branch `design-docs/001_83e7d6a-import-progress`, creation parent and integration target `main`. The intended implementation branch is `feature/001_83e7d6a-import-progress` after preparation integration.
- Open a feature campaign for progress update logging based on input bytes. Avoid a pass to count input lines. Measure bytes read and processed, and emit the update after the batch write.
- The [released phase](reports/phases/1/PHASE-REPORT.md), [specification](SPEC.md), and [decomposition](DECOMPOSITION.md) establish the baseline. The relevant code is in [the importer](../../src/wiktionary_jsonl_parser/importer.py) and [CLI](../../src/wiktionary_jsonl_parser/cli.py).

## Current control

Interactive, one pass, with strict delivery. Scope is feature campaign opening and the first brief proposal. [Milestone 6](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/6) and its nine campaign issue associations were read back before branch or document writes. The integrated manual provenance scaffolding is present and reused.

## Decisions and evidence

- User direction establishes the progress unit and reporting point. The proposal counts the actual raw bytes read and processed for each completed batch and reports them after the batch write returns. The input file size supplies the denominator.
- Proposed CLI defaults for the brief review are one flushed progress line per batch on stderr and `--no-progress` to suppress updates.
- FDOCS-001 is complete. FDOCS-002 owns the first brief review. Later preparation stages await that checkpoint.
