# Objective and impact

Read the human's objective, current checkpoint, owning TASKS or active FEATURE-TASKS, latest task commits, and relevant accepted design, SPEC, PLAN, and layout. Inspect actual implemented behavior and affected tests and documentation. Determine whether the request is assessment only or commands amendment implementation; do not convert discussion into execution.

## Establish the boundary

| Question | Finding |
| --- | --- |
| Intended end state | What functionality is removed, reduced, or otherwise amended? |
| Retained contracts | Which supported behavior and compatibility obligations must remain valid? |
| Implementation checkpoint | What has been committed, what task-list work remains, and what pending changes exist? |
| Affected ownership | Which code, tests, existing development documents, README, or guides need focused changes? |
| Dependency effects | Which consumers, interfaces, resources, build paths, or future tasks depend on the amended behavior? |
| Acceptance | What observations will demonstrate the amendment and preservation of retained behavior? |

Reducing previously implemented functionality is the primary use case; other focused amendments can follow the same human-directed boundary. Do not broaden the work to redesign unaffected components or complete pending main-list tasks.

Resolve the established request against existing instructions and pending-change ownership. Preserve unrelated or incomplete main-workflow changes; report conflicting ownership or changes that cannot be separated before mutating the affected files. Do not invoke **sdd-implement** to finish them or reset the checkpoint automatically.

If necessary decisions remain unresolved, explain the specific conflict, impact, and alternatives to the human and stop the dependent work. An already explicit implementation command needs no additional permission for routine steps. For an assessment-only request, return the proposed amendment boundary and expected evidence, then stop.

## Amendment branch and continuation

Establish the paused implementation branch and checkpoint as the amendment target under **sdd-manage**'s **Git workflows** reference. Create a scoped amendment branch before edits or reuse the branch for the same unfinished amendment. Use `docs/dev/reports/phases/<phase-id>/revisions/<revision-id>/` for retained steering records, resolving the owning phase from PLAN/TASKS and the paused checkpoint; retain applicable stage filenames and the global campaign identity. Record its objective, creation parent/full branch-off commit, target, checkpoint, stable affected IDs and parent's suspended scope/stop in existing task/change evidence and its entry HANDOFF under [continuity](../../sdd-manage/references/continuity.md). Preserve unrelated pending work; use a separate worktree when switching would endanger it. An assessment-only request creates no branch.

A human command to continue a blocked amendment resumes its existing objective and branch. Inspect accepted documents, actual changes, task claims, failed checks, and pending merge/publication state; do not reinterpret it as main-task continuation. If the target or scope is unavailable or conflicting, report that decision before affected edits.
