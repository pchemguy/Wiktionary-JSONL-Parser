# GitHub backend

## Operations and sources

Load only the additional reference needed for the request:

| Request | Load |
| --- | --- |
| Assess a ZIP or develop release package contents/names interactively | [package preparation](github-packaging.md) |
| Prepare, extend or dispatch/monitor a release workflow | [release workflows](github-release-workflows.md) |
| Create/finish a release, upload assets or recover/read back publication | [release lifecycle](github-releases.md) |
| Create/read back main preparation `sdd-docs-main` and nine DOCS issues, close preparation issues/milestone | [Main preparation tracking](github-docs-preparation.md) |
| Create/read back campaign-specific feature preparation milestone/nine FDOCS issues, resolve FDOCS lookup and complete/reset preparation | [Feature preparation tracking](github-feature-preparation.md) |
| Create or reconcile phase labels, GitHub milestones, or task issues | [TASKS projection](github-projection.md) |
| Close/reopen a milestone, assess milestone closure backlog or confirm hosted phase gates | [milestone lifecycle](github-milestone-lifecycle.md) |
| Resolve task IDs to issue numbers for a commit or handoff, check issue status, or close verified issues | [issue lifecycle](github-issue-lifecycle.md) |

For main documentation preparation, [main preparation tracking](github-docs-preparation.md) consumes bundled JSON milestone/issue definitions alongside the DOCS task template before repository writes, then target `docs/dev/DOCS_TASKS.md`; do not require product PLAN/TASKS or phase activation for that operation. It has distinct first-approval and merge-before-milestone closure semantics.

For implementation task tracking, `docs/dev/TASKS.md` supplies complete-project task IDs and progress; an active `docs/dev/FEATURE-TASKS.md` supplies its feature's scoped IDs and progress until reconciliation. Task IDs remain unique across both lists. PLAN or active FEATURE-PLAN supplies phase and milestone outcomes and exit conditions. SPEC and applicable design or feature documents supply requirements when a task brief needs them. GitHub is a projection, not the authority for task scope or verified completion. Resolve a task in its owning list; a feature task later incorporated into TASKS retains its original issue. Use **sdd-report** to compose issue drafts if available; if unavailable, use the baseline format in the projection reference. Neither dependency is required for a read-only lookup.

Package and release operations use their accepted source/build/release inputs; they do not require TASKS or tracking activation. Repository file edits are coordinated through sdd-manage and normal Git persistence; provider release/dispatch writes remain backend-owned.

## Repository and access

Determine the intended GitHub repository from the invoking workflow's explicit target or its relevant remote. Normalize SSH and HTTPS remotes to the same `owner/repo` identity. If multiple plausible GitHub repositories exist, require an explicit selection before writing. Do not use a different fork or upstream merely because a token can access it.

Use the token, whether it originated with **sdd-manage** or was provided directly to **sdd-forge**, or use an approved authenticated GitHub client. Apply **sdd-conventions**' **Hosting tokens** rules: the ignored, untracked `gh.tkn` beside the repository root `.gitignore` is the permitted local credential file. Keep the token out of all other project files, plugin settings, command arguments, URLs, logs, issue bodies, and reports. Do not assume that a credential usable for `git push` is available to the API client. Check access for the requested endpoint and repository; do not substitute another identity silently. Use the conventional permission profile below when requesting or assessing the repository token. GitHub's current endpoint documentation determines actual endpoint access; token permissions do not authorize unrequested operations.

### GitHub CLI

**When `gh` is available, it may be used for supported GitHub interactions**, through its native subcommands or `gh api`. Select it where it can fulfill the requested operation and this backend's procedure. Other supported authenticated clients remain valid; CLI availability is not a prerequisite.

- Reuse suitable existing `gh` authentication for the intended host/account. Authentication may already be configured; do not require a new login or token merely to use the CLI. Confirm access to the resolved repository and requested operation.
- When a provided or saved token is needed, apply **sdd-manage**'s [credential procedure](../../sdd-manage/references/credentials.md) and supply it to the `gh` child process as `GH_TOKEN` for github.com. This overrides stored credentials for that invocation. Keep the environment scoped to the operation; read the eligible token through protected code, without placing its value in shell command text, arguments, logs or ordinary files. A persistent `gh auth login` is unnecessary for this route.
- Run unattended commands with `GH_PROMPT_DISABLED=1` and a finite process deadline. Scope the host/repository explicitly, using the command's repository option or the exact API endpoint. Preserve complete pagination, owned-field limits, error classification and post-write readback; reconcile uncertain effects before replaying a mutation.

See the official [environment](https://cli.github.com/manual/gh_help_environment), [authentication](https://cli.github.com/manual/gh_auth_login) and [API](https://cli.github.com/manual/gh_api) contracts. HTTPS Git publication retains **sdd-manage**'s [supervised push/readback procedure](../../sdd-manage/references/git-workflows.md#monitor-pending-git-operations).

### Conventional fine-grained token

Request a fine-grained personal access token with **Only select repositories** enabled solely for the target repository and this repository-permission profile:

| Permission | Access |
| --- | --- |
| Commit statuses | Read and write |
| Contents | Read and write |
| Issues | Read and write |
| Pull requests | Read and write |
| Workflows | Read and write |
| Metadata | Read, added automatically |

This is the SDD token convention, not a claim that every endpoint requires the full profile. Workflows write supports authorized workflow-file modification together with the relevant Contents access. The profile does not add PR operations, protected-branch bypass or automatic workflow dispatch, or override account/repository policy. Verify the relevant endpoint and any indicated approval restriction using GitHub's [token management](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) and [fine-grained permissions](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens) documentation.

For HTTPS Git authentication, sdd-manage restores a supported shell credential facility from the local token. For this backend's API operations, use the client's supported protected token channel; do not assume shell recovery authenticates a connector or silently substitute a different account. SSH remotes require their transport's authentication and an explicit decision before any transport change.

### Release and workflow access

| Operation | Access to assess |
| --- | --- |
| Commit/push or API-edit workflow files | Relevant Contents write plus Workflows write; normal repository/Git protections still apply. |
| Create/update releases and upload assets | Contents write; creating a missing tag at a workflow-changing target can additionally require Workflows write under current provider rules. Prefer an explicitly verified existing tag. |
| Dispatch or perform requested run-management writes | Conditional Actions write; Workflows write is not a substitute. |
| Inspect private workflows/runs/artifacts | Conditional Actions read under the relevant endpoint; public read endpoints may permit unauthenticated access. |

Check current [workflow endpoints](https://docs.github.com/en/rest/actions/workflows), [release endpoints](https://docs.github.com/en/rest/releases/releases) and [release asset endpoints](https://docs.github.com/en/rest/releases/assets) for the selected operation. Add Actions access only for the required operation. A workflow job uses its own scoped GITHUB_TOKEN permissions, not the user PAT profile. Updating these instructions does not change an existing PAT; recover only an observed access failure through the manager. Never assume file-edit permission proves dispatch access.

### Access failures and tracking object ownership

For an access-related 403, stop the affected write and identify the repository, endpoint, attempted operation, and permission or other cause indicated by GitHub without exposing the credential. Classify rate limits before credential escalation using the response protocol below. Follow the shared access-failure protocol to obtain a suitable token from **sdd-manage**, or ask the user when invoked directly. Recheck access before retrying; do not assume every 403 is resolved by a different token or retry indefinitely.

Read existing objects before mutation. Scope all lookups to `owner/repo` and include open and closed issues or milestones as appropriate. A GitHub issue may represent a pull request in API results; exclude pull requests from task-issue matching. Treat a task ID as the stable join key and issue numbers as repository-local handles. Resolve by the exact managed ID in the issue title and body marker, validate the match, and stop on duplicates or conflicting ownership. Never silently create a second issue when lookup is ambiguous.

Reconcile only backend-owned fields: stable identity marker, generated issue title and body sections, phase label, milestone association, and state when separately authorized and verified. Preserve unrelated issue labels, comments, assignees, and user-authored material. If a user-edited generated section cannot be safely distinguished, report a conflict rather than overwriting it. Re-run safely after partial creation: lookup each object before creating the next, and report completed work if later operations fail.

The backend is optional and has no built-in token store, remote policy, issue-to-task database, or PR operation. A later PR workflow must respect one PR per source branch.

## Operational failures and uncertain writes

Inspect status, response body, rate-limit headers, and transport outcome before choosing a remedy. Keep tokens and sensitive response data out of reports. Use GitHub's [REST best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api) and [troubleshooting guidance](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api) for current provider rules.

| Evidence | Disposition |
| --- | --- |
| Authentication/permission failure, including a provider-indicated access 403 | Stop the write; use the shared suitable-credential path through **sdd-manage**, or the direct caller. Report policy restrictions requiring another remedy. A private-resource 404 can conceal denied access; do not infer absence or create replacements without resolving identity/access. |
| Rate-limit403 or 429 | Pause requests; honor Retry-After. When remaining quota is zero, wait until the reset time; satisfy both restrictions if both are present. For secondary limits without timing guidance, wait at least one minute and increase delays on repeated failures. Do not request another token merely to evade the limit. |
| Transient 5xx or transport failure | Report the affected endpoint and known outcome; use bounded backoff only when a retry is safe. A timeout, disconnect, or failed response after a write may leave the operation applied. |
| Offline or unavailable client/service | Stop affected hosted work and report synchronization pending. Preserve local verified commits and already confirmed hosted results; do not change credentials or infer remote state from cached evidence. |
| Invalid request, validation failure, conflicting objects, or unknown cause | Stop the affected operation and report actual evidence and needed correction. Do not retry unchanged invalid input or assume every error is transient. |

Use the project's bounded retry policy; otherwise permit at most three retries per operation, with exponential backoff for transient failures and the provider's rate-limit timing taking precedence. Serialize dependent mutations; for bulk writes, pause at least one second between requests. If the required delay exceeds available execution time, return the earliest eligible retry time and pending work rather than retrying early or blocking indefinitely. A successful retry does not erase earlier failures.

After any uncertain write, re-read the affected repository objects before replaying it: search all relevant states with exact task/phase/milestone identity; inspect owned fields, issue state/reason, and existing evidence comments. Reuse a uniquely matching created object, apply only remaining field differences, and avoid duplicating an evidence comment already present. If lookup is incomplete, unavailable, duplicated, or contradictory, retain outcome **unknown** and stop the replay. A search with no reliable result is not proof that the write failed.

Return repository, endpoint, attempted operation, sanitized cause/status, known successful effects, unknown effects, retry count and next eligible time where applicable, and remaining task associations or state differences. On restored access, reconcile the maintained scope including older pending task issues. Hosted failure never erases local completion or establishes successful synchronization.

## Optional local tracking mechanisms

For eligible phase or main-preparation creation/readback, [forge-project](../scripts/forge-project.md) consumes the [source-bound JSON contract](../scripts/forge-project-input.md). Phase drafting extracts structure for agent-authored dependencies/briefs; docs-main drafting copies the complete bundled definitions. The agent reviews outgoing content and the manager establishes actual readiness. Use credential-free --check before authenticated apply, and read-only reconciliation for uncertain creates. Exact-reuse conflicts or unsupported scopes use existing authorized backend procedures. The utility's result verifies projection, not activation or completion.

Use available authenticated clients normally. For completed implementation issue/milestone closure with eligible local token-file/runtime facilities, [forge-close](../scripts/forge-close.md) implements the bounded lookup/evidence/close/readback sequence. Establish the selected issue/milestone lifecycle gates before preparing its versioned handoff; its positive eligibility fields assert the caller's verified facts rather than proving them. Resolve exact repository/root/remote, expected managed objects, report/commit evidence and exclusive operation ownership without discovering a token as routine preflight.

Its generated-prefix and exact-membership contracts are deliberately narrow. DOCS preparation, retirement/reopening, other body layouts or unexpected membership remain with their owning procedures; do not falsify input or drop expected tasks to fit the utility. Keep the existing authorization through recovery. Check JSON ok/exit plus known/unknown effects and retry facts; unresolved writes require read-only reconciliation or independently settled effects before another mutating invocation. Missing facilities or unsupported scope do not waive closure gates or require repeated permission for an already authorized supported alternative.
