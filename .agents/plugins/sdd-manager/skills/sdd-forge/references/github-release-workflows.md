# Prepare and run a release workflow

Load after the [package contract](github-packaging.md) is sufficient, or when inspecting/dispatching an established release workflow. **sdd-manage** coordinates repository authoring, verification and Git persistence. **sdd-forge** owns requested GitHub dispatch/monitoring; it does not commit or push the workflow files.

## Author or extend

**Version numbers in the name of any release artifact are absolutely prohibited, regardless of type.** Establish independent stable names before writing the workflow. Generate a real failing-before-passing naming check in the existing stack, cover every staged artifact without filtering by type, and require it before uploads/publication. Provide a build-only route for pre-tag candidate verification.

Inspect existing `.github/workflows/` and project build procedures directly, including tracked hidden directories; do not infer absence from a visible-file listing. Record actual CI paths and executed versus source-only checks accurately. Reuse a suitable workflow and publishing stage rather than introduce competing release creators. Establish trigger, exact source/tag inputs, build-only versus publication behavior, supported variants, expected asset set and notes/latest/prerelease policy. Keep a simple source ZIP proportionate: an explicit inventory, relevant checks, archive inspection, checksum and one publishing stage may be enough.

Before a publishing tag push or dispatch, complete the [artifact-name gate and repair](github-packaging.md#artifact-name-gate-and-repair), including publication/readback of repaired source and checks against the rebuilt pinned candidate. Generated and reused workflows must:

- Select the exact release source. For tag triggers, use the tag's resolved commit; for manual runs, distinguish the ref containing the workflow from the release source input. Before publication, verify that the pinned release commit is on the actual remote default branch’s first-parent history and the peeled tag/version/source agree under the coordinator’s release boundary. A revision/development tip does not qualify through ordinary ancestry. Keep the workflow execution ref separate; build the pinned release commit even if default later advances.
- Support the accepted tag trigger and/or `workflow_dispatch`, plus build-only validation where needed. A manual dispatch requires the workflow to be present on the default branch and to declare `workflow_dispatch`; verify the selected ref contains the intended workflow. Inspect actual inputs rather than assume their names.
- Use declared runtimes/dependencies and supported actions. Pass user inputs as data through environment/structured arguments rather than interpolate arbitrary text into shell code. Run the meaningful project checks and the agreed package inspection against actual built archives.
- Scope job permissions: build jobs normally need Contents read; the publisher needs Contents write for release writes. PAT Workflows permission enables workflow-file modification; conditional Actions permission enables provider dispatch/run operations. These are separate from job `GITHUB_TOKEN` permissions. Keep credentials out of outputs and package inventories.
- Build every required variant, check nonempty outputs and unique stable version-free names against the independent naming contract, collect the exact asset set and create SHA-256 files. Run the project-local naming/inventory check on actual outputs before upload and before final publication; a versioned raw HTML filename fails just as a versioned archive does. Check checksum entries and documented latest URLs against the same stable set. For a matrix, collect all successful builds before one publisher creates/uploads/publishes the release. Do not upload an unexamined broad glob or silently omit a failed variant.
- Serialize publication for the same repository/tag with an appropriate concurrency group. Avoid cancellation that abandons uploads or races between tag and manual triggers. Define repeat behavior using the [release lifecycle](github-releases.md), not unconditional `gh release create` or `--clobber`.
- Keep build-only runs free of tag/release writes. Record build outputs separately from public release assets. Optional signing, SBOM or provenance steps follow actual project requirements.

A tag pushed with the repository's `GITHUB_TOKEN` does not normally trigger another push workflow. Follow [GitHub's token event rules](https://docs.github.com/en/actions/concepts/security/github_token): build/publish in the same intended workflow or use a supported dispatch route; do not claim the chain ran without evidence. Do not change accounts/tokens to evade a host denial.

If an existing workflow or packaging script produces nonconforming names, repair its producers and related code/tests/docs, publish the corrected source, rebuild and repeat the gate under the existing release authority. Do not patch only a temporary upload or stop after identifying the problem; preserve the requested effects and published-tag recovery boundaries.

Verify syntax with suitable tooling, inspect permissions/inputs/checkout identity and execute the local build/verification where supported. Use [release checks](../../sdd-verify/references/release-checks.md). Distinguish a parsed YAML file, successful local package build, actual CI run and hosted release verification. GitHub Actions syntax and runtime compatibility are not proved merely by YAML parsing.

## Notes transfer

Use [complete release-message preparation](release-message.md) to assemble final body-only notes, using [shared Git highlights](release-highlights.md) for changes and authoritative inputs for ancillary sections, through the exact intended source before dispatch or a publishing tag push. Select the previous baseline before creating the pending release tag, or explicitly exclude that tag; retries retain the validated prior baseline. Complete semantic editing on the agent side. On release requests, apply the [message freshness/release-commit gate](release-message.md#release-request-freshness-and-commit-gate): verify local coverage and stated version, tag the verified release commit and transfer its complete message body. Build-only/package preparation does not create a release marker. An ignored local draft is absent from checkout, and ordinary Actions runners do not implicitly supply an AI agent. If a workflow collects Git evidence itself, establish complete tags/history (a default shallow checkout is insufficient), but deterministic log collection is not semantic distillation.

Inspect the existing publisher’s declared mechanism. For manual dispatch, a declared string notes input can carry the finalized Markdown via a supported structured/JSON input file; the publishing job must consume that value as data through a notes file/API body, not shell interpolation. Check input size limits and preserve multiline bytes. For larger notes or tag-only workflows, establish an authorized source-associated artifact/file transfer with explicit retrieval and integrity/identity checks; never assume the ignored draft was pushed. Keep YAML control data out of the final body. Do not add an untrusted arbitrary download/execute mechanism.

If the existing workflow has no supported notes transfer, extend and verify it before triggering publication or return the prepared handoff as pending. Generated notes alone do not satisfy requested curated highlights. Reuse one publisher, preserve human notes, avoid duplicate highlights and retain the internal highlights checkpoint until published-body readback confirms consumption. Build-only or failed runs retain it. The complete-message file remains after all outcomes, including verified publication; refresh/replace it on the next preparation. Transfer its exact UTF-8 bytes with source association and body hash through the established publisher; an ignored local file is not available by CI pathname alone.

## Dispatch and monitor

**Version numbers in the name of any release artifact are absolutely prohibited, regardless of type.** Before a publishing dispatch, require current executed naming evidence for every actual candidate artifact through the [naming gate](github-packaging.md#artifact-name-gate-and-repair). Missing or failing evidence requires repair/rebuild; build-only dispatch remains nonpublishing.

For a run that will publish a release, apply the shared [advisory prerelease review reminder](../../sdd-manage/references/prerelease-review.md#advisory-release-reminder), reusing any disposition from the release handoff. Build-only runs retain their preparation boundary. Apply the same handoff before an authorized publishing tag trigger through the release lifecycle.

Dispatch only when the request covers running the selected workflow and its effects. Resolve repository, workflow ID/path, selected ref, actual inputs, exact intended release source and expected outputs. Check [operation-specific access](github.md#release-and-workflow-access); Workflows write does not imply Actions write. Do not enable a disabled workflow or change repository settings by implication.

For a configured workflow, a command recipe is:

```text
gh workflow run release.yml --repo OWNER/REPO --ref WORKFLOW_REF -f tag=RELEASE_TAG -f publish=false
```

Replace those example input names with the workflow's declared inputs. `publish=false` is meaningful only if the workflow implements that build-only behavior. Change it to publication only when the selected request covers that operation. Use structured inputs or a JSON input file for complex values. See [GitHub CLI dispatch](https://cli.github.com/manual/gh_workflow_run) and the [workflow REST API](https://docs.github.com/en/rest/actions/workflows).

Retain a returned run ID/URL when available. Where a client/API returns only dispatch acceptance, correlate the run using workflow/ref/event/time and any declared request marker; do not pick the most recent unrelated run. After an uncertain dispatch, inspect existing runs before repeating. Ambiguous correlation remains unknown and blocks a duplicate dispatch.

Inspect queued/running/completed state, conclusion and the expected jobs/artifacts. Use `gh run view RUN_ID --repo OWNER/REPO` or the supported run API; bounded monitoring may return pending with the known run URL and next action. Do not wait indefinitely or infer build success from dispatch acceptance. No automatic rerun/cancel is implied by a failure.

When the workflow owns publication, do not create the same release independently. After successful publication, apply [release readback](github-releases.md#read-back-and-report). Return workflow/ref/source, run identity and conclusion, actual outputs, release state, failures and pending work. A failed job or unavailable facility keeps its affected result unverified.
