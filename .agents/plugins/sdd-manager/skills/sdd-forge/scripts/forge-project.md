# Project GitHub tracking

[forge-project.mjs](forge-project.mjs) is the optional local execution mechanism for [implementation projection](../references/github-projection.md) and [docs-main preparation](../references/github-docs-preparation.md), after the [GitHub backend](../references/github.md) prerequisites. Project is a verb here: the utility projects tracking objects. sdd-manage retains phase/preparation eligibility and execution authority.

For routine docs-main work, use the single-call entry below: it builds a source-bound request in memory from complete [bundled definitions](../../../assets/DOCS_TRACKING_TEMPLATE.json). No draft file or shell chain is required. The [input-authoring workflow](forge-project-input.md) and [draft generator](forge-project-draft.mjs) remain available for explicit JSON; implementation phases require agent-authored briefs/dependencies and a reviewed request. Missing facilities or unsupported layouts use the existing backend without weakening its gates.

## Runtime and invocation

Requires Node 22+, native Git, bundled [projection-input.mjs](projection-input.mjs), [github-client.mjs](github-client.mjs), [forge-runtime.mjs](forge-runtime.mjs), [protected-token.mjs](../../sdd-manage/scripts/protected-token.mjs) and the same package's definition JSON. Invocation is Windows CMD-compatible, and the token file needs ordinary OS read access on Windows and Linux. No PowerShell, npm dependency, keyring, installation or credential/configuration repair is involved.

The following commands are abstract templates, not selected project identities:

~~~text
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-project.mjs" docs-main --repo "<WORKTREE_ROOT>" --check
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-project.mjs" docs-main --repo "<WORKTREE_ROOT>" --apply --confirm-eligibility
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-project.mjs" docs-main --repo "<WORKTREE_ROOT>" --reconcile-only
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-project.mjs" phase --repo "<WORKTREE_ROOT>" --request "<REQUEST_FILE>" --check
~~~

| Argument | Contract |
| --- | --- |
| phase or docs-main | Exactly one scope; a supplied request must match it. phase selects only its source-defined phase; docs-main selects the nine documentation tasks and fixed native `sdd-docs-main` milestone. |
| --repo PATH | Exact eligible native worktree root, not an implicit launch-directory assumption. |
| --remote NAME | Optional configured remote, default origin. Require one effective GitHub push destination; bind a supplied request to it. Existing HTTPS/SSH forms are normalized without changing transport/configuration. |
| --request FILE | Required for phase; optional for docs-main. Bounded UTF-8 JSON, optional UTF-8 BOM. Relative request-file paths resolve from launch directory. Cannot combine with --tasks or --confirm-eligibility. |
| --tasks FILE | Request-free docs-main only: optional repository-root-relative Markdown owner. Defaults to docs/dev/DOCS_TASKS.md; only absence of that implicit default uses the bundled task template. |
| --check | Local source/schema/structure/content preview; reads no credential, makes no API call and acquires no hosted-operation lock. |
| --apply | Create/reuse/verify after complete positive caller eligibility. Request-free docs-main also requires --confirm-eligibility. |
| --confirm-eligibility | Request-free docs-main --apply only: explicitly assert all existing scope-specific eligibility facts after establishing them. This flag does not verify facts or approve future documents. |
| --reconcile-only | Authenticated complete observation without hosted writes; missing objects remain pending. |
| --token-file PATH | Optional root-relative eligible credential path, default gh.tkn. Never a token value. |
| --timeout-ms N | Overall elapsed budget, default 120000, range 1000–300000 ms. |
| --request-timeout-ms N | Header/body budget, default 15000, range 100–60000 ms, capped by remaining overall time. |
| --help or -h | Standalone harmless usage; no other arguments. |

Exactly one execution mode is required. Reject unknown/duplicate/missing arguments. Help/imports have no credential/Git/network effects. The normal CLI emits one JSON object to stdout; it writes no required projection map or session file. The caller may retain an exact result with existing evidence. Local regular inputs/filesystem are trusted; elapsed budgets bound supported process/network waits rather than promising hard real-time behavior for arbitrary OS filesystem failure.

Request/source readers reject known non-regular files before opening and recheck the descriptor. POSIX opens use nonblocking mode to avoid waiting on a changed FIFO; Windows uses ordinary read-only opens. These checks do not remove the trusted-filesystem requirement or guarantee arbitrary device/network filesystem behavior.

## Main preparation defaults and explicit inputs

With docs-main and no --request, select --tasks when supplied; otherwise read docs/dev/DOCS_TASKS.md relative to --repo, preserving the document created from the package template and its checked progress. If that implicit default does not exist, read the running package's DOCS_TASKS_TEMPLATE.md for initial pre-write preparation. Do not create or copy a target document. An explicitly missing path, malformed existing document, directory, dangling link or unreadable source fails; these conditions do not trigger a template fallback. Hosted modes still require a repository source to match committed HEAD text. The coordinator owns separate DOCS_PREPARATION control/evidence; it is not a CLI input or a prerequisite for bootstrap projection. Older fixed-content conflicts require the backend's [explicit adoption reconciliation](../references/github-docs-preparation.md#fixed-content-updates-on-adoption), not silent payload edits or repeated apply calls.

The same source selection and origin default apply to forge-project-draft.mjs. An alternate --remote is honored; a missing origin does not cause remote guessing. --tasks paths resolve from --repo regardless of the shell's working directory. --request continues to bind its own source and repository, and cannot be overridden with --tasks. Phase projection always requires its reviewed JSON; structural drafting cannot supply semantic dependencies or briefs.

Run --check to review outgoing content without credentials or API access. Before request-free --apply, establish every fact in the [eligibility table](forge-project-input.md#eligibility-means-actual-scope-specific-facts), then pass --confirm-eligibility to carry those explicit assertions into the in-memory request. Omission fails before provider access. With --request, the existing eligibility booleans remain authoritative caller assertions and the confirmation flag is rejected. Preview and read-only reconciliation need no positive eligibility assertions; reconciliation reports missing objects as pending and creates nothing. Return only the existing JSON result; no temporary request or projection-map file is required.

## Preconditions and effects

The caller establishes actual authorization, tracking confirmation, current source/QC/acceptance, required baseline publication, selected phase/preparation eligibility, cross-list identity/dependencies, exclusive remote execution and reviewed outgoing content. Scope-specific meanings are in the input guide. Positive JSON flags and --confirm-eligibility are assertions, not independent evidence.

Native preflight binds root/remote/source identity before credentials. --apply/reconcile-only use the already eligible ignored/untracked contained token under the existing Windows/POSIX policy. No token discovery/store/configuration change occurs. The source is rechecked after hosted effects; drift blocks success while retaining known effects.

The GitHub-only transport binds repository metadata/numeric identity and reports explicit public/private/internal visibility when supplied. A Boolean-only response falls back to public/private only when visibility is absent; malformed explicit values and contradictory public/private metadata block execution. Recheck resolved visibility and repository identity at final readback, including private/internal changes with an unchanged Boolean. This observation does not prevent concurrent external changes or establish authorization to disclose content. It rejects redirects, arbitrary origins/headers and routes outside the selected capability. Completion clients cannot acquire projection permissions through a caller option; projection clients cannot close, reopen, PATCH, DELETE or post comments.

Projection may create one phase label, selected native milestones and selected task issues, or `sdd-docs-main` plus its nine predefined issues. The preparation milestone uses its exact JSON title and plain-text description without an HTML marker; the request/CLI key remains `docs-main`. Standard docs requests must retain all predefined fields. It reuses exact existing objects and preserves states, unrelated labels/comments/assignees and user material after an exact generated issue section. It does not repair/rename existing fields or rewrite edited generated briefs. Differences, contradictory/unmarked identity, duplicate stable candidates and unsupported ownership return a conflict to the backend's existing authorized reconciliation. Same-scope unprefixed titles or description markers block duplicate creation.

Complete preflight discovers all selected objects before the first mutation. Recheck each absent identity before creating it; confirm complete lookup after POST and fresh complete final readback. Validate exact label metadata, milestone title/description, generated issue title/body and parent associations, plus pinned numeric identities. Issue labels must be well-formed, with exactly one expected phase association (none for docs-main). Detect managed phase-label names case-insensitively while requiring exact expected spelling; duplicate or foreign managed phase labels conflict. Preserve unrelated labels. PRs never become task candidates. Pre-existing unrelated objects remain untouched; selected projection does not certify another list's work or whole-parent completion.

Closed states are reported and preserved. An existing closed issue/milestone does not prove a local completion claim or eligible execution; the caller still reconciles those facts under its lifecycle. Success means **projection_verified**, not phase activation, product acceptance or permission to execute tasks.

## Bounds, failures and recovery

Shared transport exhausts constrained pagination with at most 100 pages per collection and 8 MiB per response. It validates UTF-8/JSON, duplicate objects, next-link route/filters and repository identity. Incomplete lookup is not absence. Safe GETs have at most three retries; provider timing takes precedence, and unavailable delay returns deferred/error metadata. Read retry history remains visible.

Serialize writes with at least one second between mutations. A large scope may consume the overall budget before completion; retain its partial result and reconcile the same input, without removing required tasks or shortening provider waits. No creation POST is blindly retried.

After a timeout/disconnect/uncertain create, perform lookup only. A unique exact object can establish the observed effect and allow the next distinct transition. If absent/conflicted/unavailable, retain unknown and stop. Use --reconcile-only until independent evidence establishes the previous operation is settled and another write is safe. A missing read result alone is not proof that a prior create failed.

If source drift prevents that invocation, use the backend's exact readback with retained object identities/input evidence. Do not falsify a hash or drop expected objects to make recovery pass. A later local source error retains any unknown hosted effect and its exit-2 recovery boundary.

The shared Git-common-directory lock serializes local completion/projection operations, including linked worktrees. Main preparation explicitly permits this [transient coordination effect](../../sdd-manage/references/main-preparation.md#transient-projection-lock) before projection readback; all other target-repository writes remain gated. Cleanup removes only the owned nonce. Do not steal a stale lock; establish actual process/operation disposition before scoped removal. The caller prevents competing writers on other machines/clients; no distributed exactly-once guarantee is made.

Errors classify authentication, access/policy, ambiguous missing/private resource, rate, validation, service and transport outcomes without raw provider bodies or credentials. Inspect safe status/correlation/retry timing and effects. A replacement token cannot resolve every failure. A failed final readback or source check does not roll back already applied objects.

## Results and module API

Normal results contain schema_version, ok, code, stage and remote_state. Hosted results include repository, visibility, effects, associations, read_retries and retry_failures. visibility identifies the initial validated metadata observation (or not_checked before it); final drift returns repository_identity_or_visibility_changed rather than successful projection. The manager/caller still reviews outgoing content for the actual audience. Native run adds request_sha256, a fingerprint of normalized validated JSON. Optional safe fields include http_status, request_id, attempts, retry_at and a retained-lock indicator.

| Result / exit | Meaning |
| --- | --- |
| input_verified; exit 0 | Local input/source validated; payloads show authored content and stable association references. Remote state/visibility are not_checked. |
| projection_verified; exit 0 | Current selected identities/content/associations verified through final complete readback. |
| projection_pending; exit 2 | Read-only reconciliation found missing objects; no hosted write occurred. |
| remote_state=unknown; exit 2 | An attempted creation remains unresolved; stop mutation replay. |
| Other ok=false; exit 1 | Invalid, unavailable, conflicting or failed required verification; preserve effects and resolve the stated blocker. |

Each effect identifies type/key, observed id/name/number/state where available, status and verified. Status is created, reused, observed_after_error, missing, not_applied or unknown. Recovered uncertain effects retain interrupted_by and available safe status/correlation. verified records an observation, not an atomic snapshot or product acceptance. Associations identify task ID, issue/milestone numbers, observed state/reason and constructed GitHub issue URL. Normal hosted results omit full private task briefs; --check deliberately exposes reviewed payload content locally.

Exports are ForgeError, parseCli, reconcileProjection and run. The lower-level core requires a parsed source inventory and explicitly authorized projection transport; it does not replace run's real root/source/token/lock checks. Programmatic run accepts parseCli fields, including request-free docs-main with optional tasks/remote and explicit confirmEligibility for apply, and optional controlled fetchImpl; local pre-lock errors may throw. The CLI always converts failures to safe JSON/exit status. Shared dependencies remain bundled.

Source tests use synthetic credentials/provider objects plus real local Git/filesystem/token/CRLF/path/locking checks. Native Windows CMD/Linux Node 22/24 CI covers these contracts. These results do not establish live provider permissions, installed-agent routing, arbitrary OS configurations or actual project completion.
