# Feature documentation tasks

Task definitions/checkoffs only. Control, decisions, applicability/reuse and evidence belong in FEATURE_PREPARATION.md. FDOCS IDs are qualified by the campaign for hosting; product T IDs and main DOCS tasks are separate.

- [ ] FDOCS-001 — Establish feature preparation context.
    - Confirm the accepted main baseline, delta scope, campaign/branches, active source ownership, selected mode/tracking and applicable provenance setup. Initialize these task-only records, FEATURE_PREPARATION and HANDOFF after enabled projection. Do not replay main root initialization.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-002 — Prepare and accept FEATURE.
    - Depends on FDOCS-001 and required publication/issue closure.
    - Define intended outcome, included/non-goal delta, retained behavior, compatibility/constraints and material decisions. Present first brief approval unless explicitly preapproved; retain decision provenance.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-003 — Assess and accept feature architecture.
    - Depends on FDOCS-002 and required publication/issue closure.
    - Assess affected main architecture; prepare FEATURE_ARCHITECTURE and children only where required. Record evidenced reuse or review/acceptance of the necessary new proposal.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-004 — Assess and accept feature decomposition.
    - Depends on FDOCS-003 and required publication/issue closure.
    - Assess affected components, external/internal APIs and models against accepted architecture; prepare FEATURE_DECOMPOSITION and selected model/API-design artifacts where required. Include them in this task's reuse assessment or proposal/acceptance.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-005 — Prepare and accept FEATURE-SPEC.
    - Depends on FDOCS-004 and required publication/issue closure.
    - Define precise changed behavior and API/data contracts against accepted FEATURE/design, including selected contract artifacts and referenced model/API owners. Complete scoped SPEC QC/report and this task's human approval/preapproval.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-006 — Prepare and accept feature delivery strategy.
    - Depends on FDOCS-005 and required publication/issue closure.
    - Define bounded changed outcomes, phases/milestones/dependencies and exits, including needed API/model/contract refinement and consumer verification, in FEATURE-PLAN where needed, or assess sufficient existing strategy. Complete strategy QC/report and applicable approval without imposing a new MVP.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-007 — Assess and accept feature layout.
    - Depends on FDOCS-006 and required publication/issue closure.
    - Define affected public API, implementation, schema, test and documentation placement using the established layout/feature-plan owner, or assess sufficient existing allocation. Complete combined PLAN/layout QC and applicable approval; no FEATURE-LAYOUT filename is introduced.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-008 — Prepare and accept FEATURE-TASKS.
    - Depends on FDOCS-007 and required publication/issue closure.
    - Derive scoped product T tasks/reviews, including API consumers and contract checks against selected artifact owners, with global IDs and single executable ownership. Complete task QC/report and applicable approval. Include HANDOFF at the mapped pass stop; do not activate implementation solely from this completion.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
- [ ] FDOCS-009 — Pass feature documentation package QC.
    - Depends on FDOCS-008 and required publication/issue closure.
    - Assess the whole feature set, selected model/API-design/contract artifacts and affected accepted main context, preparation/decision/QC evidence and task readiness; resolve/recheck blockers. Persist passing FEATURE-QC-REPORT, preparation evidence, HANDOFF and this checked entry. Keep merge/milestone effects pending until verified.
    - Commit the accepted source or assessed reusable inputs, required QC, FEATURE_PREPARATION evidence and initial checked task together; publish/read back before enabled issue closure or dependent work.
