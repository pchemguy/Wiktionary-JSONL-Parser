# Review and revision campaign records

Apply this convention when naming, organizing, or referencing review and revision artifacts. **sdd-manage** owns the workflow; **sdd-report** owns artifact formats. Respect an established project convention when it specifies equivalent organization.

## Campaign identity and storage

Use `docs/dev/reviews/<sequence>_<baseline-sha>-<slug>/` for a general review/remediation lifecycle. Phase-checkpoint steering instead uses `docs/dev/reports/phases/<phase-id>/revisions/<sequence>_<baseline-sha>-<slug>/`. Apply [backend object lifecycle](backend-object-lifecycle.md) for milestone/phase/feature implementation report placement. For example, `003_39374c8` identifies the third repository campaign and its starting Git baseline.

- **Sequence:** Allocate one greater than the highest allocated/reserved repository-wide positive campaign number, padded to at least three digits. Use the shared [workflow identity](workflow-identity.md) allocation across reviews, features and phase-nested revisions. Inspect both collections and relevant remote state; resolve concurrent collisions before publication. Do not renumber established campaigns.
- **Baseline:** Use the campaign's starting commit, with at least seven hexadecimal characters and enough characters to resolve it uniquely. Record the full SHA inside each artifact. Keep the directory name stable as review/report/revision commits advance HEAD.
- **Start:** Create the directory when writing the first artifact, not only after completion. A focused review can begin directly from a prompt; missing optional stages need no placeholder files.
- **Files:** Use `REVIEW-PLAN.md`, `REVIEW-REPORT.md`, `REVISION-PLAN.md`, and `REVISION-REPORT.md`. Keep one current artifact per stage; Git retains its edit history. Do not repeat sequence or commit suffixes in filenames.
- **Independent reviews:** Distinguish the campaign starting baseline from the exact source reviewed by each reviewer. When importing a report with no recorded source commit, say **reviewed baseline unknown**; its addition commit does not establish what was reviewed. Additional independently authored reports may use named subdirectories such as `independent/REVIEW-REPORT.md`; retain attribution and avoid overwriting another report.

Steering uses its owning phase's revisions prefix with the same campaign/branch identity but may retain only a concise revision report; do not invent absent review/plan stages. Full campaigns and lightweight amendments share stable identity, not mandatory artifact counts.

## Stable references

Apply the [closed-record boundary](#closed-campaign-records) before maintaining a finding or reference. Stable IDs do not make a closed record a current maintenance target.

Use local finding IDs such as `R-001` and external references such as `003_39374c8/R-001`. Allocate IDs once, never reuse them, and retain IDs when a finding is deferred, superseded, or resolved. Criterion, unit, and scenario IDs may similarly identify coverage and evidence within the campaign.

For existing records, preserve their established IDs rather than renumbering evidence. Qualify a legacy ID with its campaign when necessary. Keep each finding's canonical record in the review report; link revision actions and verification back to it rather than creating conflicting copies.

## Authority and retention

Campaign review/revision plans and reports are authored and committed on the campaign revision branch. Project preparation documents and their QC reports follow design-docs ownership under [workflow identity](workflow-identity.md); campaign artifacts do not. Final verified campaign integration may carry retained records into its established target, but do not merge campaign planning into default as a prerequisite for starting the revision.

Campaign records hold scope, analysis, findings, accepted repair plans, and observed evidence. They remain after accepted changes are incorporated into PROJECT, design, SPEC, PLAN, layout, or task lists. Those governing documents describe the accepted resulting project; they do not become chronological review logs.

A review finding is not an accepted requirement or permission to mutate. Record acceptance, deferral, and scope explicitly. Keep the reviewed baseline evidence separate from current source and revision results. A reviewed unit means coverage was assessed, not that every finding is corrected. A planned check is not an observed result, and a revised finding becomes verified only after its stated recheck supports that disposition.

The directory suffix describes purpose and matches the actual branch; the stable sequence/baseline identity qualifies findings independently of that suffix. Discover both established unsuffixed and new descriptive paths under [workflow identity](workflow-identity.md#discover-descriptive-and-established-packages), without renaming retained campaigns.

## Closed campaign records

A closed campaign has finished its accepted scope and required final persistence/integration/publication, with completion or closure established by the existing request, results and Git state. A paused or incomplete campaign remains active; a directory name, checkbox or archive marker alone does not establish closure. Resolve uncertain ownership/status before editing potentially closed records, using existing evidence rather than a new registry.

Except for [authorized reopening](#authorized-reopening), after closure retain the campaign's review/revision plans and reports, imported assessments, evidence, feature design/SPEC/PLAN/layout/TASKS sources, associated QC reports and package navigation unchanged. Do not edit, append, repair links, rewrite status, rename, move or delete them in a later campaign. Finish that campaign's eligible archive/navigation/report work before its closure. Archived sources in a still-active campaign may need authorized finalization; closed package contents are frozen.

These records describe their own campaign context. They need not remain valid after subsequent changes and are not current governing documents. Later changes create no duty to validate or report historical compatibility, repair old links or claims, or create errata/supersession findings. Maintain current implementation, canonical documents and active campaign records within scope; leave closed records alone.

Do not load prior campaign documents during routine orientation, planning, implementation or verification. Read only the relevant records/sections when the current task establishes a specific historical question. Identity allocation and protected-path discovery use names/paths without reading their contents. Targeted consultation creates no maintenance duty. Exclude closed records from current-document validation and report only the actual current/active check scope.

Before staging and integration, inspect the full campaign diff for incidental changes to prior closed review, feature and nested steering packages, including evidence. Remove those changes from the proposed result; do not replace them with historical-compatibility reporting. Later corrective work changes current owners in its new campaign, leaving the closed package frozen.

## Authorized reopening

The human may explicitly reopen the eligible last closed revision campaign for a related amendment under **sdd-manage**’s [reopened campaign amendment](../../sdd-manage/references/revision-modes.md#reopened-campaign-amendment). Establish its latest first-parent merge, target, actual closure/publication and accepted scope before editing. Only that selected campaign becomes active/editable; all other closed records retain the frozen boundary.

Retain original identity, starting baseline, paths and historical observations/decisions/checks/closure facts. Record the reopening checkpoint and accepted delta; extend plans/actions and append actual rechecks/results/current disposition without pretending the earlier verification assessed the amended candidate. Reclose after required verification/integration/publication. A proactive suggestion alone does not reopen records, and later source changes still create no historical-compatibility maintenance obligation.
