# Implementation tasks

[Specification](SPEC.md) · [Mapping and normalization](spec/mapping.md) · [SQLite schema](spec/schema.sql) · [Decomposition](DECOMPOSITION.md) · [Delivery plan](PLAN.md) · [Repository layout](layout.md)

## Phase 1 — JSONL-to-SQLite converter

- [x] Phase 1 — JSONL-to-SQLite converter
    - [x] Milestone 1.1 — Entry import
        - [x] T-001 — Package the schema and establish the SQLite runtime check
            Scope covers the package schema, the importer's SQLite setup, and focused tests. Load the packaged DDL from any working directory. Check SQLiteICUex's `UTF_CI` before creating output and enable foreign keys before batch writes. Verify exact schema bytes, all 21 tables, and failure before output creation when the collation is unavailable.
        - [x] T-002 — Decode source batches and map entry rows
            Scope covers the reader, root-entry mapper, and focused tests. Implement UTF-8 framing, batch sizing, source-line reporting, JSON decoding, entry IDs in source order, and all root-field mappings. Verify BOM, LF and CRLF, an unterminated final line, repeated property names, malformed and non-object records, bare nonfinite constants, duplicates, and explicit nulls and empty values.
        - [x] T-003 — Deliver the entry importer through the CLI
            Depends on T-001 and T-002. Scope covers CLI arguments, destination handling, and the batch transaction with its log row. Verify default and explicit output paths, batch-size defaults and validation, empty input, a short final batch, missing input or collation, existing output protection, CLI status and diagnostics, and atomicity after a decode or write failure. Complete the milestone code review and checks, fix blockers, and record the results in `reports/phases/1/1.1.md` and HANDOFF.
    - [x] Milestone 1.2 — Complete relational mapping
        - [x] T-004 — Map linkage and flat child arrays
            Depends on T-003. Extend the mapper and batch writing to all linkage tables, forms, translations, and hyphenations. Verify one row per array element, exact source indices, copied linkage `sense_index`, duplicates, and missing and explicit values.
        - [x] T-005 — Map senses, examples, and sounds
            Depends on T-004. Complete the nested and transformed mappings. Verify sense and example keys, `form_of` compaction, preserved offset arrays, the fixed URL key order, and the handling of missing or invalid mapped values.
        - [x] T-006 — Verify the full mapping and batch failure boundary
            Depends on T-005. Use a fixture covering every data table and compare database values with the mapping contract. Verify one parameterized `executemany()` per populated table, parent ordering, zero foreign-key violations, and rollback after mapping, child insert, and log insert failures. Confirm the committed prefix remains queryable. Complete the milestone code review and checks, fix blockers, and record the results in `reports/phases/1/1.2.md` and HANDOFF.
    - [x] Milestone 1.3 — Installable CLI
        - [x] T-007 — Build and inspect the Python distributions
            Depends on T-006. Set initial version `0.1.0`, build the wheel and source distribution, and verify package metadata, the CLI entry point, and installation of the exact schema. Run the installed CLI from a separate working directory with SQLiteICUex and compare its database with the source-tree result.
        - [x] T-008 — Document installation, usage, and output
            Depends on T-007. Document how to provide SQLiteICUex, install and invoke the CLI, choose the output path and batch size, query the result, and interpret failures and partial committed output. Check commands and links against the installed behavior.
        - [x] T-009 — Prepare and verify the release bundle
            Depends on T-007 and T-008. Prepare release notes and document any release helpers under `tools/`. Build the stable-named bundle with both installable distributions and generate `SHA256SUMS`. Verify the complete release asset inventory and checksums. Exercise an invalid versioned asset name and verify its rejection even when it is listed in the expected inventory, then rebuild and check the valid bundle. Complete the milestone review and checks, fix blockers, and record the results in `reports/phases/1/1.3.md` and HANDOFF.
    - [x] Milestone 1.4 — Phase review
        - [x] T-010 — Review, test, and report Phase 1
            Requires completion of milestones 1.1 through 1.3 and their hosted closures when tracking is active. Review the integrated implementation and rerun the acceptance, regression, and package checks. Run the CLI with SQLiteICUex on a representative local sample and record elapsed time, committed lines, and batch size. Fix blocking findings. Record phase evidence in `reports/phases/1/PHASE-REPORT.md`, aggregate remaining findings in `reports/IMPLEMENTATION-REPORT.md`, and update HANDOFF.

After Phase 1 completes, verify integration into the default branch and publish the release from that revision. Rebuild and check the release inventory against the verified source, then verify the hosted download and checksum. See [PLAN](PLAN.md).

## Phase 2 — Import progress logging

- [x] Phase 2 — Import progress logging
    - [x] Milestone 2.1 — Progress logging
        - [x] T-011 — Report byte progress after completed batch writes
            Requires released Phase 1. Implement the optional importer callback, flushed CLI reporting, and quiet mode. Verify exact raw byte accounting, transaction visibility, errors, empty input, and the installed command contract. Document the CLI option and record the milestone review.
    - [x] Milestone 2.2 — Phase review
        - [x] T-012 — Verify and package the progress release
            Depends on T-011 and its verified milestone. Review the complete progress change. Repeat the acceptance and regression checks, exercise the installed distributions, validate the release package, and record the phase review.

See the [progress milestone review](features/001_83e7d6a-import-progress/2.1.md) and [Phase 2 report](features/001_83e7d6a-import-progress/PHASE-REPORT.md).

## Phase 3 — Parallel import

- [x] Phase 3 — Parallel import
    - [x] Milestone 3.1 — Run planning and worker execution
        - [x] T-013 — Plan the worker count and attachment groups
            Implement bootstrap, probing, warning and confirmation policy. Verify exact fits, reduction, equality at 1.5, one-slot groups, zero-limit confirmation, and the one-worker CPU fallback.
        - [x] T-014 — Partition the source at complete record boundaries
            Depends on T-013. Use ordered byte ranges and verify exact coverage for small files, very long records, coincident ranges, CRLF, and an unterminated final line.
        - [x] T-015 — Write complete worker databases with final IDs
            Depends on T-014. Implement bounded decoding and mapping, final entry and batch IDs, batch transactions, and committed byte-progress messages. Verify ID range overflow, parent relationships, duplicate preservation, and batch rollback. Review milestone 3.1 and record the result and handoff.
    - [x] Milestone 3.2 — End-to-end parallel import
        - [x] T-016 — Supervise independent worker processes
            Depends on T-015. Start fresh Python workers using a Windows-compatible process mechanism. Drain progress and diagnostics and verify cancellation, exit reporting, and child cleanup.
        - [x] T-017 — Assemble and publish the staged database
            Depends on T-016. Implement group-by-group read-only attachment, parent-first inserts, direct single-worker publication, and no-overwrite publication. Verify staged cleanup and failure injection for writes, merging, and publication.
        - [x] T-018 — Expose the parallel CLI and library interfaces
            Depends on T-017. Connect arguments, callbacks, worker failure diagnostics, quiet mode and usage docs. Verify the 10,000-line default, installed interfaces, zero-limit fallback, and valid and failing imports. Review milestone 3.2 and record the result and handoff.
    - [x] Milestone 3.3 — Release candidate review and correction
        - [x] T-019 — Build and benchmark the release candidate
            Depends on T-018. Build the wheel and source distribution. Verify schema and entry points, compare the resulting database with the serial reference after translating IDs, and measure elapsed time and throughput on the shared sample.
        - [x] T-020 — Comprehensively review the pinned release candidate
            Depends on T-019. Review the current candidate source and assets under the plan's release gate, including the shared pipeline and edition definition boundary. Record findings, platform and performance evidence, and the corrections required for release.
        - [x] T-021 — Correct candidate findings and verify the fixes
            Depends on T-020. Fix confirmed in-scope findings or record the review's verified clean disposition. Rebuild and rerun affected verification, regressions, and package checks. Complete milestone 3.3 review and record the result and handoff.
    - [x] Milestone 3.4 — Phase review
        - [x] T-022 — Verify Phase 3 and the final release boundary
            Depends on T-015, T-018, and T-021 and their milestone closures when tracking is active. Review integrated product behavior and the incorporated main documents. Verify the tested candidate and final release readiness. Record the available platform evidence, phase report, and handoff.

Publish the release after successful phase integration, candidate review and fixes, and verification of the rebuilt release inventory and hosted checksums.

See the [Phase 3 report](features/003_24f121f-parallel-importer-redesign/PHASE-REPORT.md).

## Phase 4 — Standalone redirect handling

- [x] Phase 4 — Standalone redirect handling
    - [x] Milestone 4.1 — Redirect handling and verification
        - [x] T-023 — Skip standalone Russian redirects in the shared worker
            Implement the edition predicate and worker dispatch. Verify the exact record boundary, source-position entry IDs and child keys, full and partial batches, redirect-only inputs, complete byte progress, and failure positions and overflow after redirects. Update usage and benchmark source-line accounting and run regressions.
        - [x] T-024 — Verify direct import of the complete Kaikki extract
            Depends on T-023. Build and install the distributions, verify the CLI and library, and import the pinned raw archive after extraction. Verify all entry IDs and batch counts against raw positions and mapped content against the aligned reference. Record run and SQLite checks, package and benchmark evidence, and milestone review.
    - [x] Milestone 4.2 — Phase review
        - [x] T-025 — Incorporate and verify Phase 4 for release
            Depends on T-024 and verified milestone closure when tracked. Review the tested delivery, incorporate into the main governing documents, reconcile task ownership, and record phase and release readiness evidence.

Integrate the verified phase into the default branch and publish the release with verified assets and checksums.

See the [Phase 4 report](features/008_984ad61-skip-redirect-records/PHASE-REPORT.md).
