# Verify, publish the checkpoint, and stop

## Verify the amendment

Use **sdd-verify** to assess the revised acceptance conditions, affected dependents, integration points, and required project checks. For a reduction, establish that the removed functionality is absent from the supported implementation, relevant tests and documentation agree with the reduced scope, and retained behavior remains valid. Text deletion alone does not establish behavioral removal.

Inspect governing documents and code together for obsolete claims, dangling references, inconsistent task scope, and unintended dependency effects. Use actual outcomes, including failures, warnings, skipped checks, and gaps; do not infer verification from a checklist edit. Return test-design changes to **sdd-tdd** and documentation fixes to **sdd-docs**, while this steering workflow owns production repairs.

Reassess affected task and parent completion claims against the revised acceptance and exits. Preserve unaffected verified status. Mark amended work complete only when its implementation, tests, documentation, and required evidence are complete; do not imply that all remaining tasks or the whole project are done.

## Commit and push

Before the first SDD commit, apply **sdd-manage**'s [repository bootstrap](../../sdd-manage/references/repository-bootstrap.md), including its owned root records and README links in the amendment commit while honoring explicit path limits.

Refresh HANDOFF with the verified amendment outcome and the paused parent's scope/stop under [continuity](../../sdd-manage/references/continuity.md). Include it with the owning verified amendment checkpoint; the prospective merge restores parent context without resuming tasks.

Use **sdd-report** to describe the actual amendment, reason, verification, and supported result. Identify the commit as a steering amendment to affected stable task IDs, rather than completion of the next main-list task, and include only resolved issue references. Stage only amendment-owned document, code, test, status, and evidence changes, preserving unrelated staged and unstaged work. Inspect the staged diff and exclude unrelated staged content from the commit while preserving its index state. A normal commit includes all staged changes; use a path-scoped commit only for wholly amendment-owned file contents, or isolate selected changes in a temporary index. Stop if ownership cannot be separated safely. Commit the coherent verified amendment and its status together; honor the project-designated evidence location, otherwise record check/state/coverage facts and any authorized test-first exception beside affected owning entries or existing linked evidence, or in the change report/commit body for taskless work. Add no transaction journal. Inspect the resulting commit and remaining staged and unstaged diffs; after a temporary-index commit, reconcile any stale committed owned entries in the ordinary index without altering unrelated staged content.

Apply [per-commit publication](../../sdd-manage/references/git-workflows.md#publish-each-commit) to every amendment/report commit: publish and read back each before continuing work or creating another commit, including independent amendment work. Explicit user-directed local-only/deferred publication remains a scoped exception.

Push the amendment commit and outstanding commits on the current branch to its established remote branch and confirm remote containment. Use the [supervised HTTPS publication entry](../../sdd-manage/references/git-workflows.md#monitor-pending-git-operations) from the initial attempt with deterministic credential selection, diagnosing suspected stalls automatically. Coordinate observed [helper blockage](../../sdd-manage/references/credentials.md#blocked-or-interactive-credential-helper) or credential failure through **sdd-manage**; reconcile pending process/remote effects before recovery retry. Do not guess a destination or force-push. On an unresolved push failure, preserve the commit and report the pending push; do not resume task-list implementation.

When hosted tracking is active, use **sdd-forge** to reconcile issue state warranted by the revised task scope and evidence. Apply the shared backend object lifecycle to affected review/report and milestone acceptance. Reconcile authorized milestone reopening through sdd-forge when current exits are invalidated, and retain reassessment pending until established again. Preserve earlier reports and required TODO provenance. Do not reopen an issue solely because historical functionality was removed, or close one solely because its task disappeared. Preserve issue history and report any access failure or ambiguous mapping as pending reconciliation.

## Merge the amendment

After working-branch acceptance and amendment persistence, use **sdd-manage**'s **Git workflows** reference for the default explicit merge into the paused implementation branch. Verify the merged state before making its two-parent merge commit, push the target, and confirm containment. Do not merge into the default branch unless it is the established paused target. Report an already integrated amendment without fabricating a second merge. Conflicts or failed merged checks remain scoped amendment work; preserve the exact merge state when blocked. A rejected target push retains the verified merge commit as pending publication.

## Continue after a blocker

Repair verification failures within the commanded scope and repeat affected checks until verified or concretely blocked. On a blocker, identify working and target branches, trusted checkpoint, pending paths and ownership, completed checks, failed or unavailable conditions, task claims requiring reassessment, and the needed decision or facility. Do not publish unverified work as a completed amendment.

Before integration the target retains its paused checkpoint. A merge attempt may leave a separate target worktree in progress; report that state explicitly rather than describing it as a finished checkpoint. The human can command continuation of this same amendment after the blocker is addressed. Resume the branch or in-progress merge, finish verification/persistence/publication, and return control. No automatic reset, new feature overlay, task-list advancement, or handoff to **sdd-implement** is required.

## Return control to the human

Report the accepted objective, amended implemented behavior, retained behavior, existing development documents changed, affected task statuses, verification evidence and limitations, amendment and merge commits, working/target branches, target publication, and pending hosted reconciliation. Identify consequences for remaining tasks as findings, not instructions that automatically launch their implementation.

Stop after the report, including when the amendment is successful. There is no handoff to **sdd-implement**, no automatic selection of its next task, and no automatic steering follow-up. The human decides whether and when to resume the main workflow or command another amendment.

## Affected orientation checkpoint

Apply the manager's [agent orientation](../../sdd-manage/references/agent-orientation.md) when material source/layout/check commands, governing links or active task/feature ownership changes within this workflow. Preserve controlling manual instructions and update affected root AGENTS.md with the verified owned checkpoint. Feature archive/transfer keeps current canonical owner links accurate; historical checklists are not duplicated as executable owners. Explicit path limits or real policy conflicts return to the manager. An unchanged startup requires no rewrite.
