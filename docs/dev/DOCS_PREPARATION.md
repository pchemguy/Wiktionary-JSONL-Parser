# Main documentation preparation record

## Current control

- Mode and decision source — Interactive, one pass, as directed by the project instructions.
- Current scope — Main development documents for the single-process Russian Wiktionary JSONL-to-SQLite converter.
- Approval basis — Each applicable document checkpoint requires explicit acceptance. No checkpoint has been preapproved.
- Tracking and publication — Repository policy enables GitHub preparation tracking. [Milestone #1](https://github.com/pchemguy/Wiktionary-JSONL-Parser/milestone/1) and all nine DOCS issues were verified before branch creation.
- Next boundary — Review the PLAN proposal before layout.

## Decisions and document evidence

| Task | Evidence |
| --- | --- |
| DOCS-001 | Initialization result below. |
| DOCS-002 | The user explicitly accepted the revised [PROJECT.md](PROJECT.md) presented at commit `9a710112457cef6168f7ae31e7721a70bfe05c64`, Git blob `92964f9d3047b14f6a5b94659342cf72d491fdf1`. The user subsequently set the output path default. [PROJECT.md](PROJECT.md) records that amendment at Git blob `9d149b1b3a88531e58204f8cdb3c0ce445902590`. |
| DOCS-003 | The user accepted the published [ARCHITECTURE.md](ARCHITECTURE.md) at commit `526d7051f8de7c050cf9b2fee8c4fe0635bb0738`, Git blob `e4d218d14fce4b9b9f8d6e8f5447dbb5e41c8695`. |
| DOCS-004 | The user accepted the revised [DECOMPOSITION.md](DECOMPOSITION.md) at commit `ea1493b0def01d461746bf4a260819231dd592c6`, Git blob `ada9ca6234f02d034784d8c331b71c88c0c39da8`. |
| DOCS-005 | The user directed continuation after reviewing [SPEC.md](SPEC.md) at commit `455361a5910dcea7ef6a1b537359e50d85f8595a`. Accepted set: SPEC blob `5c3cb1dfc33ba20ca5e2a16604c72f0d73f6caf9`, [mapping](spec/mapping.md) blob `f832e2eb0ab308acac1594c6ae6093057a2778b7`, [schema](spec/schema.sql) blob `d5c3253c85eb3f4434c1d6edfe92934badeb89aa`. The [review report](SPEC-REVIEW-REPORT.md) records conformance evidence. |
| DOCS-006 | [PLAN.md](PLAN.md) is proposed at Git blob `62360836fb102ea7f05cf497c2cdb415a1a8557c`. See the [plan review report](PLAN-REVIEW-REPORT.md) for coverage and milestone evidence. Human acceptance is pending. |
| DOCS-007 through DOCS-009 | Pending. |

The converter reads local, extracted Kaikki Russian Wiktionary JSONL in one process with configurable source-line batches. The user confirmed that imports start fresh, SQLiteICUex is required, and the mapper ignores `etymology_links`.

The user assigned the SQLite insert mechanism to DECOMPOSITION. Use exactly one `executemany()` call per populated table for each batch, including `batch_log`, with a fixed parameterized `INSERT` for each table and all row values bound. Group rows by table and write parent rows before dependent rows within the same batch transaction.

DECOMPOSITION also defines how the CLI passes the input path, output path, and batch size to the importer. It assigns the importer responsibility for SQLite connection setup and enabling foreign-key enforcement.

SPEC defines the user-facing CLI arguments, including the optional output path and its default, the `UTF_CI` check before output creation, the shorter final batch, and the actual source-line count stored in `batch_log`. It also defines which errors stop the import, source-line diagnostics when available, and fresh-import-only retries.

## Initialization

- Retained root files — `AI_DISCLOSURE.md`, `SDD-MANAGER.md`, `AGENTS.md`, and `SKILL_DISCOVERY_PROTOCOL.md`. Blob identities matched the baseline for all four. No root files needed copying.
- Continuation — All four root files were present at entry. Proceed to the brief proposal.
- Manual provenance — Existing instructions and records were preserved. The missing bundled template was added on `design-docs/ai-logs` at `8cd2a2fcfcbc793fe2c80669d288b64854ca0b8a`, based on `da8e87a03ec7e84a5b3021fe7ca772f3caadd251`, and merged into `main` at `c0bff86d0c13a611c930e18a040d23b42d5141e7`. The merge and exact template blob were read back from GitHub.
- Current reset — None.

## Pending transitions

GitHub verified [DOCS-003](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/3) closed as completed. GitHub verified [DOCS-004](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/4) closed as completed. GitHub verified [DOCS-005](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/5) closed as completed. Await acceptance of [PLAN](PLAN.md). [DOCS-006](https://github.com/pchemguy/Wiktionary-JSONL-Parser/issues/6) remains open.
