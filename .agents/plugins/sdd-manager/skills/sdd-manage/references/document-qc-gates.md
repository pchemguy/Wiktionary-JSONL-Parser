# Coordinate development-document QC gates

Load **sdd-conventions**' **Development-document QC** reference (`skills/sdd-conventions/references/development-document-qc.md`, bundled dependency) for canonical count/conformance/report/readiness rules. Artifact owners assess readiness; sdd-manage schedules reviews, routes corrections and enforces dependent-stage gates. **sdd-report**'s **Document QC reports** reference composes adjacent reports from their actual evidence.

## Stage handoff

Before dependent use, apply the [development-document content boundary](human-document-review.md#development-document-content-boundary) to each selected main/feature root, child and peer artifact. Check for SDD preparation mode/pass, future document-revision, approval or reset narrative in the product documents. This check applies with preapproval and in every mode; return violations to the owning author before clearing readiness. For main preparation, also check task-only DOCS_TASKS against DOCS_PREPARATION control/decision evidence; neither task checks nor a saved cursor substitute for current acceptance/QC.

| Completed input | Required owner assessment | Dependent operation |
| --- | --- | --- |
| FEATURE | sdd-design: seed/delta coverage, compatibility, consequential decision readiness and product/evidence separation; assessment referenced in FEATURE_PREPARATION | Dependent feature design/specification |
| SPEC / FEATURE-SPEC and selected contract artifacts | sdd-specify: accepted PROJECT or FEATURE and applicable design conformance | PLAN / dependent feature planning |
| PLAN / FEATURE-PLAN with relevant layout | sdd-plan: SPEC conformance and phase/milestone decomposition | TASKS / dependent feature tasks |
| TASKS / FEATURE-TASKS and applicable children | sdd-tasks: PLAN conformance, scope and task hierarchy | Implementation or creation/projection of hosted task objects |

Selected model/API-design artifacts are part of the decomposition task/checkpoint; contract artifacts are part of specification. Include their referenced definitions in conformance and whole-package QC. Use the governing root's review report and preparation evidence; do not create a separate report or checkpoint per optional artifact.

1. Establish the selected document/feature scope, accepted governing inputs, authorized effects and stopping point. Authoring includes its scoped QC correction/recheck and report; read-only review returns findings without silently correcting sources. Literal selected-path-only restrictions prevail; missing required report permission is a concrete scope blocker, not permission to widen paths.
2. At entry and each dependent transition, compare the actual selected root/child/peer artifact set and governing inputs with current review evidence, finding dispositions, scope/coverage and readiness. Reuse demonstrably current equivalent reviews; explain materiality/equivalence from actual differences. A Ready label, file presence or a historical feature review is insufficient alone. Do not fabricate a review for an older project.
3. Obtain the focused missing assessment through the relevant owner within the already authorized scope. Creation/revision of an artifact includes review, authorized bounded corrections, recheck and report persistence before downstream progression. Use existing requirement/component IDs and grouped coverage; no new administrative milestones or task chain is needed for preparation QC.
4. Route missing design/behavior/strategy decisions upstream. Do not revise SPEC to excuse PLAN omissions or PLAN to accommodate accidental TASKS strategy. The owner may resolve routine choices already authorized; ask only for a genuinely missing consequential decision. Preserve read-only limits and unselected owners.
5. For SPEC/FEATURE-SPEC, PLAN/FEATURE-PLAN and TASKS/FEATURE-TASKS, have the owner produce the established adjacent root report with current identities, coverage/count assessments, original findings, appended Revision N rechecks and Ready/Blocked evidence. FEATURE brief assessment stays in FEATURE_PREPARATION with exact source/decision evidence; it introduces no separate adjacent brief report. FEATURE-QC-REPORT is reserved for whole-package FDOCS-009, not brief-only readiness. Corrected artifacts and their report are one coherent preparation checkpoint under [coordination persistence](coordination.md#persist-repository-changes). Do not progress on a draft report, unpersisted required boundary or deferred confirmed issue. Honor explicit local-only publication limits; report any established dependent requirement for unavailable remote evidence separately.
6. For a blocked input, identify the finding, actual owner, needed correction/review scope and blocked dependent operation. Continue only independent authorized work. Explicit human exceptions name scope/consequences without relabeling Blocked as Ready or bypassing implementation acceptance.

For feature whole-package QC after the document pass, load [FDOCS-009 and the preparation completion sequence](feature-preparation.md#final-package-qc-integration-and-checkpoint). Its FEATURE-QC-REPORT covers the delta and affected accepted main context; individual root QC cannot clear this gate.

## Amendments, scope and continuation

Readiness and branch integration are separate gates. Persist project preparation artifacts and adjacent QC reports together on design-docs. Before creating a dependent implementation branch, the manager completes [preparation integration](branch-management.md#preparation-integration-gate) into the repository default branch, verifies the merged state and publishes it. A Ready report or design-docs push alone does not satisfy that baseline. Campaign plans/reports retain their revision-branch ownership.

Material changes to design, behavior, strategy, hierarchy/dependencies or layout invalidate affected downstream review until rechecked. Recheck only impacted concerns; routine completion status/evidence updates alone need not invalidate unchanged conformance. Initial preparation and focused direct calls use the same gate. Main/feature task execution still pushes eligible outstanding commits before other task work; readiness review follows that prerequisite and precedes new execution/phase projection.

sdd-integrate-feature and sdd-steer retain their accepted correction ownership. Coordinate owners' focused assessment of changed main/feature documents and their adjacent reports before dependent use. A SPEC-only incorporation does not authorize unselected TASKS/PLAN edits: report their invalidation and keep those downstream gates blocked until their separately authorized recheck. It can finish its coherent selected incorporation without claiming whole-project readiness.

Feature QC reports stay adjacent to their active roots and, when eligible/in scope, archived sources. Implementation reports retain their lifecycle phase/feature prefixes. Preserve scope, report/source identity, original findings and review history during moves; archive readiness is historical, not current main-document acceptance.

After interruption, inspect files, report source identities, pending corrections, index and commits. Finish the same correction/recheck/report/push without regenerating valid documents or duplicating Revision sections. Do not mark a gate Ready from a lost response, checkbox or commit subject. No new transaction journal is required.

## Human acceptance alongside QC

Apply [human document review](human-document-review.md) independently of technical Ready/Blocked. Pause for human review of each necessary new root/proposal before dependent progression, including direct calls and feature deltas, unless explicit applicable [future-checkpoint preapproval](human-document-review.md#future-checkpoint-preapproval) covers it. Existing acceptable startup inputs need no retrospective interactive review; requested review and actual pending human boundaries remain binding.

Review PLAN against SPEC without requiring a new layout in advance. Review layout against the accepted design and PLAN when it is prepared, and include that assessment in the adjacent PLAN review report before TASKS generation.
