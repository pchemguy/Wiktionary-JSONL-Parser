# Repository layout

This layout places the [decomposed components](DECOMPOSITION.md) and supports the milestones in the [delivery plan](PLAN.md).

| Path | Ownership |
| --- | --- |
| `pyproject.toml` | Python version, Hatchling build configuration, distribution metadata, CLI entry point, and test configuration. |
| `src/wiktionary_jsonl_parser/__init__.py` | Package marker. Importing the package does not start a conversion. |
| `src/wiktionary_jsonl_parser/cli.py` | Installed CLI entry point and command-line handling. Calls the importer with resolved arguments. |
| `src/wiktionary_jsonl_parser/importer.py` | Input reading, batch lifecycle, entry ID allocation, SQLite connection and transactions, and parameterized writes. |
| `src/wiktionary_jsonl_parser/mapping.py` | Mapping of decoded records to row tuples. Works with caller-supplied batch row lists. |
| `src/wiktionary_jsonl_parser/schema.sql` | Runtime copy of the specified DDL. Include it in the installed package so the importer can initialize the database from any working directory. |
| `tests/` | Pytest modules for mapping, importer and SQLite behavior, and CLI and package integration. Small JSONL inputs and expected data live in `tests/fixtures/`. Tests create databases in temporary directories. |
| `tools/` | Project utilities and support scripts, including release helpers as needed. Document each tool alongside it. |
| `README.md` and `RELEASE-NOTES.md` | Installation and usage guidance, plus release notes for the published version. |
| `docs/dev/` | Governing design, specification, planning, and verification records. |

The CLI calls the importer, which calls the mapper and uses the packaged schema. The mapper takes decoded data and appends row tuples. The importer owns filesystem and database access.

The [specified schema](spec/schema.sql) is the canonical DDL. The package copy must match it byte for byte, and package verification checks both content and resource availability. The [mapping contract](spec/mapping.md) governs field conversions and row relationships.

Build products belong in `dist/` and release staging in `release/`. Both stay outside the tracked source tree. Distribution builds include the runtime schema, and the source distribution includes the project sources and files needed to build and verify the package.
