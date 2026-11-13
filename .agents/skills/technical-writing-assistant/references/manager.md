# Workflow manager

## Contents

- [Scope and boundary](#scope-and-boundary)
- [Task decisions](#task-decisions)
- [Evidence modes and selection](#evidence-modes-and-selection)
- [Selection and execution](#selection-and-execution)
- [Composite workflow recipes](#composite-workflow-recipes)
- [Coordination and iteration](#coordination-and-iteration)
- [Delivery and completion](#delivery-and-completion)
- [Examples and failure handling](#examples-and-failure-handling)

## Scope and boundary

Coordinate the smallest sufficient combination of focused workflows. Retain decisions, consolidate findings, resolve conflicts, and manage justified iteration. Do not duplicate detailed procedures, load every reference, or require the manager for a focused module. Direct evidence invocation may load only the mode-selection section.

## Task decisions

Extract decisions from the request and established context before asking questions. For a short task, retain them mentally; for substantial work, keep a concise working note.

| Decision | Establish |
|---|---|
| Objective | Review, revise, develop, explore, generate or assess outlines/maps, or a combination. |
| Authority | Wording repairs, structural changes, substantive proposals, and substantive changes already authorized. |
| Evidence mode | One of the two modes below, only when evidence work is relevant. |
| Coverage | Focused dimensions, supplied excerpt, or broader editorial examination. |
| Audience and genre | Purpose, reader knowledge, register, dialect, and applicable conventions. |
| Deliverables | Findings, clean/annotated revision, alternatives, outline/map, research results, or combinations. |
| Representation | Context-specific elements, relationships, detail, scope, sources, and criteria for outline/map tasks. |

Use [writing brief](writing-brief.md) only for material uncertainties and [material assessment](material-assessment.md) for uncertain readiness. Do not ask questions already answered or introduce a research choice into a punctuation-only task.

## Evidence modes and selection

### External research and verification

Independently find and inspect sources, fact-check relevant claims, assess support, and report contradictions and uncertainty. [Source research](source-research.md) performs retrieval and verification; [evidence review](evidence-review.md) assesses claim/support relationships. An explicit request to fact-check or independently verify sources establishes this mode unless other instructions limit it.

Use available authorized host tools. If suitable tools or source access are unavailable, disclose the limit and offer supplied-content assessment or a verification plan. Do not claim verification or silently switch modes. Continue independent editorial work.

### Review without external research

Use supplied material and model knowledge to identify evidence gaps, questionable claims, suitable evidence types, prospective sources, and verification steps. Conduct no independent external research. Acquire explicitly identified task targets through permitted access, including relevant repository files and appendices explicitly requested for inspection. This makes the material available for review; it does not independently verify its claims. Do not retrieve citation-only support, follow bibliographies, or search for corroboration in this mode. A supporting URL alone remains uninspected. Respect explicit no-network, no-retrieval, and supplied-content-only restrictions even for targets. If a URL's role is consequentially unclear, clarify it while continuing unaffected work. Report acquisition failures and request accessible contents rather than substitute memory.

Distinguish observations grounded in inspected supplied material from model recollection and proposed support. Remembered facts and bibliographic leads are unverified; do not invent titles, quotations, DOIs, pages, or source metadata.

Assess available evidence in either mode; target acquisition and source inspection are not a third mode. Keep the following questions distinct; use labels only when useful, not as mandatory records.

| Dimension | Question and outcomes |
|---|---|
| Provenance/access | What was inspected, supplied but uninspected, inferred, recalled, or proposed? |
| Source-to-claim relationship | Does inspected content support, partially support, contradict, or not address the claim? Unavailable content is not assessed. |
| Researched-claim outcome | Is the claim supported, partially supported, contradicted, or unresolved within the scoped inspected evidence? |
| Criterion outcome | Is an applicable requirement satisfied, partly satisfied, failed, or not assessable? This is not a claim-truth label. |

Uninspected, unresolved, unsupported, and false are not interchangeable. Inspection establishes what a source says; independent claim verification requires relevant evidence and an actual assessment.

### Selection and persistence

When evidence work is relevant, the prompt does not establish the choice, and no applicable preference exists, ask:

> Should I independently research and verify sources, or review the supplied material and identify evidence gaps and prospective sources without external research?

Retain the answer within the task unless changed. While awaiting it, continue structure, language, and internal reasoning that do not depend on external research; do not treat silence as selection. An explicit no-research instruction controls even if a recipe normally includes source research. A focused module follows the same rule without initiating a full composite workflow.

## Selection and execution

1. Identify the requested entry point and output. Honor review-only, alternatives-only, supplied-source-only, or outline-only scope. Preserve protected expressions and essential support from the start.
2. Resolve material intake uncertainty and assess readiness only as needed. Identify blocking inputs or author decisions; continue unaffected work.
3. Select applicable genre guidance: [software](software-documentation.md), [scientific](scientific-writing.md), or [professional](professional-writing.md). Load [style guidance](style-guidelines.md) for relevant editorial criteria.
4. Choose a recipe below or construct a smaller sequence. Translate step names using the entry point's direct routing table. Include only steps justified by the request or findings; recipes are adaptable, not mandatory pipelines.
5. For outlines/maps, establish contextual criteria through [outline context exploration](outline-context-exploration.md) if needed. Adapt representation to actual relationships without a closed list of specialized cases.
6. Resolve evidence mode before dependent evidence work. Keep reasoning critique available without pretending to have empirically verified its premises.
7. Execute focused procedures and retain their useful outputs: location, issue, consequence, remedy, source/status, and unresolved decisions. Use ordinary text/Markdown; formal registers are optional.
8. Apply authorized repairs, compare results with source material, and consolidate delivery. Use [revision check](revision-check.md) for delivered revisions; diagnosis-only work needs a consistency/scope check rather than an invented rewritten artifact.

## Composite workflow recipes

Initial assessment means readiness triage only when needed, not the detailed review. Comprehensive review considers every relevant dimension and explains material exclusions or unavailable coverage. Revision changes only what needs repair; a sound structure needs no forced reorganization. Both workflows honor the selected evidence mode and preserve essential content and authorial position. Substantive revision requires existing authority; missing information is not permission to invent it. Revision checks compare changed material with its source and instructions. Findings-only branches instead check their own findings for accuracy and consistency.

Shared style and genre guidance supply criteria, not compulsory extra stages. Named steps refer to their corresponding focused modules directly discoverable from SKILL.md.

Requests to assess document size or level of detail use composition analysis. In composition and comprehensive reviews, include this assessment when relevant to the request and support the conclusion within the inspected boundary. Do not turn an assessment into shortening or summary generation, or expand an unrelated local edit into a whole-document audit.

| Workflow | Typical sequence | Result |
|---|---|---|
| Focused language edit | Brief as needed → language revision → relevant terminology checks → revision check | Revised passage preserving or flagging substantive uncertainties. |
| Composition audit | Composition analysis → optional composition exploration | Located findings and priorities, including requested size/detail judgments; rewrite only when requested. |
| Structural revision | Composition analysis → exploration if needed → structural revision → revision check | Reorganized text with accurate purposes and transitions. |
| Comprehensive editorial review | Scope and genre conventions → relevant composition, language/style, argument, evidence, and terminology/consistency assessment → consolidation | Located, prioritized findings, reader consequences, remedies, and assessment limits; no automatic rewrite. |
| Comprehensive draft revision | Revision scope → diagnosis of relevant defects → structure, reasoning, language, and terminology changes as needed within authority → revision check | Revised draft, significant changes, and unresolved substantive questions. |
| Bullets or brainstorming to prose | Brief → assessment → composition exploration → relevant argument/evidence review → draft development → revision → revision check | Grounded developed text with support gaps visible. |
| Argument strengthening | Argument review → evidence review → research if selected → composition exploration → authorized revision → revision check | Stronger argument, or an account of why support cannot sustain it. |
| Fact-checking and evidence repair | Mode selection → claim identification → evidence review → source research when permitted → proposed corrections → revision check if implemented | Claim-linked support, contradictions, gaps, and wording. In non-research mode, label it a gap review. |
| Audience or genre transformation | New brief → genre guidance → composition analysis/exploration → structural revision or development → language revision → revision check | Adapted text retaining essential meaning and qualifications. |
| Concision or executive summary | Identify indispensable content → select emphasis/structure → compress or develop summary → revision check | Shorter text preserving essential reasoning, numerical factors, and qualifications. |
| Software documentation review | Software guidance → inspect available code/docs → diagnose composition/consistency → consolidate findings → revise when authorized → revision check if revised | Findings and recommended repairs; authorized revisions when requested; unperformed behavior checks remain explicit. |
| Scientific manuscript revision | Scientific guidance → selected composition, argument, evidence review → structural/language revision → revision check | Clear reporting without unsupported methods, results, or certainty. |
| Generate an outline or map | Brief/source assessment as needed → explore unresolved structural choices → contextual criteria → outline generation → outline review with relevant evaluative and validation checks | Context-appropriate structure with proposals and gaps visible. |
| Review an outline or map | Purpose/sources/criteria → context exploration if needed → outline review with requested evaluative and/or validation coverage → priorities | Editorial recommendations distinguished from validation failures; no automatic regeneration. |
| Repair an outline or map | Review/validation → authorized revision through outline generation or targeted repairs → recheck affected criteria | Repaired structure with changes and open issues recorded. |
| Derive a specialized map | Inspect sources → explore elements/relationships → contextual contract → outline generation → outline review including source/coverage checks | Context-adapted map, with source content, proposals, and status distinguished. |
| Outline to developed text | Review/validate as needed → relevant argument/evidence work → draft development → revision → revision check | Prose grounded in the outline and sources without invented support. |

## Coordination and iteration

Consolidate duplicate findings by location and cause; retain materially distinct issues. Prioritize blocking substantive decisions, major structural/support issues, then local expression. An issue's severity comes from its consequence for this task, not its module of origin.

Reconcile conflicts using user instructions, meaning preservation, source authority, purpose, and genre. Stable technical terms take precedence over synonym variation; factual conditions take precedence over brevity; genuine relationships take precedence over smooth transitions. If two valid alternatives imply different author positions, present the decision rather than choose silently.

Iterate only when new findings justify it: source research may narrow a conclusion, structural revision may expose a missing premise, or outline validation may change boundaries. Return to the affected module, record the change, and recheck dependent work. Do not repeat full reviews after a local repair without reason. Stop when scoped criteria are satisfied or remaining limits are explicit; do not pursue unbounded perfection.

Do not make every handoff an approval gate. Ordinary authorized edits proceed. Seek an author decision for unresolved substantive choices, unavailable essential inputs, or expanded authority. Keep materially meaning-changing proposals visible even when the user authorizes their implementation.

## Delivery and completion

Deliver the requested artifact and the necessary findings, significant changes, unresolved decisions, and verification limits. A clean paragraph need not include a project report. A substantial review should explain what was inspected and which dimensions were assessed. Distinguish inspected source contents, independently assessed claims and their evidence, supplied but uninspected material, inference, and prospective evidence. Inspection alone does not establish truth.

Check that coverage matches the request, findings agree, essential meaning/support survives, and no unsupported additions or commitments entered the result. Match "complete", "verified", and "tested" language to the actual work and its scope. Document source or tool limitations; drafting does not authorize sending or publishing.

## Examples and failure handling

- "Check parallelism" loads relevant style/language work, not an argument audit or research intake.
- "Develop these preliminary results into a discussion" may require argument/evidence review and a mode question, while independent organization proceeds. Do not turn a hypothesis into a finding.
- "Map this unfamiliar process" explores relationships and purpose, not a predefined profile catalogue. Missing sources bound coverage.
- "Shorten this memo" retains assumptions, quantities, calculation factors, and conditions needed to understand its recommendation.
- An external source contradicting the preferred conclusion triggers an explicit correction proposal, not selective omission or a more persuasive unsupported rewrite.
