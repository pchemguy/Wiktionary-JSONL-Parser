# Coordinate review and revision campaigns

Use **sdd-conventions**' **Review campaigns** reference for campaign identity/storage and **sdd-report**'s **Campaign artifacts** reference for formats. Scope the work before choosing focused reviewers; a campaign does not require a separate review or revision skill.

This is the formal campaign path for the [revision core workflow](workflows.md#core-development-workflows). A directly accepted focused amendment can enter revision planning without fabricating a preceding review. At a paused implementation checkpoint, [lightweight steering](workflows.md#steering-as-lightweight-revision) uses the human-defined objective and existing documents rather than requiring campaign artifacts. Both paths retain their own scope and stop rules. Checkpoint steering records live under `docs/dev/reports/phases/<phase-id>/revisions/<campaign>-<slug>/`; general campaign records retain the reviews prefix.

For an explicitly selected comprehensive prerelease review, load the [prerelease profile](prerelease-review.md) for candidate scope, coverage, owner routing and readiness criteria. It uses this lifecycle; release reminders do not activate review.

Before campaign branch setup, load [revision modes](revision-modes.md) when opening a revision within an active campaign or extending the eligible last closed revision. Nested revision establishes parent suspension/source/return context; a reopened campaign amendment requires verified eligibility and human authority. Ordinary closed records remain frozen; only an authorized selected reopening changes that record boundary.

## Review

Review the selected current source and active records. Prior closed campaigns are [frozen historical artifacts](../../sdd-conventions/references/review-campaigns.md#closed-campaign-records), not routine review inputs or current-validity targets. Read selected historical material only for a specific task need. Maintain findings/rechecks in the active campaign only; do not append to closed reports or create findings about their incompatibility with later changes.

1. Establish the request, authoritative instructions, exact reviewed source, concerns, criteria, evidence mode, and stopping boundary. A read-only review does not authorize source repairs or external effects. Writing and committing requested review artifacts is distinct from changing the reviewed source. The review ends at its report commit; the coordinating workflow owns subsequent publication under the established workflow authority.
2. For a comprehensive/systematic review, create a review plan defining units, dependency order, criteria, representative positive/negative scenarios, tooling, evidence limits, and report checkpoints. For a focused review, the prompt may supply the plan; record its scope and criteria in the review report without requiring another file.
3. Route each concern to its owning focused skill and relevant conventions. Review both sides of consequential handoffs, not merely file presence. Distinguish inspected source, consumer assessment, actual local execution, and authorized external verification. Record unavailable checks and unknowns without fabricating evidence.
4. Maintain the review report as each unit is assessed. Allocate stable finding IDs, located baseline evidence, consequence, confidence, bounded correction, and objective recheck. Preserve no-finding coverage and deferred units. Commit the updated report after each planned review unit. Hand each committed result to the coordinating workflow for [per-commit publication](git-workflows.md#publish-each-commit) and remote readback before any next review unit or other project work, including independent work; publication remains part of the encompassing workflow, while host automatic checks have separate ownership.
5. Consolidate coverage, canonical findings, counts, priorities, dependencies, and actual readiness. Return the report and proposed revision queue. Stop before revision unless the request already authorizes it; do not ask again when accepted revisions and their execution are already covered.

## Plan accepted revisions

Create/reuse the campaign revision branch before writing campaign plans and reports. These artifacts are retained on `revision/<campaign>-<slug>` through execution; do not route them through a design-docs branch or require their preliminary default-branch merge. If the accepted revision needs preimplementation project design/SPEC/PLAN/layout/TASKS changes, prepare those project artifacts separately on design-docs and complete [preparation integration](branch-management.md#preparation-integration-gate) before dependent source execution. Preserve the campaign branch and incorporate the published default baseline there when it already exists.

For a directly accepted prompt-defined revision, record its objective, affected owners, and stable action IDs in the revision plan; omit nonexistent review stages and links rather than inventing findings or a review report. Resolve missing requirement/design decisions before dependent work.

- Record which findings are accepted, deferred, rejected, or require a decision, with reasons and retained IDs. A recommendation need not be treated as a confirmed defect.
- Build an ordered revision plan with affected owners, intended outcomes, dependencies, permitted effects, and verification/recheck criteria. Link actions to findings; one action may address several findings and a finding may require several actions.
- Identify accepted changes to governing PROJECT/design/SPEC/PLAN/layout and TASKS/FEATURE-TASKS. Incorporate relevant decisions through the owning workflows so implementation has current authoritative inputs. The revision plan remains a retained campaign record, not a replacement SPEC or PLAN.
- Preserve selected document scope and task ownership. **sdd-integrate-feature** incorporates accepted feature deltas; **sdd-tasks** creates/reviews task lists; **sdd-implement** owns task execution/completion. Human-commanded checkpoint amendments remain **sdd-steer**-owned. Do not turn an ordinary review into steering or create feature overlays by implication.

## Revision execution authorization

Review ends at its report commit; the coordinating workflow publishes the report and integrates eligible verified revisions within the accepted request and stopping boundary. Carry that scope through handoffs and use [Git recovery](git-workflows.md#platform-authorization-rejection) for a host denial. Host automatic review is a separate platform control, not a plugin review skill.

## Revise, verify, and finish

Establish the entry HANDOFF when repository persistence is authorized under [continuity](continuity.md), retaining actual scope and parent. Incremental findings/actions stay in the existing campaign records; no action-by-action handoff rewrite is required.

1. Establish/reuse the scoped working branch and target under [branch management](branch-management.md), using [Git workflows](git-workflows.md) for integration. Preserve the accepted scope and stopping boundary through commits, publication and eligible integration.
2. Coordinate accepted governing-document updates and bounded source/test/document changes with their owners. Use task-list execution where executable tasks govern the work; use authorized focused maintenance where no task is assigned. Never invent a task ID from a finding ID.
3. After each revision action, update the revision report with actual changed artifacts, relevant acceptance/recheck evidence, finding disposition, limitations, and Git state. Commit source and evidence together, then push and verify remote containment before any next revision action, independent work unit or additional commit under [per-commit publication](git-workflows.md#publish-each-commit). Unresolved failures retain their actual state; do not mark a finding verified from a planned check or commit alone.
4. Recheck composition and relevant regressions after coupled changes. Keep original review evidence intact; append current verification or update dispositions only in this active campaign, without rewriting its baseline observations or touching closed records. Exclude closed artifacts from current link/compatibility checks.
5. Refresh HANDOFF at revision finalization with actual result/evidence, remaining decisions and parent return; reconcile the parent snapshot in the prospective merge under [continuity](continuity.md#integrate-and-return). Finish this campaign's reports/navigation and inspect the full diff for changes to prior closed packages before final verification/integration. Use the [campaign integration summary](../../sdd-report/references/object-drafts.md#campaign-integration-summary) for every revision mode’s final merge, including final title, objective, review/delivered scope and verification/limits. Explicitly merge the complete verified campaign tip, verify the merged result and publish the target. Record branch/commit/check/publication facts in existing evidence or Git without leaving a post-closure report edit unintegrated. Keep campaign artifacts in their original directory; no completion-time move or transaction journal is required. Closure freezes these records for later campaigns.

For a blocked campaign, preserve valid work and report the exact active action, affected source/evidence, branch/merge state, and needed decision or facility. A later authorized continuation resumes that campaign and scope rather than repeating completed review units or starting unrelated implementation.

## Diagnose an omission from evidence

Compare the applicable instruction, actual user decision, recorded execution state and observed failure before proposing a repair. Distinguish authority to perform an operation from the choice to activate an optional capability. Identify the concrete omitted handoff/decision and its effect. Do not treat an agent-authored assumption as a user decision, invent a policy violation to justify an apology, or quote an unavailable rejection trace. State the evidence limit and correct an inaccurate diagnosis explicitly.

## Retain requested amendment findings

When findings persistence is authorized, use the established findings/backlog artifact and preserve stable IDs, context/evidence, proposed correction, owning capability, validation and disposition. If no artifact exists, select an appropriate scoped document with its provenance; do not create a plugin revision or edit installed skills merely to record a note. Preserve explicit location/branch/pause limits and secret exclusion. Where writing is outside scope, say that notes remain conversation-only and identify the pending persistence decision.

Keep original observations and later decisions/results separate. Superseded or rejected proposals remain distinguishable from accepted, revised and verified work. Link actual implementation/check evidence before marking Verified; a promise, file draft or commit alone does not establish behavioral verification.
