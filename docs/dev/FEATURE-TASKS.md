# Standalone redirect implementation tasks

[Specification](FEATURE-SPEC.md) · [Delivery plan](FEATURE-PLAN.md)

## Phase 4 — Standalone redirect handling

- [ ] Phase 4 — Standalone redirect handling
    - [ ] Milestone 4.1 — Redirect handling and verification
        - [ ] T-023 — Skip standalone Russian redirects in the shared worker
            Implement the edition predicate and worker dispatch. Verify the exact record boundary, source-position entry IDs and child keys, full and partial batches, redirect-only inputs, complete byte progress, and failure positions and overflow after redirects. Update usage and benchmark source-line accounting and run regressions.
        - [ ] T-024 — Verify direct import of the complete Kaikki extract
            Depends on T-023. Build and install the distributions, verify the CLI and library, and import the pinned raw archive after extraction. Verify all entry IDs and batch counts against raw positions and mapped content against the aligned reference. Record run and SQLite checks, package and benchmark evidence, and milestone review.
    - [ ] Milestone 4.2 — Phase review
        - [ ] T-025 — Incorporate and verify Phase 4 for release
            Depends on T-024 and verified milestone closure when tracked. Review the tested delivery, incorporate into the main governing documents, reconcile task ownership, and record phase and release readiness evidence.

Integrate the verified phase into the default branch and publish the release with verified assets and checksums.
