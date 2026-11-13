# Execution and evidence

## Run against an identified state

- Record the branch and commit, relevant pending changes, command working directory, and material runtime or dependency conditions. Evidence from committed HEAD alone does not describe uncommitted code being tested.
- Use the project's declared commands and environment. Inspect potentially mutating build, test, or example commands before execution; use controlled fixtures or temporary output locations where practical. Do not install dependencies, change configuration, or operate external services beyond the authorized scope.
- Capture the actual command, exit status, relevant output, counts, warnings, skips, and artifacts where applicable. Inspect collection and execution: zero selected tests or unexpected deselection does not verify the intended behavior merely because the runner exits successfully.
- Run independent checks together only when they do not contend for shared resources or invalidate each other's results. Keep dependent checks in the required order.
- If execution is interrupted, report the incomplete run and available output. Do not describe a started command as a completed check.

## Assess coverage

| Condition state | Meaning |
| --- | --- |
| Verified | Observed evidence supports this condition for the stated implementation and environment. |
| Failed | Observed evidence contradicts the condition or its required check failed; identify the cause separately where known. |
| Blocked | Required evidence cannot be obtained because of a concrete prerequisite or execution problem. |
| Not checked | The condition was not assessed; give the reason and remaining work. |

Associate conditions with the checks that actually exercise them. Record partial coverage, expected failures, skipped scenarios, platform limitations, or manual inspection explicitly. A passing suite is evidence about its tested behavior, not proof that every requirement is covered. Do not invent coverage percentages or measurements.

Reuse prior evidence only when its implementation state, environment, and condition coverage are still applicable; identify it as prior evidence. After relevant code, test, configuration, dependency, or generated-output changes, repeat affected checks. Do not repeatedly run already sufficient checks without a changed state, failure, or unresolved gap that justifies it.

## Preserve and return evidence

Inspect resulting worktree changes to distinguish expected generated output from unexpected mutations. Preserve unrelated work and report unexplained changes; do not reset or clean the repository to conceal them. Temporary fixtures owned by this verification operation may be cleaned up when no longer needed.

Return evidence facts and locations to the active workflow's coordinator or authorized artifact owner and **sdd-report**, including unresolved failures and limitations. Preserve raw outputs or artifacts when the project requires them or they are needed to review a consequential claim. Honor the project-designated evidence location. If none is designated, return concise durable facts for that owner to retain with the reviewed artifact or task and its existing linked evidence. For TASKS/FEATURE-TASKS implementation, use the owning entry; for taskless maintenance, use the ordinary change report or commit body rather than inventing a task ID or evidence file. Verification returns facts; the active owner persists them with its scoped result.

## Durable evidence facts

| Fact | Record |
| --- | --- |
| Identity and state | Owning task/change, branch, tested commit or pending diff, authoritative condition. |
| Check | Command, relevant environment, observed exit/outcome, material counts, warnings/skips. |
| Coverage | Conditions actually exercised, gaps, blocked checks, and evidence location when separate. |
| Prior evidence | Historical source and applicability; do not present it as a fresh run. |
| Test-first exception | Concrete limitation, applicable policy or user authorization, alternative evidence actually obtained, and remaining gap. |

Carry these facts to **sdd-report** without requiring a new JSON schema or journal. Preserve raw output when needed to review a consequential claim. For branch integration, identify the working tip and target tip tested in the prospective merge, and retain merged-state outcomes in existing boundary evidence or the merge commit body.

## Environment coverage

Report the capabilities actually exercised by readiness probes, not just installation success. Distinguish artifact validity, executable launch, suite lifecycle, rendering and native delivery when relevant. A modeled or injected handler check does not establish native delivery; preserve its useful evidence and record the missing facility separately.
