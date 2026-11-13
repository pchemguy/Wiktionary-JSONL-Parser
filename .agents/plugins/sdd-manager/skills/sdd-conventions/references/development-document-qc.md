# Development-document quality and conformance

Include the shared [Markdown style](markdown-style.md) in scoped document checks: heading, top-level list and code-block separation, four-space structural/list indentation, single-space marker separators, continuation attachment and Markdown templates. Preserve literal code/data syntax and exclude closed records. Formatting checks do not replace substantive conformance or authorize repairs.

Apply these invariants through the artifact owner and coordinator. This reference defines shared criteria and readiness, not authorization to edit an artifact.

## Preparation gates

| Completed artifact | Required review | Gate before |
| --- | --- | --- |
| SPEC root and selected children/contract artifacts | Conformance to accepted PROJECT, ARCHITECTURE and DECOMPOSITION; coherent, complete and assessable contracts. | Dependent PLAN authoring. |
| PLAN root and applicable children, with layout where relevant | SPEC coverage/conformance, bounded incremental delivery, phase/milestone decomposition and feasible exits/dependencies. | Dependent TASKS generation. |
| TASKS or active FEATURE-TASKS | PLAN conformance, complete executable coverage, bounded task decomposition, dependencies, unique identity and review units; trace acceptance back to SPEC. | Dependent implementation or hosted projection. |

Creating/revising an artifact includes its QC review, bounded corrections within accepted scope, recheck and report persistence before dependent progression. Review-only requests remain read-only with respect to governing artifacts; report findings without silently correcting them. Writing a requested review report is distinct from editing the reviewed document. No stage authorizes code implementation by implication.

If a correction needs a new behavioral, architectural or delivery decision, the coordinator routes it to the governing owner/human and blocks dependent work. Do not rewrite SPEC to fit PLAN, or PLAN to fit an accidental task breakdown. A prerequisite decision can be resolved within existing authorization; do not request redundant approval for already accepted scope.

## Decomposition and count policy

Assess bounded coherent functionality scope for every phase first, including later phases; greenfield Phase 1 additionally establishes the simplest sensible usable baseline. Apply counts to the justified functional boundaries, never use counts to choose extra scope.

Prefer approximately **3–5 delivery milestones per phase** and **3–5 delivery tasks per milestone** when the real work naturally supports that shape. These are planning heuristics, not quotas or a claim of universal optimality. Minimal useful increments, contracts, dependencies, integrated acceptance and maintainable scope determine the actual boundaries.

Count delivery milestones separately from the dedicated phase review milestone. Count delivery tasks separately from dedicated review/report-only tasks. Product implementation, integration, test, documentation and packaging work counts as delivery when it contributes to the capability; administrative/report-only work does not inflate the count. A delivery task's own testing/documentation remains part of that task. Counts must expose actual work, not hide oversized units behind labels.

| Delivery count | Required assessment |
| --- | --- |
| 1–2 | Explicitly review potential fragmentation or a boundary with too little independent value. Retain a small group when its narrow scope, cohesive outcome and dependency/risk/handoff purpose are clear. |
| 3–5 | Preferred starting range; still inspect actual scope and cohesion. A count in range cannot establish good decomposition. |
| 6–9 | Assess normal scope/cohesion and explain a material departure from the preferred range. Do not mechanically split an otherwise coherent group. |
| 10 or more | Explicitly review overloading, scope drift, weak boundaries and delayed integration. Split or narrow if evidence shows excessive scope; justify retention if the units genuinely form a bounded coherent outcome. |

Apply the same table to delivery milestones per phase during PLAN review, then to delivery tasks per milestone after TASKS generation. Report counts for each group, any excluded review units, triggered questions and the retained/revised boundary rationale. Empty delivery groups require correction or an accepted explicit purpose; the mandatory one-task phase review milestone is an intentional excluded review unit.

A single task implementing a subsystem is still oversized even when its milestone has only three tasks. Likewise, ten trivial file edits are not ten useful increments. Inspect behavioral contracts introduced, component/dependency breadth, prerequisite chains, failure/integration paths, verification effort and handoff overhead. Early meaningful end-to-end usefulness and timely regression checks remain required; do not defer coherent behavior until an enormous final milestone.

Do not add requirements, padding tasks, artificial milestones or phases to reach the preferred range. Do not merge independent outcomes solely to reduce counts. An occasional small phase is acceptable with a documented bounded scope; repeated tiny phases require assessing the larger delivery structure. Counts flag review questions; a finding needs a concrete consequence and evidence.

## Conformance review criteria

**SPEC against design:** include selected model/API-design and detailed contract artifacts; check explicit provided/required API surfaces, consumers and canonical type/contract ownership. Compare structural ownership, interfaces, dependency direction and cross-component obligations with ARCHITECTURE/DECOMPOSITION; trace accepted project outcomes and non-goals into canonical behavioral contracts and objective acceptance. Assess missing/contradictory responsibilities, invented behavior, unsupported structural assumptions, error/resource/lifecycle contracts and parent-child coherence. Design may need correction rather than SPEC; resolve that conflict explicitly.

**PLAN against SPEC:** establish complete version coverage and bounded phase-specific contract/acceptance routes. Assess every phase's useful integrated outcome, scope necessity, justified dependencies, independent deferrals and preservation of its predecessor; apply the additional simplest-usable-baseline check to greenfield Phase 1. Neither a small early milestone nor in-range counts excuses oversized phases or a final backlog bucket. Distinguish an explicit shape exception from version scope. Apply the [plan review](../../sdd-plan/references/review.md) for concrete checks. Assess omissions, duplication, invented scope, deferred work claimed complete and incompatible exits; later scheduled contracts do not automatically block a complete earlier phase. Layout must support the planned integration. Review semantic scope before counts and TASKS derivation.

**TASKS against PLAN:** map each delivery outcome/exit to sufficient executable work, preserving phase/milestone IDs and boundaries. Assess gaps, duplication, new requirements, strategy changes hidden in tasks, excessive/trivial task scope, feasible dependency order, tests/docs/failure/integration coverage and evidence. Validate project-wide unique task IDs, one owning list, exact checklist form, conditional standalone milestone review tasks and the unchanged special phase review task under the [backend lifecycle](backend-object-lifecycle.md#explicit-review-units). Verify the implementation-task/milestone counts and the final implementation task's report/review obligations when a standalone review task is omitted. Review task counts without counting the dedicated review tasks toward the preferred delivery range. TASKS may reveal an inadequate PLAN; return that amendment to sdd-plan, then recheck, instead of silently changing strategy.

Use existing requirement/component IDs and local links for traceability. A compact grouped coverage table is sufficient when it demonstrates completeness; do not require a new traceability database, one row/task per SPEC sentence or duplicate contracts in the reports. Review both numerical shape and actual meaning.

## Review reports and correction records

Place the root review report beside the artifact being reviewed:

| Reviewed root | Adjacent report |
| --- | --- |
| `docs/dev/SPEC.md` | `docs/dev/SPEC-REVIEW-REPORT.md` |
| `docs/dev/PLAN.md` | `docs/dev/PLAN-REVIEW-REPORT.md` |
| `docs/dev/TASKS.md` | `docs/dev/TASKS-REVIEW-REPORT.md` |
| Active `FEATURE-SPEC.md`, `FEATURE-PLAN.md`, `FEATURE-TASKS.md` | `FEATURE-SPEC-REVIEW-REPORT.md`, `FEATURE-PLAN-REVIEW-REPORT.md`, `FEATURE-TASKS-REVIEW-REPORT.md` beside their respective roots. |

Adjacency governs these preparation QC reports, including reports beside active FEATURE documents in docs/dev. The existing phase/feature prefixes continue to govern implementation reports and feature package records; source revision must distinguish these categories explicitly.

A governing root report covers its selected children and peer artifacts, including models, API design and contracts; do not require a separate report per optional artifact. During feature archive, retain selected reports beside the corresponding archived feature sources and repair in-scope links. After accepted incorporation, reassess affected main-document conformance; a feature review is not proof that the complete main documents conform. General campaign records retain their standard reviews layout. These preparation reports are distinct from implementation milestone/phase reports defined by the backend lifecycle.

Keep each report concise: artifact identity and exact reviewed state, governing source identities, scope/criteria, coverage and counts, stable located findings with consequence and correction/recheck, current gate result and limits. Use `Ready` only after current applicable conformance and QC pass; otherwise `Blocked`, with explicit reasons. Counts and justified exceptions are assessment results, not findings automatically.

Append a **Revision 1**, **Revision 2**, etc. section for each correction/recheck cycle. Record original finding IDs, actual edits/owners, why, exact revised document state, checks/outcomes, disposition and remaining blockers. Preserve original observations and append evidence; update the concise current finding index and gate result without overwriting review history. Git records commits; no report needs to contain its own commit SHA or a parallel transaction log.

Correct every confirmed QC/conformance issue before dependent progression. Resolve false positives or retain an acceptable small/large group with explicit reasoning rather than manufacture a defect. A knowingly deferred unresolved confirmed issue cannot support `Ready`; an explicit human exception records its scope and consequences without relabeling the review as passed. The non-critical code TODO deferral policy for implementation reports does not automatically apply to these document preparation gates.

Persist corrected artifacts and report/recheck evidence together. On interruption, inspect actual files, source identities and commits; finish the pending correction/recheck/report/push within scope. Do not regenerate good documents or duplicate reports merely because a response was lost.

## Ownership and invalidation

| Owner | Responsibility |
| --- | --- |
| sdd-conventions | Shared QC/count/conformance invariants and report identity. |
| sdd-manage | Schedule gates, establish authorized scope, route corrections/upstream decisions, persist preparation boundaries and block dependent progression. |
| sdd-specify | SPEC/design conformance review and authorized SPEC corrections. |
| sdd-plan | PLAN/SPEC conformance, phase/milestone decomposition and layout review; authorized strategy/layout corrections. |
| sdd-tasks | TASKS/PLAN conformance, delivery task decomposition, hierarchy/dependency review and authorized initial task-list corrections. |
| sdd-report | Review report and appended revision-section composition from actual owner evidence; no independent readiness decision. |
| sdd-design | Accepted architectural/decomposition corrections where required; no automatic redesign by downstream owners. |
| sdd-integrate-feature / sdd-steer | Accepted feature incorporation or commanded checkpoint amendments retain their established correction ownership; trigger affected QC reassessment. |
| sdd-orient / sdd-implement | Observe current readiness/evidence; implementation consumes eligible reviewed inputs and does not redefine document policy or run unrequested corrections. |

Initial preparation QC needs no extra implementation milestones/tasks solely for administrative review. It is part of the authoring workflow. Milestone/phase implementation code review remains mandatory later and is owned as defined by the backend lifecycle.

Review readiness is tied to actual artifact and governing source state. Material amendments invalidate affected downstream assessments until rechecked; unchanged scope may retain supported evidence. Review the impacted dependency chain rather than rerunning every project audit after every edit. Reuse demonstrably current equivalent prior reviews for existing projects; absent or stale evidence requires the focused missing review, not a new fictional historical pass. Feature preparation reviews its selected delta and affected interfaces against accepted main inputs, without forcing a whole-project rewrite.

## Evidence currency during implementation

Identify each reviewed root, selected child/peer artifact and governing input by available commit plus blob identities, or exact content hashes for pending edits. A material change confined to a linked model/API-design/contract artifact still requires reassessing affected readiness. Assess material changes to requirements, design, delivery strategy, task scope, dependencies, hierarchy or physical ownership. Routine task completion checkbox/evidence updates do not invalidate an unchanged decomposition or contract assessment by themselves; establish and report equivalence of the reviewed concern against the actual diff. A changed scope or upstream guarantee requires affected review even when its report says Ready. Do not infer currency from a filename or status label alone.

A direct dependent-stage invocation follows the same gate as a coordinated request. Obtain the focused missing review within the already authorized scope; read-only assessment can return its result without persisting a report when writes are prohibited, but absent durable required evidence remains a progression blocker. An explicit human exception names its affected scope and consequences; it does not turn a Blocked report into Ready or supply missing implementation acceptance.

## Human review and staged layout

Technical QC does not supply human acceptance. Apply the manager's [human document review](../../sdd-manage/references/human-document-review.md) for necessary newly created main/feature proposals and selected interactive reviews; acceptable existing inputs allow ordinary startup continuation. Record actual human decision/scope separately from Ready/Blocked.

At new PLAN creation before dependent layout authoring, assess strategy against SPEC and any relevant existing layout, state the pending placement coverage, and hold TASKS. A scoped Ready conclusion is limited to strategy. After human PLAN acceptance, prepare/review layout and update the adjacent PLAN report with combined readiness. Present the layout proposal and QC evidence for human approval before TASKS.
