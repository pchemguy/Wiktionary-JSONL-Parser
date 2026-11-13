# Scoped change specification

Use `docs/dev/FEATURE-SPEC.md` when an additive, corrective, subtractive, or compatibility-sensitive change needs a reviewable behavioral delta before it is integrated into the complete system specification. A small unambiguous correction may instead revise the owning main SPEC node directly when that is the requested scope.

For a feature campaign, use the accepted [FEATURE brief](../../sdd-design/references/feature-brief.md), its recorded decisions and applicable main documents as governing inputs. Keep the brief's scope and compatibility constraints while refining exact contracts; unresolved material intent returns to sdd-design/coordinator before dependent work.

Define:

1. the change objective, affected users and existing SPEC nodes, and whether the work adds, alters, or removes behavior;
2. the final supported behavior and explicit unsupported boundaries or non-goals;
3. changed public and internal contracts, errors, data and persistent formats, compatibility, and transition requirements where material;
4. dependencies and effects on completed consumers, including a required rejection behavior when a capability is removed;
5. acceptance conditions for the changed behavior and affected cross-component guarantees;
6. unresolved decisions whose answer would alter the contract, without pretending they are settled.

Reference unaffected main SPEC nodes rather than copying them. If the change alters structural boundaries, align with applicable FEATURE_ARCHITECTURE or FEATURE_DECOMPOSITION decisions; those documents are needed only when their level actually changes. Treat implementation evidence as observed state, not automatic approval of a new requirement.

The feature document describes an intended delta while active. Say explicitly which main requirement it revises; if it conflicts without declaring a change, resolve the conflict before authoring further. It does not contain implementation tasks or chronological migration notes. Use **sdd-integrate-feature** to incorporate settled final behavior into the main SPEC when requested.

## Review the scoped delta

Apply [SPEC/design QC](review.md#required-specdesign-qc-gate) to the selected delta and affected interfaces against accepted main/feature sources. Produce the adjacent FEATURE-SPEC review report and resolve confirmed issues before dependent feature planning. Do not force a complete main-document rewrite or incorporate the delta implicitly. Absent feature design overlays can be replaced by demonstrably sufficient accepted main design.
