# GitHub TASKS projection

Main documentation preparation uses [its separate lifecycle](github-docs-preparation.md), including pre-write projection without product PLAN/TASKS, first-approval issues and milestone closure after published integration. The implementation lifecycle below does not reopen completed DOCS issues for later document revisions.

Apply the [backend object lifecycle](../../sdd-conventions/references/backend-object-lifecycle.md): read the full hierarchy but project only the eligible phase identified by sdd-manage. Do not create future-phase objects before predecessor completion/integration/publication. First-phase bootstrap needs no predecessor. Create and verify all phase objects, including dedicated review milestones/tasks, before its first task. Preparation or a complete local backlog does not activate every phase.

For that phase in the requested TASKS or active FEATURE-TASKS projection, create one GitHub issue per task, one GitHub milestone per SDD milestone, and one phase label per SDD phase. Assign each task issue its parent milestone and phase label when creating it. Do not duplicate an issue already projected from the other list. After a task is implemented, verified, committed, and reconciled in its owning task list, close its issue as completed under [issue lifecycle](github-issue-lifecycle.md).

Project the Phase → Milestone → Task hierarchy into one GitHub repository. Re-read TASKS, any active FEATURE-TASKS, and relevant PLAN or FEATURE-PLAN outcomes and exit conditions before writing. Take IDs and names from the task's owning list; use the applicable plan for supporting descriptions, not to rename hosted objects. For reused parents, ensure names match TASKS; stop for conflicting IDs, names, or parentage across the lists. Follow an established project naming convention only when it preserves unambiguous stable identity and the hierarchy.

| SDD item | GitHub object | Name or title | Brief description or body |
| --- | --- | --- | --- |
| Phase `2` — Archive streams | Label | `sdd-phase-2-Archive-streams` | Brief phase name and purpose. |
| Milestone `2.2` — ZIP support | GitHub milestone | `sdd-2.2-ZIP-support` | Milestone outcome and exit conditions. |
| Task `T-012` — Implement ZIP stream support | GitHub issue | `[T-012] Implement ZIP stream support` | Task brief and exact identity marker. |

Derive names from the owning task list using the hierarchy convention's normalization rule. Match managed objects by stable ID before reconciling a changed name; do not create a duplicate because a title changed. Give the phase label a brief description rather than copying the whole PLAN. The GitHub milestone reflects the milestone's outcome and exit condition; it is not a nested child of the phase. Assign each task issue the phase label and its GitHub milestone. Do not strip unrelated labels when reconciling.

When **sdd-report** is available, supply the exact task identity marker and request its issue draft (`title`, `body`) using the owning task list and applicable documents. Use its title and body format; verify that the title and marker identify the same task. When **sdd-report** is unavailable, compose a baseline draft with the `[<task-id>] <task title>` title and a body covering task outcome, reason or relevant context, expected scope, dependencies, acceptance and prescribed checks, and document links where present. Include code context, measurements, or task-kind instructions when the actual task calls for them; example prose from other projects is not a source of requirements. Do not fill absent facts with invented content. Apply the shared [Markdown style](../../sdd-conventions/references/markdown-style.md) to generated issue bodies, including heading/list/code-block spacing, single-space list-marker separators and nested lists. Include a clearly delimited identity marker, for example:

```markdown
## Task brief <!-- sdd-forge:task-id=T-012 -->

**Outcome:** ...
**Context:** ...
**Scope and dependencies:** ...
**Acceptance and verification:** ...
**Sources:** ...
<!-- /sdd-forge:task-id=T-012 -->
```

Use the exact ID for lookup. Before creation, search open and closed issues and exclude pull requests; validate any candidate's marker and title against the owning task list and the other active list for duplicate IDs. Reuse a unique match and report a conflict for multiple or contradictory matches. Create or reconcile the phase label and GitHub milestone, then the task issue with both associations. Apply the GitHub operational-failure protocol after failed or interrupted writes: re-read affected identities before retrying, preserve unknown outcomes, and create nothing when lookup is incomplete or ambiguous. Do not close or reopen an issue merely because a task list changed; use the issue lifecycle procedure.

Complete the phase label, all native milestones and all task issues/associations with provider readback before returning activation ready. A partial or uncertain projection remains pending; recover by identity lookup before creation. Preserve and report pre-existing future-phase objects rather than deleting them retrospectively.

Report created, matched, updated, and conflicted objects with IDs and URLs. Return the task-to-issue associations as the handoff; a separate checked-in mapping artifact is not required for this projection.

## Optional local projection mechanism

For the supported canonical hierarchy, [input authoring](../scripts/forge-project-input.md) can generate a source-bound JSON draft; the agent enriches dependencies, review roles and briefs from actual governing documents. After the manager's gates and outgoing-content review, [forge-project](../scripts/forge-project.md) creates absent/reuses exact objects and performs bounded complete readback. --check previews authored content locally; --reconcile-only resolves interrupted state without writes. Source hashes/positive flags do not prove semantic readiness. Edited metadata/briefs or unsupported layouts return to this backend's authorized reconciliation; do not overwrite user material or alter valid source scope to fit the utility.

## Document QC prerequisite

Before creating/projecting task issues, phase labels, native milestones or task issues, establish current owning-list and upstream preparation readiness through **sdd-manage**'s **Document QC gates** reference. A direct forge call uses the same gate; report missing/stale or blocked conformance to the coordinator without silently editing governing documents or creating objects first. Read-only mapping assessment may proceed and report blocked projection. This prerequisite does not turn report Ready into task completion or replace lifecycle verification for existing issue/milestone closure.

## Confirmed scope and late activation

Require the manager's [tracking decision](../../sdd-manage/references/tracking-decision.md) handoff to identify the established repository/lifecycle selection and its request or project-policy source before projection. Authentication or an inactive-state statement is not activation confirmation. Late confirmed projection discovers existing objects first and reconciles eligible completed work from retained commits/checks without replaying tasks. Return pending/unknown effects separately from recommendation and confirmation.
