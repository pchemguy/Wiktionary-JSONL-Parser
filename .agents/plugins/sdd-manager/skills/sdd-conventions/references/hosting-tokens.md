# Repository hosting tokens

Apply these invariants when storing, locating, or consuming a hosting token for an authorized operation. **sdd-manage** owns credential acceptance, discovery, shell authentication recovery, and protected supply; **sdd-forge**'s active backend owns provider-specific access rules. This convention executes neither authentication nor Git/hosted mutations.

## Files and identity

- **Location:** Keep the conventional token beside the eligible repository's root `.gitignore`; use `gh.tkn` for GitHub or an unambiguous equivalent for another backend.
- **Discovery:** Prefer the active backend's conventional file, then suitable `*.tkn` candidates within that repository. Exclude unrelated repositories and nested Git worktrees. Resolve ambiguous provider/account/repository associations before consumption; file presence proves neither identity nor permission.
- **Exclusion:** Ensure `*.tkn` is in the root `.gitignore`, preserving existing rules. Verify effective exclusion and untracked status before writing or reusing a token; a negating rule can defeat a pattern, and ignore rules do not untrack files. An already tracked token requires explicit remediation, not automatic history rewriting.
- **Persistence:** Save an accepted token only after those checks. Ordinary OS read access is sufficient; do not inspect or change file ownership, permission modes or ACLs as an authentication prerequisite. Preserve unrelated files and staged/unstaged changes. Replace the selected credential only when a suitable replacement is provided for that purpose.
- **Handling:** The ignored token file is the intentional project-local secret exception. Keep values out of tracked files, normal handoffs, reports, fixtures, command arguments, remote URLs, logs, history, and diagnostic output. Read locally and transfer through a supported protected credential channel or process input.

## Authentication and scope

HTTPS Git publication follows **sdd-manage**'s [deterministic supervised selection](../../sdd-manage/references/credentials.md#deterministic-git-publication) from the first attempt: use an already supplied eligible conventional token before inherited helpers, or supervise existing authentication when absent. A present invalid token blocks rather than silently switching accounts. Do not request credentials before every push or alter persistent helper configuration as a ceremony. Repository token files provide continuity; API authentication remains separate.

Prefer fine-grained repository-scoped tokens when supported. The active backend defines the permission profile and supported authentication mechanism. Git transport and API clients have separate authentication; success in one does not prove access in the other. Token scope does not authorize unrequested operations, a different destination, or bypassing repository protections.

Provider classification determines whether a 403 concerns credentials, policy, or rate limits. Reauthentication is bounded and cannot fix every failure; retain valid local commits and report unresolved publication or hosted effects. Use synthetic credentials for tests and separate controlled fixtures from observed live-provider outcomes.
