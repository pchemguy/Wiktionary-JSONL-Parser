# Workflow examples

These examples illustrate routing and boundaries; repository instructions and the actual request determine the concrete work. Document-review examples assume interactive/onepass unless a selected mode or scoped preapproval changes the checkpoint. Apply the [mode owner](doc-design-modes.md) and [main-preparation pre-write gate](main-preparation.md#establish-preparation-before-repository-writes) before relying on a shortened example.

## Workflow selection and continuity

Apply [the selection procedure](workflows.md#workflow-selection-and-continuity). Each initial or materially changed decision is reported in chat with its request/project basis, stage/owner, authorized outputs and next checkpoint/stop.

| Request and observed context | Decision, route and boundary |
| --- | --- |
| “Help develop project XYZ”; project/workflow state unknown | Orient to establish new/existing/interrupted state; choose purpose from the request and evidence, then report the selected entry. A preliminary seed does not establish greenfield or accept downstream documents. |
| Existing project needs whole-system design/specification | Main development at the next established stage; reuse accepted inputs and hold each necessary new document for its human checkpoint. |
| Add a bounded capability to an existing system | Feature preparation/continuation with only necessary deltas; report the established scope and next document or implementation boundary. |
| Review/revise existing work | Revision or a scoped direct assessment/correction; report whether repairs are authorized. Review-only stops at findings. |
| Amend implemented behavior at a paused task checkpoint | Revision's steering variant through sdd-steer; report paused target and assessment/execution scope; return without resuming tasks. |
| Correct the PROJECT/SPEC currently under human review | Continue its current document owner/stage, preserve the pending decision and present the revised state; no unrelated campaign or feature package. |
| Request a feature while another campaign is active | Assess switching against actual parent/pending work and target context; load applicable branch/revision-mode rules. Preserve/suspend established context; resolve only consequential ambiguity before dependent work. |
| Resume the same established task range | Recover actual pending work and reuse sufficient workflow evidence; preserve its stop without a ceremonial selection replay or per-response preamble. |
| Prepare release notes or perform a narrow direct check | Select the standalone operation/owner and its boundary; no compulsory core campaign, release publication or source repairs. |

## Workflow loading and reporting

| Request and context | Result and boundary |
| --- | --- |
| “Read and explain the greenfield workflow; development starts later.” No target repository is supplied. | Load selected main-development instructions; report actual sources, stages/checkpoints, scope and next step in chat. Stop without project writes, bootstrap, branches or hosted objects. |
| PROJECT awaits acceptance; the human answers a mechanics question. | Use the answer as a scoped requirement, revise the brief when requested and return to its pending checkpoint. Do not treat the answer as acceptance or begin ARCHITECTURE. |
| “Keep updates minimal.” The active range and authority are unchanged. | Check scope before work; report new progress without repeating the whole brief. A blocker, verification result or required human decision remains visible. |
| The human then asks “Explain this choice and list the sources you read.” | Provide the requested rationale and actual sources despite the earlier brevity preference; do not claim unread instructions were loaded. |
| “Switch to explicit reporting.” Later: “Return to standard reporting.” | Apply the selected profile to subsequent reports and handoffs. Explicit supplies relevant detail at reporting triggers, not an unchanged full preamble on every reply. |
| “Explain this decision fully, then resume minimal reporting.” | Give the requested explanation for this response; retain Minimal afterward. An explanation/source request alone does not change the ongoing profile. |
| Handoff retains the selected profile / reporting preference is lost with context. | Carry the known preference; otherwise use Standard without claiming to recover a lost choice. Preserve operational scope and human decisions separately. |
| Composite-workflow entry with no selected profile | Announce “Explicit during workflow setup; then Standard,” briefly explain Minimal/Standard/Explicit and how to switch, and report scope/checkpoint before dependent work. |
| Recover composite context with known Minimal preference / unrecoverable preference | Use Explicit for reconstruction and announce return to Minimal when known; otherwise declare Standard fallback. Do not guess lost approval/range. |
| Established workflow; next task or minor evidence refresh | Continue with the selected level; no repeated bootstrap/profile introduction. |
| A proposed edit is in an allowed file but adds behavior outside the task. | Withhold the unrelated change. Path ownership does not expand authorized behavior. |
| A new feature is requested while implementation is paused. | Preserve the paused context; load the selected procedure/dependencies before definitive reporting and dependent work, establish its scope/return and do not resume the parent by implication. |

## Operation examples

| Request and context | Coordinated result |
| --- | --- |
| “Prepare the project through TASKS.” An eligible Git worktree exists. | Apply main preparation's tracking/initialization gates, then prepare and publish the necessary documents and per-document QC on design-docs under the selected approvals. Honor the explicit TASKS stop; do not infer DOCS-009, integration or implementation. |
| “Review this SPEC.” The files are outside Git. | Perform read-only behavioral review and return findings. Do not initialize Git or rewrite files. |
| “Implement milestone 2.2.” TASKS contains its accepted requirements. | Orient; pass the boundary to **sdd-implement**; it preflights and pushes eligible outstanding commits first, executes/persists tasks on the owning phase branch, and pauses if the phase remains incomplete. A fully verified phase explicitly merges and publishes before stopping. |
| “Resume milestone 2.2.” The last checked task is ahead of its last task commit. | Pass pending changes and evidence to **sdd-implement**. It verifies and commits the completed result without repeating implementation, then continues only within the selected boundary. |
| “Continue.” The tree is clean but task commits are unpushed. | Orient; **sdd-implement** pushes those commits before selecting tasks, testing, or editing. A push blocker prevents further implementation. |
| “Assess removing encrypted streams.” Implementation is paused at a checkpoint. | Route impact assessment to **sdd-steer**; return the proposed scope without mutation. |
| “Implement that removal.” The amendment objective is established. | **sdd-steer** amends existing documents, code, tests, and guides; verifies, commits, pushes, explicitly merges into the paused implementation branch, verifies/pushes the target, and reports. Create no feature documents and do not resume the main task list. |
| “Integrate FEATURE-SPEC into SPEC only.” FEATURE-TASKS is still active. | Incorporate accepted behavior into SPEC; retain sources still required by active work; leave the task lists unchanged and report affected links outside scope. |
| “Incorporate feature tasks into TASKS only.” FEATURE-TASKS owns their active entries. | Explain that ownership transfer requires both lists in scope; defer the transfer rather than duplicating IDs or editing an unselected source. Independent reconciliation of existing TASKS entries may proceed. |
| “Verify this phase.” Some required checks are blocked. | **sdd-verify** returns observed evidence and blocked acceptance conditions. Do not repair code, mark tasks complete, or close issues. |
| “Align README.” **sdd-docs** finds a conflict with SPEC. | Report the conflict and proposed governing-document amendment to the user; continue independent authorized README work. Do not invoke **sdd-specify** automatically. |
| “Create task issues on GitHub.” No suitable token is available. | Try the available authenticated API client for the requested scope. If credential recovery is needed, find a suitable ignored token or ensure `*.tkn` exclusion and request/save `gh.tkn` with the GitHub backend profile. Local work needs no token. |
| Resume active hosted tracking after an outage left several completed tasks open. | Reconcile verified completed tasks in the maintained tracking scope, including older pending issues; do not inspect only the latest task or add a recovery journal. |
| Active hosted tracking returns 403 during issue closure. | Receive sanitized operation context; check suitable ignored repository tokens and escalate when necessary; recheck access before retrying. Report pending hosted closure separately from verified local completion. |

## Task audit recovery examples

| Observed context | Recovery and boundary |
| --- | --- |
| Published T-022 missed a required production failure; full-P1 repair/publication authority remains established | Classify acceptance separately from composition, inspect the failure, verify the correction and reconcile affected claims. Publish a task-specific forward correction under existing authority, then continue only eligible remaining P1 work; no blanket reapproval or false historical compliance. |
| Current code passes, but T-022's result and initial checkbox were split across commits | Preserve history. Tests do not repair composition; obtain a specific human exception for the blocked integration rather than treating the code fix as that exception. |
| Retained unpushed completion is known-invalid | Hold its publication, resolve bounded authorized recovery and inspect corrective persistence before publishing the coherent tip/retained history. No next-task batching, reset or automatic replay. |
| Required range/repair authority is missing, or the human paused work | Preserve work and ask only for the actual missing decision. Recovery does not authorize expanding or resuming the range. |

## Branch and artifact examples

| Request/context | Result |
| --- | --- |
| Main phase 2 contains an accepted milestone request, but other phase work remains. | Use phase/2-<slug>, verify/commit/push selected work, and pause without main merge or phase 3 creation. |
| Phase 2 and all exits are complete; phase 3 execution is authorized. | Explicitly integrate/publish phase 2, then branch phase 3 from updated main; absent authorization, stop. |
| Commanded steering at paused phase 2. | Allocate matching review identity/revision branch, retain a minimal revision report, amend and integrate into phase 2, and return control. |
| Feature SPEC alone is incorporated while FEATURE-TASKS remains active. | Retain necessary active sources and task owner; do not archive the whole package. |
| A complete feature is incorporated with tasks transferred. | Retain eligible sources in its features directory, repair links, mark historical snapshots, then verify/integrate the feature boundary. |
| A legacy working branch already owns the interrupted scope. | Preserve the suitable identity/name and target; do not rename from the new convention alone. |

## Credential recovery examples

| Context | Result |
| --- | --- |
| Supervised authorized push succeeds with existing noninteractive authentication and no supplied token. | Verify process cleanup and exact remote state; no token discovery or credential prompt is needed. |
| Push returns access 403 and gh.tkn is suitable. | sdd-manage verifies ignored/untracked status, refreshes supported shell authentication, retries the established destination, and confirms publication. |
| Shell lacks credentials and no token file exists. | Use [credential recovery](credentials.md). Before enabled main-preparation projection, authenticate through an existing or externally protected mechanism and defer repository token/ignore writes. After that gate, ensure exclusion, save the supplied repository token and use supervised publication. |
| A token creates an issue but cannot close it. | Treat actual endpoint denial as failed access; check Issues write suitability and request a suitable replacement when needed. Creation alone does not prove closure permission. |
| Several token files have ambiguous provider/repository ownership. | Resolve suitability before selection; preserve unrelated files and do not print values. |
| A token file is already tracked or an ignore negation exposes it. | Block tracked-secret remediation for an explicit decision; fix effective ignore coverage for an untracked file before reuse/save. Preserve unrelated work. |
| Git push succeeds but a connector's API operation is denied. | Recover the API client through its supported credential mechanism or report that mechanism unavailable; shell authentication is not connector authorization. |

## Blocked steering continuation

When a commanded amendment is blocked by an unavailable check, report its branch, paused target, pending changes, and concrete missing facility. A later “Continue that amendment” resumes the same scoped steering workflow after the facility is supplied; it verifies, explicitly merges and publishes, then stops without selecting the next task.

## Branch and operational boundaries

| Context | Result |
| --- | --- |
| Feature preparation through implementation is requested. | Prepare/commit/push project documents on design-docs; explicitly merge, verify and publish them into the actual default branch; then create the feature implementation branch from its recorded parent containing that checkpoint (propagating accepted preparation to an active phase first when required). Incorporate selected accepted deltas before final implementation verification and integration. |
| Initial preparation is accepted and implementation is requested. | Explicitly merge the design-docs tip into the actual default branch, verify/publish the merge and confirm containment; only then create the first phase branch from that baseline. |
| Preparation merge is committed but default publication fails. | Preserve the merge and stop before creating the implementation branch; finish publication on continuation without repeating the merge. |
| Accepted preparation is already merged and published. | Verify the exact preparation tip is contained; reuse that default baseline without another merge. |
| New accepted default preparation must reach an unfinished phase or existing revision. | Use incoming synchronization into that receiver, preserving its original parent, HANDOFF, pending scope and stop. Verify/publish before dependent branching/work; do not complete or merge the unfinished receiver into default. |
| A revision campaign needs only its plan/report and bounded source edits. | Author campaign records on the revision branch; do not create design-docs or preliminarily merge the campaign plan into default. |
| A revision campaign also needs new project SPEC/PLAN/TASKS preparation. | Keep campaign records on revision; prepare project documents on design-docs, integrate/verify/publish them into default, then incorporate that baseline into the retained revision branch before source implementation. |
| Only one feature task is requested, but the branch includes unrelated unfinished work. | Resolve the scope/branch conflict; do not merge the entire feature by implication. |
| Document incorporation stopped after SPEC changed but before TASKS reconciliation. | Inspect checkpoint and accepted sources; finish only selected owners, preserve history and reassessment notes, then verify/persist the document boundary. |
| A merge is committed but target push was rejected. | Preserve the merge and reconcile destination/divergence/access; finish publication without creating a second merge. |
| Hosted requests encounter rate-limit 403 or 429. | Defer according to backend timing and report pending effects; do not replace a suitable token to evade limits. |
| A hosted write times out. | Backend re-reads exact identities and effects before retrying; incomplete lookup leaves outcome unknown. |

## Review and revision campaigns

| Request | Result |
| --- | --- |
| “Review the credential protocol.” | Start from the prompt; record scope/criteria, located findings, and limits in the campaign review report. Stop before repairs. |
| “Plan and run a comprehensive plugin review.” | Create a review plan; assess and commit each unit's report; the coordinator publishes the committed checkpoint before dependent work; consolidate findings and revision handoff. |
| “Implement the accepted revision plan.” | Incorporate relevant accepted decisions into governing documents, perform bounded revisions with evidence checkpoints, then verify, explicitly merge, and publish. Retain the campaign plans/reports. |

## Prerelease review and reminder examples

| Request / context | Coordinated result |
| --- | --- |
| “Run comprehensive prerelease review.” Only a small release diff exists. | Load the [prerelease profile](prerelease-review.md), pin the candidate and inventory the complete current supported product; prioritize changed/risky paths and publish the review report. Stop before repairs or release unless independently authorized. |
| “Create this release.” No review was selected. | Give the shared advisory reminder once, then continue the authorized release under its ordinary required checks. Do not ask for confirmation, infer a waiver or start review. |
| Direct sdd-forge call to a publishing workflow after the manager already gave the reminder. | Reuse the handoff disposition; no duplicate reminder or new review gate. Build-only preparation remains outside publication. |
| Human previously declined review, or an applicable candidate-specific review is available. | Reuse the actual decision/evidence and its scope. Candidate changes identify affected evidence/rechecks without automatically activating review. |
| “Review before publishing.” Publication was otherwise authorized. | Honor the explicitly requested review-first sequence and report boundary; review selection alone does not expand repair or external-check authority. |

## Proactive tracking choices

| Context | Coordinated result |
| --- | --- |
| Explicit “Enable and maintain GitHub tracking” accompanies the broad project request | Carry requested/confirmed tracking without another question; after accepted preparation verify the eligible phase label, all milestones/tasks and associations before task edits/tests. No objects yet means projection pending, not tracking declined. |
| Token supplied for the established GitHub workflow; no tracking choice or applicable project policy | Recommend enable and ask to manage the eligible phase label, milestones/task issues, associations and verified lifecycle closures. Keep confirmation pending; create no objects yet. |
| Prior explicit decline, followed by a token for normal Git pushes | Preserve the decline and perform authorized pushes; do not interpret the credential as activation. |
| Requested tracking has no verified objects, or initial projection is partial/unknown | Stop affected task edits/tests; finish projection/readback or report the blocker. Do not apply the later-outage allowance or silently choose local-only execution. |
| Provider outage after full phase activation | Retain verified results and pending closures; continue only independent already-projected tasks with satisfied dependencies. Added unprojected work and dependent phase/review transitions remain blocked. |
| Original explicit request was omitted during execution | Preserve the request/work/evidence, publish retained verified commits and reconcile the missed gate before further affected implementation. No repeated enable question or fabricated earlier compliance. |
| Tracking confirmed after several local tasks completed | Discover/reconcile eligible objects and attach verified retained evidence; leave incomplete work open and keep historical inactive-state reports truthful. |
| Implementation tracking confirmation is pending; independent preparation is authorized | Resolve main preparation's effective tracking policy/pre-write gate first. Continue only work eligible under that decision; the implementation confirmation example does not waive an enabled preparation gate. |

## Release preparation and publication

| Request or state | Coordinated result |
| --- | --- |
| Prepare a release message; draft/update release notes | Run complete-message preparation through forge highlights and report assembly; retain body-only root `RELEASE-NOTES.md` and stop before publication. |
| Repeat preparation with an existing complete message | Refresh source and ancillary facts, preserve applicable human edits/cuts, then atomically replace one file; preserve the old copy on failure and avoid unchanged-body writes. |
| Publish after message preparation | Verify local source/coverage context and stated version; refresh stale notes, publish the release commit with the complete message body, tag that commit and transfer the same body to GitHub. Verify provider readback; retain the message, cleaning only an eligible owned internal checkpoint. |
| Edit only supplied release text | Perform scoped editorial work without expanding into Git collection or publication. |
| Collect highlights locally since the last stable release | Run shared forge Git preparation without selecting a host or requesting a token; create/update the ignored YAML draft and stop before release/tag writes. |
| Existing highlights draft has manual cuts; target advances | Validate its tag/ancestry/release line, analyze only pending commits and preserve curation; a revert can remove an old claim. Save coverage only after successful complete analysis. |
| Supplied ZIP; prepare a building workflow only | Inspect real contents/source and resolve package layout; prepare/verify/persist the workflow through existing Git ownership. Stop before product release creation. |
| Several platforms need different package contents | Resolve material variants interactively, retain decisions, use stable conventional suffixes and collect the full expected asset set before one publisher. |
| Create release from an accepted verified tag and package set | Select direct publication or the established workflow; create/reuse a matching draft, upload/verify all assets, publish within the requested state/latest policy and read back. No TASKS or tracking activation prerequisite. |
| Ignored highlights draft; tag-only CI has no notes-transfer input | Prepare/extend the single publisher’s declared transfer mechanism before triggering; pushing a tag does not carry the ignored file. |
| Release remains draft-only or published body cannot be confirmed | Retain the local highlights draft; successful assets or accepted dispatch alone do not justify cleanup. |
| Contents/Workflows access exists; Actions dispatch is denied | Diagnose operation-specific Actions access; do not assume workflow-file permission authenticates dispatch or replace a token for a policy denial. |
| Upload times out after a draft asset may exist | Read draft/tag/assets before replay; resume only missing matched work and preserve pending/unknown effects. Do not clobber published assets. |
| Latest release lacks an advertised variant | Keep the asset/latest result unverified; latest URLs do not fall back to older variant assets. |

## Authority, diagnostics and retained notes

| Context | Coordinated result |
| --- | --- |
| Verified report push has existing user authority; host requests destination/payload context and permits reconsideration | Supply exact repository/ref, commit/paths, actual user grant, checks and stated denial through that channel, then attempt the contextualized request; no repeated user authorization question. |
| Suitable credential but genuine policy rejection, or authority revoked | Preserve state and report the observed restriction/revocation. Do not substitute credentials, fabricate authority or evade controls. |
| Tracking omission discovered; earlier PLAN merely says inactive | Diagnose missing capability-choice coordination, not a proven user refusal or compulsory activation. Offer the actual pending decision. |
| User requests amendment notes be collected in the current findings file | Persist stable findings within that scope; report its actual commit/push state. Do not start source repairs unless selected. |
| Notes exist only in conversation and no write scope exists | Report conversation-only storage; no claim of a durable register or implementation. |

## Human document review examples

- “Prepare the whole greenfield project through TASKS”: create/QC/persist PROJECT, present substantive analysis and pause. Acceptance permits the authorized ARCHITECTURE step; repeat at each necessary root in dependency order.
- “Continue preparation; PROJECT through SPEC already exist”: orient and assess actual progress, reuse acceptable inputs, then create PLAN and pause at its new-document review. Do not replay existing documents unless requested or actually pending.
- “Review the existing architecture with me, then continue”: begin with concise structural analysis and resolve that selected interactive review before dependent work.
- Startup finds contradictory feature contracts: explain the concern and offer interactive review; an unselected offer is not interactive mode, and declining cannot clear the contract blocker.
- A small feature reuses sufficient architecture/strategy/layout: create only the necessary FEATURE-SPEC and FEATURE-TASKS deltas, reviewing each new proposal before dependent work. A larger delta reviews each needed design/PLAN/placement proposal separately.
- Human requests revisions or the conversation is interrupted at PLAN review: preserve the pending decision, revise/recheck the same owner and present its actual state. No assumed acceptance and no regenerated chain.
- Standing Git/token authority: persist the checkpoint without another repository-operation permission question; still pause for document acceptance.

## Revision campaign modes

- “Open a focused revision while this feature campaign is active”: use a new nested revision identity from the feature’s published branch, suspend its execution, and default the child merge to that same branch. A review-only request publishes findings and stops; accepted repairs verify/publish the child and parent merge, then return the worktree to the feature branch without automatically resuming feature tasks.
- “Reopen the last campaign to extend this closely related change”: first verify that the active branch’s latest first-parent merge is the selected revision’s published final merge and that target/source/closure match. Reuse its original identity and append the accepted delta/new actions and rechecks; explicitly merge again and return the worktree to the interrupted target branch. Preserve earlier closure and check evidence.
- A later ordinary commit does not itself disqualify amendment: preserve it in the current target checkpoint and inspect dependencies/scope. A later unrelated merge, different return target or unknown closure blocks this mode; do not skip back to an older convenient merge.
- If readily available context suggests a qualifying amendment, propose the campaign and relation to the human. Do not reopen or edit frozen records until actual authority is established. Unrelated work uses a new campaign, and incomplete integration/publication resumes the existing active operation.

Use [revision modes](revision-modes.md) for the controlling eligibility, authority, preservation and worktree-return rules. Neither mode silently resumes an interrupted parent or bypasses required project-preparation/phase gates.

## Main documentation preparation

| Request / observed state | Required boundary |
| --- | --- |
| Fresh main preparation with requested GitHub tracking | Verify native sdd-docs-main and all nine template issues before target writes; then create/reuse docs branch, copy the task template and perform DOCS-001. No product PLAN/TASKS prerequisite or implementation phase objects. |
| Two of the four root setup files existed | Preserve them, copy the missing files, publish initialization with DOCS-001 complete, close/read back its issue, warn with both file groups and stop unless that continuation was explicitly preapproved. |
| SPEC is approved after its proposal was published | Commit the approved SPEC state, approval evidence and checked DOCS-005 together; push/read back, then close its issue before PLAN. No rewrite of unchanged SPEC bytes. |
| Ordinary later SPEC correction or resumed incomplete preparation without a cursor reset | Retain first-approval task/issue completion; reassess current readiness and continue the earliest unmet operation without duplicate objects or guessed approvals. |
| DOCS-001–008 are complete and the selected range permits package QC | Pass DOCS-009 QC, publish its report/checked task, close final issue, explicitly merge/verify/publish docs, close/read back sdd-docs-main, then confirm final checkpoint. Implementation still needs its authorized range. |
| Autodoc/onepass completes TASKS, or a human explicitly selected a TASKS stop | Finish required completion/publication/tracking effects and stop before DOCS-009; package completion and integration remain pending. |
| Autodoc with human-controlled multipass reaches DOCS-008 | Report the current pass and wait for reset or advance direction. |
| Autodoc/autoloop has another predefined scope after DOCS-008 | Follow the mode owner's retained-document reset and same-issue reopening, then continue that pass. Stop before DOCS-009 after the last predefined pass. |
| Explicit preapproval covers remaining document and final checkpoints | Retain its actual scope; report/check/persist each result without repeated acceptance pauses. Technical, tracking and publication gates remain required; do not guess an implementation range. |
