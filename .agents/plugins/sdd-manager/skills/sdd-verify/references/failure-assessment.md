# Assess failures and gaps

Inspect the failed command and relevant output before classifying it. Separate a test assertion failure from failure to collect tests, unavailable tooling, a crashed process, or an interrupted run. Do not infer the cause solely from the exit code or the changed file names.

Return findings to the active workflow's coordinator or authorized artifact owner. During document preparation, **sdd-manage** coordinates scoped corrections with the relevant document skill; during implementation or checkpoint amendments, **sdd-implement** or **sdd-steer** coordinates repairs. A standalone verification request returns findings without initiating repair.

| Classification | Evidence needed and handoff |
| --- | --- |
| Defect in the selected change | Reproduction or inspected evidence connects the failure to the selected artifact or behavior; return the failure and affected condition to its active owner. |
| Pre-existing failure | Applicable earlier evidence or a safe isolated baseline demonstrates the same failure before the change. Report it even if outside the selected repair scope. |
| Environment problem | Evidence identifies a missing dependency, configuration, resource, service, platform, or other execution prerequisite. Report the blocked check and needed action. |
| Test or fixture problem | Independent contract evidence shows that the check or fixture is incorrect; return the needed test review to the active owner for coordination with **sdd-tdd**. |
| Unknown cause | Evidence is insufficient to distinguish the causes. Report the failure and uncertainty without calling it unrelated or pre-existing. |

A baseline comparison must preserve the current worktree. Use an existing suitable result or an authorized isolated baseline when needed; do not reset dirty files to obtain one. Do not claim baseline equivalence when dependency or environment differences could explain the result.

Warnings, expected failures, flaky outcomes, and skips remain visible evidence. Apply project policy to whether they block the requested boundary. A successful retry does not erase a failed run; report both and any unresolved instability. Bound retries and investigate what they establish rather than retrying until a green result appears.

When a requirement, expected result, or governing instruction is contradictory or unclear, identify the conflicting sources and affected condition for the user or coordinating workflow. Do not rewrite SPEC, PLAN, design, layout, or TASKS to make the verification pass. Independent selected checks may continue where their meaning remains sound.

Return a concrete repair or investigation handoff: command, affected condition, observed failure, relevant state and evidence, classification and confidence, and missing information. Verification supplies evidence; the owning workflow coordinates authorized correction and recheck under its completion and human-decision gates.
