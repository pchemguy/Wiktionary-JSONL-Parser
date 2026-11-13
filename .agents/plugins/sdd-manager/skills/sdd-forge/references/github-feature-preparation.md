# GitHub feature documentation preparation

Load through the [GitHub backend](github.md) for selected feature preparation tracking. sdd-manage establishes eligibility/mode and actual campaign identity under [feature preparation](../../sdd-manage/references/feature-preparation.md); this backend owns hosted mechanics, not document acceptance or implementation.

## Project and read back

1. Confirm repository, tracking scope, allocated full campaign ID/baseline, current source and pre-write eligibility. Reuse existing authenticated access; keep required external drafts and protected transient credential supply outside the target until projection clears.
2. Reconcile one native milestone named `sdd-docs-<campaign>` for this campaign. Its description states the feature's scoped document preparation, nine FDOCS stages, required whole-package QC and closure only after verified published preparation integration. Do not reuse sdd-docs-main or create a product phase label/Phase 0.
3. Read the nine definitions from the pinned [feature task template](../../../assets/FEATURE_DOCS_TASKS_TEMPLATE.md). Create/reconcile exactly one issue per stage, with stable title prefix `[<campaign>/FDOCS-001]` through `[<campaign>/FDOCS-009]`, the template's actual stage title, scope/acceptance, dependencies and milestone association. Qualify dependency IDs with the campaign. Preserve complete briefs, not title-only placeholders. Include the standard opening/closing `sdd-forge:task-id=FDOCS-001` markers (using the actual stage ID) from [task issue rendering](github-projection.md), plus `<!-- sdd-forge:docs-scope=feature:<campaign> -->` with the exact allocated campaign. The title, task marker, scope marker and selected milestone must agree; title/milestone alone are insufficient identity. Optional/reused inputs still have assessment stages; do not create extra child issues or omit a stage.
4. Read back the milestone, every issue's exact campaign/stage identity and native association before clearing the coordinator's pre-write gate. Discover matching/conflicting objects first, preserve unrelated issues, reconcile uncertain writes before retry and report partial/conflicting/unknown state. Token possession alone selects neither tracking nor acceptance.

## Resolve feature preparation issues

For a direct lookup, closure or reset, identify the selected repository, actual campaign and stage from FEATURE_PREPARATION/FEATURE_DOCS_TASKS or the explicit scoped request. A bare FDOCS ID can recur in another campaign; missing consequential campaign context is an ambiguity to resolve, not permission to choose by recency. Before initial local records exist, use the coordinator's verified allocated identity and pinned template.

Enumerate open and closed issues with complete pagination, excluding pull requests. Match the exact campaign-qualified title prefix, opening/closing task markers, feature-scope marker and native milestone association against the selected source. Return the unique issue number/URL/state and campaign/stage. Missing, duplicate, unmarked or contradictory candidates block the affected operation; do not infer identity from a remembered number, title substring or milestone alone. Reconcile uncertain writes by reading these same identities before retry. Use this preparation evidence for completion/reset, not product TASKS/FEATURE-TASKS or implementation-only completion helpers.

## Complete, reset and close

After each coordinator-owned accepted-document/reuse assessment plus task/evidence commit is published, close/read back only its corresponding issue with exact source and actual acceptance/preapproval/QC basis. A draft, local checkbox, Ready label or preapproval alone is insufficient. Reuse existing issue identities rather than allocating another issue on revisions.

On an authorized pass reset, the local reset commit preserves FDOCS-001 and source files, reopens FDOCS-002–009 checkboxes and records scope/authority. After its publication, reopen/read back those same eight issues and reopen a closed preparation milestone before document work resumes. Keep product T-task issues untouched. Unknown or partially applied reopening blocks dependent preparation; resume missing effects by exact identity without another pass reset.

After FDOCS-009 source/report/evidence/checkoff publication, close/read back that issue.

Before closing the unique campaign preparation milestone, enumerate every associated issue in open and closed states with complete pagination, including pull requests. Validate all nine campaign/stage identities and milestone associations under [feature issue lookup](#resolve-feature-preparation-issues). Require their verified completion closures and the coordinator's exact preparation merge/default-branch publication. Missing, duplicate or contradictory identities and incomplete lookup block closure. Unexpected open foreign issues, associated PRs or ambiguous/conflicting ownership also block closure; preserve them and report the needed disposition rather than closing or detaching unrelated work to clear the gate.

Close/read back the exact milestone only after these gates pass; an already correctly closed milestone needs verification, not another write. After an uncertain closure, re-read its actual state and complete associated membership/evidence before replay. Unavailable or contradictory readback leaves the outcome unknown and dependent completion pending.

Autodoc's FDOCS-008 stop leaves package-QC issue and milestone open. A feature phase completion or a product release cannot substitute for preparation completion. Honor explicit narrower/local-only scope and report pending hosted effects accurately.

Use supported provider APIs/CLI under the parent backend's access/failure rules. Existing local `docs-main` projection/extraction/reset helpers and their fixed JSON are main-only: do not rename feature IDs into DOCS IDs, feed feature records to that mode or claim it supports features. No local feature projection utility is required by this procedure; unsupported tool scope returns to this backend contract rather than bypassing readback.
