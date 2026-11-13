# Task derivation

Derive the complete `docs/dev/TASKS.md` from the accepted design, SPEC, PLAN, and layout. For an active feature workflow, derive `docs/dev/FEATURE-TASKS.md` from its design, FEATURE-SPEC, FEATURE-PLAN when present, main governing documents, current TASKS, and layout. Feature-delta reconciliation of existing task lists belongs to **sdd-integrate-feature**; direct human-commanded checkpoint amendments belong to **sdd-steer**. Preserve PLAN's phase and milestone boundaries and meaningful exit gates. The main hierarchy covers the complete intended work; FEATURE-TASKS covers only the feature delta. Both show progress and the next stopping point. Name the feature objective and affected main requirements and tasks. Give feature work new task IDs, including changes to a completed task's behavior; link to existing TASKS IDs for affected work or prerequisites rather than duplicating their items. Preserve existing phase and milestone IDs and names, or use proposed IDs and names from the accepted FEATURE-PLAN for new groups. Parent checkboxes in FEATURE-TASKS measure only the feature's work in that group, not the entire parent in TASKS.

For packaging/release work, **Version numbers in the name of any release artifact are absolutely prohibited, regardless of type.** Derive expected names from the independent package contract before producing scripts; include an observed negative naming check and corrected-source rebuild in the existing delivery task, with no extra administrative task.

## Form tasks

Apply [cross-platform artifact and native-verification scope](../../sdd-verify/references/check-selection.md#cross-platform-artifacts-and-native-verification) when deriving platform build/test work. Include feasible artifact production and checks; unavailable native execution is not a mandatory task or dependency by default. Preserve its exclusion and evidence limit without an unchecked native-only task blocking later work.

In multipass preparation, apply the selected [strict/flexible delivery mode](../../sdd-manage/references/doc-design-modes.md#multipass-delivery-modes) to retained TASKS, rather than regenerating the list. Strict preserves earlier-pass tasks and their phase/milestone ranges; append tasks under the new accepted phases. Explicitly permitted flexible mode may amend the corresponding earlier range for small, fitting scope changes; retain stable IDs, reassess affected dependencies/review tasks and add new work with unused IDs. Record permission and rationale in the mapped DOCS_PREPARATION or FEATURE_PREPARATION record. Neither choice retroactively changes completed implementation evidence.

1. Trace each milestone outcome to the relevant component boundaries, behavioral contracts, physical owners, integration points, and exit checks. Identify prerequisites and work that must be coordinated across components.
2. Split work into coherent increments that can be implemented, reviewed, and verified without leaving dependent behavior incoherent. Derive bounded work within PLAN's meaningful capability increments; not every task must independently deliver user-visible functionality. Prefer one code module or a few closely related modules, plus their tests and documentation, where feasible. Small module scope does not substitute for bounded behavioral growth. An interface change may need a compatibility step and subsequent consumer changes. Avoid tasks that are merely a single keystroke or an entire subsystem.
3. Give each task a project-wide unique stable ID, outcome, expected edit scope, prerequisite task IDs where needed, and concrete verification or acceptance evidence. Point to the canonical SPEC/design or selected model/API-design/contract artifact when the connection would otherwise be unclear. Any permitted refinement identifies that owner, its decision scope and dependent consumer tasks; material unresolved contracts return upstream. The task can identify likely paths from layout but must not make an exhaustive speculative file list.
4. Put meaningful integration, failure-path, documentation, packaging, and milestone-exit work into the breakdown. Include public API usage and internal collaboration checks against their contracts; tests must not depend on private implementation details merely to exercise a public surface. Reach integrated acceptance and relevant regression evidence within each capability increment; preserve the usable path and account for required failure remediation before dependent growth. Include work needed to gather the milestone's functional/usability decision evidence without requiring a usability trial per task. Do not make every SPEC sentence a separate task or repeat all acceptance wording. Surface an unresolved choice as a blocker with its owning document rather than settling it in a task.
5. Apply the [backend object lifecycle](../../sdd-conventions/references/backend-object-lifecycle.md#explicit-review-units): omit a standalone milestone review task when there are fewer than four implementation tasks in that milestone OR only one implementation milestone in its phase. Otherwise append one dependent on the implementation tasks. When omitted, assign whole-milestone code review/testing/repair/report and HANDOFF to the final implementation task, dependent on the other milestone tasks; count it once. The special final milestone of each phase remains exactly one phase code review/testing/report task dependent on completion/closure of all implementation milestones. Give each assigned boundary task stable identity, review scope, required evidence and report links. The last phase review includes the final implementation report/TODO aggregation when the full list completes. If the accepted PLAN lacks these boundaries, return the needed PLAN amendment rather than inventing strategy in TASKS.
6. Check the critical path and phase/milestone totals. Verify that every intended milestone has executable coverage and that its exit evidence can be gathered. TASKS does not prescribe a test implementation for every contract; later verification and implementation workflows choose and run checks.

## Checklist form

Use a `##` Markdown heading for each phase and a checkbox item directly beneath it for the same phase. The heading provides navigation; the checkbox records completion. Use one checkbox item for each phase, milestone, and task. Indent each child **exactly four spaces** beyond its parent; do not use tabs or replace milestone or phase check items with headings. Keep task details within or immediately beneath their own item, indented to remain attached to it. For example:

```markdown
## Phase 1 — Streaming sources

- [ ] Phase 1 — Streaming sources
    - [ ] Milestone 1.1 — Plain stream foundation
        - [ ] T-001 — Define stream ownership and close behavior
            Scope: stream module and focused tests. Depends on: none.
            Evidence: close and early-exit behavior verified against SPEC.
        - [ ] T-002 — Integrate the public stream API
            Scope: public API and integration checks. Depends on: T-001.
            Evidence: package-level usage and error behavior verified.
            Milestone exit: whole-capability code review, required checks and blocker repairs; include the milestone report and HANDOFF with T-002 completion.
            Report: docs/dev/reports/phases/1/1.1.md.
    - [ ] Milestone 1.2 — Phase review
        - [ ] T-003 — Review, test and report phase 1
            Depends on: milestone 1.1 completion/closure. Evidence: phase review, exits, repairs and committed report.
            Report: docs/dev/reports/phases/1/PHASE-REPORT.md.

```

Stable IDs may follow the project's existing convention; otherwise use monotonic task IDs such as `T-001`. Do not reuse or renumber an ID because a task is inserted or removed. Keep parent IDs and names in TASKS consistent with PLAN, and in FEATURE-TASKS with the active feature plan and unaffected main hierarchy. Resolve collisions across the lists before selection or hosted projection. The owning task list supplies task and parent names for hosted projection; do not project conflicting names for one stable ID. Use [progress review](progress-review.md) to assess existing completion evidence; the initial breakdown is unchecked unless verified prior completion is established. **sdd-implement** owns completion updates during execution. Apply the same checklist form and indentation to FEATURE-TASKS. Keep feature progress there until **sdd-integrate-feature** incorporates it into TASKS; do not insert its tasks into TASKS merely to select or implement them.

## Required preparation review

Require current PLAN/SPEC QC evidence before deriving dependent work. After generation, run [conformance review](conformance-review.md) before implementation or hosted projection: inspect PLAN coverage and semantic scope, count delivery tasks separately from mandatory review tasks, resolve confirmed issues, append recheck evidence and persist the adjacent root report with the list. This is authoring work, not a new administrative implementation milestone or task. Do not use completion/progress review as proof of generation quality.
