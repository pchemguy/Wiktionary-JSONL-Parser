# Execute the amendment

## Revise existing development documents

This workflow directly owns the document amendments necessary for the human-commanded objective. Edit only affected owners and focused children; preserve their distinct responsibilities.

| Document | Focused amendment |
| --- | --- |
| PROJECT and design | Scope, component responsibilities, dependency direction, and interfaces affected by the objective. |
| SPEC | Supported and unsupported behavior, contracts, errors, invariants, and acceptance. |
| PLAN | Remaining delivery work, dependencies, phase or milestone outcomes, and exit conditions. |
| TASKS or existing FEATURE-TASKS | Affected task scope, dependency edges, parentage, and current completion claims. |
| Layout | Changed or removed physical owners and their documentation links. |

Keep the selected documents coherent descriptions of the intended end state. Do not add a feature overlay, chronological amendment appendix, or a discarded-approaches inventory; Git preserves history. An already active FEATURE-TASKS may be amended within its scope without incorporating it into TASKS.

Preserve stable task and parent IDs and unaffected completion evidence. Remove obsolete remaining work from the current task list where the accepted objective eliminates it; never reuse its IDs or mark removed work complete merely to tidy progress. Reassess previously checked items whose acceptance changes. Identify any newly necessary work beyond the focused objective for the human rather than executing it silently.

## Align code, tests, and user documentation

1. Use **sdd-tdd** to identify scenarios protecting retained contracts and exposing amended behavior. Existing accepted coverage may protect a behavior-preserving part of the change; missing historical RED evidence does not require deleting existing code.
2. Perform focused production changes. Remove the amended feature's obsolete paths, interfaces, configuration, or resources where the objective requires it; inspect consumers before deleting or narrowing shared behavior. Do not leave dead paths solely to satisfy obsolete tests.
3. Update tests against the revised accepted contracts. Remove obsolete scenarios or replace their expectations when the objective changes that behavior; preserve regression coverage for retained behavior. Do not weaken assertions to conceal an implementation defect.
4. Use **sdd-docs** to align affected module/API documentation, README, guides, examples, and links with the accepted amendment and implementation. Additional governing-document decisions outside the commanded objective remain findings for the human; they are not automatic scope extensions.
5. Use **sdd-verify**, repair amendment defects, and repeat affected checks until required evidence supports the result or a concrete blocker remains.

Do not execute subsequent main-list tasks, invoke **sdd-integrate-feature**, or hand production repairs to **sdd-implement**. All work in this execution cycle remains within the commanded steering amendment. If blocked, preserve valid work and report its state without claiming completion or resuming the main workflow.

## Reassess affected preparation gates

Before production work consumes materially amended governing inputs, apply **sdd-manage**'s **Document QC gates** to the selected affected SPEC/PLAN/TASKS and relevant design/layout. This skill retains commanded correction ownership; obtain focused owner assessment and append the adjacent report's Revision N evidence within scope. Correct confirmed conformance issues before dependent use; route new decisions beyond the amendment rather than rewriting upstream intent. Preserve original findings and unaffected valid evidence. Report unselected invalidated assessments without editing them or resuming main implementation; a coherent scoped amendment does not claim whole-project preparation Ready.
