# Implementation tasks

[Specification](SPEC.md) · [Mapping and normalization](spec/mapping.md) · [SQLite schema](spec/schema.sql) · [Decomposition](DECOMPOSITION.md) · [Delivery plan](PLAN.md) · [Repository layout](layout.md)

## Phase 1 — JSONL-to-SQLite converter

- [ ] Phase 1 — JSONL-to-SQLite converter
    - [x] Milestone 1.1 — Entry import
        - [x] T-001 — Package the schema and establish the SQLite runtime check
            Scope covers the package schema, the importer's SQLite setup, and focused tests. Load the packaged DDL from any working directory. Check SQLiteICUex's `UTF_CI` before creating output and enable foreign keys before batch writes. Verify exact schema bytes, all 21 tables, and failure before output creation when the collation is unavailable.
        - [x] T-002 — Decode source batches and map entry rows
            Scope covers the reader, root-entry mapper, and focused tests. Implement UTF-8 framing, batch sizing, source-line reporting, JSON decoding, entry IDs in source order, and all root-field mappings. Verify BOM, LF and CRLF, an unterminated final line, repeated property names, malformed and non-object records, bare nonfinite constants, duplicates, and explicit nulls and empty values.
        - [x] T-003 — Deliver the entry importer through the CLI
            Depends on T-001 and T-002. Scope covers CLI arguments, destination handling, and the batch transaction with its log row. Verify default and explicit output paths, batch-size defaults and validation, empty input, a short final batch, missing input or collation, existing output protection, CLI status and diagnostics, and atomicity after a decode or write failure. Complete the milestone code review and checks, fix blockers, and record the results in `reports/phases/1/1.1.md` and HANDOFF.
    - [ ] Milestone 1.2 — Complete relational mapping
        - [ ] T-004 — Map linkage and flat child arrays
            Depends on T-003. Extend the mapper and batch writing to all linkage tables, forms, translations, and hyphenations. Verify one row per array element, exact source indices, copied linkage `sense_index`, duplicates, and missing and explicit values.
        - [ ] T-005 — Map senses, examples, and sounds
            Depends on T-004. Complete the nested and transformed mappings. Verify sense and example keys, `form_of` compaction, preserved offset arrays, the fixed URL key order, and the handling of missing or invalid mapped values.
        - [ ] T-006 — Verify the full mapping and batch failure boundary
            Depends on T-005. Use a fixture covering every data table and compare database values with the mapping contract. Verify one parameterized `executemany()` per populated table, parent ordering, zero foreign-key violations, and rollback after mapping, child insert, and log insert failures. Confirm the committed prefix remains queryable. Complete the milestone code review and checks, fix blockers, and record the results in `reports/phases/1/1.2.md` and HANDOFF.
    - [ ] Milestone 1.3 — Installable CLI
        - [ ] T-007 — Build and inspect the Python distributions
            Depends on T-006. Set initial version `0.1.0`, build the wheel and source distribution, and verify package metadata, the CLI entry point, and installation of the exact schema. Run the installed CLI from a separate working directory with SQLiteICUex and compare its database with the source-tree result.
        - [ ] T-008 — Document installation, usage, and output
            Depends on T-007. Document how to provide SQLiteICUex, install and invoke the CLI, choose the output path and batch size, query the result, and interpret failures and partial committed output. Check commands and links against the installed behavior.
        - [ ] T-009 — Prepare and verify the release bundle
            Depends on T-007 and T-008. Prepare release notes and document any release helpers under `tools/`. Build the stable-named bundle with both installable distributions and generate `SHA256SUMS`. Verify the complete release asset inventory and checksums. Exercise an invalid versioned asset name and verify its rejection even when it is listed in the expected inventory, then rebuild and check the valid bundle. Complete the milestone review and checks, fix blockers, and record the results in `reports/phases/1/1.3.md` and HANDOFF.
    - [ ] Milestone 1.4 — Phase review
        - [ ] T-010 — Review, test, and report Phase 1
            Requires completion of milestones 1.1 through 1.3 and their hosted closures when tracking is active. Review the integrated implementation and rerun the acceptance, regression, and package checks. Run the CLI with SQLiteICUex on a representative local sample and record elapsed time, committed lines, and batch size. Fix blocking findings. Record phase evidence in `reports/phases/1/PHASE-REPORT.md`, aggregate remaining findings in `reports/IMPLEMENTATION-REPORT.md`, and update HANDOFF.

After Phase 1 completes, verify integration into the default branch and publish the release from that revision. Rebuild and check the release inventory against the verified source, then verify the hosted download and checksum. See [PLAN](PLAN.md).
