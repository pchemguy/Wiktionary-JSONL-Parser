# Revision campaign modes

Use these modes within the existing [review/revision lifecycle](review-and-revision.md). They select campaign identity, suspension and integration context; they are not additional core development workflows or authority to execute a proposed repair. [Branch management](branch-management.md), [Git workflows](git-workflows.md) and the selected focused owners perform the work.

## Select the mode

| Context and actual authority | Mode |
| --- | --- |
| New revision campaign while another campaign is active | Nested revision campaign: new identity, suspended parent and default parent branch source/return target. |
| Human requests a closely related amendment to the eligible last closed revision campaign | Reopened campaign amendment: same identity, new reopening checkpoint and added accepted actions. |
| Relevant context suggests an eligible related amendment, but the human has not selected reopening | Propose the amendment with campaign/merge/relationship evidence; do not reopen automatically. |
| No eligible active parent or qualifying closed campaign | Use the ordinary revision lifecycle with an explicitly established target; explain a requested amendment’s failed eligibility before substituting a new campaign. |

## Nested revision campaign

When opening a new revision campaign while another campaign is active, suspend the parent’s execution and default to branching from and merging back into its actual campaign branch. An already suspended, incomplete parent remains active for this purpose. Identify the immediate parent from the request, current worktree and retained evidence; branch prefixes alone do not establish ownership. Respect an explicit human target override rather than silently selecting main/default or the parent’s eventual integration target.

1. Establish the parent campaign, actual branch, refreshed published checkpoint, unfinished scope and pending-work ownership. Publish outstanding owned verified checkpoints before further work; unresolved publication or a missing usable source/target blocks dependent setup. Preserve files/index and unrelated work without implicit stash/reset/clean. Use a separate worktree when safe switching is unavailable; do not manufacture a completion commit for unverified work.
2. Allocate a new [campaign identity](../../sdd-conventions/references/workflow-identity.md) and branch/directory. Record parent suspension, child creation parent and full branch-off commit, source/target, return boundary and actual authority in existing active campaign evidence and the child HANDOFF under [continuity](continuity.md). No additional registry is required. Parent source and return target default to the same established branch. Existing project-preparation, review and execution prerequisites remain in force.
3. Run only the selected child review/revision scope. A review-only request publishes its report and stops before source repairs/integration. Accepted execution follows the normal action verification, per-commit publication and explicit two-parent merge into the refreshed parent target, merged-state checks and target publication. Do not infer implementation authority from opening a campaign.
4. During the prospective merge, restore the parent HANDOFF with the child result/evidence and original pending boundary. After verified integration/publication and child closure, switch the worktree back to the interrupted parent campaign branch and confirm its actual branch/HEAD. Return with the child’s verified merge/publication, remaining work and affected inputs/evidence identified. Child integration does not complete, close or automatically resume the parent. Resume only when actual human continuation authority already covers that action; otherwise return control with the parent suspended. A candidate-specific review must re-pin changed source and recheck affected units when resumed.

Lightweight [steering](workflows.md#steering-as-lightweight-revision) remains the human-directed path at a task-list checkpoint without obligatory formal campaign artifacts. A formal nested revision uses its own campaign records; do not silently substitute one path for the other.

## Reopened campaign amendment

A related change can extend the last closed revision campaign by reopening it, executing an accepted delta and explicitly merging it again. This retains campaign identity and published history; it is not Git commit amend, a new campaign allocation or automatic permission to maintain closed records.

### Eligibility and authority

Before reopening, establish all of the following from the current worktree, retained request/results and Git:

- The amendment logically extends, belongs to or closely relates to the selected last closed revision campaign. Unrelated work requires its own scope/campaign.
- The most recent merge on the active worktree branch’s **first-parent history** is that campaign’s final published explicit two-parent merge. Verify both parents, merged source tip containment, established campaign branch/return target and actual completed closure/publication. A merge subject, branch prefix, highest sequence or ancestry alone is insufficient. The newest merge anywhere in ancestry is not this test.
- The active branch is that established return target. Retain any non-merge commits after the qualifying merge in the current refreshed target checkpoint and assess their scope/dependencies. HEAD itself need not be a merge. Another intervening merge fails this eligibility test; do not search farther back to reopen a convenient older campaign.
- The human has authorized reopening and its bounded amendment. An explicit eligible request supplies that authority; do not ask again for an already granted scope. Readily available relevant context may justify a concise suggestion naming the campaign, qualifying merge and proposed relationship, but a suggestion is not permission. Do not load unrelated closed histories to hunt for reuse opportunities.

Missing/contradictory identity, target, closure or publication evidence blocks affected reopening. Explain the concrete mismatch and resolve it or propose a new campaign; do not silently broaden authority or substitute an older campaign. An incomplete campaign, uncommitted merge or completed merge awaiting push resumes its existing active operation under [Git recovery](git-workflows.md#continue-a-blocked-workflow), rather than being declared closed/reopened.

### Reopen, execute and close

1. Reopen only the selected campaign under the [closed-record exception](../../sdd-conventions/references/review-campaigns.md#authorized-reopening). Keep its original ID, full starting baseline, directory and branch association. Record the qualifying prior merge, current target/reopening checkpoint, accepted delta and unfinished parent return boundary in existing campaign evidence. Other closed packages stay frozen.
2. Bring the recovered campaign branch forward to the refreshed target checkpoint using [branch management](branch-management.md) and [incoming synchronization](git-workflows.md#merge-purpose). Preserve the receiving campaign's identity, original parent and current amendment boundary in HANDOFF; this catch-up is not its final return merge. Reuse the named branch when established; a missing branch can be recovered from verified history under the same association. Inspect divergence, worktree occupancy, pending files/index and the full amendment difference. Preserve unrelated work/history; no implicit reset, replay, force-push or renaming to hide a conflict. Publish/read back every resulting owned commit before further work.
3. Extend the plan with unused stable action IDs and accepted scope, then execute/verify only those actions. Append actual reopening/revision evidence and current disposition without erasing original observations, earlier decisions, prior check outcomes or closure/integration facts. Distinguish original baseline from reopening source and earlier acceptance from the amended candidate’s rechecks. Do not invent a preceding review for a directly accepted amendment.
4. Finish active reports/navigation and applicable rechecks, publish action checkpoints, explicitly merge the complete verified amended tip again into the established return target, verify/publish that target and record the integration facts before closure. A new amendment tip requires its own integration even though the earlier tip is already contained. Retain branches and the campaign directory. Further qualifying amendments reuse the same process and original identity.
5. Close the amended campaign only after its selected scope and required final persistence/integration/publication are complete. Blockers retain active amendment state and actual pending work. After closure, switch the worktree back to the interrupted campaign branch (the established return target) and confirm its actual branch/HEAD. Do not resume/close that campaign unless actual continuation authority covers that action; affected candidate-specific review evidence requires reassessment when resumed.

## Integration summaries and closure

Both modes use the shared [campaign integration summary](../../sdd-report/references/object-drafts.md#campaign-integration-summary): final campaign title/objective, actual review and executed/delivered scope, merged-state checks/limits and compact provenance. A reopened amendment carries a concise cumulative retained result plus separately identified new actions/delta, prior integration, unchanged original campaign-opening commit pointer, full original branch-off SHA and current reopening checkpoint; an enclosing merge identifies included nested outcomes without duplicating them. Use integrated commit ancestry for release evidence, not current branch tips. The message precedes publication/return and cannot by itself establish campaign closure.

## Return worktree safely

For both modes, branch return is a required completion step distinct from resuming work. Final integration may already leave the worktree on the interrupted campaign branch; verify that state instead of switching redundantly. If separate worktrees were required, return through the established parent/target worktree rather than checking out its branch in two worktrees. Preserve pending files/index and unrelated work; do not implicitly stash/reset/delete to force a switch. Report a blocked safe return and the actual worktree/branch if it cannot be completed, rather than claiming the workflow’s return boundary is satisfied.
