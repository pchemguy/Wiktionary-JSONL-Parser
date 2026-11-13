# Specification review report

**Gate result — Ready for human review.** The specification and schema conform to the accepted brief, architecture, and decomposition. Planning depends on specification acceptance.

| Reviewed or governing file | Git blob |
| --- | --- |
| [SPEC.md](SPEC.md) | `4e7ab68717813505de17cecf77744fa26d13613e` |
| [SQLite schema](spec/schema.sql) | `d5c3253c85eb3f4434c1d6edfe92934badeb89aa` |
| [PROJECT.md](PROJECT.md) | `9d149b1b3a88531e58204f8cdb3c0ce445902590` |
| [ARCHITECTURE.md](ARCHITECTURE.md) | `e4d218d14fce4b9b9f8d6e8f5447dbb5e41c8695` |
| [DECOMPOSITION.md](DECOMPOSITION.md) | `ada9ca6234f02d034784d8c331b71c88c0c39da8` |

## Coverage and evidence

- The CLI and input contract covers the default sibling output, explicit output overrides, destination conflicts, positive batch sizes, runtime preflight, and record decoding failures.
- The schema defines all 21 tables. The mapping preserves source order and duplicates, maintains entry and sense keys, and documents the handling of etymology, optional fields, and transformed values.
- The seven acceptance scenarios cover successful import, relational integrity, field mapping, preflight failures, parse failures, SQLite failures, and empty input. The batch contract matches the grouping and write order in DECOMPOSITION.

An in-memory probe loaded the proposed schema, checked its 21 table names, and verified that duplicate data and explicit entry IDs survive a successful batch. It also triggered a sense foreign-key violation and verified that the entire failed batch rolled back while earlier data and its log row remained. The probe registers a test collation under the `UTF_CI` name and covers schema and transaction behavior only.

No unresolved conformance findings.
