# Phase, milestone, and task hierarchy

Use one Phase → Milestone → Task hierarchy. Each task has exactly one parent milestone, and each milestone has exactly one parent phase. `docs/dev/TASKS.md` holds the complete intended hierarchy. An active `docs/dev/FEATURE-TASKS.md` may hold its feature's scoped delta, using the same three-level form and project-wide unique task IDs. Reused phase and milestone IDs and names match the main hierarchy; new groups follow the accepted feature plan. In either list, phase heading and checkbox agree. PLAN or active FEATURE-PLAN defines strategic outcomes and exit conditions, and the owning task list supplies host-facing names.

Keep IDs stable across both lists and feature reconciliation. A host projection uses the project-wide task ID to recognize an object and reconciles its name when the owning list changes. Resolve duplicate task IDs across lists, mismatched parent identities, phase headings and checkboxes, or ambiguous parentage before publishing. Task completion remains evidence-backed in its owning list; a host object's state is not completion authority.

## Delivery and decision boundaries

Every delivery phase expresses a bounded, coherent functionality increment on the preceding usable baseline; greenfield Phase 1 establishes the simplest sensible usable product. A necessary enabling/risk stage needs bounded evidence and a route to integrated behavior. Milestones expose meaningful integrated capabilities and exit evidence; tasks supply bounded executable work within them. PLAN owns these boundaries under the [delivery procedure](../../sdd-plan/references/delivery-plan.md), including version coverage across phases. Small milestones/tasks do not justify an oversized phase, including a later phase; a task need not independently produce user-visible value.

At consequential milestones, identify the demonstration or feedback that informs a human decision to continue, amend, simplify, or stop. Keep these decisions with the human; the hierarchy does not authorize automatic steering, stopping, or task-list continuation. Stable identities, parentage, and completion evidence remain governed by the owning lists and execution workflow.

Apply [backend object lifecycle](backend-object-lifecycle.md) for conditional standalone milestone review tasks, the unchanged special single-task phase review milestone, folded boundary evidence, completion gates and report placement. PLAN reserves those milestones/exits; TASKS derives their tasks.

## Hosted projection

When the selected backend supports issues, as GitHub does, create an associated issue for every task of the eligible phase in TASKS or the active FEATURE-TASKS being projected; never duplicate an issue for the same project task ID. Represent each phase with a phase label and create a host milestone for each SDD milestone when supported; use a milestone label only when a backend defines equivalent completion/reconciliation semantics; otherwise report milestone lifecycle unsupported. Assign each task issue its phase label and its parent milestone or milestone label when creating it. After the task is implemented, verified, committed, and reconciled in its owning task list, close its issue as completed. A feature parent checkbox does not establish completion of the whole-project phase or milestone.

The active backend owns object creation, lookup, and reconciliation. It may define equivalent host objects while preserving the phase → milestone → task relationships and issue lifecycle.

For the GitHub backend, use these names from the task's owning list:

| Host object | Title or name |
| --- | --- |
| Phase label | `sdd-phase-2-Archive-streams` |
| Milestone | `sdd-2.2-ZIP-support` |
| Task issue | `[T-012] Implement ZIP stream support` |

If a host has no native milestones, an equivalent milestone label may be named `sdd-milestone-2.2-ZIP-support`. Replace example IDs and words with the actual ID and name in the owning task list. For labels and milestone titles, trim the name and replace whitespace with hyphens while preserving meaningful case and acronyms; normalize other host-incompatible characters deterministically. The stable ID distinguishes objects even when their names change. Give labels brief descriptions of their phase or milestone scope; use the backend's available metadata for milestone outcomes and exit conditions.
