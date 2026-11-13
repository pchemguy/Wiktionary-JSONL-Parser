# Project brief

## Purpose and ownership

`docs/dev/PROJECT.md` is the concise project brief: a reviewable statement of the project's purpose, intended users, desired outcomes, principal scope, non-goals and consequential constraints, formed from the initial description and clarified decisions. Identify material assumptions and open questions where needed.

The brief provides shared context for architecture and later specification. Keep it proportionate to the project and clear enough for the human to confirm its direction. No fixed heading schema, word count or exhaustive feature catalogue is required. A short seed is an input, not necessarily a sufficient brief. Use [guided exploration](exploration.md) to proactively uncover consequential gaps and alternatives; reuse established context rather than administer a fixed interview. Expand the brief using actual clarification rather than inventing accepted decisions.

PROJECT owns project intent and principal scope. ARCHITECTURE owns structural arrangements and rationale; DECOMPOSITION owns logical components; SPEC owns precise observable behavior/acceptance; PLAN owns delivery order; layout owns physical paths; TASKS owns executable work. Do not turn the brief into any of those documents. Consequential accepted technical choices or distinctive requirements may appear as constraints/principal scope without copying their full downstream contracts.

For a bounded capability addition, use the [FEATURE brief](feature-brief.md) and its preparation companion rather than creating another PROJECT.

## Inputs and decision state

Use the user's seed, actual clarification answers, applicable project instructions, accepted decisions and relevant existing project evidence. Apply [exploration decision state](exploration.md#facilitate-decisions): distinguish facts, confirmed choices, proposals/working assumptions, unresolved questions and delegated details. Do not infer approval from silence or agent-authored prose.

For an existing project, inspect/reuse its suitable brief rather than regenerate it as ceremony. Separate observed implementation from intended project scope. If the existing PROJECT contains operating instructions, preserve their authority and resolve its intended role before replacing content. Accepted feature incorporation into PROJECT belongs to [sdd-integrate-feature](../../sdd-integrate-feature/SKILL.md); a direct brief correction remains design-owner work within its requested scope.

Resolve missing decisions that would force the brief's intent, principal scope or consequential constraints to be invented. Structural choices needed before architecture may remain explicitly deferred with their dependency and resolution path; the brief need not contain a completed architecture. Non-blocking details may remain explicitly delegated to later stages. Reasonable proposed defaults can be presented for human confirmation; do not label them accepted requirements. State missing clarification provenance rather than claiming the seed supplied later choices.

Important interactions and boundary cases that materially affect current scope are brief-readiness work: identify and resolve them proactively during creation or revision before PROJECT approval. For main doc-design, apply [mode-specific decision authority](../../sdd-manage/references/doc-design-modes.md#prepare-scope-and-decisions). Autoloop retains first PROJECT approval but waives later approvals after announcing that policy; new material choices are delegated agent decisions, explained visibly and recorded with their actual basis. Keep non-material contract precision with downstream owners and preserve the brief's scope/detail boundary.

## Adaptable content structure

| Concern | Suitable content |
| --- | --- |
| Overview | What is being developed, the problem/use context and principal intended outcome |
| Users and scope | Intended users and principal capabilities included in the complete project |
| Goals | Outcomes the project should deliver, including important qualities |
| Non-goals | Explicit exclusions or proposed exclusions clearly identified for confirmation |
| Constraints | Accepted platform/technology/integration limits and consequential requirements |
| Assumptions/open questions | Material unresolved choices, proposals and intentionally delegated details |

The main brief describes the complete currently intended project, not only its first delivery increment. Select the applicable scope from the preparation records and express the resulting project directly, under the shared [content boundary](../../sdd-manage/references/human-document-review.md#development-document-content-boundary). Keep main-preparation scope-revision sequences in DOCS_PREPARATION until adopted; other workflows retain their owning evidence. PLAN can select an MVP and subsequent delivery increments within the intended scope. Keep finalized project descriptions focused on the intended state rather than editing history or unsupported maturity claims; use [evidence-backed positioning](exploration.md#evidence-backed-project-positioning) where relevant.

## Create or revise

1. Establish the selected artifact, authorized effects and stop. Use the design entry's manager/orientation prerequisites and actual dirty-path ownership. Document creation is not implied by conversational exploration.
2. Gather the relevant seed, decisions and current project evidence; clarify material gaps or label proposals/questions. Preserve explicit requirements without expanding scope silently.
3. Draft/revise PROJECT using an appropriate concise structure. Check that purpose/users/outcomes/scope/constraints are understandable and mutually consistent; non-goals and proposed assumptions are distinguishable from confirmed decisions.
4. Review against the inputs and document boundaries, including the shared content check: PROJECT must be understandable without knowing its SDD preparation mode or pass sequence. Remove preparation-process narrative, redundant wording and premature detail without losing currently intended requirements. State unresolved product decisions and deliberately deferred choices.
5. Under the established preparation/workflow Git authority, commit the reviewable artifact, push and verify remote containment before presentation or handoff, following [per-commit publication](../../sdd-manage/references/git-workflows.md#publish-each-commit). New preparation uses design-docs. Include applicable bootstrap records with the first authorized SDD checkpoint. No new mandatory PROJECT review-report file or administrative task is introduced.
6. Apply the manager's [human document review](../../sdd-manage/references/human-document-review.md): present the brief and concise substantive analysis, then pause after a newly created necessary PROJECT before dependent architecture/other use unless explicit applicable future-checkpoint preapproval covers it. Clarification, QC and commits/pushes do not supply human acceptance. Requested interactive review or an actual pending decision remains binding on continuation.

## Read-only review and handoff

For an explicit review, assess the existing brief against its accepted inputs, intended purpose, scope/detail boundaries and actual decision state. Flag SDD preparation-process narrative even when its scope distinctions are accurate. Return located findings, relevant gaps and a recommendation without source repairs or downstream authoring. Apply human review when interactive review was selected. Routine assessment of acceptable existing inputs does not require retrospective interactive replay.

The handoff identifies the actual PROJECT state, accepted/proposed/pending decisions, material constraints/questions and next authorized owner. Only after the necessary human checkpoint and technical readiness are satisfied may the manager hand the accepted brief to [architecture](architecture.md). If a brief-only scope was requested, stop at its review/result; acceptance alone does not authorize unrelated downstream work.
