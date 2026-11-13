---
name: sdd-design
description: Use when exploring a software project or feature, forming architecture decisions, defining component APIs and data models, developing a component decomposition, or creating, reviewing and revising docs/dev/PROJECT.md, FEATURE.md, ARCHITECTURE.md, DECOMPOSITION.md, and scoped architectural change documents before specification.
---

# Explore and design

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

**Development documents describe the project; they must not narrate their SDD preparation process.** Apply the [content boundary](../sdd-manage/references/human-document-review.md#development-document-content-boundary) when authoring, revising or reviewing any root, feature counterpart or focused child, in every mode.

Obtain human approval of new FEATURE before dependent feature design/specification, and of new PROJECT before ARCHITECTURE, ARCHITECTURE before DECOMPOSITION, and DECOMPOSITION before SPEC, unless that checkpoint is explicitly preapproved. Apply [human document review](../sdd-manage/references/human-document-review.md) to necessary feature proposals and direct calls. Reuse acceptable existing inputs; begin with any requested interactive review.

For **feature preparation**, load [feature preparation](../sdd-manage/references/feature-preparation.md) and the shared [mode/pass policy](../sdd-manage/references/doc-design-modes.md) before dependent authoring. Use its applicable FDOCS stage, FEATURE_PREPARATION decision/QC evidence and mapped approval/stop; preserve sufficient main inputs and do not replay main initialization.

For fresh/resumed **main preparation**, load [main preparation](../sdd-manage/references/main-preparation.md) before repository writes, including direct calls. Its pre-write tracking gate, DOCS_TASKS first-approval commit and issue progression, package QC and merge/final-checkpoint rules govern this path. The coordinator persists the accepted document, current-pass decision/QC references in DOCS_PREPARATION and its checked DOCS task together; DOCS_TASKS contains task definitions/checkoffs only. Ordinary later edits retain completion; an explicit cursor reset reopens the same tasks/issues. Apply the [selected mode and pass boundary](../sdd-manage/references/doc-design-modes.md), including autodoc’s stop after DOCS-008 before package QC. The preparation-branch guidance below retains other paths’ scope and does not waive these main gates.

For preimplementation project authoring, have **sdd-manage** establish the dedicated design-docs branch under its [preparation integration gate](../sdd-manage/references/branch-management.md#preparation-integration-gate). Commit project documents and required QC reports there, then push and verify remote containment before handing off or advancing, under [per-commit publication](../sdd-manage/references/git-workflows.md#publish-each-commit). Before a dependent implementation branch is created, the manager explicitly merges accepted preparation into the actual default branch, verifies and publishes that baseline. Campaign plans/reports remain on revision branches; active implementation and steering amendments preserve their working-branch ownership. Read-only work creates no branch.

Choose the work requested and load only its reference. A request for a later stage can start there when its inputs are established; do not replay earlier stages as ceremony.

| Work | Load |
| --- | --- |
| Create, revise or review PROJECT.md as a concise project brief | [project brief](references/project-brief.md) |
| Create, revise or review FEATURE.md and its required preparation companion with the coordinator | [feature brief](references/feature-brief.md) |
| Proactively refine an initial idea before PROJECT, explore a feature delta, or resolve consequential uncertainty during later design | [exploration](references/exploration.md) |
| Define or revise major system blocks, dependency direction, and architectural decisions | [architecture](references/architecture.md) |
| Define or revise component responsibilities, external/internal APIs, data models and selected design artifacts | [decomposition](references/decomposition.md) |

When the request crosses stages, load the next reference as that stage becomes relevant. Exploration can remain conversational. Do not create project documents solely because discussion has matured. Document creation or revision requires **sdd-manage** to coordinate the user's request and a current **sdd-orient** handoff identifying a usable Git worktree, applicable instructions, target paths, and unresolved dirty state. This skill does not perform orientation or authorize a different workflow.

Use the **sdd-conventions** modularity reference when defining or reviewing boundaries, and its design heuristics when assessing a chosen approach or comparing options. Keep these checks separate from the document-specific procedures below. Observe project instructions and existing contracts; do not overwrite unowned changes. If required project evidence conflicts, resolve the conflict before mutation.

`FEATURE.md` owns the [scoped feature brief](references/feature-brief.md); its companion retains preparation evidence. `PROJECT.md` owns the [concise project brief](references/project-brief.md), `ARCHITECTURE.md` owns high-level design, and `DECOMPOSITION.md` owns detailed logical component boundaries. Both ARCHITECTURE and DECOMPOSITION may have focused children. Model and API-design detail may also use linked peer documents under the [decomposition ownership rules](references/decomposition.md#model-and-api-design-artifacts). Scoped feature documents express a proposed architectural delta where necessary. These documents inform SPEC; they neither replace its behavioral contracts nor authorize implementation, planning, layout authoring, or task execution.

## Document boundaries

| Document | Governing concern |
| --- | --- |
| PROJECT | Concise purpose, users, outcomes, principal scope/non-goals and consequential constraints, with material decision gaps identified. |
| FEATURE | Intended capability delta, retained behavior, compatibility/constraints and material product questions. |
| ARCHITECTURE | Major blocks, system-wide relationships and dependency direction, and consequential structural rationale. |
| DECOMPOSITION | Logical components, provided/required external and internal APIs, state ownership, model design and verification seams; owns selected model/API-design artifacts. |
| SPEC | Observable behavior and precise success/failure contracts, required qualities, and acceptance. |
| PLAN | Practical delivery order, capability increments, dependencies, and exit/decision evidence. |
| layout.md | Physical allocation of source, tests, documentation, and artifacts. |

Support required modularity, extensibility, scalability, decoupling, and testability through the accepted design. Tie variation and load decisions to actual requirements and credible needs; these qualities do not require realizing every anticipated capability in the first increment.

Use the relevant architecture or decomposition reference for read-only design review. Incorporation of accepted feature design into main PROJECT, ARCHITECTURE, or DECOMPOSITION belongs to **sdd-integrate-feature**.

At completion, state what was explored or changed, the decisions established, unresolved material questions, and which documents were inspected or updated. Report design as design, never as implemented functionality.
