# Preserve and recover workflow context

Use this subworkflow at composite-workflow entry or reconstruction, scheduled handoff checkpoints, nested/steering return and explicit handoff preparation. Focused calls affecting an active workflow use the same continuity contract. Read-only discovery/review does not authorize adoption, checkout or execution.

## Checkpoint and owners

Maintain tracked target-project `docs/dev/HANDOFF.md` from the bundled [template](../../../assets/HANDOFF_TEMPLATE.md). It describes a named checkpoint; later task commits need not change it. The coordinator owns continuity, the active owner supplies its facts and persistence, and **sdd-orient** observes/reconstructs without writes. AGENTS links the record and this coordinator route. The main/default branch retains its integrated checkpoint; workflow branches inherit and update their own copies until integration.

Keep a brief outcome summary and four groups:

1. Workflow/variant, stage/owner and links to governing documents, task list and evidence.
2. Authorized objective/range, exclusions, exact stop, pending approvals and scoped preapprovals/overrides with decision sources.
3. Working branch, recorded creation parent, full branch-off commit, integration target, suspended parent stage and return boundary.
4. Pending work/effects, blockers and next eligible action **as of the checkpoint**. Include necessary package/version/setup/input availability and transfer limits when relevant.

TASKS, current campaign/phase reports and accepted documents own their details. Feature preparation retains its current decisions, exact acceptance/QC references and pending stage in [FEATURE_PREPARATION](feature-preparation.md), with checkoffs in FEATURE_DOCS_TASKS, package readiness in FEATURE-QC-REPORT and product scope in FEATURE; HANDOFF links these owners rather than duplicating their records. In main preparation, DOCS_TASKS owns task definitions/checkoffs and DOCS_PREPARATION owns control, scope sequence, decisions and evidence; HANDOFF links both rather than duplicating their detail. Preserve later grants, revocations, stops and tracking decisions in those existing records when received, before dependent work; ordinary commits retain their normal result/evidence. Link their locations from the handoff. Retain the selected reporting preference here when needed. Summarize older phase/campaign outcomes with links instead of repeating tasks, logs or a conversation. Require no additional journal, issue registry, incremental handoff files or saved patch series.

## Establish and refresh

At authorized workflow entry/adoption, reconcile existing context and create/update the checkpoint with the actual scope, sources and parent. Preserve controlling/manual content and unrelated work. Apply [main preparation](main-preparation.md) before its first repository write; its initial handoff is generated workflow metadata, outside DOCS-001's four-file presence test. Do not merge unfinished preparation merely to expose the handoff on default.

| Boundary | Required persistence |
| --- | --- |
| Each main/feature milestone's assigned final boundary task: standalone review when required, otherwise final implementation task | Refresh HANDOFF with the verified outcome, evidence, remaining scope, pending effects and next stop in the same commit as that task's report/result and initial checked completion. |
| Phase review/report task | Refresh with overall exits and integration readiness in its completion commit. One task closing both a review milestone and the phase produces one combined update. |
| Revision finalization | Refresh its outcome and return boundary with existing campaign finalization evidence; intermediate action detail stays in campaign records. |
| Completed main/feature preparation or other composite operation | Refresh the preparation/operation checkpoint with its actual pending human/hosted boundary. Intermediate document approvals stay in their owning evidence. |
| Nested entry, steering return or eligible integration | Preserve parent suspension or restore parent context under the return procedure below. |
| Doc-design cursor reset or autodoc DOCS-008 stop | Refresh with concise mode/pass/next-boundary context and a DOCS_PREPARATION evidence link, retaining outstanding hosted effects under [pass control](doc-design-modes.md); include the snapshot in the reset or DOCS-008 completion commit. |

Refresh at these boundaries automatically, without waiting for a handoff request. Include it in the owning commit; do not add handoff tasks or routine maintenance commits. Failed/blocked review retains its findings and incomplete boundary; it cannot produce a successful-completion snapshot. A completed milestone inside an incomplete main phase pushes/pauses without merging.

No per-commit handoff edit or handoff audit is required between checkpoints. Refresh earlier only when existing records cannot adequately preserve a consequential change or a transfer is explicitly requested. Keep every owned commit's [publication](git-workflows.md#publish-each-commit) and task/document atomicity unchanged.

Identify the checkpoint by workflow/milestone and the commit containing its explicit snapshot. Inspect path history, for example `git log -1 --format=%H -- docs/dev/HANDOFF.md`, and verify the selected content/ancestry; a timestamp alone is insufficient. A snapshot must not contain its own future SHA. Completion reports may name known baseline/end commits for on-demand diffs. A checkpoint cannot prove its own later push, issue closure or merge: record required subsequent effects as requiring confirmation and reconcile them by readback.

## Select the continuation branch

At initial/reconstructed startup, inspect local and remote workflow refs and relevant active navigation. Include revision/feature and unfinished preparation/phase branches. Establish remote freshness through permitted coordinator Git operations; orientation inspects available refs without fetching or switching. An unavailable remote means unknown state, not no unfinished work. Inspect only the identities/current sections needed; closed campaigns are not a reading queue.

Reserved `design-docs/ai-logs` is a [manual provenance branch](ai-logs.md), not a continuation candidate merely because manual records are unmerged. Do not read transcripts or ask to resume it during unrelated startup. A known interrupted adopted initialization still requires reconciliation of its actual seed/merge/publication; explicit provenance requests may select that scope.

For each candidate, recover its recorded creation parent, branch-off checkpoint and actual unfinished boundary. Test source-tip containment against that parent and its established remote destination, not main alone. A retained child already merged into its unfinished parent is integrated; a target merge awaiting push is pending publication, not a reason to repeat the merge. Unmerged history alone does not prove execution remains authorized.

If the continuation branch is not already explicitly selected or established in sufficient current context, present candidate branches with their parent and pending stage and **ask which branch to continue**, even for one candidate. Do not select by recency or prefix. Preserve an explicit selected branch and avoid repeating the question on ordinary continuation. With no unfinished candidate, use the main/default checkpoint and actual request without resurrecting completed work. Missing/ambiguous parent or authority requires the consequential decision before affected mutation.

After selection, follow [branch management](branch-management.md) for safe checkout/worktree handling. Do not stash, reset, discard incomplete milestones or switch over unrelated work implicitly.

## Reconstruct after the checkpoint

1. Read applicable AGENTS instructions, selected HANDOFF and relevant current owners. Establish actual branch/HEAD, worktree/index ownership and package availability. If the record is absent, reconstruct derivable facts from existing documents/Git and establish it only within authorized write scope; do not invent past grants.
2. Locate and verify its checkpoint. Inspect relevant commits/diffs since it, current TASKS or campaign evidence, and main DOCS_TASKS plus DOCS_PREPARATION and later decisions as applicable. Include non-task and merge changes; an older handoff followed by valid task commits is expected, not a failure.
3. Recover the current objective/range, stop, approvals/revocations, tracking choice, accepted inputs, unfinished operation and parent return. Current controlling instructions and actual later human decisions supersede the older snapshot. Branch names, ready tasks and checkboxes do not supply missing authorization.
4. Inspect uncertain Git/hosted effects by exact identity before retrying. Preserve an eligible retained commit, in-progress merge, issue operation and their evidence; use the owning recovery procedure. Do not replay completed work or infer external success from saved text.
5. Hand reconstructed facts to the selected owner and resume the earliest eligible operation within actual authority. Report a concrete missing decision/facility if evidence is contradictory, unresolvable or outside scope. A current clean snapshot is not a prerequisite for safe recovery.

## Integrate and return

For workflow completion, new branches record their creation parent and branch-off commit at setup and integrate their completed eligible scope into that same parent under [Git workflows](git-workflows.md). Preserve explicit target overrides and established legacy associations; corroborate history rather than guessing an original branch name. Partial ranges and explicit no-merge boundaries remain unmerged.

For [incoming synchronization](git-workflows.md#merge-purpose), retain the receiving workflow's identity, original creation parent, scope, pending human decisions and stop; record the incorporated baseline and resulting readiness. Do not replace its HANDOFF with the incoming baseline's context or treat catch-up as child completion/parent return.

Before nesting, retain the immediate parent's unfinished stage, scope, pending decision and return boundary in active campaign evidence and the child checkpoint. At the child's finalization, record its actual result and pending integration. During the prospective merge, deliberately reconcile HANDOFF to the parent's resulting context, retaining a concise child outcome/evidence link. Do not choose the entire child or parent file mechanically or edit a closed child report afterward.

Verify/publish the eligible merge, then return through the actual parent worktree/branch. Restoring context does not resume parent tasks, accept its pending document or expand its range. Completed root work leaves a completed/paused checkpoint and the actual next human boundary. Interrupted merge/publication resumes the retained operation rather than creating another campaign.

## Explicit transfer preparation

Requests such as “prepare a handoff” run this same reconstruction and may refresh a mid-milestone snapshot without declaring the milestone complete. Verify that the selected branch/checkpoint and necessary non-secret files are available through the receiving mode, and publish eligible owned results within existing authority. No explicit transfer command is needed for ordinary repository-based continuation.

A fresh clone cannot reconstruct unpublished/index/ignored bytes; identify missing inputs and use an authorized transfer or report the limit. Required package availability, credentials and host permissions must be supplied separately when the repository cannot provide them. Never place secrets or transient credential/helper paths in the handoff. Do not manufacture task completion, overwrite foreign state or bypass required gates to make a transfer appear complete.
