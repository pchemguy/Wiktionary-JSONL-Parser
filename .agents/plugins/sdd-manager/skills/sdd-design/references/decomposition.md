# Decomposition

Refine accepted architecture into understandable component responsibilities and collaboration. ARCHITECTURE owns the major arrangement and consequential rationale; DECOMPOSITION owns logical units within it. Use the [document boundaries](../SKILL.md#document-boundaries) comparison when routing overlapping structural concerns. Read only the relevant ARCHITECTURE root and children, existing code or contracts where applicable, and the shared **sdd-conventions** modularity reference. Revisit architecture when decomposition reveals a weak block boundary rather than hiding the conflict in detail.

When a consequential uncertainty needs human-guided comparison, use [exploration](exploration.md) at the affected component/interface depth, then return here. Preserve settled project direction and route an actual architectural change to its owner.

## Document ownership

`docs/dev/DECOMPOSITION.md` owns the logical component model: responsibilities and exclusions, dependencies, state/resource ownership, provided/required APIs and verification seams. Its root maps components and their relationships; linked artifacts own cohesive detail.

## API surfaces

For each library, package or component, identify its external consumers and internal collaborators. External means outside the selected unit, including in-process callers; internal APIs are cross-component collaboration boundaries, not every private helper.

Define the provided/required operations, types and useful signatures or message shapes, visibility/entry points, provider and consumers, dependencies and state/resource ownership. Give enough precision for consumers to design their use without inventing the interface. Select details from actual use; do not catalogue private functions or add speculative abstraction layers.

Link precise behavioral contracts to their SPEC owner when established. Separate settled surface design from semantics SPEC must resolve. A material open choice blocks dependent use; permitted later refinement identifies its owning artifact, decision scope and prerequisite. Return structural conflicts to architecture rather than hiding them in API detail.

## Model and API-design artifacts

Keep detail inline or extract it when shared across components or independently substantial. Focused children under `docs/dev/decomposition/` and peer documents are both allowed; `MODELS.md` and `API-DESIGN.md` are illustrative names, not required files or paths. DECOMPOSITION links each selected artifact and states its scope and ownership.

Model design defines entities/value types, identities, relationships, representations and invariants. API design defines the structural surface and collaboration. Each definition has one canonical owner; reference shared types and declarations instead of copying them into each component or contract. A small cohesive design needs no extra files.

Selected model/API-design artifacts belong to DOCS-004 or FDOCS-004 alongside decomposition: one proposal, approval/preapproval, accepted-state commit and evidence scope. They add no preparation task or checkpoint. SPEC assesses required behavior against these definitions and routes structural corrections to the design owner. Do not turn design artifacts into file inventories, implementation order or task checklists.

## Existing systems and changes

Inspect actual component boundaries and dependents before proposing changes. For a feature, retain the accepted [FEATURE brief](feature-brief.md) scope and decisions alongside the applicable accepted architecture. `docs/dev/FEATURE_DECOMPOSITION.md` may describe only affected units, altered collaborations and interface boundaries, compatibility needs, and component impact for a scoped architectural revision. Reference unchanged main nodes rather than copying them. It may accompany FEATURE_ARCHITECTURE when both levels change; neither is obligatory for a change that does not affect its level.

Main ARCHITECTURE and DECOMPOSITION describe the coherent intended system after accepted decisions are incorporated. Feature documents serve the proposed delta until **sdd-integrate-feature** incorporates the accepted change into the main documents. Do not leave both contradictory descriptions as current truth.

## Review

For each unit, answer what it does, how it is used, what it depends on, and how its boundary can be checked without inspecting its internals. Inspect dependency cycles and unclear ownership; prefer a focused contract or a genuine combined unit to artificial layers. Check external/internal API coverage, canonical model/type ownership and whether consumers can use each boundary without inventing its surface. Check that SPEC can define objective behavior for each affected boundary, and that planned implementation could proceed in localized, verifiable changes. Report unresolved design decisions rather than inventing final contracts.

Read the main DECOMPOSITION and affected children as the intended component model. Remove narration of prior drafts or implementations after incorporating a feature; describe each settled boundary and responsibility directly. A feature overlay may describe the proposed change while it is active.
