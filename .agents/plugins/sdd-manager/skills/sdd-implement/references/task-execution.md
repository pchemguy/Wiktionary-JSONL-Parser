# Execute one task

Execute only the current task before its closing commit and verified publication. Follow the [task commit contract](completion-and-checkpoints.md#task-commit-contract); do not implement the next task early to accumulate a combined result.

Read its outcome, dependencies, acceptance conditions, expected paths, and relevant SPEC, design, PLAN, and layout. For feature work, include applicable accepted feature documents. Inspect existing implementation and tests before editing; preserve useful pending work and project conventions.

## Coordinate the development cycle

1. Use **sdd-tdd** to derive relevant scenarios and write or revise tests. For changed behavior or a bug fix, observe the intended failure before the production change; apply authorized exceptions and preserve existing work when historical RED evidence is absent. Behavior-preserving refactoring can use established coverage.
2. Apply production changes within the task scope. Satisfy the accepted contract rather than merely weakening an assertion or hardcoding a passing fixture. Keep component ownership and physical placement consistent with governing design and layout.
3. Use **sdd-docs** after substantive changes to review affected module and API documentation, README, guides, and examples. It reports amendments needed in governing documents to the user; independent work may continue, but a disputed acceptance condition remains unresolved.
4. Use **sdd-verify** for the required checks and acceptance assessment. Inspect actual evidence, failures, warnings, skips, coverage limitations, and declared project or boundary checks.
5. Repair implementation failures within scope. If a claimed completion was premature or later invalidated, apply [task recovery](completion-and-checkpoints.md#resolve-a-task-recovery), separating acceptance from commit-composition and authority issues. Coordinate test repairs with **sdd-tdd** and documentation repairs with **sdd-docs**. Repeat affected verification after relevant changes; existing evidence may be reused only when still applicable.

Development-cycle test runs do not replace the verification campaign. Verification does not mark the task complete or repair code itself. Read the evidence and decide completion under [completion and checkpoints](completion-and-checkpoints.md).

## Scope and blockers

- Preserve unrelated code, documentation, and pending changes. Do not reset or delete existing implementation to reconstruct a test-first history.
- Report missing requirements, conflicting authoritative documents, unavailable prerequisites, or dependencies outside the selected range. Do not turn an unresolved decision into implementation policy.
- Report observed pre-existing or unrelated failures; do not silently expand repairs beyond authorization or claim the suite passes. Resolve whether required acceptance can be established before marking completion.
- If work cannot be completed, keep the task unchecked or correct an unsupported checked claim, including one from an earlier durable task result. Preserve partial work, historical evidence, and any unresolved completion-reassessment note; report the blocker and remaining steps. Commit a partial checkpoint only when the user or project policy authorizes it, clearly distinguishing it from a completed task commit.
- Do not create feature overlays, reconcile the task hierarchy, or perform a checkpoint amendment merely to make the selected task pass. Those changes require their own established scope and owning workflow.

