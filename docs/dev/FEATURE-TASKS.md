# Parallel importer implementation tasks

[Specification](FEATURE-SPEC.md) · [Delivery plan and layout](FEATURE-PLAN.md)

## Phase 3 — Parallel import

- [ ] Phase 3 — Parallel import
    - [ ] Milestone 3.1 — Run planning and worker execution
        - [ ] T-013 — Plan the worker count and attachment groups
            Implement bootstrap, probing, warning and confirmation policy. Verify exact fits, reduction, equality at 1.5, one-slot groups, zero-limit confirmation, and the one-worker CPU fallback.
        - [ ] T-014 — Partition the source at complete record boundaries
            Depends on T-013. Use ordered byte ranges and verify exact coverage for small files, very long records, coincident ranges, CRLF, and an unterminated final line.
        - [ ] T-015 — Write complete worker databases with final IDs
            Depends on T-014. Implement bounded decoding and mapping, final entry and batch IDs, batch transactions, and committed byte-progress messages. Verify ID range overflow, parent relationships, duplicate preservation, and batch rollback. Review milestone 3.1 and record the result and handoff.
    - [ ] Milestone 3.2 — End-to-end parallel import
        - [ ] T-016 — Supervise independent worker processes
            Depends on T-015. Start fresh Python workers using a Windows-compatible process mechanism. Drain progress and diagnostics and verify cancellation, exit reporting, and child cleanup.
        - [ ] T-017 — Assemble and publish the staged database
            Depends on T-016. Implement group-by-group read-only attachment, parent-first inserts, direct single-worker publication, and no-overwrite publication. Verify staged cleanup and failure injection for writes, merging, and publication.
        - [ ] T-018 — Expose the parallel CLI and library interfaces
            Depends on T-017. Connect arguments, callbacks, worker failure diagnostics, quiet mode and usage docs. Verify the 10,000-line default, installed interfaces, zero-limit fallback, and valid and failing imports. Review milestone 3.2 and record the result and handoff.
    - [ ] Milestone 3.3 — Release candidate review and correction
        - [ ] T-019 — Build and benchmark the release candidate
            Depends on T-018. Build the wheel and source distribution. Verify schema and entry points, compare the resulting database with the serial reference after translating IDs, and measure elapsed time and throughput on the shared sample.
        - [ ] T-020 — Comprehensively review the pinned release candidate
            Depends on T-019. Review the actual candidate source and assets under the plan's release gate. Record findings, platform and performance evidence, and the corrections required for release.
        - [ ] T-021 — Correct candidate findings and verify the fixes
            Depends on T-020. Fix confirmed in-scope findings or record the review's verified clean disposition. Rebuild and rerun affected verification, regressions, and package checks. Complete milestone 3.3 review and record the result and handoff.
    - [ ] Milestone 3.4 — Phase review
        - [ ] T-022 — Verify Phase 3 and the final release boundary
            Depends on T-015, T-018, and T-021 and their milestone closures when tracking is active. Review integrated product behavior and the incorporated main documents. Verify the tested candidate and final release readiness. Record the available platform evidence, phase report, and handoff.

Publish the release after successful phase integration, candidate review and fixes, and verification of the rebuilt release inventory and hosted checksums.
