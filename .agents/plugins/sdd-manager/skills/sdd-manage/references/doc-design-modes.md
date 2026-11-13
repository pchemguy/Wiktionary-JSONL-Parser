# Doc-design modes and pass control

Use for main and feature document preparation mode selection, pass boundaries, decision authority and multipass recovery. [Main preparation](main-preparation.md) and [feature preparation](feature-preparation.md) retain their mapped task/QC/publication mechanics; [human review](human-document-review.md) retains presentation and decision evidence. A cursor reset changes workflow progress, not Git history or file contents.

## Workflow mapping

| Concern | Main | Feature |
| --- | --- | --- |
| Brief | PROJECT | FEATURE |
| Control/evidence record | DOCS_PREPARATION | FEATURE_PREPARATION |
| Task-only progression | DOCS_TASKS, DOCS-001–009 | FEATURE_DOCS_TASKS, campaign-scoped FDOCS-001–009 |
| Document pass / package QC | DOCS-002–008 / DOCS-009 | FDOCS-002–008 / FDOCS-009 |
| Package report | DOCS-QC-REPORT | FEATURE-QC-REPORT |

In the shared rules below, **brief**, **preparation record**, **document pass** and **package QC** mean these mapped artifacts/stages. Feature scope is the intended delta against the existing system; assess unchanged main design/layout for reuse instead of manufacturing new overlays. Main initialization is not repeated for a feature.

## Select and retain the mode

The ordinary default is **interactive/onepass**. Document approval and pass control are separate choices:

| Selection | Human approval | End of document pass |
| --- | --- | --- |
| interactive/onepass | Each necessary document checkpoint unless explicitly preapproved | Follow the selected preparation range and existing final-QC gates |
| autodoc/onepass | Brief approval remains active; ARCHITECTURE through TASKS are preapproved | Stop before package QC |
| autodoc with human-controlled multipass | Brief approval remains active each pass; subsequent document checkpoints are preapproved | Stop for reset or advance direction |
| autodoc with autoloop | First brief approval remains active; later brief approvals are waived | Reset for the next predefined scope; stop after the last pass, before package QC |

When autodoc includes an explicitly predefined sequence of later scope revisions, use autoloop unless the human requests human-controlled multipass. Do not infer future scopes or select multipass for an ordinary onepass request. At entry, state the actual selection, pass scope and stop. In autoloop, **explicitly announce that later brief approvals are waived** before the first brief approval. Retain explicit human overrides and later steering.

Record mode, current pass/cursor, scope sequence and actual approval/delegation basis in the mapped preparation record; the mapped documentation task list holds only tasks/checkoffs. For multipass, also retain the delivery mode below and its permission scope/source. Carry them into each document-owner handoff so delegated decisions and preapproval are not replaced by generic interactive defaults. HANDOFF snapshots link that owner; no second registry is needed. Selection supplies its scoped checkpoint preapproval; ordinary autodoc does not delegate unresolved material scope choices unless explicitly authorized. Autoloop decision delegation is defined below. Initialization continuation, technical QC, Git publication, tracking and implementation authority keep their existing gates.

## Multipass delivery modes

Select **strict multipass by default**, independently of document approval and human-controlled/autoloop continuation. **Flexible multipass requires explicit human permission**; autoloop delegation, document preapproval and cumulative scope do not supply it. Announce and retain the effective selection before dependent planning or task revision.

- **Strict:** Later passes must not change phases or tasks established by earlier passes. Preserve their IDs/names, scope, milestone membership, order, dependencies and exits. Add new scope through subsequent bounded delivery phases and tasks; do not regenerate prior ranges from the cumulative SPEC or broaden their exits to include later requirements. An intermediate reset protects ranges already established, without inventing missing phases/tasks.
- **Flexible:** Small changes that fit an earlier pass's scope may be integrated into its corresponding phase/task range. Assess semantic fit, dependencies, functional size and verification effects; retain the affected range and concise rationale in the per-pass decisions. Keep stable IDs and bounded phases, preserving the existing useful baseline for features and the simplest sensible initial product for greenfield. Permission does not cover substantial replanning or large/poorly fitting additions, which still require subsequent bounded increments.

Compare the proposed PLAN/TASKS with their retained prior-pass versions during authoring and QC. Keep the selected policy, permission and pass-to-range references in the preparation record; product documents describe the resulting delivery strategy and work, without pass history. One pass may introduce several phases: this policy does not impose one phase per pass or feature. Design/SPEC may evolve to describe the complete current scope; later implementation may modify shared code while preserving prior working behavior.

If scope or a discovered defect conflicts with a protected range, report the concrete conflict and use or obtain explicit scoped human direction; do not ask again for an already granted override, silently relax strict mode or pass invalid documents. Neither mode authorizes rewriting completed implementation evidence or reopening completed work outside its existing amendment procedure. Retain mode changes and their prospective scope; returning to strict does not undo earlier authorized flexible changes.

## Prepare scope and decisions

Use sdd-design's [exploration](../../sdd-design/references/exploration.md) during brief preparation and revision. Proactively identify and resolve important interactions and boundary cases, surfacing decisions that materially affect current application scope before brief approval. Keep the brief at principal-scope depth rather than drafting a detailed SPEC early.

For human-controlled passes, obtain the current scope/revision and resolve its important choices with the human before brief approval. For predefined autoloop, clarify the initial scope and important interactions across all supplied later-pass scopes upfront; do not draft all later document sets. Each brief describes the complete current-pass scope; retain future changes in the preparation record's scope sequence until their turn rather than folding them into the first brief. Apply the [development-document content boundary](human-document-review.md#development-document-content-boundary) to every authored root/child: express the intended project state without narrating the pass sequence. The first brief approval authorizes the agreed sequence and resets, with later document checkpoints preapproved as stated above.

In autoloop, newly discovered material decisions outside the initial agreement are delegated to the agent. Use best judgment from available project/conversation context and general domain knowledge, distinguish assumptions from verified facts, and record consequential decisions in the owning documents. Give timely, concise commentary identifying the issue, relevant assumptions, key tradeoffs, chosen action and scope consequences so the human can steer. Proceed without an acknowledgment or extra approval pause. Actual execution failures and missing required facilities retain their gates; do not turn an eligible delegated decision into a blocker.

## Retain pass and cross-scope decisions

In multipass mode, The preparation record must retain a compact decision summary for each pass, including material choices resolved interactively. Record the issue/resolution, brief rationale, actual human or delegated-agent basis/source, originating pass, applicable scopes and current status. Distinguish proposals/unresolved questions from settled choices and product decisions from document approval. An upfront decision about a future pass belongs under its originating pass with that future applicability; do not adopt future requirements into current product documents early. When no new choice is resolved, identify carried-forward decisions rather than inventing a resolution.

Maintain a named **Cross-scope decisions** section for choices governing interactions across multiple or later passes. Reference the per-pass summaries rather than repeating full decisions. State applicability and material reconsideration conditions; derive concerns from the project rather than a mandatory checklist. Detailed current contracts stay in their owning product documents. Use the mapped [main](../../../assets/DOCS_PREPARATION_TEMPLATE.md) or [feature](../../../assets/FEATURE_PREPARATION_TEMPLATE.md) preparation template; no separate decision files or mandatory identifier scheme is needed.

Persist resolved choices before brief approval or other dependent use, in the existing proposal/owning checkpoint rather than per-turn commits. Keep completed-pass summaries through resets and later turns. Before a new pass or resumed work, review applicable inherited/cross-scope decisions; reuse settled choices unless changed scope, evidence or human steering warrants reconsideration. Record an authorized replacement, reason and decision basis, retaining the superseded summary and its origin. Autoloop delegation remains applicable without inventing human confirmation or another approval pause; unresolved authority conflicts retain their existing gates.

## Complete a pass

For features, use the same approval/decision policy above with [feature pass completion and reset mechanics](feature-preparation.md#pass-completion-reset-and-recovery); do not run main DOCS issue operations on feature IDs. The remaining mechanics in this module describe main preparation.

For **main preparation**, one full pass spans **DOCS-002 through DOCS-008** in dependency order. Revise retained documents against the current pass scope and recheck affected dependents. Reuse unchanged acceptable content without artificial edits, but record fresh pass acceptance/preapproval and relevant QC; prior-pass approval alone does not complete a reset task.

Complete each document with its approved state, current-pass decision/QC references in DOCS_PREPARATION and checked DOCS task together, then publish/read back and close/read back its existing issue when tracking is enabled. A preapproved document needs no extra proposal/approval round trip. Earlier user-requested stops and resets remain controlling.

After DOCS-008 and its required publication/issue closure, autodoc stops or performs the next authorized autoloop reset. At an autodoc stop, include DOCS_PREPARATION pass evidence and refresh HANDOFF in the DOCS-008 completion commit with the pass result and pending reset/advance boundary; confirm subsequent hosted effects by readback. Keep DOCS-009 unchecked and its issue and documentation milestone open. Do not call the package complete, run whole-package QC, merge documentation or activate implementation. Per-document QC remains required. Human-controlled multipass waits for reset/scope or advance direction; autoloop proceeds through only the predefined remaining scopes, then stops. Incorporating those revisions means updating the document set, not Git integration.

An explicit advance selects the existing [package-QC stage](main-preparation.md#final-package-qc-integration-and-checkpoint) within its actual scope. It does not select implementation or a new pass. Do not waive the separate final package/integration gates because a loop completed.

## Reset the cursor

A human may request reset at any intermediate checkpoint in active doc-design. Autoloop also authorizes reset after DOCS-008 when a predefined pass remains. This is an explicit exception to ordinary first-approval tasks staying complete during later edits.

1. Reconcile the current checkpoint, pending publication/hosted effects, approval/loop and delivery modes, prior delivery ranges and next scope. Preserve unrelated or incomplete work; do not use git reset, delete documents or allocate another preparation branch. Retain all existing development documents as version N−1 inputs for revision into version N. Git stores those versions; no copied file set or filename suffix is required.
2. In one reset commit, record the prior pass/checkpoint, reason/scope change, next pass/scope and approval basis in DOCS_PREPARATION; set the cursor to DOCS-002 and uncheck **DOCS-002 through DOCS-009** in DOCS_TASKS. Keep DOCS-001 complete, preserve existing PROJECT/design/SPEC/PLAN/layout/TASKS content, per-pass/cross-scope decision summaries and task IDs. Refresh HANDOFF with this reset boundary and outstanding hosted operations. Existing QC/approval evidence remains historical and does not certify the new pass.
3. Publish/read back the reset commit. If tracking is enabled, have sdd-forge [reopen the same eight issues](../../sdd-forge/references/github-docs-preparation.md#reset-a-document-design-pass), verify identity/association and open states, and resolve contradictory milestone state. Do not resume document work while required reopening is pending or unknown. Tracking-disabled resets use the same local commit/cursor without hosted writes.
4. Resume PROJECT using the retained brief and new scope. Apply the selected mode's current-pass approval policy, then revise dependents through DOCS-008. Reset grants no implementation range or unrelated scope.

## Resume or steer

Recover DOCS_PREPARATION control/evidence, strict/flexible selection and permission scope, prior delivery ranges and applicable inherited/cross-scope decisions, DOCS_TASKS checkboxes, document/Git and hosted states before acting. Review decision applicability/status before dependent work; a reset does not erase settled choices. A published reset with partial issue reopening needs reconciliation of those same issues, not another reset commit or pass increment. Reuse already verified effects and complete only outstanding operations. A completed pass awaiting reset/advance remains at that boundary; file presence or closed prior-pass issues do not advance it.

Retain human changes to scope, pass order or mode in DOCS_PREPARATION before dependent work. Switching to human-controlled multipass restores its PROJECT and end-of-pass checkpoints for subsequent work; do not retroactively invent approvals. Reuse existing owning records and normal continuity checkpoints rather than per-action HANDOFF updates.
