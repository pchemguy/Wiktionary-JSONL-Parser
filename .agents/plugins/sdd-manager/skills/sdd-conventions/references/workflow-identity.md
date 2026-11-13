# Workflow identity, branches, and artifact locations

Apply these provider-neutral defaults when naming workflow branches or associating them with retained documents. **sdd-manage**'s **Branch management** procedure performs allocation and Git setup; **sdd-integrate-feature** owns incorporation/archive eligibility. This convention grants no mutation or hosting authority.

## Naming

| Workflow | Branch | Associated documents |
| --- | --- | --- |
| Initial project preparation | `design-docs/main` | Project design, SPEC, PLAN/layout, TASKS and adjacent QC reports in `docs/dev/`. |
| Scoped project preparation | `design-docs/<campaign>-<slug>` | Active feature or accepted project-document deltas and their QC reports under established owners. |
| Revision | `revision/<campaign>-<slug>` | `docs/dev/reviews/<campaign>-<slug>/` |
| Steering | `revision/<campaign>-<slug>` | `docs/dev/reports/phases/<phase-id>/revisions/<campaign>-<slug>/`; a minimal revision record is sufficient. |
| Feature | `feature/<campaign>-<slug>` | `docs/dev/features/<campaign>-<slug>/` for package identity/navigation and completed incorporated sources. |
| Main phase | `phase/<phase-number>-<slug>` | Main governing documents and owning TASKS remain in `docs/dev/`. |

A campaign is `<sequence>_<baseline-sha>`, for example `007_df531c2`; new revision/feature/steering directory basenames match the branch suffix `<campaign>-<slug>`. The stable campaign ID is the sequence/baseline prefix, not the descriptive suffix. Use the phase number/name from accepted PLAN/TASKS, not a campaign counter. The main integration branch is established explicitly; a workflow name never selects Git's default branch.

`design-docs/ai-logs` is reserved for the [manual-provenance initialization convention](../../sdd-manage/references/ai-logs.md). It allocates no campaign number and is not ordinary preparation. After its initial scaffold integration, unmerged manual log changes do not establish an unfinished SDD workflow or require branch selection; explicit provenance work and a known interrupted adopted setup retain their actual scope.

Project preparation and implementation are distinct branch stages. Commit newly authored preimplementation project documents on the applicable `design-docs/` branch. Explicitly merge, verify and publish the accepted preparation boundary into the actual repository default branch before creating a dependent implementation branch from its recorded parent containing that checkpoint. New workflow branches integrate into their creation parent; preparation propagation to an active phase follows the gate below. Apply **sdd-manage**'s [preparation integration gate](../../sdd-manage/references/branch-management.md#preparation-integration-gate). Completed main preparation integrates its documentation before `sdd-docs-main` milestone closure and the final preimplementation checkpoint under [main preparation](../../sdd-manage/references/main-preparation.md). Other preparation-only paths stop on their design-docs branch; an implementation request includes the prerequisite preparation merge. Explicit earlier stops remain controlling.

Campaign REVIEW-PLAN, REVIEW-REPORT, REVISION-PLAN and REVISION-REPORT belong on the campaign's `revision/<campaign>-<slug>` branch. Do not send these campaign artifacts through design-docs or merge them into default merely to authorize revision execution. A revision requiring separate project preparation uses design-docs for those project documents; its campaign records retain revision-branch ownership. One campaign identity and directory association spans its participating branches.

## Identity and collisions

- **Allocate once:** Inspect `docs/dev/reviews/`, `docs/dev/features/` and `docs/dev/reports/phases/*/revisions/` plus relevant published records/refs. Use one greater than the highest allocated/reserved repository-wide positive sequence, padded to at least three digits across reviews, features and phase-nested revisions; do not fill historical gaps or reuse an ID. Reserve identity at the first record/branch preparation; resolve concurrent allocation conflicts before publication, without renumbering established records.
- **Pin baseline:** Use the campaign's starting commit, at least seven uniquely resolving hexadecimal characters, and record its full SHA in retained context. Keep branch/directory identity stable as HEAD advances, including review-to-revision continuation.
- **Slug:** Use concise lowercase ASCII words separated by hyphens. Validate the full name with `git check-ref-format --branch`. If occupied by unrelated work, keep identity and choose a distinct descriptive suffix; never reuse a branch from its name alone.
- **Overrides:** Respect explicit project/user naming and location policy; record its equivalent identity/target association. Preserve suitable legacy/in-flight branches and historical directories on continuation; never rename or delete them automatically. An occupied old phase branch needs a verified matching continuation or a distinct slug.
- **Context:** Retain workflow, campaign or phase ID, full baseline, actual creation parent/branch-off commit, working/target branch and destinations, authoritative sources, and scope in existing campaign/task/change evidence and the entry HANDOFF. Preserve explicit exceptions and legacy associations rather than inferring an original branch name from history alone. No separate branch registry is required.

For a human-authorized eligible [reopened campaign amendment](../../sdd-manage/references/revision-modes.md#reopened-campaign-amendment), recover the original campaign identity/branch/directory rather than allocating a new sequence. Its original full baseline stays fixed; record the current reopening/source/target checkpoint separately. A nested revision allocates a new identity and records its actual parent branch/context.

## Artifact lifecycle

Apply the [closed campaign record boundary](review-campaigns.md#closed-campaign-records). Complete archive moves, navigation and historical markers while the owning campaign is active; closure freezes its resulting package. Later naming, link or implementation changes do not reopen its documents or require compatibility review.

Review/revision artifacts use the **Review campaigns** convention. Lightweight steering allocates the same global identity under `docs/dev/reports/phases/<phase-id>/revisions/<campaign>-<slug>/` and can use a concise REVISION-REPORT recording objective, scope, baseline, paused target, verification, and publication, without a fabricated review or plan.

Feature preparation uses active `docs/dev/FEATURE.md` and `docs/dev/FEATURE_PREPARATION.md` under the coordinator's [feature preparation contract](../../sdd-manage/references/feature-preparation.md). FEATURE_PREPARATION records campaign/full baseline, design-docs branch, default preparation target, intended implementation branch and active source paths. Reserve the associated `docs/dev/features/<campaign>-<slug>/` identity for reports/archive; preparation requires no extra package navigation artifact. Active sources remain in docs/dev; isolated branches/worktrees may carry separate packages, but one worktree must not overwrite an unrelated active package. The preparation merge retains the feature delta as an active source; it does not incorporate that delta into complete main documents or complete feature tasks.

After complete accepted feature incorporation and task/evidence disposition, retain eligible feature sources, including FEATURE.md, FEATURE_DOCS_TASKS.md, FEATURE_PREPARATION.md and FEATURE-QC-REPORT.md, under that directory with their basenames. Update links and mark archived sources historical: main documents/TASKS own current state, and archived checkboxes are not executable task owners. Partial incorporation retains still-needed active sources. The feature owner verifies archive eligibility on the feature branch before final integration; naming alone proves neither incorporation nor completion.

## Discover descriptive and established packages

Parse the leading numeric sequence and hexadecimal baseline prefix in both `007_df531c2` and `007_df531c2-piece-controls`; the suffix never allocates a second campaign. Inspect the repository-wide maximum across reviews, features, phase-nested revisions and relevant refs. Two reservations using the same sequence with different slugs or baseline abbreviations require identity/ownership reconciliation before publication, not silent acceptance as separate campaigns. Resolve abbreviated baselines to their recorded full SHA.

New directory basenames include the same complete descriptive slug as their branch, including an approved collision suffix. Keep campaign ID and descriptive association stable as HEAD advances. Record actual directory, branch, full baseline and target in existing navigation/report context. Established unsuffixed packages and explicit overrides remain valid on continuation; do not infer their path by substituting the new default.

Rename an active package only when explicitly selected. Include its affected maintained/active navigation, source paths and evidence references in one coherent scoped update; verify active owners and archive links before publication. Closed packages and their links remain unchanged. Never rename an existing package merely because the default changed. Main phase directories retain phase numbers.
