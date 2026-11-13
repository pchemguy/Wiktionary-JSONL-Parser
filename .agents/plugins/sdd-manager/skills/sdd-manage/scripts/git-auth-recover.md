# Supervised HTTPS Git publication

Use [git-publish.mjs](git-publish.mjs) from the first authorized HTTPS publication attempt under [Git workflows](../references/git-workflows.md#monitor-pending-git-operations) and [hosting credentials](../references/credentials.md). It validates one destination/ref, selects credentials deterministically, supervises the entire operation and verifies exact remote state. It does not choose authority, release readiness or repository policy.

## Runtime and interface

Require Node.js 22+, Python 3.11+ and native Git on PATH. Supported execution hosts are Windows 10+ and Linux with the child-subreaper and procfs facilities described below. The supervisor uses Python's standard library; no PowerShell, GNU timeout, npm package, libsecret or persistent credential manager is needed. Report a missing runtime/facility before transport; do not substitute an unbounded raw push or install software automatically.

Keep [git-process-supervisor.py](git-process-supervisor.py), [git-auth-recover.mjs](git-auth-recover.mjs) and [protected-token.mjs](protected-token.mjs) beside the canonical entry. These are implementation modules of one publication utility. The old git-auth-recover.mjs CLI delegates to the same supervisor and retains token mode as its default. Its exported synchronous `recover` API retains per-child limits for controlled callers; it is not the supervised workflow entry.

Illustrative invocation, with every placeholder replaced from the established operation, works in Windows CMD and Linux shells:

```text
node "PLUGIN_ROOT/skills/sdd-manage/scripts/git-publish.mjs" push --repo "REPOSITORY_ROOT" --remote "REMOTE_NAME" --url "https://host.example/owner/project.git" --ref "refs/heads/BRANCH_NAME" --expect "FULL_OBJECT_ID"
```

| Argument | Contract |
| --- | --- |
| `push` / `readback` | At most one non-forced explicit ref push followed by readback, or readback alone. No arbitrary command tail. |
| `--repo` | Explicit existing non-bare worktree root. |
| `--remote` / `--url` | Established named remote and its exact single effective canonical HTTPS push URL. No userinfo, query, fragment, redirects, ambiguous push URLs, foreign-VCS helpers, unexpected rewrites or implicit SSH conversion. |
| `--ref` / `--expect` | Full heads/tags ref and lowercase full 40/64-character object ID. Push requires that local ref to equal it; readback requires the object locally and may reconcile an older object. Annotated tags compare the tag object, not its peeled target. |
| `--auth` | `auto` (canonical default), `token`, or `existing`. Token mode is the compatibility entry's default. |
| `--token-file` | Root-relative ignored/untracked ordinary token file; default gh.tkn. Explicit selection implies token mode unless an explicit compatible auth mode is provided. |
| `--credential-repo` | Optional exact worktree root sharing the destination worktree's actual Git common directory. The token remains in this source worktree; no copying/search of unrelated repositories. Explicit selection implies token intent. |
| `--timeout-ms` | Whole-operation deadline, default 60000; integer 1000–600000 ms. Startup, validation, workers, transport, cleanup and readback share this budget. |
| `--python` | Optional Python executable path, default `python`; directly executed without a shell. |
| `--progress` | Optional sanitized stage/auth-mode JSON lines on stderr. Final stdout remains one result. |

No force/deletion/multi-ref, follow-tags expansion or submodule push occurs. Existing hooks still apply and run inside the owned process tree. Readback uses the verified push URL. Credential path matching follows Git's leading-slash removal, single URL decoding and trailing-slash trimming; embedded/encoded leading slashes remain significant.

## Credential selection and protection

In auto mode an already supplied conventional token, when present and eligible, bypasses inherited credential helpers on the first attempt. When absent, use existing noninteractive authentication for the single supervised attempt. A present malformed, tracked, unignored, symlinked, external or unreadable token is an input failure, not permission to try another account. Explicit token mode requires the selected file. Explicit existing mode does not inspect token files and cannot be combined with token-source options. The selected route is pinned for readback; eligibility is rechecked, and loss of eligibility retains unknown remote state.

The existing hosting-token/preparation write gates still apply. No ignore rule, file, helper setting or credential store is written by this utility. Ordinary OS read access suffices; no ownership/ACL inspection or repair occurs. The protected file accepts one terminal LF/CRLF, rejecting empty/oversized content, controls and whitespace. Credential values never cross the controller protocol, argv, URLs, environment or public output.

Token mode resets inherited global and URL-scoped helpers/extra headers for this invocation and supplies x-access-token/token only to the exact HTTPS host/repository credential request. Store/erase are no-ops. The helper rereads the validated file, retaining normal TLS/proxy settings and disabling credential trace/redirect channels. Never invoke private `--credential-helper` mode in a terminal: stdout is a secret-bearing Git protocol channel.

Public calls reject ambient Git relocation and command-configuration variables. The private helper separately accepts Git's own GIT_DIR only after matching the selected worktree's actual administration directory; inherited command-configuration channels are removed before local validation. A linked credential-source worktree must share the actual common Git directory. Neither boundary changes process.env or persistent Git config.

## Deadline and process ownership

The responsive Node controller launches one Python supervisor per network operation. Blocking Git/helper/preflight calls occur only in a private worker. Push and readback have distinct owned trees: cleanup must be confirmed before readback starts. One quarter of the total budget, capped at 15000 ms, is reserved for readback; each attempt includes at most 3000 ms of cleanup. Internal Git child limits remain an additional bound, not the source of lifecycle guarantees. No new stage or retry renews the controller's monotonic deadline.

Windows starts the worker suspended, assigns it to a non-breakaway, kill-on-close Job Object and then resumes it. Termination checks the job's active process count, covering descendants after parent exit. If assignment fails, the suspended process is terminated and checked; transport cannot start without ownership. Linux starts a new session/process group and makes the supervisor a child subreaper. Cleanup kills the group, verifies and terminates adopted children, and reaps them. Where task/children is unavailable, bounded procfs enumeration checks parent identity; it never selects processes by image name. PID namespace translation preserves the kernel-confirmed parent relationship. Unrelated processes are not eligible for termination.

Worker exit and pipe closure are distinct. The controller does not wait forever on inherited output descriptors; private output is capped at 1 MiB. Cancellation signals request owned cleanup. Controller pipe EOF also asks the backend to stop. On Windows an externally forced controller termination cannot emit a final JSON result, although the backend still receives EOF; callers must retain uncertainty and read back after confirming disposition. No software can promise cleanup when the OS denies termination or the owner/backend is forcibly destroyed. Cleanup uncertainty is a finite explicit blocker, never successful publication or permission to overlap another write. Privileged process escape through an external broker/service is outside this ordinary descendant model.

This entry supervises HTTPS push/readback only. It cannot cancel an earlier separately launched command, and it is not a wrapper for clone, fetch, SSH, forge HTTP APIs or browser login. Those operations require their own supported finite runner/ownership controls before launch. Do not imply that running this utility afterward supervised them.

## Results and recovery

Each normal invocation emits one JSON object with schema_version 1. `--help` prints usage. Results include code/stage, auth_mode, elapsed_ms, timeout_ms, cleanup_state, remote_state, push_attempted, next_action and independent push_result/readback_result. Completed readback includes expected/observed/ref. No raw exception, Git stderr, helper output or argument is returned.

| Exit | Meaning |
| --- | --- |
| `0` | Confirmed cleanup and matching exact remote ref: remote_verified or verified_after_push_error. A matching ref does not establish which attempt wrote it, API permissions or whole-workflow completion. |
| `1` | Local scope/input/runtime/credential failure before the requested network operation. supervisor_unavailable/supervision_unavailable identifies a missing executable or ownership facility. |
| `2` | Completed readback finds absent/different state, or readback fails and state remains unknown. local_error retains a safe preflight category when readback validation could not proceed after a push. |
| `3` | Timeout, cancellation, worker/protocol failure, output limit or cleanup uncertainty. No success is inferred merely from a previous matching observation. |

Process summaries retain code, exit_status and signal; not_attempted is explicit. Categories include succeeded, git_failed, process_timeout, process_unavailable, process_output_limit, process_signal and worker_failed. Readback content validation can report invalid_readback/ambiguous_readback. Generic git_failed does not establish invalid credentials or denied permission: reproduce the local helper failure or inspect a protected diagnostic channel before choosing a remedy.

The private helper emits only `SDD_GIT_AUTH_HELPER ` plus allowlisted code/stage JSON on stderr when it fails. Public extraction rejects unknown, malformed, extra-field or conflicting reports. This is an advisory hint, because provider/Git stderr can imitate it; it is not authenticated permission evidence. For example, remote absence plus helper_error token_not_ignored points to local input eligibility, not provider denial.

After an uncertain write, the original owned tree must be settled before bounded exact-ref readback. Matching can verify publication after a failed push; absent/different/unknown state needs reconciliation. The utility never retries a push. Follow the coordinator's bounded recovery policy, diagnose unchanged deterministic failures locally, and do not replace a valid token merely because a helper failed to transfer it. cleanup_unconfirmed requires resolving ownership before another attempt.

## Verification and maintenance

Source-only contracts use synthetic credentials, isolated repositories, actual spawned trees and local HTTPS with Git's git-http-backend. The explicitly public localhost test certificate/key is excluded from the package. Run from the SDD Manager Git root:

```text
node --test tests/git-auth-recover.test.mjs tests/git-publish.test.mjs
```

The CI matrix runs native Windows CMD/Linux with Node 22/24 and Python 3.11. Tests cover token-first selector bypass, existing auth, stalls, orphaned pipe holders, excess output, cancellation, linked credential roots, eligibility changes and lost-response reconciliation. Prepared jobs do not establish observed Windows behavior; consult actual candidate-specific results. Native local transport does not prove installed-agent/Antigravity integration or live-provider authorization.

Imports have no effects. Preserve the fixed private protocol, token/context checks, total deadline, no-store behavior and one-push limit. Keep unrelated scripting candidates outside this cohesive utility.
