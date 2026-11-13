# Specification review

For a review-only request, read the relevant SPEC root and children, accepted design, and any active change specification. Assess completeness, clarity, ownership, objective acceptance, and consistency without editing governing documents. State concrete findings and their consequences; do not demand invented detail where the project intentionally delegates a decision.

Check the canonical behavioral owner, relevant structural owner links, and affected consumers using [design traceability](system-specification.md#design-traceability). Ensure cross-component guarantees identify participating boundaries and design/contract conflicts are surfaced for accepted decisions. Recheck root/artifact routing, external and internal API contracts, errors, formats, compatibility, and end-to-end acceptance. Check referenced model/type definitions for single ownership and completeness. Compare with PROJECT, ARCHITECTURE, and DECOMPOSITION; report needed decisions to their owners. Identify impacts on PLAN, TASKS, any active FEATURE-TASKS, tests, and user documentation. A direct correction belongs to the owning SPEC node under [system specification](system-specification.md); incorporating an accepted feature delta into main documents belongs to **sdd-integrate-feature**.

## End-state language

Write the main SPEC and its children as direct descriptions of the complete intended system. Do not turn an incorporated change into an amendment or a story about prior versions. Replace transition wording such as “previously,” “formerly,” “now supports,” “newly added,” “was changed to,” “no longer,” and “this revision replaces” when it describes the document's editing history. For example, write “Encrypted archives are rejected” instead of “Encrypted archives are no longer supported.” Apply the same check to headings, rationale, acceptance conditions, and linked children.

An active feature specification may describe the baseline and proposed delta. A genuine compatibility contract may name earlier released versions or formats, but express their currently required treatment as a present guarantee. Historical steps belong in Git history, not in the main SPEC. This is an editorial check on meaning, not a ban on individual words that have a legitimate role in a requirement.

A review does not authorize document edits, code changes, or implementation of a newly specified capability.

## Required SPEC/design QC gate

Apply **sdd-conventions**' **Development-document QC** criteria. Review the selected SPEC root and applicable children against accepted PROJECT, ARCHITECTURE and DECOMPOSITION (feature deltas against their accepted main/feature inputs). Identify exact reviewed/governing states and group contract-to-design coverage using existing IDs/links. Check outcomes/non-goals, responsibility/interface/dependency consistency, unsupported structural assumptions, success/error/resource/lifecycle obligations, objective acceptance and parent-child coherence. Missing or contradictory significant obligations block dependent PLAN authoring.

When authoring or correction is authorized, fix bounded SPEC issues through its owning node and recheck. A needed design or behavioral decision goes to its actual owner; do not reshape design to make a deficient contract look consistent. Pure review leaves governing files untouched and returns findings; write a review report only when requested or included in authoring scope.

Use **sdd-report**'s **Document QC reports** reference to place `SPEC-REVIEW-REPORT.md` beside SPEC (or `FEATURE-SPEC-REVIEW-REPORT.md` beside FEATURE-SPEC). Cover selected contract artifacts and relevant model/API-design references in that root report. Retain located original findings, append each Revision N correction/recheck, and report Ready only for the currently reviewed scope with all confirmed issues resolved. Persist corrected documents and report together through sdd-manage. Reuse current equivalent review evidence; report affected downstream invalidation. Do not proceed to PLAN merely because SPEC exists.
