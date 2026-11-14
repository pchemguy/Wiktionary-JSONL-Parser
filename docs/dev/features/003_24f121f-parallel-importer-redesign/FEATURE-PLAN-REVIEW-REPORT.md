# Parallel importer plan and layout review

**Result — Ready for layout verification.** Three delivery milestones and a dedicated phase review cover the accepted specification. Bootstrap and isolated worker writes are independently testable before process supervision. The full CLI and library run before the candidate is pinned. Comprehensive review, correction, and rerun of affected regressions precede the final phase review and release.

The plan uses the benchmarked pipeline as evidence. The runtime and package checks include the installed worker entry point, schema, and database equivalence. Platform claims must state which environments actually ran the checks.

## Layout verification

**Result — Ready.** The plan assigns startup, supervision and publication to the public importer. Worker batch execution and grouped merging have separate module owners. The CLI owns user interaction, and the existing mapper and packaged schema remain shared. Current test, tool, and report locations support component, integration, and distribution checks. The source and wheel builds must include both new runtime modules and the schema.
