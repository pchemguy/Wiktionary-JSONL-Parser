# Completion and status reports

For feature preparation, report mapped FDOCS stage completion using FEATURE_DOCS_TASKS and FEATURE_PREPARATION evidence, separately from current document validity, FEATURE-QC-REPORT readiness, preparation integration, selected campaign preparation milestone closure and the final implementation checkpoint. Use [feature preparation](../../sdd-manage/references/feature-preparation.md); no preparation checkbox proves later publication or whole-feature implementation.

For main preparation, report DOCS_TASKS task completion using DOCS_PREPARATION approval/control evidence, separately from current document validity, DOCS-009 package QC, documentation integration, `sdd-docs-main` milestone closure and the final preimplementation checkpoint under [main preparation](../../sdd-manage/references/main-preparation.md). Ordinary later revisions retain completion; an authorized cursor reset reopens the same active-pass tasks/issues. Keep result/decision narrative in DOCS_PREPARATION, not the task list.

For implementation, use the requested boundary from the owning TASKS or FEATURE-TASKS list. A checked box is a claim to compare with actual artifacts, verification output, and Git commits. Inspect the current implementation and relevant acceptance or exit conditions; distinguish task commits, working-branch acceptance, integration into the established target, target publication, and hosted issue state. The target need not be the default branch.

## Task

State task ID, outcome, status, and an implemented-feature summary. Then give the change and reason, files or components affected at a useful level, exact checks and outcomes, commit SHA or pending commit, and resolved issue URL or pending hosted reconciliation if applicable. Describe omissions and unverified conditions plainly. Report **completed** only when task-specific acceptance, documentation and tests, required verification, durable commit, and task-list status are reconciled. An issue closed by the host is not proof.

## Milestone and phase

Summarize the actual capabilities delivered across constituent tasks, rather than a list of checkboxes. Name task IDs and relevant commits, aggregate verification and integration evidence, the PLAN or FEATURE-PLAN exit conditions checked, unresolved defects, and the next stopping boundary. In FEATURE-TASKS, a checked parent covers only that feature's listed work and exits; it does not assert completion of the whole-project parent in TASKS. If some tasks or exits remain, report **partial** or **blocked** with the specific cause.

Name known baseline/end commits or stable boundary identities so changes can be retrieved from Git on demand; do not export patch files or embed the report's own future SHA. The assigned milestone boundary task (standalone review or final implementation task) or phase review task refreshes HANDOFF with this report's checkpoint in the same closing commit under [continuity](../../sdd-manage/references/continuity.md#establish-and-refresh). Summarize older completed phases with links and keep detail in the report; no per-task handoff progress log is required.

## Review reports and TODO aggregation

Use the [backend object lifecycle](../../sdd-conventions/references/backend-object-lifecycle.md) for report placement and deferral rules. Main phase reports use `docs/dev/reports/phases/<phase-id>/PHASE-REPORT.md`; milestone reports share that directory as `<milestone-id>.md`. Steering records use its nested `revisions/<revision-id>/`; feature reports remain under their feature directory. Link from the assigned boundary task; draft reports before its commit, without requiring the report to contain its own commit SHA.

For a milestone/phase review report, state stable identity, actual reviewed source, delivered capability, implementation code review coverage and findings, commands/outcomes and limits, repairs/commits, exit assessment, TODO and next boundary. Distinguish inspection from test execution. Include fixed findings and rechecks. An unresolved required check, bug, critical issue or contract violation blocks completion; the report does not waive that blocker. Execution owns report persistence and completion decisions.

Put required repairs and findings of unestablished deferral eligibility in Findings/Blockers, not the deferred TODO. Write `TODO: None` when empty. For each admissible deferred non-critical item include stable finding ID, location/evidence, impact/severity, contract-preserving deferral rationale, proposed solution options/tradeoffs and follow-up owner/scope. Phase reports retain unresolved milestone findings and add phase findings, preserving IDs/provenance. When the full owning task list completes, draft its final IMPLEMENTATION-REPORT.md aggregating unresolved/deferred items and solution options, deduplicated by ID, with references to resolved findings. The final phase review task includes this report; a partial range produces no full-list completion claim. Do not create a second progress journal.

## Interrupted or limited evidence

For an interrupted task or unavailable check, state the last trusted Git state, observed dirty or staged work, checks completed and not completed, and the exact blocker. Do not infer that a half-written commit or test log finished the task. **sdd-orient** identifies interrupted task state, **sdd-manage** coordinates scope, and **sdd-implement** owns continuation; this skill summarizes their evidence. If a performance result is statistically inconclusive, a security fix has only partial regression coverage, or a test run excludes a required suite, make that limit visible in the result.

Use the kind-specific sections in [change kinds](change-kinds.md) where they materially explain the outcome. Keep source attribution near claims: task and document sections for intended behavior; command/output and commits for observed behavior. Do not create a second progress journal or alter TASKS while drafting a report.

## Evidence and test-first limits

Carry task/change identity, tested state, actual commands/outcomes, condition coverage, and material limitations from the verification handoff. Name the designated or owning-entry evidence location; taskless maintenance may use its ordinary report/commit body. Include any authorized test-first exception with its concrete rationale, applicable policy or user authorization, observed alternative evidence, and remaining gaps. Missing RED history remains missing; a sensitivity check or characterization run is not proof of an earlier test-first cycle. Do not add a separate mandatory evidence format.

## Branch boundary

Include the campaign/phase identity and retained directory where applicable. A completed task range in an incomplete main phase is a pushed checkpoint, not a completed integration; report phase work/exits remaining and the paused branch. Report eligible feature archive paths and main task owners, without treating historical lists as executable.

Report working and target branches, starting checkpoint, task or amendment commits, merge SHA and parent tips, working-branch and merged-state verification, and remote containment or pending publication. Distinguish a verified task from a completed integrated workflow. A failed merge or target push remains an explicit blocker even when task commits are verified and pushed. Identify already integrated work without claiming a new merge, and state when an explicit user instruction retained work on its branch.

## Optional capability state

For hosted tracking, report recommendation, pending/confirmed/declined decision, activation and observed provider objects separately. Cite the actual user decision or carried scope. An inactive-state line in an agent-authored plan does not prove refusal; a token or general push authority does not prove activation confirmation. Late reconciliation is current recovery, not proof that projection preceded historical task execution.
