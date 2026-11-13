# Feature brief

## Purpose and ownership

`docs/dev/FEATURE.md` is the concise product brief for a new feature campaign. **sdd-design** owns its authoring and review. It defines the intended change to an existing system, not a new whole-project brief or a campaign journal. Read accepted main documents and relevant implementation evidence; distinguish already supported behavior from the requested delta. Do not impose a new MVP or reopen unrelated project choices.

Create the brief at FDOCS-002 with the coordinator's current [feature preparation record](../../sdd-manage/references/feature-preparation.md). The record retains the original request, proposal/decision provenance, acceptance and preparation progress. FEATURE describes the intended capability directly under the shared [content boundary](../../sdd-manage/references/human-document-review.md#development-document-content-boundary); it contains no branch operations, document approval status or preparation cursor. Material unresolved product questions can appear, clearly distinguished from settled scope, without copying the decision history.

## Content and readiness

Choose a concise structure proportionate to the actual change; no fixed heading schema, word count or exhaustive catalogue is required. Establish:

- Purpose, users/use context and intended observable outcome of the addition.
- Included capability and explicit non-goals, distinguishing existing behavior to retain from changed or added behavior.
- Affected existing guarantees, compatibility/integration consequences and consequential constraints.
- Material assumptions or unresolved product choices, with a clear resolution/delegation path before dependent use.

Reference sufficient accepted main context instead of copying it. Keep structural design with optional FEATURE_ARCHITECTURE/FEATURE_DECOMPOSITION, exact behavioral contracts with FEATURE-SPEC, delivery with FEATURE-PLAN, physical placement with the applicable layout owner and executable work with FEATURE-TASKS. A precise consequential requirement may belong in the brief without duplicating all its downstream contracts.

Use [exploration](exploration.md) for uncertainty that could materially change scope or compatibility. Clarification answers establish only their actual decisions; silence, a proposed default or a broad implementation request is not document acceptance. Explicitly delegated choices may be resolved within that authority and recorded with their rationale in FEATURE_PREPARATION. Resolve material choices needed for the next stage; deliberately deferred details retain their owner/dependency. No mandatory extra exploration approval or separate brief-QC report is introduced.

## Prepare, review and hand off

1. Have sdd-manage establish the selected feature package, authorized design-docs branch and source ownership. Preserve another active package and unrelated work; follow existing pre-write and Git gates.
2. Draft/revise FEATURE with the coordinator's FEATURE_PREPARATION update and FDOCS-002 evidence; FDOCS-001 already establishes the control/task records. Check seed coverage, changed-versus-retained behavior, scope/constraints, decision basis and content boundaries. Record the concise assessment/current source identity in the companion rather than inventing another report file.
3. Publish/read back the reviewable state under the existing Git authority. Present its substantive scope, consequences, material choices/open questions and recommendation; apply [human document review](../../sdd-manage/references/human-document-review.md).
4. Hold dependent feature design/specification until the brief is accepted or the selected mode/explicit scoped preapproval covers that checkpoint, with technical readiness satisfied. Record actual acceptance, revision requests or scoped preapproval against exact presented document identities in FEATURE_PREPARATION. The companion itself has no independent approval checkpoint. Acceptance does not authorize implementation or widen the selected range.
5. Pass the accepted brief, applicable main context, material decisions/delegation and deliberately deferred questions to the next necessary design/specification owner. Reuse sufficient main architecture/decomposition/layout; do not create overlays simply to fill a sequence. A brief-only request stops at its review/result.

For a read-only review, report located issues and readiness without repairs. For resumed preparation and narrow later-stage calls, follow [continuation](../../sdd-manage/references/feature-preparation.md#pass-completion-reset-and-recovery): reuse accepted documents/decisions and preserve actual pending checkpoints without restarting completed preparation. Accepted scope incorporation and archive belong to **sdd-integrate-feature**, not this authoring procedure.
