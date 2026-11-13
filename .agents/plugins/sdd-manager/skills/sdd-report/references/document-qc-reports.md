# Document QC review reports

Compose from the artifact owner's actual review/correction evidence under **sdd-conventions**' **Development-document QC** policy. This skill does not decide readiness, execute checks or authorize corrections. Use the owner's current Ready/Blocked conclusion with its supported scope and limits.

## Placement and identity

Place `SPEC-REVIEW-REPORT.md`, `PLAN-REVIEW-REPORT.md` or `TASKS-REVIEW-REPORT.md` beside the reviewed root; feature counterparts use `FEATURE-SPEC-REVIEW-REPORT.md`, `FEATURE-PLAN-REVIEW-REPORT.md` and `FEATURE-TASKS-REVIEW-REPORT.md` beside the selected feature roots. One report covers the root and its selected children and peer artifacts, including model/API-design/contract definitions. PLAN review covers relevant layout. These preparation reports are distinct from phase/milestone implementation reports and general campaign records. At feature archive retain selected QC reports beside archived sources and repair authorized links; historical feature readiness does not certify current main documents.

Identify the complete selected artifact set, its paths and exact reviewed/governing states: available full Git commit with file/blob identities, or content hashes for pending edits. A report need not contain its own future commit SHA. Use existing IDs/links and a compact grouped coverage table; no separate traceability database or row per SPEC sentence is required.

Brief assessment evidence for PROJECT/FEATURE belongs in its mapped preparation record; this report procedure introduces no separate brief report. DOCS-QC-REPORT and FEATURE-QC-REPORT are whole-package reports under their coordinator completion gates; an individual brief or root assessment does not certify package readiness.

## Compact report structure

```markdown
# PLAN review report

## Current gate

State: Ready or Blocked, as established by the owner.
Reviewed scope/state: root, selected children/peer artifacts, layout and exact identities.
Governing inputs: accepted upstream roots and selected artifacts with exact identities.
Checks/evidence: actual review methods and outcomes; limitations/exceptions.
Remaining blockers and affected downstream stage: explicit findings or none.

## Initial review

Record date/reviewer, original reviewed states, grouped conformance coverage,
count assessments and stable located findings with consequences and rechecks.

| Group | Delivery count | Excluded review units | Scope/count assessment and rationale |
| --- | --- | --- | --- |
| Actual phase or milestone ID | Observed number | IDs/count | Retained or revised boundary with evidence |

| Finding | Location / consequence | Correction owner / objective recheck | Current disposition |
| --- | --- | --- | --- |
| Stable review ID | Concrete evidence | Actual responsible owner | Open / resolved / rejected with evidence |

## Revision 1

Preserve the original finding IDs. Record actual corrected files/owners, why,
exact revised artifact and governing states, performed rechecks/results,
current dispositions, exceptions and remaining blockers.
```

Use equivalent concise prose where a table adds no clarity. Count tables apply to PLAN phases and TASKS delivery milestones; SPEC instead reports design/contract coverage. Label planned checks as planned, not performed. Do not fabricate a Revision section when no correction/recheck cycle occurred.

## Retained review and revisions

Append `Revision 1`, `Revision 2`, etc. for each correction/recheck cycle, including a later recheck after changed inputs; never erase original observations or earlier revised-state evidence. Update only the concise current gate/index to reflect the latest result. Explain retained equivalent evidence where changes do not affect its reviewed concern. Preserve finding IDs across cycles and avoid duplicate reports after interruption.

Ready requires current applicable coverage and no unresolved confirmed issue. A justified small/large group or rejected false positive is an assessment with reasoning; a knowingly deferred confirmed issue is Blocked. Explicit human exceptions keep their scope/consequences visible and do not relabel the review as passed. The implementation report's non-critical code TODO allowance does not clear document preparation gates.

Return the report, checked source identities, gate supplied by its owner, actual checks, limits and required corrections. The active authoring/integration/steering workflow persists corrected artifacts and report together under ordinary scoped Git rules.

## Human decision evidence

Use the actual owner/coordinator evidence under [human document review](../../sdd-manage/references/human-document-review.md). Keep technical readiness and human review pending/accepted/revise state separate. Record presented document/proposal scope, exact source identity and actual decision in existing preparation/handoff evidence; never infer acceptance from Ready, a commit, silence or broad operation authority. A PLAN strategy-only report identifies pending layout coverage and blocked TASKS readiness; the subsequent layout review updates combined QC without erasing the separate human decisions.
