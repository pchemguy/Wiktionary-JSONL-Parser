# Main documentation preparation record

Current preparation control and evidence. `DOCS_TASKS.md` alone owns task definitions/checkoffs; HANDOFF provides periodic continuity. Keep this record current and concise, linking detailed QC and product decisions. Retain compact multipass decision summaries here; Git retains historical document/QC versions. Do not append transcripts, command logs or successive copies of these sections.

## Current control

- Mode and decision source: {effective selection; human instruction or applicable mode basis}.
- Multipass delivery mode: {strict by default; flexible only with explicit human permission, its scope/source and affected prior-pass phase/task ranges; omit for onepass}.
- Current pass and scope: {pass identity and scope/sequence reference; onepass when applicable}.
- Approval/delegation basis: {active grants, conditions and revocations; distinguish human acceptance from preapproval}.
- Tracking/publication selection: {actual scope/source; pending or explicit local-only exception when applicable}.
- Next boundary: {candidate task or pending operation and exact stop; reconcile DOCS_TASKS and actual effects before acting}.

## Scope sequence

{For onepass, state the intended scope source. For multipass, use a numbered list: each pass begins with a concise bold descriptive title, followed by its scope delta. Preserve recognizable pass identities/titles across updates and identify the current position. Retain enough substance to execute remaining passes without transient chat; link durable detail where available. Do not invent later passes or copy the product documents.}

## Per-pass decisions

{For multipass, retain material decisions resolved during each pass, including interactive exploration. Use concise named entries or the table below; record originating pass separately from the passes/scopes where a decision applies. Distinguish human-confirmed, delegated-agent and unresolved/proposed choices. Retain completed-pass summaries across resets; mark replacements/supersession with their basis rather than silently overwriting them. Omit unused scaffolding for onepass.}

| Pass / decision | Resolution and brief rationale | Basis / source | Applicability / status |
| --- | --- | --- | --- |
| {originating pass; short decision title} | {material choice and why} | {actual human clarification or delegated authority; known source, or unknown} | {current/future scopes; active, proposed or superseded with replacement reference} |

## Cross-scope decisions

{Retain a compact view of decisions governing interactions across multiple or later passes. Reference per-pass decisions where sufficient; do not repeat their full text. Keep applicability and reconsideration conditions explicit, updating this view when an authorized change supersedes a decision. No fixed concern checklist or separate registry is required.}

| Concern | Decision / applicable scopes | Reconsideration condition |
| --- | --- | --- |
| {short concern title} | {decision reference or concise resolution; affected passes/scopes} | {material change/condition requiring reassessment, or none known} |

Keep detailed current contracts in their owning product documents and link them when available. Future-scope choices remain here until applicable; summaries do not themselves approve a document. These sections retain decision substance/provenance, not transcripts or duplicate specifications.

## Decisions and document evidence

Record selected model/API-design artifact paths, owners and exact states with DOCS-004; contract artifacts with DOCS-005. Their governing-root approval/preapproval and QC cover the whole set. Include referenced definitions in package QC; do not add a parallel artifact registry.

Qualify entries by pass and task. Identify proposed/accepted roots and required children by known commit/blob or content identity, with the actual decision/preapproval basis and QC references. For a completion commit, use a known proposal/content identity rather than its own future SHA. Do not duplicate task checkboxes or treat historical approval as current readiness.

| Task | Current evidence / decision basis |
| --- | --- |
| DOCS-001 | {Initialization result below; known evidence or pending} |
| DOCS-002 | {Pass; PROJECT state/decision; evidence or pending} |
| DOCS-003 | {Pass; ARCHITECTURE state/decision; evidence or pending} |
| DOCS-004 | {Pass; DECOMPOSITION state/decision; evidence or pending} |
| DOCS-005 | {Pass; SPEC state/decision; QC reference or pending} |
| DOCS-006 | {Pass; PLAN state/decision; QC reference or pending} |
| DOCS-007 | {Pass; layout state/decision; combined QC reference or pending} |
| DOCS-008 | {Pass; TASKS state/decision; QC reference or pending} |
| DOCS-009 | {Pass; package QC source/report/outcome or pending} |

Material unresolved decisions: {issue, affected scope/next step and actual authority, or none}. Record adopted product decisions in their owning documents and link them here rather than duplicating their contracts.

## Initialization and current reset

- Original root-file presence: {retained and copied filenames; unknown if unsupported}.
- Preservation/copy verification: {actual result/evidence, or pending}.
- Initialization continuation: {none/all/mixed presence and actual continuation/preapproval/stop basis}.
- Manual provenance setup: {default enabled, or explicit human/project opt-out/deferral with decision source; verified seed/base/merge identities or blocked/pending effects; no transcript required}.
- Current reset: {none, or prior pass/checkpoint, reason/scope change, next pass and approval basis; outstanding reopening goes below}.
- Prior-pass evidence: {known Git checkpoint references where needed; not current-pass acceptance}.

## Pending transitions

{Only unresolved publication, hosted closure/reopening, integration or checkpoint effects, with known identities, current observation and next permitted action; or none. A recorded completion cannot prove its later push, issue closure or merge. Reconcile actual state before retry and clear resolved items at the next owning update; no extra maintenance commit is required merely to record an already recoverable readback.}
