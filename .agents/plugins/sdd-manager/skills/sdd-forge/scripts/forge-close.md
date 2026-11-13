# GitHub completion utility

Use `forge-close.mjs` through **sdd-forge** after its [GitHub backend](../references/github.md) and selected [issue](../references/github-issue-lifecycle.md) or [milestone](../references/github-milestone-lifecycle.md) lifecycle establish eligibility. It performs exact completion mechanics; it does not decide whether work, review, publication or a human checkpoint is complete.

## Runtime and effects

Requires Node.js 22+, native Git and the bundled [protected-token.mjs](../../sdd-manage/scripts/protected-token.mjs), [github-client.mjs](github-client.mjs) and [forge-runtime.mjs](forge-runtime.mjs). Keep these support modules with the executable. The token file needs ordinary OS read access on Windows and Linux. No PowerShell, keyring, npm package, configuration repair or installation is involved. Missing facilities block this mechanism.

The CLI reads an explicit request and an eligible ignored/untracked root-relative token, sends authenticated HTTPS requests only to api.github.com for the selected repository and can add one managed evidence comment and close one issue or milestone. It neither creates issues/milestones nor changes titles, associations, other comments, Git refs/configuration or credential stores. Imports/help read no credential and invoke no Git/network operation.

Supported scope is completed implementation task issues and delivery/phase-review milestones. DOCS preparation, retirement, reopening, PR completion, other providers, unexpected membership or other managed-body layouts use the existing backend procedures. Do not adapt those cases by falsifying the handoff.

## Invocation

The following is an abstract invocation template; substitute actual established paths and scope. One quoted command works in Windows CMD and POSIX shells:

```text
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-close.mjs" task --repo "<WORKTREE_ROOT>" --remote origin --request "<REQUEST_FILE>"
```

| Argument | Contract |
| --- | --- |
| task or milestone | Exactly one completed-closure operation. |
| --repo PATH | Exact eligible Git worktree root; no implicit current-directory root. |
| --remote NAME | Selected configured remote. Its sole effective push URL must normalize to the request repository. Existing GitHub HTTPS/SSH forms are supported without changing transport. |
| --request FILE | Explicit UTF-8 JSON file, at most 1 MiB; optional UTF-8 BOM accepted, UTF-16/invalid Unicode rejected. Relative paths resolve from the launch directory. |
| --token-file PATH | Optional root-relative credential path, default gh.tkn; existing root/file/ignore/untracked eligibility is required. No token value in arguments. |
| --timeout-ms N | Overall elapsed execution budget, default 60000, range 1000–300000 ms. |
| --request-timeout-ms N | Individual header/body budget, default 15000, range 100–60000 ms, capped by remaining overall time. |
| --reconcile-only | Inspect/reconcile remotely without POST/PATCH. It still uses a local operation lock. Missing effects return pending. |
| --help or -h | Standalone harmless usage; no other options. |

Unknown, duplicated or missing arguments fail. The normal CLI emits one JSON object to stdout and no raw provider body or credential diagnostic. Help emits usage text. Local filesystem calls operate on trusted explicit regular inputs; the elapsed budget bounds supported process/network waits, not an OS-level hard real-time guarantee for arbitrary filesystem failure.

Request/source readers reject known non-regular files before opening and recheck the descriptor. POSIX opens use nonblocking mode to avoid waiting on a changed FIFO; Windows uses ordinary read-only opens. These checks do not remove the trusted-filesystem requirement or guarantee arbitrary device/network filesystem behavior.

## Caller authority and request schema

The caller first verifies accepted owning tasks/PLAN, requested tracking, tests/documentation, task result/status or review/report commits and their published containment, relevant exits and exclusive execution ownership. The utility does not independently prove those facts by parsing development documents or by trusting GitHub counters. Schema assertions state what the caller has already established; copying true is not authorization or evidence.

All requests have exactly these common fields:

| Field | Meaning |
| --- | --- |
| schema_version | Integer 1. Unknown versions/fields are rejected. |
| repository | Explicit GitHub owner/repository, normalized case-insensitively and matched to the selected remote and API metadata. |
| phase_label | Exact expected phase-label name on every selected task issue. |
| milestone | Object with stable numeric dotted id, positive GitHub number, exact full title beginning sdd-ID-, and exact description string or null. Nonblank descriptions use the same bounded multiline UTF-8 rules as projection (at most 16000 bytes, LF line endings, no reserved managed marker); content is not rewritten. |
| eligibility | Object with tracking, verified, published and exclusive, all true only after actual caller checks. |

Task mode adds exactly one task object:

| Task field | Meaning |
| --- | --- |
| id, issue, title | Stable T-ID with at least three digits, positive GitHub issue number and exact full title beginning [T-ID] followed by a space. |
| commit | Full lowercase 40- or 64-hexadecimal object ID for the verified published result. |
| branch | Its actual literal Git branch; checkout shorthand such as @{-1} is rejected. The CLI also checks native Git branch-name syntax before credential/network access. |
| verification | Nonblank bounded UTF-8 summary, at most 16000 bytes after CRLF-to-LF normalization. LF and CRLF newlines are accepted; exclude secrets and reserved managed-marker text. |
| report | Root-relative POSIX-style report path, or explicit null for a task without a report. No absolute/traversing path. The utility displays this association; the caller verifies the published report. |

This complete abstract example illustrates the shape only. Its identifiers, commit, target and positive eligibility claims are synthetic and must not be used as operational inputs:

```json
{
  "schema_version": 1,
  "repository": "example-owner/example-project",
  "phase_label": "sdd-phase-1-Delivery",
  "milestone": {
    "id": "1.1",
    "number": 7,
    "title": "sdd-1.1-Outcome",
    "description": "Accepted bounded outcome."
  },
  "eligibility": {
    "tracking": true,
    "verified": true,
    "published": true,
    "exclusive": true
  },
  "task": {
    "id": "T-001",
    "issue": 10,
    "title": "[T-001] Complete bounded work",
    "commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "branch": "phase/1-outcome",
    "verification": "Required acceptance and publication checks passed.",
    "report": null
  }
}
```

Milestone mode omits task and adds exactly these fields:

| Field | Contract |
| --- | --- |
| kind | delivery or phase-review. |
| tasks | Complete nonempty array of task objects with the shape above, at most 1000. IDs/numbers are unique; every issue must already be completed with matching managed evidence. |
| review_task | ID of the included report-bearing boundary task: standalone review, or final implementation task when the milestone review task is omitted. |
| report | Nonempty path equal to that boundary task's report field; its commit/branch/verification identify the review/report evidence. No extra issue is required for a folded milestone boundary. |
| predecessors | Array of milestone objects with the same shape as milestone, at most 1000 and unique/disjoint from the selected milestone. Empty for delivery; nonempty for phase-review. |

A phase-review request contains exactly one task, the review task, and all required preceding delivery milestones. The caller establishes that the expected set is complete; the utility checks the supplied set against actual hosted objects and states. Retired/not-planned work is not converted into completed work. A scope requiring such disposition uses the existing lifecycle rather than excluding it to make this request pass.

## Identity, evidence and transitions

Lookup exhausts relevant pages across states. It rejects missing/duplicate IDs, conflicting number/title/description/phase/milestone associations, malformed/cyclic/foreign/filter-changing pagination and incomplete reads. Repository metadata permits GitHub's equivalent numeric-repository pagination paths; no arbitrary origin, redirect or header override is accepted.

Each selected issue must have exactly one occurrence of its expected phase label and no other managed phase label. Managed sdd-phase-<positive-integer>- names are recognized case-insensitively; the expected spelling remains exact. Malformed or duplicate phase-label records conflict. Unrelated labels and an explicitly supplied custom phase-label convention are preserved, provided no conflicting managed phase is present. Apply the same check to constituent issues before milestone closure and each fresh issue readback. An observed conflict blocks further writes; earlier confirmed effects remain reported.

The task body must have exactly one managed opening marker identifying the same task as its title, on its first nonblank line, either standalone or on a Markdown heading. An optional matching closing marker must follow it. Quoted, fenced, indented, HTML-wrapped, duplicate and contradictory identity copies do not establish ownership. This conservative generated-prefix contract avoids implementing a general Markdown parser; other valid managed layouts remain with the backend.

Evidence is deterministic Markdown from task/commit/branch/verification/report, beginning with an exact sdd-forge:completion task/commit marker. Complete comment lookup reuses one exact matching record and preserves unrelated comments. Conflicting or duplicate records for that operation block; evidence for other commits remains historical. The active credential's literal occurrence in request content is rejected before any API request. The caller remains responsible for excluding all other secrets/private inappropriate material.

Task mode validates identity immediately before writes, adds missing evidence, closes only as completed and re-reads identity, reason and evidence. A closed not_planned/null/other reason is a conflict, not permission to reopen or change it. A completed issue with existing matching evidence needs no write.

Milestone mode checks the exact expected associated issue set, every completed reason/evidence record, review/report assertion and required closed predecessor milestones. Any unexpected associated issue/PR blocks this mechanism. It closes only the selected milestone, verifies its state/open count and rechecks membership/evidence afterward. An empty milestone or zero open count cannot replace these gates.

## Interruption and exclusive ownership

An atomic directory lock under the Git common directory serializes local invocations, including linked worktrees. It holds only nonce/PID/time ownership metadata, not progress or credentials. Normal cleanup removes only the owned lock. Another invocation never steals it. After termination, establish actual process/operation disposition before scoped removal of a stale lock; PID existence alone is not proof of identity or cleanup.

The caller must also prevent concurrent writers on other machines/clients. Lookup followed by POST is not an atomic exactly-once service. The script cannot promise distributed exactly-once comments.

Mutations are never blindly retried. On an uncertain write, exact readback can prove its effect and allow the next distinct transition. Otherwise the result retains unknown effects and the caller stops replay. Re-run with --reconcile-only to inspect; if the effect remains absent/unknown, do not drop that flag until independent evidence establishes that the old operation is settled and a new write is safe. Existing task/Git/report evidence carries this state; no extra transaction journal is required.

## Bounds, failures and results

Each collection has at most 100 pages and each response at most 8 MiB. Bounds, malformed data and cancellation retain incomplete state. HTTP decoding is strict UTF-8/JSON. Safe GETs have at most three retries with bounded backoff; rate timing takes precedence. An unavailable required delay is returned with retry_at where representable. Dependent mutations are serialized and separated by at least one second inside an invocation; the caller paces bulk invocations too.

Read retries retain sanitized prior failure codes/statuses in the result, capped at eight records plus the total retry count. A successful retry does not erase the failure. Provider 401, access/policy 403, ambiguous private-resource 404, rate limits, validation, service and transport failures are distinguished without echoing provider bodies. Request correlation is retained when valid and available. A replacement token cannot resolve every failure.

Every normal result contains schema_version, ok, code, stage, remote_state and effects. Hosted results also identify repository and the exact object type/number, read_retries and retry_failures. Optional fields include http_status, request_id, attempts, retry_at and a retained lock indicator.

| Result / exit | Interpretation |
| --- | --- |
| ok=true; closed_verified; exit 0 | Selected effects and final state verified. |
| ok=true; already_verified; exit 0 | Existing matching state/evidence verified without unnecessary writes. |
| ok=true; verified_after_error; exit 0 | An uncertain mutation response was resolved by exact readback. Review retained effects/retry facts. |
| ok=false; reconciliation_pending; exit 2 | Read-only inspection found missing transitions; no hosted write was attempted. |
| ok=false; remote_state=unknown; exit 2 | One or more attempted hosted effects remain unknown; stop mutation replay. |
| Other ok=false; exit 1 | Invalid/unavailable/contradictory scope or failed required verification. Preserve known effects and resolve the specific blocker. |

Effects distinguish comment/closure not_attempted, existing, created/changed, observed_after_error, not_applied, not_needed and unknown as applicable. An acknowledged mutation can still need final readback; failure is not rollback. Lock cleanup failure makes the result unsuccessful while retaining the observed hosted effects.

## Module API and evidence

The import-safe exports are ForgeError, parseCli, validateRequest, evidenceComment, GitHubClient, reconcileClosure and run. The lower-level client/core take an explicitly authorized protected credential/transport and caller handoff; they do not replace run's native root/token/lock preflight. Use run for normal scoped execution. Dependency injection in source tests substitutes HTTP/clock boundaries; it is not a CLI option for changing API destinations.

Source tests use synthetic credentials/hosted data plus real local Git/filesystem/token validation and a local stalled-response fixture. Native Windows CMD/Linux CI evaluates those contracts. Such results do not establish installed-agent routing, live-provider permissions, arbitrary OS configurations or actual completion in a user's project. The caller consumes the exact outcome under the existing forge lifecycle and retains its own publication/phase gates.
