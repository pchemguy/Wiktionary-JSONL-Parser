---
name: sdd-manager
displayName: SDD Manager
---

# SDD Manager

SDD Manager provides specification-driven development workflows for Git projects through focused skills. This entry orients the agent and routes workflow and capability requests. Each skill's `SKILL.md` owns its procedure; `references/*.md` supply selectively loaded sub-workflows. The [README](README.md) explains capabilities and workflows to humans.

**`sdd-manage` is SDD Manager’s workflow coordinator. Generally load its [entry](skills/sdd-manage/SKILL.md) alongside `PLUGIN.md` before other skills at workflow entry.**

Read an available `PLUGIN.md` explicitly when the client has not loaded it and entry guidance is needed. If it is unavailable, use the coordinator and skill entries directly. This is a non-standard entry convention, not a guarantee of automatic discovery. Bundled skills use relative Markdown links and named handoffs; load only relevant entries and references.

## Establish the request and context

Identify the actual execution host and available tools at startup, following applicable user and repository instructions. Orientation observes read-only.

For a new development, functionality, review or revision request without sufficient workflow context, use `sdd-manage` to establish project state and select the path. Use [sdd-orient](skills/sdd-orient/SKILL.md) when current repository evidence is insufficient. Select by purpose; new, existing or interrupted state determines the eligible stage, not the workflow by itself.

| Core workflow | Purpose |
| --- | --- |
| Main development | Define and deliver the whole project, reusing sufficient accepted inputs. |
| Feature | Add a bounded capability to an existing system. |
| Revision | Correct, simplify or improve defined or implemented work. Steering is its focused variant at a paused implementation checkpoint. |

Follow the coordinator's [selection and continuity](skills/sdd-manage/references/workflows.md#workflow-selection-and-continuity). At entry or a material routing/boundary change, explain the selected workflow or standalone operation, its request/project evidence, current stage/owner, authorized outputs and next checkpoint in chat.

A request to read/explain a workflow before development uses the coordinator's [workflow-loading operation](skills/sdd-manage/references/workflows.md#workflow-loading): report actual sources, stages/checkpoints, scope and next step in chat, then stop without project changes.

Check scope before work and both the path and proposed change before writes. Honor requested reporting detail: omit unchanged context and routine explanation when brevity is requested, while preserving consequential decisions, blockers, verification and human checkpoints. Use Standard reporting by default; “minimal reporting” or “explicit reporting” selects the corresponding [profile](skills/sdd-manage/references/coordination.md#reporting-profiles). Follow [scope checks and reporting detail](skills/sdd-manage/references/coordination.md#scope-checks-and-reporting-detail); an unchanged turn needs no repeated full brief.

At composite-workflow entry, material switching or context reconstruction, the coordinator uses [Explicit bootstrap reporting](skills/sdd-manage/references/coordination.md#composite-workflow-bootstrap-reporting), briefly explains the profiles and announces Standard for subsequent work unless a human preference is established. Routine continuation does not repeat this introduction.

**Established workflow and skill context normally resolves follow-ups.** A request to implement through a milestone belongs to `sdd-implement` in that context; it does not require plugin re-entry or a repeated selection brief. If context cannot identify a clear workflow/owner, use `sdd-manage` to recover it. Recover discoverable state; ask only for consequential missing decisions. Do not guess lost approvals, ranges or integration authority, or require the user to name lower-level skills.

Preserve narrow direct/standalone requests, pending decisions and unfinished work. Read-only discussion/inspection may proceed without Git; repository mutations require an eligible worktree and do not implicitly initialize Git.

**Product development documents must describe the project, not their preparation workflow.** Apply the [development-document content boundary](skills/sdd-manage/references/human-document-review.md#development-document-content-boundary) to every main/feature root and focused child, in every mode. Keep documentation-pass sequencing, cursor and approval/reset state in DOCS_PREPARATION for main preparation, in FEATURE_PREPARATION for new feature preparation, or revision evidence. DOCS_TASKS holds tasks/checkoffs only. Check these boundaries during authoring and review.

## Human checkpoints and Git publication

**Push every workflow-owned commit and verify remote containment before further work or another commit.** This includes completed documents, tasks, review reports, revision actions and merges. A failed push blocks progression. A retained implementation task completion with known failure or uncertain eligibility first follows [publication preflight](skills/sdd-implement/references/startup-and-continuation.md#push-before-task-work); only bounded authorized recovery/corrective persistence may precede its safe publication. Follow [per-commit publication](skills/sdd-manage/references/git-workflows.md#publish-each-commit); preserve explicit human-directed local-only or deferred-publication exceptions.

**At each necessary document checkpoint, publish the reviewable proposal and its selected artifacts, present substantive results and pause for human acceptance before dependent work unless applicable preapproval covers it.** Model/API-design artifacts share the DECOMPOSITION checkpoint; contract artifacts share SPEC, without extra DOCS/FDOCS tasks or approval rounds. The same checkpoints apply to necessary feature documents/proposals. Reuse sufficient existing inputs rather than creating optional documents to fill the sequence.

For main or feature document preparation, select or recover the [doc-design mode](#doc-design-modes) before applying the document checkpoints below. The selected mode determines which approvals remain active and where its preparation pass stops.

| Human checkpoint | Hold before |
| --- | --- |
| PROJECT / FEATURE | Dependent project/feature design or specification, unless mapped mode/preapproval covers the checkpoint |
| ARCHITECTURE | DECOMPOSITION or contract work |
| DECOMPOSITION | SPEC |
| SPEC | PLAN |
| PLAN | New layout or TASKS |
| layout | TASKS |
| TASKS | Implementation or hosted task projection |
| Requested implementation range completed | Any task beyond the requested count, milestone, phase or named checkpoint |
| Steering amendment completed | Resuming implementation |
| Assessment-only review completed | Repairs or revision execution |

**The human defines the implementation range and decides what follows it.** Commit each task’s verified result, evidence and initial completion checkbox together, then push and verify remote containment. At the end of the requested range, report the boundary results and stop. Do not add ready tasks, review tasks or another phase beyond the selected range. The human may request continuation or steering; start neither automatically. Partial main phases push and pause without merging. A complete phase or feature integrates only when its established verification and scope gates are met.

**The human may preapprove future checkpoints at any point, individually or as a scoped set.** Retain that decision through interruptions; report covered results without repeated approval pauses. Preapproval preserves QC, publication/tracking gates and the authorized implementation range. See [future-checkpoint preapproval](skills/sdd-manage/references/human-document-review.md#future-checkpoint-preapproval).

Clarification, agent QC, passing tests and commits/pushes do not constitute human acceptance. Broad development authority does not preaccept unseen documents or expand a selected implementation range. Preserve pending decisions after interruption. See [document review](skills/sdd-manage/references/human-document-review.md) and [implementation checkpoints](skills/sdd-implement/references/completion-and-checkpoints.md#parent-completion-and-stopping).

## Requested backend tracking

**For fresh/resumed main preparation, enabled tracking precedes repository modifications:** use [main preparation](skills/sdd-manage/references/main-preparation.md) for the native `sdd-docs-main` milestone and all nine issues defined in bundled JSON before writes. DOCS_TASKS holds the nine task definitions/checkoffs; DOCS_PREPARATION owns mode/pass, decisions and evidence. Publish each accepted-document/preparation-evidence/checked-task commit before issue closure; ordinary later edits retain completion, while an explicit cursor reset reopens DOCS-002–009 for a new pass. Final QC issue closure → verified/published docs merge → milestone closure → final preimplementation checkpoint. This is separate from implementation phase activation.

Feature preparation tracking uses a separate campaign milestone and nine FDOCS issues before writes, under [its preparation contract](skills/sdd-manage/references/feature-preparation.md); it does not reuse main DOCS objects or product phase labels.

### Implementation tracking

**When tracking is requested, prepare and maintain hosted objects throughout task-list-based implementation.** Use `sdd-manage` to coordinate and `sdd-forge` for GitHub issues, labels and milestones, or supported provider equivalents.

- **Before execution:** create/reconcile the eligible phase's phase label, all milestones and all task issues, including review/report tasks. On GitHub, use milestone objects and verify each issue's phase label and milestone association. Use milestone labels only where the provider lacks native milestones and its backend defines equivalent completion/reconciliation semantics. Missing or unverified objects block affected implementation. Activate later phases only when eligible.
- **During execution:** project added tasks and update changed associations before their execution. After each task is verified, committed and pushed, close its issue with evidence. Close milestones only after all constituent issues, required reviews and exit conditions are complete.
- **After amendments or interruption:** reconcile actual hosted state, reuse existing identities, finish pending operations and reopen affected issues/milestones when acceptance is invalidated.
- **At each implementation checkpoint:** report tracking status and unresolved operations. Provider failures preserve local results but do not waive required projection or dependent closure gates.

Follow [phase activation](skills/sdd-manage/references/phase-activation.md) and the [tracking lifecycle](skills/sdd-conventions/references/backend-object-lifecycle.md).

## Skill routing

This capability directory identifies owners, including skills normally activated within a workflow. It does not replace their procedures or interpret every contextual follow-up.

| Capability | Owner and entry |
| --- | --- |
| Workflow selection, coordination, branches, credentials and transitions | [sdd-manage](skills/sdd-manage/SKILL.md) |
| Read-only repository/instruction state and interruption inspection | [sdd-orient](skills/sdd-orient/SKILL.md) |
| Modularity, design review, task hierarchy and shared conventions | [sdd-conventions](skills/sdd-conventions/SKILL.md) |
| Project brief, architecture, component APIs and model design | [sdd-design](skills/sdd-design/SKILL.md) |
| Behavior, interfaces, contracts and acceptance requirements | [sdd-specify](skills/sdd-specify/SKILL.md) |
| Delivery strategy, milestones, dependencies and physical layout | [sdd-plan](skills/sdd-plan/SKILL.md) |
| Executable tasks, dependencies and task-list review | [sdd-tasks](skills/sdd-tasks/SKILL.md) |
| Bounded task-range selection, implementation and resumption | [sdd-implement](skills/sdd-implement/SKILL.md) |
| Human-directed amendment at a paused implementation checkpoint | [sdd-steer](skills/sdd-steer/SKILL.md) |
| Accepted feature incorporation and task-ownership reconciliation | [sdd-integrate-feature](skills/sdd-integrate-feature/SKILL.md) |
| Test strategy, scenarios and test changes | [sdd-tdd](skills/sdd-tdd/SKILL.md) |
| Checks, failures, acceptance coverage and boundary code review | [sdd-verify](skills/sdd-verify/SKILL.md) |
| README, guides and module/API documentation | [sdd-docs](skills/sdd-docs/SKILL.md) |
| Issues, commit/merge messages and evidence-backed reports | [sdd-report](skills/sdd-report/SKILL.md) |
| Git highlights, release messages/packages and hosted tracking/releases | [sdd-forge](skills/sdd-forge/SKILL.md) |

Name the next owner and preserve accepted inputs, actual context and the stopping boundary; use its handoff procedure. A sibling reference supplies shared guidance without selecting that skill's entire workflow. Execution handoffs depend on client facilities.

## Composite workflows

The [canonical catalog](skills/sdd-manage/references/workflows.md) owns definitions and transitions. These summaries show principal stages, owners, outputs and stops; implementation and release operations can also be selected independently within scope.

### Doc-design modes

Main and feature document preparation support the following mapped selections. Load [mode and pass control](skills/sdd-manage/references/doc-design-modes.md) before applying a selection or handling a cursor reset; it owns approval/delegation, retained-document revision, reset and recovery rules.

| Selection | Approval and pass boundary |
| --- | --- |
| **interactive/onepass** (default) | Each necessary document checkpoint remains active unless explicitly preapproved; follow the selected preparation range. |
| **autodoc/onepass** | Approve PROJECT or FEATURE; later applicable document checkpoints through TASKS/FEATURE-TASKS are preapproved. Stop at DOCS-008/FDOCS-008 before package QC. |
| **autodoc with human-controlled multipass** | Approve the mapped brief each pass; later applicable document checkpoints are preapproved. After the document pass, wait for reset or advance direction. |
| **autodoc/autoloop** | Use predefined scope passes: first mapped brief approval remains active; announce that later brief approvals are waived. Run the agreed passes, then stop after final DOCS-008/FDOCS-008 before package QC. |

Predefined autodoc scope sequences default to autoloop unless human-controlled multipass is requested. New material autoloop decisions are delegated to agent judgment with visible rationale while proceeding. A cursor reset retains documents and reopens mapped DOCS-002–009 or FDOCS-002–009 and their existing issues; mode selection preserves required QC, publication and tracking gates.

Multipass delivery is **strict by default**: later passes preserve earlier phase/task ranges. **Explicitly permitted flexible multipass** may integrate small changes fitting an earlier pass's scope into its corresponding range. This choice is independent of approval/loop control; [mode details](skills/sdd-manage/references/doc-design-modes.md#multipass-delivery-modes) govern selection, retention and planning/task review.

### Project preparation and bounded delivery

`PROJECT.md` is the concise project brief: purpose, users, outcomes, scope/non-goals and consequential constraints, with material assumptions/questions identified. Use `sdd-design`'s [brief contract](skills/sdd-design/references/project-brief.md); PROJECT supplies context rather than architecture or exact SPEC behavior.

[Main preparation](skills/sdd-manage/references/main-preparation.md) starts with DOCS-001: preserve existing root guidance/disclosure/discovery files, copy missing ones and publish initialization. Mixed initial presence requires a named retained/copied warning and a continuation pause unless explicitly preapproved; none/all present adds no pause.

Main preparation routes `sdd-manage`/`sdd-orient` → `sdd-design` (PROJECT, ARCHITECTURE, DECOMPOSITION) → `sdd-specify` (SPEC) → `sdd-plan` (PLAN, layout) → `sdd-tasks` (TASKS), with `sdd-conventions` as needed. Existing work enters at the next eligible stage; requested interactive review comes first. Apply the [human checkpoints](#human-checkpoints-and-git-publication) and [document QC](skills/sdd-manage/references/document-qc-gates.md).

Completed main preparation includes DOCS-009 whole-package QC and published documentation integration, then `sdd-docs-main` milestone closure and the final implementation checkpoint. Autodoc stops earlier at DOCS-008; advancing to package QC is separate. Otherwise completed preparation-only stops at that final checkpoint; an authorized implementation handoff requires accepted preparation to be integrated, verified and published to the actual default branch before creating the dependent branch; see [preparation integration](skills/sdd-manage/references/branch-management.md#preparation-integration-gate).

### Task implementation and continuation

`sdd-implement` selects and executes the authorized range, composing `sdd-tdd`, `sdd-docs` and `sdd-verify`, with `sdd-report` for evidence/messages. `sdd-manage` establishes the [tracking decision](skills/sdd-manage/references/tracking-decision.md) and [phase activation](skills/sdd-manage/references/phase-activation.md); `sdd-forge` maintains confirmed hosted effects.

Follow [task completion and recovery](skills/sdd-implement/references/completion-and-checkpoints.md) and the prominent [publication/range stops](#human-checkpoints-and-git-publication). Finish pending work before advancing. Requested tracking and unresolved dependent effects retain their gates; partial main phases push and pause, while complete verified phases use eligible integration.

### Feature preparation, execution and incorporation

`sdd-manage`/`sdd-orient` establish the bounded addition and accepted main inputs. Feature preparation follows the shared interactive/autodoc/multipass policy mapped through [FEATURE, task-only FEATURE_DOCS_TASKS and FEATURE_PREPARATION](skills/sdd-manage/references/feature-preparation.md). First FEATURE approval precedes dependent stages unless preapproved; assess unchanged design/layout for reuse. Autodoc stops after FDOCS-008 before FEATURE-QC-REPORT/package QC. Completed preparation passes FDOCS-009, verified/published preparation integration and selected preparation milestone closure before its implementation checkpoint. Design/specification/planning/task owners produce only necessary deltas, with human checkpoints and QC. Accepted preparation integrates before the dependent implementation branch; FEATURE-TASKS drives its authorized range through `sdd-implement`.

Use [feature phase delivery](skills/sdd-manage/references/feature-delivery.md) for the retained campaign branch, complete-phase integration and continued later scope. Incomplete phases pause; completed phases incorporate only their selected delivered delta and verify/publish the receiving target. Final campaign completion alone permits eligible final archive. Before final feature verification, `sdd-integrate-feature` incorporates accepted deltas within the selected scope. Task transfer needs both owning lists in scope; document-only incorporation does not authorize execution. A complete coherent feature verifies/integrates/publishes its established target, then stops. Follow [feature incorporation](skills/sdd-integrate-feature/SKILL.md).

### Review and accepted revision

`sdd-manage` establishes source, concerns, evidence mode and boundary; selected owners assess, with `sdd-report` retaining located findings. Systematic reviews plan units; focused reviews may use prompt-defined criteria. Publish authorized report checkpoints and stop before repairs unless execution is included.

Accepted revisions route bounded changes to owners and `sdd-verify` for rechecks. Integrate only the complete authorized verified boundary. [Review/revision](skills/sdd-manage/references/review-and-revision.md) owns the procedure; [nested/reopened modes](skills/sdd-manage/references/revision-modes.md) preserve parent/return context and opening provenance. Do not automatically resume a suspended parent.

### Checkpoint steering

At a paused implementation checkpoint, `sdd-manage` routes the human-defined amendment to [sdd-steer](skills/sdd-steer/SKILL.md). Assessment-only returns impact. Commanded execution reconciles existing documents, code, tests and documentation without feature overlays or an obligatory formal campaign; verify/commit/push and integrate/verify/publish into the paused target. Return control without resuming `sdd-implement`.

### Release preparation and publication

`sdd-manage` routes [highlights-only](skills/sdd-forge/references/release-highlights.md) versus [complete messages](skills/sdd-forge/references/release-message.md) through `sdd-forge` and `sdd-report`. Complete preparation refreshes retained notes, preserving human curation and explicit template/path or supplied-text scope. Root RELEASE-NOTES.md is the default final destination; release documents may be committed within the active revision directory and moved in the release commit. Complete required Git persistence of owned ignore/tracked-note changes; stop before tagging or hosted release publication.

**Version numbers in the name of any release artifact are absolutely prohibited, regardless of type.** Before any release tag, publishing trigger, upload or publication, require an executed [artifact-name check](skills/sdd-forge/references/github-packaging.md#artifact-name-gate-and-repair) over the complete actual inventory. No type/extension may be skipped. Prior releases and explicit project naming policies/templates/examples create no exemption: correct all conflicting active definitions and use compliant names in every new release. Failures require persistent producer/code/docs repair, source publication, rebuild and recheck before continuing the authorized release.

An authorized release verifies notes coverage/context and version; version match alone is insufficient. The tag targets a verified release commit on the actual default branch: either a direct commit or the merge from its designated primary development branch. Its body and GitHub body use the exact finalized Markdown. Follow [release Git boundaries](skills/sdd-manage/references/git-workflows.md#release-commit-and-tag) and the [GitHub release owner](skills/sdd-forge/references/github.md). `sdd-verify` checks actual release evidence; reports distinguish prepared, Git-published and hosted-complete states. Package preparation alone does not authorize a release; prerelease review requires explicit selection.

### Focused maintenance and optional hosting

Select independent work through its owner and preserve its narrow outputs. Assessment/checks/drafts do not authorize repairs, task completion, PR creation or release publication. Persist reports or owned changes only within established repository authority; required Git publication still applies.

Hosted-only requests stop after their selected effects. Local work needs no provider credential. Accept supported supplied credentials through [protected handling](skills/sdd-manage/references/credentials.md); do not echo values into generated prompts, source, reports, diagnostics or normal handoffs. Authentication recovery preserves scope and does not bypass policy.

## Branches, integration and continuity

Use the coordinator's [continuity subworkflow](skills/sdd-manage/references/continuity.md) for `docs/dev/HANDOFF.md` and recovery from later records/Git. Milestone/phase review tasks refresh it in their completion commits; revision finalization and parent return refresh their boundaries. Ordinary task commits need no handoff update. At reconstructed startup, inspect unfinished branches against their recorded parents and request the continuation branch unless already selected.

Establish actual working/source/target identities, creation parent and branch-off checkpoint; completed new workflows integrate into that parent and restore its context without automatic task resumption. Preparation uses `design-docs`, main execution uses phase branches, and feature/revision identities follow [branch management](skills/sdd-manage/references/branch-management.md). Prefixes do not establish acceptance or authorize a merge.

For invalid implementation task completions, the manager resolves [forward recovery](skills/sdd-implement/references/completion-and-checkpoints.md#resolve-a-task-recovery) under existing authority; a repaired verification failure alone does not require renewed approval of the original range. Historical composition exceptions remain human decisions. For TASKS/FEATURE-TASKS, follow the [task commit contract and audit](skills/sdd-implement/references/completion-and-checkpoints.md#task-commit-contract): one executable task closes per commit with result/evidence and initial checkbox; exactly one owning task ID leads its subject. DOCS/FDOCS preparation persistence belongs to the coordinator's mapped [main](skills/sdd-manage/references/main-preparation.md) or [feature preparation](skills/sdd-manage/references/feature-preparation.md), not the product implementation audit. Non-task work invents no task ID. Preserve pending/unrelated work; a dirty tree does not authorize reset.

Eligible integration uses an explicit two-parent merge, merged verification and target publication. Partial ranges do not imply complete integration. On conflict, denied publication or uncertain effects, preserve work and reconcile state through [Git recovery](skills/sdd-manage/references/git-workflows.md); never reset or force-push unrelated work. Hosted state follows verified local evidence and the [backend lifecycle](skills/sdd-conventions/references/backend-object-lifecycle.md).

## Campaign records and shared conventions

Use the [campaign convention](skills/sdd-conventions/references/review-campaigns.md) for records and `sdd-report` for evidence/integration summaries. Preserve original opening provenance, accepted scope and return boundaries. Campaign records stay on their revision branch; no preliminary default/design-docs merge is required.

Current owners and active records guide routine work. Closed packages are frozen history: do not load without a specific need, edit or assess later compatibility. Eligible reopening uses the selected coordinator mode.

Apply [Markdown conventions](skills/sdd-conventions/references/markdown-style.md): heading/list/block separation, four-space indentation and one space after list markers. Preserve literals and closed records. Git provides checkpoints; no transaction journal is required.
