# Progress review

TASKS and an active FEATURE-TASKS are human-readable status views of the complete hierarchy and scoped feature delta respectively. Git commits, verification results, and inspected artifacts provide the evidence behind them. Compare checked items in the applicable list with the present implementation and the task's acceptance evidence; do not infer completion from a checkbox, a commit message, or file presence alone. Review is read-only; report missing or conflicting evidence to the owning workflow.

## Completion evidence

Review existing claims against their accepted task or parent exit conditions and the implementation, verification, documentation, and Git evidence supplied by **sdd-implement**. It owns completion criteria and task or parent checkbox updates. **sdd-report** composes the resulting implementation summaries. Report missing evidence or a claimed scope broader than the evidence supports; this review does not perform completion updates.

Validate explicit review units and their report paths against the [backend object lifecycle](../../sdd-conventions/references/backend-object-lifecycle.md). Checked parents need review/report evidence as well as delivery-task exits; a feature parent cannot establish whole-project hosted closure. Report missing review tasks as an accepted-hierarchy amendment need, never silently insert them.

## Route findings

Pass task-list reconciliation, including feature-delta changes to task scope, dependencies, or parentage and FEATURE-TASKS incorporation into TASKS, to **sdd-integrate-feature**. Direct checkpoint amendments belong to human-commanded **sdd-steer**. Pass unfinished main implementation or completion-evidence gaps to **sdd-implement**. Report eligibility and dependency findings to **sdd-implement** before it selects further work.

## Distinguish preparation readiness

Use [conformance review](conformance-review.md) for task structure, PLAN alignment and preparation gates. Progress checks report missing/stale preparation evidence without automatically repairing documents. Ordinary status/evidence changes alone do not invalidate unchanged contract/decomposition review; changed scope, hierarchy, dependencies or upstream decisions require affected reassessment under the shared QC policy.
