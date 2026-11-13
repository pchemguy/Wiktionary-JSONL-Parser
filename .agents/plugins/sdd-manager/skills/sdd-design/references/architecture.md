# Architecture

Define the system's high-level arrangement and why it fits the project's purpose. Read the accepted PROJECT brief, exploration decisions and relevant existing project evidence. For a feature delta, use the accepted [FEATURE brief](feature-brief.md) and its recorded decisions alongside the applicable main architecture; do not recreate PROJECT. Apply the shared **sdd-conventions** modularity checks to major boundaries. Use [decomposition](decomposition.md) when responsibility analysis reaches detailed components.

Use [exploration](exploration.md) for consequential unresolved structural choices before relying on them. Reuse accepted brief decisions and delegated boundaries; resolve the selected uncertainty and return here without replaying pre-brief discovery. Do not invent a material choice from a deferred question.

## Document ownership

- `docs/dev/PROJECT.md` provides the accepted project context under the canonical [project brief contract](project-brief.md). Preserve its intent/constraints without repeating the brief as architecture.
- `docs/dev/ARCHITECTURE.md` is a compact but substantive design entry point: a short orientation back to the brief; major blocks and their responsibilities; dependency direction and cross-block interactions; relevant external systems and data ownership; selected patterns, design principles, and consequential tradeoffs; system-wide architectural invariants; and a map of focused children when present.
- Focused children under `docs/dev/architecture/` may own a substantial architectural area. The root defines their scopes and system-wide relationships; each child adds detail within its area. Split for independent responsibility and navigability, not a fixed size or one child per task.

Keep project-specific links in ARCHITECTURE limited to useful navigation. Put detailed logical component responsibilities and collaboration in DECOMPOSITION, exact observable behavior and acceptance in SPEC, physical placement in layout, and delivery order in PLAN. Use the [document boundaries](../SKILL.md#document-boundaries) comparison to route shared interface, ownership, and invariant concerns by granularity. Record a design choice and its reason where that reason is needed to understand a durable constraint; avoid a chronological decision log in the current-state architecture.

## Initial and existing systems

For a new system, establish its intended blocks and dependency direction before expanding detailed components. For an existing system, inspect the relevant actual code and contracts; distinguish observed architecture from the intended change. Do not claim an inferred or proposed capability is already implemented. If the task is adoption of project-wide documents, describe the intended whole within the evidence available and surface gaps.

For a material architectural change, `docs/dev/FEATURE_ARCHITECTURE.md` may define the feature or revision's objective and scope, affected baseline blocks, proposed final arrangement, dependency or compatibility effects, and explicit non-goals. It is a scoped delta; unchanged architecture remains owned by the main document. Do not require this overlay for every feature or correction.

## Review

Check that every major responsibility has one owner, important interactions and dependencies are legible, architectural constraints support the desired outcomes, and remaining unknowns are explicit. Confirm PROJECT and ARCHITECTURE do not repeat one another and that any child scope is navigable from the root. Stop at architecture when the user requested only architecture; a sound architecture is not permission to author SPEC or start implementation.

Read PROJECT, the main ARCHITECTURE, and affected children as descriptions of the intended end state. Remove narration of earlier drafts or implementations, including “formerly,” “now,” or “replaces” when those words describe an editing transition. State the settled arrangement directly; keep genuine compatibility constraints as present design constraints. A feature overlay may describe its proposed delta until **sdd-integrate-feature** incorporates the accepted change.
