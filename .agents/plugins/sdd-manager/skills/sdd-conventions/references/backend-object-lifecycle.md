# Backend object lifecycle and review boundaries

Apply these shared invariants to PLAN/TASKS generation, bounded implementation, hosted reconciliation and interruption recovery. Local governing documents and verified Git/check evidence are authoritative; backend objects are projections. Hosting is optional to select; requested/confirmed tracking must satisfy its activation and lifecycle gates before dependent execution. sdd-manage coordinates transitions; sdd-implement executes tasks and persists results; sdd-forge owns provider writes.

## Main documentation preparation

Fresh/resumed main preparation uses [main preparation](../../sdd-manage/references/main-preparation.md) and [its hosted lifecycle](../../sdd-forge/references/github-docs-preparation.md): verify native `sdd-docs-main` and nine DOCS issues before target-repository writes; local DOCS_TASKS owns the nine task definitions/checkoffs and DOCS_PREPARATION owns mode/pass, initialization/decision evidence and pending transitions. Publish the accepted-document/preparation-evidence/checked-task commit before issue closure. Ordinary later edits keep these tasks/issues complete; an authorized [cursor reset](../../sdd-manage/references/doc-design-modes.md#reset-the-cursor) reopens DOCS-002–009 and the same issues after the reset commit is published. DOCS-001 and documents are retained. Autodoc stops after DOCS-008 or performs the next predefined reset, before package QC. When final QC is explicitly reached and its issue closed, merge/verify/publish documentation, then close the milestone and confirm the preimplementation checkpoint. This is not Phase 0 and needs no product PLAN/TASKS, phase label or implementation review milestone. The phase rules below apply to implementation; preparation creates no future implementation objects.

## Phase activation

Keep the complete intended hierarchy in local PLAN/TASKS. Create a phase's label, all its milestones and all its task issues only after its predecessor is complete and before its first task executes. First-phase activation has no predecessor. Completion includes the predecessor's reviews, required reports, all milestone closures when tracking is active, local exits and required target integration/publication. Starting the next phase also requires authorization within the selected range.

Preparation does not activate a phase. Projection reads the complete hierarchy to resolve identity/dependencies but writes only the eligible phase. Added work in an already active phase is projected before execution. Future-phase work remains unprojected, including feature deltas. When tracking is requested or confirmed for the scope, incomplete or unverified phase projection blocks affected task implementation edits/tests unless the human explicitly authorizes local-only continuation. Preserve existing future-phase objects as historical/pre-existing state; report them rather than deleting them to enforce timing retrospectively.

## Explicit review units

Each phase has one or more implementation/delivery milestones followed by a **special phase review milestone containing exactly one phase code review/testing/report task**. That special milestone is unaffected by the rule below and is excluded from the implementation-milestone count.

When generating tasks, **do not add a standalone milestone review task if the milestone has fewer than four implementation tasks OR the phase has a single implementation milestone**. Add one only when both counts meet the threshold: at least four implementation tasks in that milestone and at least two implementation milestones in its phase. Count capability-bearing delivery work under [QC counting rules](development-document-qc.md#decomposition-and-count-policy); exclude dedicated review/report-only units. Do not pad tasks or milestones to change the result.

Every delivery milestone still requires whole-capability code review, applicable tests/repairs, a committed milestone report and HANDOFF update. Where the standalone review task is omitted, assign these to the **final implementation task**, after its implementation is ready and before its completion commit. It depends on all other milestone tasks and closes with its result, report, HANDOFF and initial checkbox together. It retains its implementation identity and counts once; do not create a replacement administrative task or defer this evidence to phase review.

PLAN owns milestones/exits; TASKS assigns the appropriate final boundary task and stable IDs. Explicit review tasks count toward next-N ranges; folded obligations are part of their single implementation task. Phase review still waits for all delivery milestones to complete/close, not its own open milestone. Accepted existing hierarchies require a scoped amendment; never remove, insert or renumber tasks implicitly during execution or violate retained multipass ranges.

## Completion ordering

1. Verify task acceptance, tests and documentation; reconcile its owning checklist/evidence; commit result and status together, push and verify containment. Then close its task issue with evidence when tracking is active. A task issue records work on its working branch; target integration is separate.
2. Complete the delivery milestone's assigned final boundary: its standalone review task when required, otherwise its final implementation task with the folded obligations above. Review the whole capability and relevant dependencies, test applicable exits/regressions, fix blockers and commit/push its report/HANDOFF with that task's result and completion. Close its issue like any other task.
3. Close/read back the delivery milestone only after every constituent issue, including any standalone review issue, is closed and its review/report/exit evidence is established. No extra review issue is needed for a folded boundary. Unexpected open or foreign issues and ambiguous ownership block closure; never close foreign issues to clear the gate.
4. After all delivery milestones close, execute the phase review task: review cross-milestone interactions, phase exits and remaining findings, run required checks, repair blockers, commit/push the phase report and close its issue. Then close/read back the final review milestone.
5. Reconcile local parent claims, verify the full phase and perform required explicit integration, merged-state verification and publication before activating an authorized next phase. A partial range pushes and pauses without inventing additional review work beyond its selected tasks.

Local-only execution applies the same review/report/exit gates without hosted closure. If an enabled backend cannot complete closure, keep local verified results and report hosted reconciliation pending; dependent phase review/advancement remains blocked. Independent tasks in an already verified activated phase may continue within scope only when their own required projection and dependencies are satisfied. Initial/added-work projection and dependent review/closure/next-phase gates are not waived by an outage. A phase label has no close state on GitHub: retain its historical associations. Unsupported backend state transitions need an explicit backend procedure, not deletion or an invented equivalent.

## Review, repairs and deferral

sdd-verify owns read-only implementation code review and check evidence for milestone/phase boundaries, with focused specialists routed by sdd-manage as needed. sdd-implement owns repairs and completion; sdd-tdd designs/changes tests; sdd-docs maintains documentation; sdd-report presents evidence. Code review and testing are separate obligations. Passing tests without code review cannot complete an assigned review boundary, including one folded into an implementation task.

Fix bugs, critical code issues and every SPEC/PLAN violation before completing its review-bearing boundary task. Missing or failing required evidence blocks completion. Route governing-contract or out-of-scope changes to their owner; do not disguise them as deferrable findings. Only non-critical code issues consistent with SPEC/PLAN may be postponed.

Keep required repairs and findings whose deferral eligibility is unestablished in Findings/Blockers, outside the deferred TODO section. Each report has a TODO section (`None` when empty). A deferred finding has a stable ID, location/evidence, impact/severity, deferral rationale showing contracts/exits remain satisfied, proposed solution options/tradeoffs and follow-up owner/scope. Phase reports carry unresolved milestone findings and add phase findings. The final implementation report aggregates unresolved/deferred milestone and phase TODOs without losing options or provenance; preserve resolution references for earlier findings. The last phase review task includes the final report when the full task list completes. Partial requests cannot claim full-project completion.

## Report locations

| Workflow / artifact | Path or prefix |
| --- | --- |
| Main development phase report | `docs/dev/reports/phases/<phase-id>/PHASE-REPORT.md` |
| Main development milestone report | `docs/dev/reports/phases/<phase-id>/<milestone-id>.md` |
| Main development final report | `docs/dev/reports/IMPLEMENTATION-REPORT.md` |
| Phase-checkpoint steering revision records | `docs/dev/reports/phases/<phase-id>/revisions/<revision-id>/` |
| Feature reports and records | `docs/dev/features/<feature-id>/` |

Use filesystem-safe stable IDs; link reports from their assigned final boundary tasks. Steering retains applicable review/revision stage basenames including `REVISION-REPORT.md` within its phase-specific prefix, instead of the general reviews directory. General campaigns retain [review campaign](review-campaigns.md) storage. Feature milestone/phase reports remain under their feature prefix; qualify paths by phase ID when multiple phases would collide, and place the feature's final `IMPLEMENTATION-REPORT.md` at that prefix. Feature archive eligibility is separate from report placement. Preserve established historical paths unless an authorized migration includes them.

## Recovery and changed scope

On resume, inspect actual lists, reports, Git commits/pushes and hosted states. Finish the earliest unmet authorized transition, including older pending closures. Reuse exact managed identities after partial creation. For an uncertain issue/milestone write, read actual state and evidence before replay; incomplete or contradictory lookup leaves the outcome unknown. A report partly written needs missing review/check/repair work; a committed report needs its pending push, not repeated review. A closed milestone with uncommitted local parent status needs status reconciliation. A completed phase review with integration pending needs that existing integration finished before next-phase activation. Do not introduce a second progress registry or require a report to contain its own commit SHA.

Failed or invalidated task verification, as well as accepted steering/feature changes, can invalidate task and parent acceptance. Task completion recovery follows the implementation owner's [recovery procedure](../../sdd-implement/references/completion-and-checkpoints.md#resolve-a-task-recovery) and actual hosted authority. Preserve stable IDs, earlier reports and evidence; mark reassessment pending and reconcile authorized issue/milestone reopening when current acceptance fails. Retired work is not verified completion and must not be silently closed as completed. Feature transfer retains its original issue; a scoped feature parent cannot close a whole-project milestone while another owning list still contains unfinished work. Existing completed phases require a scoped accepted amendment and dependency reassessment, not silent replay or advancement.
