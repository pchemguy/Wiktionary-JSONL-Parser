---
name: sdd-specify
description: Use when creating, reviewing, or revising docs/dev/SPEC.md, focused specification or contract artifacts, or FEATURE-SPEC.md; defining required software behavior, interfaces, data contracts, error semantics, invariants, and objective acceptance for a new or existing system.
---

# Specify required behavior

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

**Development documents describe the project; they must not narrate their SDD preparation process.** Apply the [content boundary](../sdd-manage/references/human-document-review.md#development-document-content-boundary) when authoring, revising or reviewing any root, feature counterpart or focused child, in every mode.

Obtain human approval of new SPEC or FEATURE-SPEC before dependent planning, unless that checkpoint is explicitly preapproved. Apply [human document review](../sdd-manage/references/human-document-review.md) to necessary feature proposals and direct calls. Reuse acceptable existing inputs; begin with any requested interactive review.

For **feature preparation**, load [feature preparation](../sdd-manage/references/feature-preparation.md) and the shared [mode/pass policy](../sdd-manage/references/doc-design-modes.md) before dependent authoring. Use its applicable FDOCS stage, FEATURE_PREPARATION decision/QC evidence and mapped approval/stop; preserve sufficient main inputs and do not replay main initialization.

For fresh/resumed **main preparation**, load [main preparation](../sdd-manage/references/main-preparation.md) before repository writes, including direct calls. Its pre-write tracking gate, DOCS_TASKS first-approval commit and issue progression, package QC and merge/final-checkpoint rules govern this path. The coordinator persists the accepted document, current-pass decision/QC references in DOCS_PREPARATION and its checked DOCS task together; DOCS_TASKS contains task definitions/checkoffs only. Ordinary later edits retain completion; an explicit cursor reset reopens the same tasks/issues. Apply the [selected mode and pass boundary](../sdd-manage/references/doc-design-modes.md), including autodoc’s stop after DOCS-008 before package QC. The preparation-branch guidance below retains other paths’ scope and does not waive these main gates.

For preimplementation project authoring, have **sdd-manage** establish the dedicated design-docs branch under its [preparation integration gate](../sdd-manage/references/branch-management.md#preparation-integration-gate). Commit project documents and required QC reports there, then push and verify remote containment before handing off or advancing, under [per-commit publication](../sdd-manage/references/git-workflows.md#publish-each-commit). Before a dependent implementation branch is created, the manager explicitly merges accepted preparation into the actual default branch, verifies and publishes that baseline. Campaign plans/reports remain on revision branches; active implementation and steering amendments preserve their working-branch ownership. Read-only work creates no branch.

Choose the requested operation and load only its reference. Enter directly when adequate decisions and project evidence exist; do not replay design exploration as ceremony.

Apply **sdd-conventions**' **Development-document QC** reference (`skills/sdd-conventions/references/development-document-qc.md`, bundled dependency). Authoring includes scoped review, correction/recheck and the adjacent report before dependent progression; pure review does not authorize corrections.

| Work | Load |
| --- | --- |
| Create or revise the system specification and selected detailed contract artifacts | [system specification](references/system-specification.md) |
| Define a scoped change to existing specified behavior | [change specification](references/change-specification.md) |
| Review SPEC quality and identify conflicts | [review](references/review.md) |

Before authoring, identify accepted decisions and the relevant PROJECT, ARCHITECTURE, DECOMPOSITION, existing SPEC, applicable focused children and selected model/API-design/contract artifacts. For an existing implementation, inspect only relevant code and tests to establish observed behavior; do not promote an observation into a requirement without an accepted decision. If a material architectural boundary is undecided or governing sources conflict, return that decision to design or the user rather than inventing a contract.

Read-only review can proceed without modifying files. Creating, revising, or removing project documents requires **sdd-manage** to coordinate the user's request and a current **sdd-orient** handoff establishing an eligible Git worktree, applicable instructions, affected paths, and ownership of dirty changes. This skill does not implement orientation or authorize another workflow.

SPEC is authoritative for intended observable behavior and acceptance; linked contract artifacts own their assigned detailed definitions under the [specification ownership rules](references/system-specification.md#contract-artifacts). PROJECT owns the project brief and FEATURE the scoped feature brief; ARCHITECTURE and DECOMPOSITION own structural design; PLAN owns delivery strategy; TASKS and an active FEATURE-TASKS own their respective executable units; layout owns physical paths. Use **sdd-conventions** when evaluating contract boundaries and necessary decomposition, without moving those shared checks into SPEC procedure. For feature specification, consume the accepted [FEATURE brief](../sdd-design/references/feature-brief.md) respecting the coordinator's first-brief checkpoint and recorded decisions. A feature specification states a scoped intended delta; it does not silently replace the complete main SPEC.

Incorporation of an accepted FEATURE-SPEC into main SPEC belongs to **sdd-integrate-feature**. Direct SPEC corrections remain in the owning system specification workflow.

Report the behavior specified or changed, affected contracts and acceptance conditions, unresolved material questions, and the precise documents inspected or updated. Document work does not authorize code changes, task selection, or continuation into implementation.
