# Review and revision artifacts

Author and commit campaign plans/reports on the campaign revision branch. Project preparation artifacts and their QC reports have separate design-docs ownership; campaign records do not require a preliminary default-branch merge. Final eligible campaign integration carries its retained records into the established target.

Use these formats for campaign documents coordinated by **sdd-manage**. Apply **sdd-conventions**' **Review campaigns** naming and identity rules. The templates define presentation, not permission to review, revise, run checks, or merge.

- [Review plan](#review-plan)
- [Review report](#review-report)
- [Revision plan](#revision-plan)
- [Revision report](#revision-report)

Fill fields from actual scope, accepted decisions, source evidence, and observed outcomes. Omit inapplicable sections and never publish unfilled placeholders as facts. A focused review can omit REVIEW-PLAN; its report still records prompt-defined scope and criteria. Expand coverage/scenario tables for a systematic campaign rather than imposing a fixed criterion count on every review.

Record campaign ID, full starting SHA, exact reviewed/tested state when different, scope, stage status, and companion links. For imported reports, distinguish an unknown reviewed baseline from the campaign's known starting commit. Preserve stable legacy IDs and attribution. Use the canonical finding record once; other views reference it. Link existing companion files; identify not-yet-created artifacts as planned filenames rather than creating placeholders or implying that they exist.

Apply the [closed campaign record boundary](../../sdd-conventions/references/review-campaigns.md#closed-campaign-records). These update/recheck/disposition templates apply to active records. Finish final reports and feature package navigation before closure; later campaigns do not amend closed reports or snapshots. Historical records need no current-validity checks or compatibility findings. Load prior records only for a specific current question, not routine report preparation.

Final campaign integration uses the [integration summary contract](object-drafts.md#campaign-integration-summary), keeping title/objective, actual review/delivered scope and verification/limits concise and self-contained. Once committed, identify the campaign’s verified original opening commit separately from its branch-off baseline; amendment integration keeps that opening pointer unchanged and may retain compact original/reopening scope references and action IDs in its cumulative summary. Closure additionally depends on actual required publication and worktree return; writing a merge message alone does not close the campaign.

## Reopened amendment evidence

Only an authorized eligible [reopened campaign amendment](../../sdd-manage/references/revision-modes.md#reopened-campaign-amendment) permits updates to the selected formerly closed package. Retain the original campaign ID/baseline and observations, decisions, checks and closure facts. Record qualifying prior merge, current reopening checkpoint/target, human acceptance and added stable action IDs; append actual amendment checks/dispositions and subsequent integration/publication separately. Mark the amendment active/blocked until required final persistence completes, then record its new closure. Other closed records remain frozen. Do not infer new-candidate verification from old results or rewrite historical completion as though the amendment existed then.

## Workflow context

Apply **sdd-conventions**' **Workflow identity** for branch/directory association. Record campaign or phase ID, full baseline, creation parent and full branch-off commit, actual working/target branches, current authoritative sources and relevant artifact status. The entry HANDOFF links this provenance and the suspended parent/return boundary where applicable. A lightweight steering revision report may contain only objective/context, actual changes, verification, and publication; omit absent review/plan links.

Use the convention's workflow-specific report prefix: general campaigns under reviews, checkpoint steering under its phase's nested revisions, and feature records/reports under the feature directory. Retain stable identity and stage filenames; no implicit migration of historical records.

For feature preparation, use [FEATURE_PREPARATION](../../sdd-manage/references/feature-preparation.md) for request/decision provenance, campaign/full baseline, branches/targets, active source links, exact acceptance/QC evidence and current preparation boundary; FEATURE owns product intent. Do not create an extra preparation navigation record. At final archive, package navigation identifies actual archived paths, historical status/evidence and current main/task owners without copying preparation history. A partial phase report distinguishes pushed task-range completion from uncompleted phase integration.

## Review plan

Define what will be reviewed and how evidence will be obtained. Order independent foundations before dependent implementation/coordinator concerns where appropriate. Prescribe a report update and commit after each planned unit, then [per-commit publication](../../sdd-manage/references/git-workflows.md#publish-each-commit) and remote verification by the coordinating workflow before the next unit, including independent work. Reviewer assessment ends at the report commit; publication remains an execution step of the complete workflow. Host automatic tool review is a separate platform control. Do not claim the plan's scenarios have run.

```markdown
# Review plan

## Campaign and scope

- Campaign: <sequence_baseline>.
- Starting baseline: <full SHA>; reviewed source: <exact state>.
- Objective and included concerns: <scope>.
- Exclusions and evidence mode: <limits and permitted effects>.
- Companion report: <existing link or planned REVIEW-REPORT.md>.
- State: Planned.

## Review order and criteria

| Unit | Scope / resources | Dependencies | Criteria | Scenarios / checks |
| --- | --- | --- | --- | --- |
| U-001 | <bounded concern> | <prerequisites> | <criterion IDs and expectations> | <positive/negative cases and evidence method> |

## Evidence and persistence

Record inspected baseline locations, commands/outcomes, evidence class, unknowns, and exclusions. Allocate stable finding IDs with objective rechecks. After each unit, update and commit the report. The coordinating workflow pushes that committed checkpoint and verifies remote containment before any next review unit, project work or additional commit.

## Consolidation and stopping

Reconcile coverage, findings, priorities, dependencies, and readiness. Return a proposed revision queue and limits; do not implement revisions unless authorized.
```

## Review report

Keep baseline observations separate from later dispositions. Report no-finding coverage as well as findings. Use Open, Accepted, Deferred, Rejected, Revised, or Verified as applicable, explaining each transition. Reviewed coverage is not corrected source; severity, type, confidence, and disposition are separate dimensions.

```markdown
# Review report

## Campaign and assessment

- Campaign and starting baseline: <identity; full SHA>.
- Reviewed source and reviewer/date: <actual provenance>.
- Scope, criteria, and exclusions: <plan link or prompt-derived scope>.
- Evidence boundary: <inspection / consumer / execution / external checks>.
- State and readiness: <actual conclusion with limits>.

## Coverage and findings index

| Unit / criterion | Outcome | Evidence / reason | Finding IDs | Checkpoint |
| --- | --- | --- | --- | --- |
| U-001 / C-001 | <satisfied / finding / blocked / not applicable> | <located evidence> | <IDs or none> | <commit and verified push> |

| Finding | Type | Priority | Status | Related findings |
| --- | --- | --- | --- | --- |
| R-001 | <defect / recommendation / evidence gap> | <project severity> | <disposition> | <IDs or none> |

## Finding records

### R-001 — Actionable title

| Field | Evidence |
| --- | --- |
| Baseline location and confidence | <path/section and basis> |
| Observation and consequence | <actual conflict/result; supported impact> |
| Correction and dependencies | <bounded proposal; decisions needed> |
| Objective recheck | <observable acceptance> |
| Current disposition | <decision/revision evidence link; baseline observation retained> |

## Scenarios and limits

| Scenario | Setup / expected result | Evidence method / command | Observed outcome | Limits |
| --- | --- | --- | --- | --- |
| SC-001 | <actual setup and expectation> | <actual method> | <result or not executed> | <coverage boundary> |

## Revision handoff

Prioritize the proposed queue, dependencies, needed decisions, blocked checks, and evidence limits. Link accepted revisions when available; report counts consistent with canonical findings.
```

## Revision plan

Link accepted actions to review findings; retain rejected/deferred findings with rationale. Identify relevant governing-document changes and their owners. Acceptance of the plan does not mean changes or verification have happened.

```markdown
# Revision plan

## Campaign and decisions

- Campaign and starting baseline: <identity; full SHA>.
- Current revision source: <exact state if different>.
- Review report: [REVIEW-REPORT.md](REVIEW-REPORT.md).
- Revision report: <existing link or planned REVISION-REPORT.md>.
- Accepted, deferred, and rejected findings: <IDs and rationale>.
- Authorized scope/effects and state: <boundary; Planned>.

## Authoritative project updates

| Document / owner | Accepted change | Related findings | Required before |
| --- | --- | --- | --- |
| <SPEC/PLAN/design/layout/task owner> | <relevant resulting requirement> | <IDs> | <dependent action> |

## Ordered revisions

| Action | Findings | Outcome / targets | Dependencies | Recheck and regressions |
| --- | --- | --- | --- | --- |
| V-001 | R-001 | <bounded intended change> | <prerequisites> | <observable checks> |

## Execution and persistence

Establish the scoped working branch, target, and checkpoint. Update retained revision evidence, publish and verify each action commit before any next work unit or additional commit, then verify the boundary and explicitly merge, verify, and publish the target. Governing documents hold accepted project state; campaign artifacts remain retained.

## Limits and stopping

State concrete blockers, unresolved decisions, permitted repair scope, and unexecuted external/client checks. Stop at the authorized campaign boundary.
```

## Revision report

Record what changed and why, observed verification and limitations, finding disposition, and publication. Update after each action; reference original finding records rather than duplicating their baseline analysis. Planned, revised, verified, committed, merged, and published are distinct states.

```markdown
# Revision report

## Campaign and result

- Campaign, plan, and reviewed baseline: <identity and links>.
- Working/target branches and checkpoint: <actual Git identities>.
- Result and state: <completed / partial / blocked; supported outcome>.

## Revision evidence

| Action / findings | Actual changes | Commands / observed outcomes | Disposition / limits | Commit / push |
| --- | --- | --- | --- | --- |
| V-001 / R-001 | <changed owners and reason> | <actual checks and coverage> | <verified / revised / blocked; gaps> | <SHA and remote evidence> |

## Composition and integration

Record relevant regressions, working-branch and merged-state verification, merge SHA and parents, target publication/containment, and any pending effects. A passing structural check does not prove client or provider execution.

## Remaining findings and limits

List unresolved/deferred IDs, partial or blocked checks, exception rationale, and needed decisions. Preserve baseline evidence and retained plans/reports; do not infer global completion from the number of closed findings.
```

## Imported and conversation-only findings

Preserve imported reports and their attribution, original inconsistencies and source-relative evidence; describe such limits in a companion record rather than rewriting baseline history. Requested amendment notes use stable IDs, evidence, proposed changes, owner, validation and disposition. Report whether notes are conversation-only, written, committed/published, revised or verified. Record actual user decisions separately from agent assumptions and performed state. A later execution result does not retroactively validate the original diagnosis.

New campaign records state the stable campaign ID and the actual descriptive directory/branch separately. Their new directory basename is `<campaign>-<slug>`; use recorded established paths for continuation and historical links. A suffix change does not allocate a new stable ID.
