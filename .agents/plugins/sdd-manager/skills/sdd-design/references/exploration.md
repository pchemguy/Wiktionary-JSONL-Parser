# Exploration

Use this subworkflow to critically evaluate an initial problem or objective and proactively help the human form a coherent direction. Its primary entry is before PROJECT creation; reuse it for consequential uncertainty in a feature or during later design. Begin from the actual objective, supplied context and accepted decisions, not a prescribed interview or technology catalogue.

Discussion, read-only inspection, small illustrative examples and explicit tradeoffs are allowed. Exploration can remain conversational. Do not write project files or run a project-changing prototype merely because a direction appears ready. An exploratory prototype inside the governed project is implementation and needs its own authorization and governance; a disposable experiment stays outside the project and establishes no relied-on contract.

## Assess the seed

Reflect the intended outcome briefly. Identify significant omissions, contradictory constraints, hidden assumptions and materially different interpretations. A terse idea may name a solution without explaining the problem or users; help uncover those aspects rather than merely asking whether the human has more requirements.

Reuse relevant preferences, existing assets and accepted project context. Distinguish preferences from hard constraints and observed implementation from intended scope. Scale exploration to uncertainty, consequences and reversibility: a well-constrained short seed may need little discussion, while a long description may still conceal a decisive conflict.

## Scan relevant concerns

Use these lenses to discover high-influence questions, not as a form to administer. Discuss only concerns that can materially affect direction, scope, feasibility, user experience or later autonomous decisions.

| Lens | What to establish |
| --- | --- |
| Purpose and use | Intended users, problem/use situation, desired observable outcome and what makes the result useful |
| Scope and experience | Principal capabilities/interactions, meaningful alternative interpretations, exclusions and complete intended project breadth |
| Environment and delivery | Where/how the product runs, distribution, relevant devices, offline needs and external dependencies |
| Constraints and priorities | User preferences, existing skills/assets, time/cost limits and consequential quality priorities |
| Foundational choices | Technology or structural directions whose consequences would materially change the product or development approach |
| Risks and delegation | Premises that could invalidate the direction, decisions needing human input and details the agent may resolve later |

Raise security, privacy, accessibility, persistence, integration, scale or other concerns when the actual use context makes them consequential. Concerns absent from this table may be central to a particular project. Distinguish complete intended scope from a possible initial delivery slice without turning exploration into phase planning or detailed specification.

During PROJECT or FEATURE preparation or revision, proactively identify important interactions and boundary cases and resolve choices that materially affect current application scope before its approval checkpoint. Do not automatically defer those choices because SPEC will later define precise contracts. In main or feature doc-design, use the selected [mode and pass decision authority](../../sdd-manage/references/doc-design-modes.md#prepare-scope-and-decisions): clarify predefined autoloop scopes upfront, and later make delegated material decisions with visible concise rationale while continuing. This delegation does not imply that the human personally supplied or approved each choice.

## Facilitate decisions

1. Select the most consequential unresolved gap or tension. Explain why it matters using practical consequences rather than implementation vocabulary alone.
2. Present a small number of credible directions and recommend a context-aligned option when supported. Explain when an important alternative would be preferable; avoid option catalogues, unsupported feasibility claims and generic pros/cons.
3. Ask a focused question or small coherent group where the answer changes the direction. Reuse supplied answers and honor explicit delegation; do not make the human discover the questions or micromanage eligible details.
4. Incorporate the answer and check consistency with the emerging direction. Challenge conflicts and unjustified complexity constructively. Revisit settled choices only for new evidence or changed objectives.
5. Periodically synthesize confirmed direction, proposed assumptions, unresolved risks and delegated decision boundaries. Continue while conversation has decision value; do not impose a fixed interview length.

Keep separate verified facts and their sources, explicit user decisions, working assumptions/proposals, open questions, delegated details, and considered/rejected alternatives. Silence after a recommendation or example is not acceptance. Document preapproval and broad execution authority do not fill missing requirements. Explicit delegation permits agent choices within its constraints; retain their rationale where consequential.

If new evidence conflicts with an accepted decision, expose the conflict before relying on a changed premise. Ask for the consequential decision when it is outside delegated authority. Keep safe unknowns explicit rather than blocking progress for every detail.

## Choose appropriate depth

Discuss purpose, consequences and reversibility before implementation mechanics. Surface a technical or architectural choice early when it affects principal scope, deployment, interaction, constraints or the cost of changing direction. Defer package versions, directory trees, class/API shapes and precise behavioral contracts unless the current decision actually depends on them.

Concrete examples below are illustrative and non-exhaustive. They demonstrate reasoning, do not bound supported domains or available options, and must not bias recommendations or become required questions. Derive coverage from the actual project, including concerns unrepresented by the examples.

For illustration, a browser game may merit early discussion of DOM versus Canvas rendering through interaction needs and accessibility. JavaScript/TypeScript, React and Node.js represent different language, UI and tooling/server-runtime choices; they are not one interchangeable option list, and a browser product does not inherently require React or a Node.js backend. A Python preference calls for understanding its purpose and considering credible delivery/runtime implications, rather than assuming it either settles or rules out the direction. A systems project might instead warrant C/Rust/Go tradeoffs when deployment, resources, safety or ecosystem needs make those alternatives relevant. None of these comparisons is mandatory.

For a feature, start with accepted scope, architecture, contracts and implementation evidence; explore the delta and compatibility consequences. Route the resulting intent and material choices through the [FEATURE brief](feature-brief.md) and coordinator-owned FEATURE_PREPARATION record before dependent design/specification. Greater technical precision may be useful at an affected interface, but do not reopen unrelated project choices. During architecture or decomposition, resolve the selected uncertainty at the needed depth and return to that owner without restarting initial discovery. Use the shared design/modularity conventions for actual boundary assessment rather than duplicating them here.

## Readiness and handoff

Exploration is sufficiently developed for a project brief when purpose/use, principal scope and consequential constraints/directions are coherent, with material uncertainties identified and a resolution or deferral path. Not every architectural choice must be settled before PROJECT. Separate what the brief needs from what must be decided before architecture or later dependent work; identify the owner/dependency of deliberately deferred questions.

When PROJECT creation, revision or review is requested, load the [project brief](project-brief.md) contract. An explicit draft request may proceed with identified proposals and safe unknowns; do not invent accepted choices or an extra exploration approval gate. Existing document checkpoints and scope still govern. Conversational maturity alone does not authorize drafting.

For architecture, purpose and scope must be understood, principal boundaries arguable, and no unresolved question may force a material structural choice to be invented. If architecture is requested earlier, distinguish blockers from deliberately open design options. Load [architecture](architecture.md) or [decomposition](decomposition.md) when that work is selected.

Hand off confirmed choices, consequential rationale, constraints, unresolved risks and delegated decision boundaries to the selected owner. PROJECT retains intent/principal constraints; ARCHITECTURE retains structural rationale. For main multipass preparation, persist material exploration outcomes through [per-pass and cross-scope decision retention](../../sdd-manage/references/doc-design-modes.md#retain-pass-and-cross-scope-decisions) before dependent use. Use existing owning records for durable decisions and existing continuity rules for checkpoints; do not introduce a mandatory exploration document, task list or per-turn HANDOFF update. Stop at the requested discussion/artifact boundary and preserve pending human decisions.

## Evidence-backed project positioning

Establish actual purpose, intended audience, learning objectives when applicable, and demonstrated maturity separately from intended capabilities. Describe a learning experiment as such only when supported by the brief. Related projects supply context, not inferred affiliation, dependencies, superiority or provenance.
