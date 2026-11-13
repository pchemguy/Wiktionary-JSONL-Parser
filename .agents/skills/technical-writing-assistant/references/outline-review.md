# Outline review

## Contents

- [Scope and authority](#scope-and-authority)
- [Inputs and coverage](#inputs-and-coverage)
- [Evaluative review](#evaluative-review)
- [Validation checks](#validation-checks)
- [Outputs and repairs](#outputs-and-repairs)
- [Examples and failure handling](#examples-and-failure-handling)
- [Completion checks](#completion-checks)

## Scope and authority

Assess an existing or generated outline/map for fitness for purpose and for conformity with applicable criteria and inspected sources. Review includes selectable evaluative and validation activities. Recommend changes without automatically rewriting, inventing scope, or equating preferences with requirement failures. A well-formed structure does not establish factual correctness or universal completeness.

## Inputs and coverage

Use the artifact/version, purpose, audience, governing sources and requirements where available, and contextual criteria. A working contract means the task's agreed representation criteria; ordinary prompt instructions can supply them without a separate document or intake.

Select coverage from the request:

| Coverage | Work |
|---|---|
| Evaluative only | Assess organization, clarity, usefulness, and alternatives. Do not add an unsolicited criterion-by-criterion validation report. |
| Validation only | Check applicable structural, requirement, and source-fidelity criteria. Do not add unsolicited design alternatives or a comprehensive compositional critique. |
| Comprehensive | Perform both activities as relevant and consolidate overlapping findings. |

Infer a provisional purpose or derive and state defensible provisional criteria when the material makes them clear and the risk is low. Use [outline context exploration](outline-context-exploration.md) for consequential ambiguity; ask only if needed to resolve it. Do not invent a mandatory schema or mode questionnaire.

Identify the artifact, inspected sources, scope, and applicable criteria once where practical. Separate required constraints from preferences. Without source access, assess supported internal properties and mark source fidelity or completeness not assessed; absence of an item in an excerpt does not prove omission from the whole artifact. Criteria may require qualitative judgment.

## Evaluative review

1. Read the structure as its intended user. Identify the organizing principle and whether it serves the purpose.
2. Examine coverage: central content, missing prerequisites, irrelevant additions, and exclusions. Separate a suspected source gap from an observed structural gap.
3. Examine hierarchy and relationships. Are containment, dependency, ownership, chronology, or comparison used consistently? Are cross-cutting relationships hidden by nesting?
4. Examine granularity and boundaries: overloaded nodes, isolated fragments, overlapping responsibilities, duplicates, and unexplained abstraction shifts. Do not require equal node counts or branch depth when content differs.
5. Check titles and content notes for usefulness, accurate function, and intelligible sibling groups. Conventional headings such as "Methods" and "Results" can be effective; generic wording alone is not a defect. Flag headings whose promised content conflicts with their notes.
6. Check sequence and emphasis where meaningful. Place prerequisites before dependent concepts and proportion detail to importance, audience need, and evidence.
7. Test practical usefulness: can readers navigate, writers develop the text, or reviewers assess coverage? Add traceability or status fields only when useful for that purpose.
8. Propose local repairs or an alternative organizing principle when local fixes cannot resolve the cause. Distinguish necessary repairs, optional recommendations, and unresolved contextual choices.

## Validation checks

1. Establish the validation boundary from the shared inventory: exact artifact/version, inspected sources, scope, and criteria. State any provisional criteria and their basis.
2. Check structural validity in the chosen representation: node references resolve; labels are distinguishable where needed; hierarchy or typed relationships are coherent; required fields exist; order and dependencies are consistent. A cycle is a defect only when the relationship requires acyclicity.
3. Check source fidelity. Trace claims, nodes, status labels, and relationships to inspected material. Identify omissions, contradictions, unsupported additions, and proposals presented as established facts. A declaration alone does not establish implementation or testing status.
4. Check coverage against identified requirements. Map each required item to a location or an explicit gap. Account for exclusions and unavailable sources; do not turn optional improvements into requirements or invent missing policy.
5. Check cross-view consistency when a tree, table, and diagram represent the same material. Names, boundaries, statuses, and relations must agree or explain the different perspectives.
6. Report each assessed criterion as satisfied, failed, or not assessable, with location/source and reason. Use partly satisfied only when identifiable subparts warrant a partial outcome and explain the remainder. Use not applicable only for criteria genuinely outside scope, not for missing evidence.
7. Recommend precise repairs and recheck affected criteria after authorized changes. A title correction may affect notes and cross-references. Editorial preferences remain recommendations unless they violate an applicable criterion.

Keep criterion outcomes separate from provenance/access, source-to-claim support, and researched-claim outcomes; these answer different questions. See [manager evidence distinctions](manager.md#evidence-modes-and-selection) only when needed. Inspect available source content in either evidence mode; independent corroboration follows the selected mode. No inaccessible source is represented as inspected.

## Outputs and repairs

Return located findings with reader consequence, remedy, priority, substantive implications, and criterion outcome/basis where applicable. For a simple artifact, prose and a bounded conclusion suffice. A substantial validation may benefit from a criterion/requirement, location/source, result, and repair table; no formal record is mandatory.

State what was checked, material failures, unresolved choices, and limits. "Complete against the supplied requirements" is narrower than "complete". Do not claim unperformed automated checks. When both activities identify the same issue, report it once with its editorial consequence and criterion basis rather than in duplicate lists.

Offer a revised sample only when requested or useful to explain a recommendation; do not replace the whole artifact in review-only work. Use [outline generation](outline-generation.md) for an authorized redesign. Recheck affected criteria and dependencies after repair; use [revision check](revision-check.md) for comparison of changed material against its source and instructions, without repeating the full review.

## Examples and failure handling

- A required "Context" topic appears as a heading, but no supplied content explains it. Topic presence is satisfied; explanatory adequacy is not assessable. If the brief also requires content notes, their absence fails that separate requirement. Do not invent a note requirement for a topic-only outline.
- One contradictory status claim fails both source fidelity and required-topic representation. Report one finding carrying both criterion bases and its shared remedy. Keep independent defects separate.
- "Operations" and "Problems" duplicate troubleshooting: recommend consolidation or clearer boundaries and explain the navigation cost.
- "Reliability" contains only installation steps: identify the misleading promise. Accurate "Methods" and "Results" headings need no renaming solely for specificity.
- "Validated capabilities" is based only on filenames: fail that status claim's source-fidelity check, even if the tree is balanced. Implementation may exist elsewhere; do not claim it is universally absent.
- A required error-handling topic has no node: report a coverage failure and a proposed location without inventing error policy.
- A shared-services map can have uneven branch depth. A two-way communication cycle can be valid; a strict prerequisite cycle requires repair. Judge relationship semantics rather than visual symmetry.
- Half the sources are inaccessible: report internal checks and partial source assessment, not an unqualified completeness pass.

## Completion checks

Coverage matches the request. Applicable quality dimensions and assessed criteria have a stated basis; source limitations and unavailable evidence are explicit. Required constraints, optional preferences, source-derived content, and proposals remain distinct. Shared issues are consolidated. Recommendations guide authorized repair without imposing a template, and the conclusion reflects the actual boundary and remaining defects.
