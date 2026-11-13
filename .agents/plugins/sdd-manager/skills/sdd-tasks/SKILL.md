---
name: sdd-tasks
description: Use when deriving or reviewing executable software-development tasks from an accepted design, SPEC, PLAN, and layout; creating docs/dev/TASKS.md or scoped docs/dev/FEATURE-TASKS.md; or reviewing task status and dependencies.
---

# Create and review task lists

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

**Development documents describe the project; they must not narrate their SDD preparation process.** Apply the [content boundary](../sdd-manage/references/human-document-review.md#development-document-content-boundary) when authoring, revising or reviewing any root, feature counterpart or focused child, in every mode.

Obtain human approval of new TASKS or FEATURE-TASKS before implementation or hosted task projection, unless that checkpoint is explicitly preapproved. Apply [human document review](../sdd-manage/references/human-document-review.md) to necessary feature proposals and direct calls. Reuse acceptable existing inputs; begin with any requested interactive review.

For **feature preparation**, load [feature preparation](../sdd-manage/references/feature-preparation.md) and the shared [mode/pass policy](../sdd-manage/references/doc-design-modes.md) before dependent authoring. Use its applicable FDOCS stage, FEATURE_PREPARATION decision/QC evidence and mapped approval/stop; preserve sufficient main inputs and do not replay main initialization.

For fresh/resumed **main preparation**, load [main preparation](../sdd-manage/references/main-preparation.md) before repository writes, including direct calls. Its pre-write tracking gate, DOCS_TASKS first-approval commit and issue progression, package QC and merge/final-checkpoint rules govern this path. The coordinator persists the accepted document, current-pass decision/QC references in DOCS_PREPARATION and its checked DOCS task together; DOCS_TASKS contains task definitions/checkoffs only. Ordinary later edits retain completion; an explicit cursor reset reopens the same tasks/issues. Apply the [selected mode and pass boundary](../sdd-manage/references/doc-design-modes.md), including autodoc’s stop after DOCS-008 before package QC. The preparation-branch guidance below retains other paths’ scope and does not waive these main gates.

For preimplementation project authoring, have **sdd-manage** establish the dedicated design-docs branch under its [preparation integration gate](../sdd-manage/references/branch-management.md#preparation-integration-gate). Commit project documents and required QC reports there, then push and verify remote containment before handing off or advancing, under [per-commit publication](../sdd-manage/references/git-workflows.md#publish-each-commit). Before a dependent implementation branch is created, the manager explicitly merges accepted preparation into the actual default branch, verifies and publishes that baseline. Campaign plans/reports remain on revision branches; active implementation and steering amendments preserve their working-branch ownership. Read-only work creates no branch.

Choose the requested operation and load only its reference. A request to generate TASKS does not authorize implementation.

Apply **sdd-conventions**' **Development-document QC** reference (`skills/sdd-conventions/references/development-document-qc.md`, bundled dependency). Authoring includes scoped review, correction/recheck and the adjacent report before dependent progression; pure review does not authorize corrections.

| Work | Load |
| --- | --- |
| Derive the complete task hierarchy or a scoped feature task list | [task derivation](references/task-derivation.md), then [conformance review](references/conformance-review.md) |
| Review generated task structure and PLAN conformance | [conformance review](references/conformance-review.md) |
| Review status, completion evidence, and dependencies | [progress review](references/progress-review.md) |

Read the relevant accepted PROJECT, ARCHITECTURE, DECOMPOSITION, SPEC, PLAN, layout, and their selected children/peer artifacts or active feature documents as needed for the operation. Inspect TASKS and any active FEATURE-TASKS, Git evidence, and affected code or tests when status or existing work matters. Use **sdd-conventions** to assess task boundaries and Phase → Milestone → Task identity and parentage. Do not invent requirements, delivery strategy, or physical ownership when those inputs are unresolved.

Read-only review can proceed without mutation. Creating or modifying TASKS or FEATURE-TASKS requires **sdd-manage** to coordinate the user's request and a current **sdd-orient** handoff establishing an eligible Git worktree, applicable instructions, target paths, and ownership of dirty changes. This skill does not implement orientation, verification, recovery, or code changes.

`docs/dev/TASKS.md` owns the complete intended phase → milestone → task hierarchy. An active `docs/dev/FEATURE-TASKS.md` owns the feature's scoped executable delta and inspectable progress until reconciled into TASKS. Use one project-wide task ID space; never copy a task as a second independently checked item. Give each phase a Markdown heading and keep its phase checkbox as the root of the nested checklist. Use **four spaces per nested level**: phase check item at the left margin, milestone indented four spaces, task indented eight. PLAN or an active FEATURE-PLAN owns strategic phase and milestone definitions and exit conditions; the applicable task list breaks them into executable work without redefining them. Layout owns physical placement; SPEC owns required behavior and acceptance. A checked box is a claim to verify against evidence, not evidence by itself.

Feature-delta reconciliation of TASKS and FEATURE-TASKS and incorporation into the main hierarchy belong to **sdd-integrate-feature** within its selected scope. Human-commanded direct checkpoint amendments belong to **sdd-steer**. **sdd-implement** owns executable range selection, main task-list execution, and completion updates.

At completion, report the task structure established, completion findings and evidence checked, dependencies or blockers, and documents inspected or updated. Do not report planned tasks as implemented features or continue beyond the selected work boundary.
