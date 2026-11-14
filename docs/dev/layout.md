# Repository layout

This layout places the [decomposed components](DECOMPOSITION.md) and supports the milestones in the [delivery plan](PLAN.md).

| Path | Ownership |
| --- | --- |
| `pyproject.toml` | Python version, Hatchling build configuration, distribution metadata, CLI entry point, and test configuration. |
| `src/wiktionary_jsonl_parser/__init__.py` | Package marker. Importing the package does not start a conversion. |
| `src/wiktionary_jsonl_parser/cli.py` | Installed CLI entry point and command-line handling. Calls the importer with resolved arguments. |
| `src/wiktionary_jsonl_parser/importer.py` | Edition selection, planning, partitioning, worker supervision, staging and publication. |
| `src/wiktionary_jsonl_parser/worker.py` | Chunk reading, decoding, ID allocation and transactional writes. |
| `src/wiktionary_jsonl_parser/merge.py` | Grouped attachment and assembly into the staged destination. |
| `src/wiktionary_jsonl_parser/editions/` | Edition definition and lookup, plus database initialization with shared batch-log DDL. |
| `src/wiktionary_jsonl_parser/editions/ru/` | Russian mapping, ordered inserts, and runtime mapped-table DDL. Include the schema resource in the installed package. |
| `tests/` | Pytest modules for mapping, importer and SQLite behavior, and CLI and package integration. Small JSONL inputs and expected data live in `tests/fixtures/`. Tests create databases in temporary directories. |
| `tools/` | Project utilities and support scripts, including release helpers as needed. Document each tool alongside it. |
| `README.md` and `RELEASE-NOTES.md` | Installation and usage guidance, plus release notes for the published version. |
| `docs/dev/` | Governing design, specification, planning, and verification records. |

The CLI calls the importer, which selects the edition and supplies it to the shared pipeline. Workers use the edition's mapper to turn decoded records into row tuples. Workers and the merger initialize their databases from the same edition schema and the shared batch-log DDL.

The [specified schema](spec/schema.sql) is the canonical Russian DDL. The shared batch-log DDL and the packaged Russian mapped-table DDL together match it byte for byte. Package verification checks the combined content and resource availability. The [mapping contract](spec/mapping.md) governs field conversions and row relationships.

Build products belong in `dist/` and release staging in `release/`. Both stay outside the tracked source tree. Distribution builds include the runtime schema, and the source distribution includes the project sources and files needed to build and verify the package.
