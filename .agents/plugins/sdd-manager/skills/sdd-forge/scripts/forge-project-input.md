# Prepare tracking projection input

Use this local authoring workflow after sdd-manage selects tracking scope and sdd-forge loads the [implementation projection](../references/github-projection.md) or [docs-main preparation](../references/github-docs-preparation.md) lifecycle. [forge-project](forge-project.md) consumes explicit requests and also provides the routine single-call docs-main path without an intermediate file. Input authoring makes no hosted changes and does not establish readiness or acceptance.

## Generate and review

1. Identify the actual repository/root/remote and owning list. For an eligible implementation phase, read the complete TASKS or active FEATURE-TASKS and the other active list for identity/dependency conflicts; use accepted PLAN/SPEC/layout and current QC. For initial docs-main preparation, use the running package's DOCS task template and [predefined tracking content](../../../assets/DOCS_TRACKING_TEMPLATE.json) before target files exist. On resume use task-only DOCS_TASKS and DOCS_PREPARATION decisions/control, checking its identity and scope against those definitions.
2. For an implementation phase or when an explicit request artifact is needed, run [forge-project-draft.mjs](forge-project-draft.mjs) with the selected scope. Routine docs-main uses forge-project directly and builds the same source-bound content in memory. It extracts exact IDs/names/parentage and a raw-byte source hash. Phase drafts leave semantic fields null for the agent; docs-main drafts copy complete predefined content. Both leave eligibility false. The helper never infers dependencies from order/prose, classifies implementation reviews or copies raw task details into payloads.
3. For implementation phases, read the governing content and fill semantic fields: milestone outcomes/exits/reviews, task scope/acceptance/sources, dependency IDs and prerequisite gates. Resolve dependency cycles and acceptance that requires a later post-task operation. Review roles and milestone boundaries come from accepted planning. For standard docs-main, retain the fixed content and dependencies; no semantic enrichment is needed. Do not alter the task set or invent facts to fit the utility.
4. The agent establishes the selected lifecycle's real prerequisites and reviews the rendered outgoing content. Run forge-project with --check; inspect its payloads. This is an agent QC operation, not an additional mandatory human approval. Preserve actual pending human checkpoints and ask only for a consequential missing decision.
5. Invoke the hosted mechanism only after all required facts hold. Retain known/unknown outcomes under the existing lifecycle. An input file is an execution handoff, not another task authority, issue database or progress journal.

These commands are abstract templates; substitute actual paths and IDs. Quoted commands work in native Windows CMD and POSIX shells:

~~~text
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-project-draft.mjs" phase --repo "<WORKTREE_ROOT>" --tasks "docs/dev/TASKS.md" --phase "<PHASE_ID>" --output "<NEW_REQUEST_FILE>"
node "<PLUGIN_ROOT>/skills/sdd-forge/scripts/forge-project-draft.mjs" docs-main --repo "<WORKTREE_ROOT>" --output "<NEW_EXTERNAL_REQUEST_FILE>"
~~~

Omit --output to receive the draft JSON on stdout. An explicit output file requires an existing parent directory and is created exclusively; existing files are never overwritten. Before docs-main's pre-write projection gate, the helper refuses output within the target repository. Both CLIs default --remote to origin. For docs-main, optional --tasks selects a repository-root-relative owner; by default use docs/dev/DOCS_TASKS.md, falling back to the bundled template only when that implicit default is absent. Missing explicit or invalid existing sources fail. For phases, --tasks and --phase remain required by the draft generator. Native slash/backslash task paths become portable slash paths in JSON. No token is read; no Git configuration/ref is changed. Requires Node 22+ and native Git.

## Supported source grammar

Implementation sources use a Phase heading, matching phase checkbox, milestone checkboxes indented exactly four spaces, and T-ID task checkboxes indented eight spaces. Tasks/details remain under their owning milestone; IDs are unique throughout the full list. Recognize the established em dash, en dash or hyphen separator and checked/unchecked state. Ignore fenced examples; refuse malformed, duplicate, missing or ambiguous hierarchy instead of guessing a Markdown interpretation. Only the selected phase enters the draft; future task IDs remain available for dependency validation.

Docs-main sources contain the nine ordered DOCS-001–DOCS-009 top-level task checkboxes, with exact names matching the bundled JSON. The utility preserves the selected template/list and checked progress rather than regenerating a resumed list. The caller assesses semantic scope; source-name/order mismatch is `docs_template_source_conflict` or `unsupported_source_format`. Alternative established formats/custom IDs or conflicting semantics return to the existing backend/coordinator; this optional canonical reader does not justify changing valid source documents.

## Predefined main preparation content

[DOCS_TRACKING_TEMPLATE.json](../../../assets/DOCS_TRACKING_TEMPLATE.json) is reusable definition data with exactly `schema_version` (1), `kind` (`docs-main`), `milestones` and `tasks`. Its single milestone and nine ordered tasks use the fields below. It defines the exact native milestone name `sdd-docs-main`, plain-text description, issue names, dependency IDs, prerequisites, scope, acceptance and source descriptions. Neither the milestone title nor its description receives generated project text or HTML metadata. Issue bodies retain the standard task/scope identity markers from the renderer.

This asset contains no repository/source binding, credential, eligibility or completion state. The helper consumes it directly and adds the real repository, Markdown source/hash, null phase, empty external-ID list and false eligibility to produce the schema-v1 request. That request is content-complete and ready for `--check`; the agent then establishes the actual scope-specific facts before enabling `--apply`. Explicit requests carry these facts in eligibility booleans; request-free docs-main carries them through the explicit --confirm-eligibility assertion described in the [CLI contract](forge-project.md#main-preparation-defaults-and-explicit-inputs). Import both definition and Markdown assets from the same pinned/running package. JSON content is copied into independent requests; changing a request cannot mutate the bundled definitions.

The validator requires every docs milestone/task field to equal the definitions, allowing JSON object-key order and supported line-ending normalization. Missing, reordered or altered content fails; arbitrary external tasks are not part of this standard preparation. Its predefined dependencies express the known preparation sequence, including all prior tasks before DOCS-009. The final documentation merge and milestone closure follow that task; they are not circular prerequisites for its completion. Other authenticated clients consume these same fields and outgoing templates, preserving the coordinator's pre-write/readback and closure gates.

DOCS_TASKS owns task definitions/checkoffs; DOCS_PREPARATION owns preparation control/decision evidence; the JSON owns standard hosted content. Neither generated requests nor these assets are an issue database or progress journal. DOCS_PREPARATION is not a parser/CLI input or a prerequisite for pre-write projection. For older fixed briefs/requests, use the backend's [explicit adoption reconciliation](../references/github-docs-preparation.md#fixed-content-updates-on-adoption); do not modify payloads to evade a conflict. On resume, retain real source/approval/publication and hosted evidence, and resolve content/identity conflicts through the owning lifecycle rather than editing generated text to force reuse.

## Request contract

The top-level object has exactly these fields. Unknown versions, fields and incomplete drafts are rejected.

| Field | Contract |
| --- | --- |
| schema_version | Integer 1. |
| repository | Selected GitHub owner/repository; normalized case-insensitively and bound to the explicit remote/API metadata. |
| kind | phase or docs-main, matching the CLI operation. |
| source | Object with root, path and sha256. root is repo or plugin; path is a root-relative Markdown path using forward slashes; sha256 is lowercase raw-file SHA-256. plugin is allowed only for docs-main assets/DOCS_TASKS_TEMPLATE.md. |
| phase | For phase, object with exact id/name from the source, description (nonblank single-line brief, at most 100 UTF-8 bytes), and six lowercase hexadecimal color digits. For docs-main, null. |
| milestones | Ordered complete selected milestone array, at most 1000. Fields below. |
| tasks | Ordered complete selected task array, at most 1000. Fields below. |
| external_task_ids | For phases, unique caller-verified task IDs outside the owning list, at most 1000. The agent checks these against other active/retained owning sources; the utility cannot prove that assertion. Do not hide duplicate task ownership. Empty for standard docs-main. |
| eligibility | Exactly tracking, ready, accepted, published, eligible, exclusive and content_reviewed booleans. --apply requires all true. |

The JSON and each source are bounded to 1 MiB. UTF-8 with optional UTF-8 BOM and LF/CRLF text are supported. Other encodings, invalid Unicode, controls, managed-marker injection, traversing/absolute JSON source paths and stale hashes are rejected.

The runtime checks source bytes/hash and exact extracted IDs/names/parentage/order. For authenticated execution, repo sources must match committed HEAD text, allowing CRLF-to-LF normalization only for native checkout line endings. Substantive unpublished changes fail. Remote containment, actual QC/approval and source completeness across active lists remain coordinator/agent obligations. A transferred input may need rebinding after checkout line-ending conversion changes its raw-byte hash; never update the hash without rechecking the content.

### Milestone and task fields

| Milestone field | Contract |
| --- | --- |
| id, name | Exact selected source identity/name. For docs-main the logical ID is docs-main and name/native title is the predefined sdd-docs-main. Host titles are rendered deterministically. |
| kind | delivery or phase-review for implementation; docs-main for documentation preparation. |
| description | Phase outcome/exit conditions are agent-authored; docs-main uses the exact predefined description. Nonblank UTF-8, at most 16000 bytes; no unrelated project defaults. |
| review_task | Exact final report-bearing boundary task ID: standalone review or eligible final delivery task; null for docs-main. |

| Task field | Contract |
| --- | --- |
| id, name, milestone_id | Exact source task identity/name/parent. Supported IDs are T- with at least three digits, or the nine DOCS IDs. |
| role | delivery, milestone-review or phase-review for implementation; documentation for docs-main. |
| depends_on | Phase dependencies are agent-authored; docs-main uses the predefined array. [] only when no prerequisite task exists. No self-reference, unknown ID or selected-task cycle. Other owning-list phases may supply IDs without being projected. |
| prerequisites | Nonblank gate text, at most 8000 UTF-8 bytes: applicable reviews/closures/QC/approval/integration or other actual conditions. Predefined for docs-main. It complements task IDs; no parser infers its truth. |
| scope, acceptance | Nonblank scope and observable checks/evidence, each at most 16000 UTF-8 bytes. Agent-authored for phases, predefined for docs-main. Resolve contradictions against governing documents. |
| sources | One to sixteen explicit relevant reference strings, each at most 1024 bytes. Include only useful available sources; do not invent links before files exist. |

New task generation follows the [milestone review threshold](../../sdd-conventions/references/backend-object-lifecycle.md#explicit-review-units): omit the separate review task below four implementation tasks or when the phase has one implementation milestone, excluding the special phase review. In that case all milestone tasks keep role delivery, review_task points to the final one, and that task depends on every other constituent task and owns the milestone review/report/HANDOFF obligations. Otherwise the final task has role milestone-review and depends on the preceding delivery tasks. The special last milestone still contains exactly one phase-review task depending on each delivery milestone's final boundary task.

The validator accepts eligible folded boundaries and retains previously accepted explicit-review layouts without deleting IDs. Generation/QC enforces the new threshold; changing an existing accepted list requires scoped amendment, including multipass preservation. Structural checks do not establish correct dependency semantics, actual review/report work or completed prerequisites. Docs-main has its single predefined native milestone and all nine template/list tasks; the agent establishes actual first-approval and merge-after-task evidence.

For clarity, this abstract example is **one task object**, not a complete operational request or a prescribed work breakdown:

~~~json
{
  "id": "T-101",
  "name": "Deliver bounded work",
  "milestone_id": "1.1",
  "role": "delivery",
  "depends_on": [],
  "prerequisites": "Caller verifies required preparation and scope.",
  "scope": "Implement the accepted bounded behavior with its documentation.",
  "acceptance": "Required checks and observable evidence pass.",
  "sources": ["docs/dev/PLAN.md"]
}
~~~

### Eligibility means actual scope-specific facts

| Assertion | Selected phase | docs-main preparation |
| --- | --- | --- |
| tracking | Tracking confirmed for this repository/phase. | Preparation tracking confirmed for this repository. |
| ready, accepted | Current owning/upstream QC and necessary human acceptance/preapproval established. | Preparation/template/list selection and current prerequisites established; not a claim that the documents being prepared already exist or are approved. |
| published | Required preparation/baseline/source publication verified. | Required current repository/package baseline established; not future document or documentation-merge publication. |
| eligible | Authorized phase/range and applicable predecessor integration/reviews/closures established. | Main preparation selected and eligible for its early pre-write projection. |
| exclusive | Local and cross-machine operation ownership established. | Same. |
| content_reviewed | Exact rendered authored content is appropriate for the selected repository/audience. | Same. |

Setting true cannot establish any of these facts. --check and read-only reconciliation permit false eligibility but still require a complete valid input. They cannot accept unresolved null semantic fields in an unenriched phase draft; the standard docs draft already has complete content.

## Outgoing template and data boundary

The renderer supplies the phase label, native milestone title/description, task title and one generated issue section. It includes identity-derived outcome/context, dependency IDs plus prerequisite text, scope, acceptance and selected source references. Docs bodies add the main-preparation scope marker; `sdd-docs-main` gets no milestone marker or implementation phase label. Dependencies are readable brief content; this mechanism does not create native provider dependency/subissue relationships.

Only those reviewed fields enter GitHub payloads. Full local source files, source hashes, eligibility flags, external-ID inventories and request paths are not uploaded. --check shows authored payload content with stable milestone references; actual numeric milestone handles are resolved by complete hosted lookup during execution. It does not claim to preview not-yet-allocated provider numbers.

The active credential's literal occurrence in request content is rejected before authenticated API calls. The agent remains responsible for other secrets/private inappropriate content and the intended repository audience. Existing user material outside an exact generated section is preserved; edited/ambiguous generated content is a conflict for the backend, not permission to overwrite it.
