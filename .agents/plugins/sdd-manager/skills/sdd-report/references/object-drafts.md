# Issue, commit, and PR drafts

Keep the same task identity across all outputs. Use the ID from its owning TASKS or FEATURE-TASKS entry, or the predefined DOCS/FDOCS ID from its main/feature documentation task list; include a resolved issue reference only when **sdd-forge** supplies a unique repository and number. Match the requested object's time perspective: an issue describes intended work, while a commit or PR describes actual changes and available evidence.

## Task issue

Return `title` and `body` separately. For product T tasks and main DOCS tasks, format the title as `[<task-id>] <task title>`, using the owning task list. For feature preparation, use `[<campaign>/FDOCS-xxx] <stage title>` under forge's [feature issue identity contract](../../sdd-forge/references/github-feature-preparation.md#resolve-feature-preparation-issues). Establish the selected campaign from FEATURE_PREPARATION/FEATURE_DOCS_TASKS or the explicit scoped request; missing campaign context must be resolved before drafting the title, not inferred by recency. Keep the bare FDOCS stage in the task body marker and the exact campaign in its separate feature-scope marker. This hosted qualification does not change the bare stage ID in [task commit subjects](#task-commit-subjects).

Draft the body from the task outcome, reason and project context, expected scope and dependencies, objective acceptance and prescribed checks, and source document links. Add relevant kind-specific details. For example:

- **Performance:** Describe the problem with the current implementation, explain how the proposed approach may improve it, and identify the measurement plan and any established baseline. Do not present an expected speedup as an achieved result.
- **Security:** State the affected guarantee and risk without exposing exploit instructions or credentials.

**sdd-report** owns the title and body format. Preserve an exact task identity marker when one is supplied. Never invent host labels, milestone associations, issue URLs, or resolution state.

For forge's optional [structured projection handoff](../../sdd-forge/scripts/forge-project-input.md), supply the corresponding reviewed brief/dependency fields instead of an arbitrary complete-body override. Its renderer derives title/context/markers from validated source identities. Mechanical extraction does not author dependencies or acceptance; use actual governing documents and preserve the same task identity and evidence boundaries.

## Git commit

For a first SDD commit or adoption backfill, load **sdd-manage**'s [repository bootstrap](../../sdd-manage/references/repository-bootstrap.md). For main preparation use [its initialization exception](../../sdd-manage/references/main-preparation.md): normal DOCS-001 completion has four preserved/copied root files and the task list; the default provenance scaffold has a preliminary unchecked checkpoint unless explicitly overridden. README links follow at PROJECT. Otherwise confirm the commit owner has included or validly retained root disclosure/usage records and README links within scope. Return missing bootstrap evidence to that owner; drafting does not perform bootstrap or establish a committed result.

Draft a short imperative subject naming the actual change, based on the inspected diff and checks rather than merely the task brief. Use a body when the reason, verification, migration implications or verified issue references need explanation.

### Task commit subjects

For every task-associated commit, use exactly `[<owning-task-id>] <imperative description>`. The single owning task marker must be the first content of the subject, followed by one space and the description. Preserve the exact ID from TASKS/FEATURE-TASKS or the mapped DOCS_TASKS/FEATURE_DOCS_TASKS. FDOCS subjects use their stage ID; hosted issue identity also includes the campaign. Feature document completion follows [feature preparation](../../sdd-manage/references/feature-preparation.md), keeping checkoffs in FEATURE_DOCS_TASKS and decision/QC evidence in FEATURE_PREPARATION; it does not use the product T-task audit. DOCS subjects use the same single-ID shape, but document task completion means first approval under [main preparation](../../sdd-manage/references/main-preparation.md), not implementation task completion. Proposal commits leave the DOCS task unchecked; approval commits include its checked task, accepted document state and DOCS_PREPARATION decision/QC evidence. Keep narrative out of DOCS_TASKS. Later revisions retain completed first-approval tasks/issues. Do not prepend a conventional-commit type/scope, put the ID only at the end, or use multiple task IDs or a task range in the subject. Apply this format to production, tests, documentation and explicit milestone/phase review/report tasks, as well as authorized partial checkpoints and later task-specific repairs or parent-status follow-ups. Describe partial or follow-up work accurately; a subject does not establish completion.

For numeric `T-` IDs padded to at least three digits, `^\[T-[0-9]{3,}\] [^\r\n]+$` checks the basic subject shape. Also check that the ID is the exact owning entry, the subject has no second task identity, and the description is concise, imperative and truthful. A regex alone cannot establish ownership, single-task composition or completion.

| Subject | Assessment |
| --- | --- |
| `[T-028] Implement lock delay` | Valid shape for one verified owning task. |
| `[T-030] Complete Milestone 2.4 review` | Valid for the review task's actual result and completion. |
| `[T-028] Record partial lock-delay checkpoint` | Valid shape; retain unchecked status and required checkpoint authority. |
| `feat(mechanics): [T-028] Implement lock delay` | Invalid: content precedes the task marker. |
| `Implement lock delay (T-028)` | Invalid: task marker is not at the beginning. |
| `[T-028, T-029] Implement lock delay and wall kicks` | Invalid: multiple owning tasks. |
| `[T-028] Implement lock delay and close T-029` | Invalid: second task identity, despite passing the shape regex. |

For implementation tasks, closing composition follows **sdd-implement**'s [task commit contract](../../sdd-implement/references/completion-and-checkpoints.md#task-commit-contract): one executable task's result, required evidence and initial completion checkbox together. Return a detected composition conflict to the commit owner; do not merely improve the subject of a bundled or split closing commit.

For DOCS tasks, use [main preparation](../../sdd-manage/references/main-preparation.md): verified initialization or package QC, or first human approval for a document, with the checked DOCS task in its completion commit. For FDOCS stages, use the [feature counterpart](../../sdd-manage/references/feature-preparation.md) for context, accepted/reused documents and package QC. The implementation history audit does not govern DOCS/FDOCS preparation tasks.

For other preparation, campaign actions or maintenance without an assigned executable task, do not invent a task ID. Merge commits use their integration-summary format and may summarize several completed tasks; they do not close those tasks for the first time.

Use `Refs owner/repo#123` when the commit advances an issue without completing it. Use `Fixes owner/repo#123`, `Resolves owner/repo#123`, or `Closes owner/repo#123` when the commit fully resolves that issue and the evidence supports completion. One task may have multiple verified issue associations, with a separate appropriate reference for each; these references do not permit bundling multiple executable tasks in one closing commit. Omit issue references when no verified association exists. On GitHub, closing keywords may close an issue when the commit reaches the default branch. **sdd-forge** still reconciles issue closure after verified task completion, without waiting for that automation. If verification has not been run, say so in a proposed body rather than claiming it passed. The active implementation workflow makes and checks its commits; **sdd-manage** coordinates persistence for other authorized repository changes.

## Merge commit

Draft a subject identifying the actual feature, revision campaign, steering amendment or selected completed range. For a campaign, include its stable ID and a concise title derived from the final delivered scope, such as `Merge revision 040_a0685b5 — Revision campaign modes`; do not retain a stale opening title when scope changed. A main milestone/task subset does not justify a merge while its phase remains incomplete. Return subject/body separately; the coordinator owns the explicit two-parent integration.

### Campaign integration summary

Every ordinary, nested or reopened revision integration, and every feature, steering, completed phase or accepted document-preparation integration, carries a concise, self-contained summary for [release highlights](../../sdd-forge/references/release-highlights.md#use-integration-summaries-first). Include the following facts, with labels when useful rather than a mandatory machine schema:

- **Objective:** The problem or intended outcome and why it matters.
- **Review:** Actual reviewed scope/coverage and material conclusions; state when no separate review was performed. Do not imply a comprehensive review from a focused amendment.
- **Delivered:** Actual executed scope and consequential features/fixes/documentation or workflow changes, including effects relevant to users. Separate accepted/executed work from proposals, exclusions and unfinished parent work.
- **Verification:** Actual boundary and merged-state checks/results, with relevant counts/environment and evidence limits. Record blocked/unrun checks, material conflict resolutions, compatibility/migration consequences and deferred work when applicable; passing local tests does not prove live acceptance.
- **Integration:** Campaign/phase/preparation identity and mode where applicable, working and recorded creation-parent/return-target branches, full original campaign-opening commit ID, full original branch-off/base commit ID (the starting baseline), and distinct reopening checkpoint when applicable, verified parent/source tips and affected task/action IDs. Apply campaign-opening provenance to campaigns; do not invent a campaign ID/opening for an initial preparation or phase that has none. Git parents establish ancestry; titles/branch names alone do not establish coverage.

A reopened amendment carries forward a concise cumulative summary of the campaign’s retained result and objective/review coverage, then clearly separates the new delta and added actions. Include prior integration, the original campaign-opening commit pointer and original branch-off SHA alongside the reopening checkpoint. Every amendment retains the first opening pointer; do not replace it with an amendment’s first commit. Make the latest cumulative summary sufficient for release highlights without tracing earlier campaign merges: carry forward all relevant retained outcomes, review coverage and material superseded/withdrawn consequences, with original opening provenance and separately identified new delta. Retain relevant earlier information without copying raw prior messages or presenting original delivery as new. Correct superseded outcomes in the cumulative result and distinguish historical checks/source from actual new merged-state verification; inherited verification is not fresh evidence.

Subsequent summaries may also retain compact explicit scope references for the original opening and individual reopenings: identify each opening/reopening commit or checkpoint, added action IDs and its review/execution scope. Carry needed scope distinctions forward in the latest message rather than requiring readers to follow older merge bodies; distinguish these provenance references from the cumulative user outcome and current delta. They are not a new registry or raw chronological transcript.

The campaign-opening commit is the verified first commit opening that campaign and its retained records. It is distinct from the branch-off/shared source checkpoint and from later reopening commits; do not infer it from current branch tips or invent an unavailable identity.

An enclosing integration summarizes the combined delivered result and identifies included nested campaigns/amendments sufficiently to prevent duplicate release highlights. Keep the semantic summary prominent and technical provenance compact; do not substitute raw logs or a list of commit subjects for the outcome.

Phase summaries describe actual completed phase scope, delivery/reviews/exits and verification; retain the full-phase merge gate and report an explicit partial-integration override accurately. Document-preparation summaries identify accepted documents/review coverage and readiness for their dependent stage, without claiming implementation or task completion. Use the plugin’s established `design-docs/*` document-preparation branches; prefixes discover candidates but never establish scope or acceptance. Preserve repeated preparation deltas as distinct scope, with appropriate source/checkpoint evidence.

The message is an **integration summary**, not proof that closure/publication already happened. It is committed before its push and final worktree return; do not claim those future steps succeeded. Closure still requires the applicable verified target publication and return boundary. Review-only publication does not fabricate a closure merge. Do not represent an amendment as completion of the next task, an interrupted parent or a product release. Drafting authorizes no extra work or hosted PR.

```text
Merge revision 040_a0685b5 — Revision campaign modes

Objective: Define nested revisions and eligible campaign amendments.
Review: Assessed campaign routing, branch ownership, closure and reporting.
Delivered: Added both modes, eligibility checks, scoped reopening and
explicit return to the interrupted campaign branch.
Verification: 16 source scenarios checked; 113 support tests passed on the
merged state. Package and link checks passed; live compliance not assessed.
Integration: <campaign/mode, original opening, branch-off/reopening, branches/parents>
```

## Pull request

Draft a title and description only when requested; this skill does not create a PR. Scope the text to the actual branch diff and its included task IDs. Summarize **What**, **Why**, **Verification**, and **Result**; add the relevant fields from [change kinds](change-kinds.md). State the base branch and integration status only when known. List unrun checks, limitations, and remaining work explicitly rather than presenting partial work as complete.

A code health PR should explain the ownership or maintainability problem and the checks supporting behavior preservation. A performance PR should include baseline and current times, input size, environment, method, and whether the measured gain is meaningful. Do not imply that GitHub PR operations are available through **sdd-forge**.

## Examples

These show formatting for an issue title, commit message, and PR draft. Use actual task IDs, issue references, checks, and results for the current work.

### Issue title

```text
[T-012] Implement ZIP stream support
```

### Commit message

```text
[T-041] Clarify filesystem utility ownership

Move shared filesystem helpers into the module named by the project layout.
Update its documented responsibility; the focused unit suite passed.

Refs owner/repo#123
```

### Code health PR

```markdown
# 🧹 Clarify filesystem utility ownership

- 🎯 **What:** Renamed `common.py` to `fs.py` and updated its documented responsibility.
- 💡 **Why:** A focused module name makes ownership clear under the project's layout rules.
- ✅ **Verification:** Inspected layout references and passed the focused unit tests.
- ✨ **Result:** Filesystem utility ownership is explicit, with behavior preservation supported by the cited checks.

```

## Release commit message

Use for the release commit selected by manage's [release commit/tag boundary](../../sdd-manage/references/git-workflows.md#release-commit-and-tag). Compose a concise `Release <version/tag>` subject, a blank line, then the exact finalized release-message Markdown body. Assemble the UTF-8 message file as subject bytes + `b"\n\n"` + body bytes, without shell interpolation, reflow or newline normalization. Preserve hard-break spaces, CRLF when present, trailing blank lines and the presence or absence of a final newline. The same body bytes remain in the notes and publisher handoff; no task ID is invented.

The Git owner commits the prepared file with `git commit --cleanup=verbatim -F <message-file>`; ordinary file-message cleanup can strip Markdown spaces/blank lines or append a newline. This applies both to a direct default-branch release commit and the release merge from the designated primary development branch into default; the merge uses this release message, with integration provenance retained in existing evidence. Add `--allow-empty` only when an authorized direct release requires it, never to add a marker after the release merge. Include necessary owned release-document moves from campaign staging without relocating campaign plans/reports. If a client or hook alters the text, actual raw-body comparison must catch the mismatch before publication; do not silently change finalized notes to match cleaned Git output. No task/campaign-summary formatting or premature provider-success claim is added. This skill supplies the draft; manage owns the commit, comparison and publication.
