# Specification review report

**Gate result — Ready for human review.** The specification and schema conform to the accepted brief, architecture, and decomposition. Planning depends on specification acceptance.

| Reviewed or governing file | Git blob |
| --- | --- |
| [SPEC.md](SPEC.md) | `5c3cb1dfc33ba20ca5e2a16604c72f0d73f6caf9` |
| [Mapping contract](spec/mapping.md) | `f832e2eb0ab308acac1594c6ae6093057a2778b7` |
| [SQLite schema](spec/schema.sql) | `d5c3253c85eb3f4434c1d6edfe92934badeb89aa` |
| [PROJECT.md](PROJECT.md) | `9d149b1b3a88531e58204f8cdb3c0ce445902590` |
| [ARCHITECTURE.md](ARCHITECTURE.md) | `e4d218d14fce4b9b9f8d6e8f5447dbb5e41c8695` |
| [DECOMPOSITION.md](DECOMPOSITION.md) | `ada9ca6234f02d034784d8c331b71c88c0c39da8` |

## Coverage and evidence

- The CLI and input contract covers the default sibling output, explicit output overrides, destination conflicts, positive batch sizes, runtime preflight, and record decoding failures.
- The schema defines all 21 tables. The mapping preserves source order and duplicates, maintains entry and sense keys, and documents the handling of etymology, optional fields, and transformed values.
- The nine acceptance scenarios cover successful import, input framing, relational integrity, field mapping, preflight failures, parse and mapping failures, SQLite failures, and empty input. The batch contract matches the grouping and write order in DECOMPOSITION.

An in-memory probe loaded the proposed schema, checked its 21 table names, and verified that duplicate data and explicit entry IDs survive a successful batch. It also triggered a sense foreign-key violation and verified that the entire failed batch rolled back while earlier data and its log row remained. The probe registers a test collation under the `UTF_CI` name and covers schema and transaction behavior only.

## Finding

| ID | Observation | Status |
| --- | --- | --- |
| SPEC-01 | The reading and mapping section in the proposal at Git blob `4e7ab68717813505de17cecf77744fa26d13613e` grouped several table families and left explicit nulls, required nested fields, and parts of the JSON representation implicit. This left multiple plausible implementations for the same input. | Resolved in Revision 1. |

## Revision 1

Expanded the decoding guarantees in [SPEC.md](SPEC.md) and added the [mapping contract](spec/mapping.md). It covers all 20 data tables, source keys and indices, required fields, missing and explicit values, and normalized JSON representations. Acceptance covers input framing and mapping failure in addition to the existing batch scenarios.

Checked the documented field sets against all 20 data tables using the SQLite schema, including the composite sense foreign key. A probe with a test collation checked initial BOM handling, repeated JSON member names, rejection of bare nonfinite constants, serialization examples, optional value storage, and ordered example offsets. These checks cover the specification and schema. Importer execution and SQLiteICUex comparison behavior remain implementation verification work.

## Revision 1 — Import progress

**Result — Ready.** Checked byte progress, the quiet CLI flag, and failure and empty-input reporting against the accepted design and tests. See the [archived package review](features/001_83e7d6a-import-progress/FEATURE-QC-REPORT.md).
