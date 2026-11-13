# Feature documentation preparation

Load at feature preparation entry/resume, mode selection, document completion, reset, package QC or implementation handoff. **sdd-manage** coordinates; **sdd-design** owns the [FEATURE brief](../../sdd-design/references/feature-brief.md). Apply the shared [mode/pass policy](doc-design-modes.md) and [human review](human-document-review.md); a feature is a scoped change to an existing system, not a new whole-project MVP.

## Establish preparation before writes

1. Establish the request/range, applicable instructions, accepted main baseline, actual default/creation-parent branches, existing state and owned paths. Allocate the campaign identity read-only, preserving other active work. Select/recover interactive/onepass by default, autodoc or the supported explicit/predefined multipass/autoloop policy; announce brief approval, delegation, scope and the exact stop before dependent work.
2. Resolve [tracking selection](tracking-decision.md#feature-documentation-preparation). When enabled, have sdd-forge verify the campaign-specific preparation milestone and all nine issue associations under [feature preparation tracking](../../sdd-forge/references/github-feature-preparation.md) before any target-repository write, including branch/ref, token/ignore/config or document changes. Keep projection drafts/protected transient credentials outside the repository until this gate clears. Reuse eligible existing access; unknown projection blocks writes unless an explicit scoped local-only override applies. This is separate from product phase activation.
3. Establish the authorized `design-docs/<campaign>-<slug>` branch, original baseline/parent and intended implementation target under [branch management](branch-management.md). Execute/reuse applicable manual provenance setup under its existing default/override rules; do not replay main DOCS-001 or copy/reconcile all root guidance as a feature bootstrap. Resolve missing governing instructions/ownership before dependent work.
4. Initialize task-only `docs/dev/FEATURE_DOCS_TASKS.md` from the [task template](../../../assets/FEATURE_DOCS_TASKS_TEMPLATE.md) and `docs/dev/FEATURE_PREPARATION.md` from the [record template](../../../assets/FEATURE_PREPARATION_TEMPLATE.md). Record identity/source navigation directly here, without a preparatory package navigation artifact. Do not overwrite another feature's active sources. Establish HANDOFF under existing continuity checkpoints. FDOCS-001 closes with its context/record/task evidence, publication and enabled issue closure. The first FEATURE draft travels with updated preparation evidence at FDOCS-002.

## Artifact ownership and stage model

| Artifact | Responsibility |
| --- | --- |
| FEATURE | Concise intended delta, retained behavior, compatibility/constraints and material product questions; sdd-design owns content. |
| FEATURE_PREPARATION | Original request/reference, identity/branches/active paths, mode/pass/scope sequence, consequential proposed/confirmed/delegated/open decisions, exact document acceptance/QC and pending transitions; sdd-manage owns evidence/control. |
| FEATURE_DOCS_TASKS | FDOCS definitions/dependencies and completion checkboxes only; no decision log or second preparation cursor. |
| FEATURE-QC-REPORT | Whole-set readiness and findings; sdd-verify assesses, coordinator routes repairs. |
| FEATURE-TASKS | Product implementation tasks and evidence; global T IDs remain distinct from campaign-qualified FDOCS IDs. |
| HANDOFF | Durable boundary checkpoint linking these owners, without per-decision rewrites. |

| Stage | Output / acceptance | Owner |
| --- | --- | --- |
| FDOCS-001 | Feature context, identity, governing sources, records and tracking/provenance readiness | sdd-manage |
| FDOCS-002 | FEATURE first approval | sdd-design |
| FDOCS-003 | Architectural assessment: accepted FEATURE_ARCHITECTURE if needed, otherwise evidenced reuse of main architecture | sdd-design |
| FDOCS-004 | Component/API/model assessment and selected design artifacts; scoped proposals or evidenced reuse | sdd-design |
| FDOCS-005 | FEATURE-SPEC and selected contract artifacts, required QC and applicable acceptance | sdd-specify |
| FDOCS-006 | FEATURE-PLAN or sufficient accepted strategy, required QC and applicable acceptance | sdd-plan |
| FDOCS-007 | Scoped layout proposal or sufficient existing allocation, combined PLAN/layout QC and applicable acceptance | sdd-plan |
| FDOCS-008 | FEATURE-TASKS, required QC and applicable acceptance | sdd-tasks |
| FDOCS-009 | Whole-feature-package QC and FEATURE-QC-REPORT | sdd-verify; sdd-manage coordinates |

Each stage records applicable/new or reusable input, exact identity, assessment/decision basis and relevant report in FEATURE_PREPARATION. Reuse completes an assessment stage with evidence, not a fabricated new document or human approval. Selected model/API-design artifacts share FDOCS-004's proposal/acceptance; contract artifacts share FDOCS-005's, whether inline, children or peer documents. Record paths/owners and exact accepted/QC states in FEATURE_PREPARATION. These artifacts add no stage, issue or approval round; whole-package QC includes them. Unchanged accepted inputs do not require ceremony. Stage dependencies remain ordered even when no overlay is needed. No FEATURE-LAYOUT document or additional child issues are introduced.

## Decisions, completion and proactive guidance

Keep product content under the [content boundary](human-document-review.md#development-document-content-boundary); workflow records may describe preparation. Preserve the original seed and distinguish supplied requirements, agent proposals, accepted/delegated choices and unresolved matters. The evidence record has no independent approval gate. Link detailed contracts/QC and retain compact per-pass/cross-scope decisions under the shared mode policy, without transcripts or parallel ledgers.

Before FEATURE approval, proactively compare requested scope with existing behavior, identify material interactions/compatibility constraints, recommend credible choices and resolve intent within actual decision authority. Do not duplicate already supported capabilities, reopen unrelated project decisions or defer consequential brief gaps merely because SPEC comes later. At each handoff, report the actual stage, changed/reused inputs, material rationale, pending human choice and next stop. Autodoc preapproval never replaces technical QC; eligible autoloop decisions receive concise visible rationale and proceed under the shared delegation rules.

For each document stage, publish/read back a reviewable proposal before a required human checkpoint. After actual acceptance or applicable preapproval/reuse assessment, commit the accepted source and selected child/peer artifacts, required QC, preparation evidence and initial checked FDOCS entry coherently; publish/read back before closing/readback of its existing issue or advancing. Use known proposal/blob/content identities rather than a containing commit's future SHA. Preparation tasks use this coordinator contract, not the product T-task execution/audit protocol. Ordinary later revisions retain first-completion status while invalidating/rechecking affected readiness; reset below explicitly reopens the pass.

## Pass completion, reset and recovery

A feature document pass spans FDOCS-002–008. After FDOCS-008 publication and enabled issue closure, apply the selected shared mode: autodoc stops before FDOCS-009; human-controlled multipass waits for reset/advance; autoloop resets for only remaining predefined scopes and then stops. Refresh HANDOFF with the pass result and pending boundary in the FDOCS-008 completion checkpoint. Do not run package QC, merge preparation, close its milestone or activate implementation solely because the pass completed. An explicit request covering package QC and implementation may select the subsequent stages; generic feature implementation authority alone does not override the named autodoc stop. Honor a narrower stop.

For an authorized intermediate reset or remaining autoloop scope, retain source files, stable campaign/task identities, first-stage completion, per-pass/cross-scope decisions and prior delivery ranges. Under shared strict/flexible policy, record old/current pass, new scope and approval/delegation basis; in one reset commit uncheck FDOCS-002–009 and set the record's next stage to FDOCS-002, refreshing HANDOFF. Do not reset Git, copy document sets, rewrite completed product evidence or allocate a new preparation branch. Publish/read back; when tracking is enabled, reopen/read back the same eight campaign issues and reconcile milestone state before new document work. Recover partial effects by exact identities, not another pass increment.

On continuation, reconcile task checkoffs, current record, documents/QC, Git and selected hosted effects. Preserve pending approvals and material blockers, reuse valid completed work and resume the earliest unmet authorized operation. Mode/scope changes are prospective and retained before dependent use; an old pass's acceptance does not certify the new one. Narrow later-stage requests preserve their actual scope, and simple corrections/steering retain their own workflows.

## Final package QC, integration and checkpoint

When the selected range permits FDOCS-009 and FDOCS-001–008 plus enabled issue closures are complete, sdd-verify assesses FEATURE, necessary design/spec/plan/layout/tasks and children/reports, both feature preparation records, actual decisions/publication and affected accepted main documents/implementation. Check delta scope and preserved guarantees, cross-document contracts, traceability, dependencies, physical allocation, task derivation, compatibility/regression coverage, unresolved choices and implementation readiness. Individual Ready reports are insufficient. Retain exact source, outcomes/findings and limits in `docs/dev/FEATURE-QC-REPORT.md`; main-project unrelated areas need no rewrite or retest as ceremony.

Route scoped repairs and material choices to their owners; recheck affected readiness/acceptance. While required evidence is blocked, FDOCS-009 and its issue stay open. On a passing result:

1. Commit the report, FEATURE_PREPARATION evidence, refreshed HANDOFF and FDOCS-009 checked together; publish/read back, then close/read back its issue.
2. Complete the explicit preparation merge, merged verification and default-branch publication under [preparation integration](branch-management.md#preparation-integration-gate). This publishes active feature deltas; it does not incorporate them into complete main product documents or complete product tasks. Preserve an earlier/no-merge/local-only boundary and its dependent implementation restriction.
3. Only after verified published integration, close/read back the selected feature preparation milestone. Recover pending merges/pushes/closures without replaying completed work.
4. Report package readiness, published baseline and pending effects; pause before implementation unless its final checkpoint is preapproved and a range is authorized. Then apply phase activation and dependent branch setup. A request covering QC and implementation supplies that scope without another routine permission question.

At eligible final feature completion, sdd-integrate-feature incorporates accepted product intent within scope and archives eligible feature sources, FEATURE_DOCS_TASKS, FEATURE_PREPARATION and FEATURE-QC-REPORT with adjacent QC. Partial incorporation retains still-needed sources/evidence. Never copy preparation narrative or FDOCS checkboxes into main product documents/TASKS. Closed records remain frozen; withdrawal preserves actual evidence/disposition without implying implemented completion.
