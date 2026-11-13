# Test-first cycle

Use the cycle for one observable behavior at a time. Read [writing good tests](writing-good-tests.md) before writing or changing a test. Run the project's actual commands; commands in examples are not evidence from the current task.

## RED

1. State the contract and the defect the test should catch. Write a focused test with an independently established expected result.
2. Execute the test before the relevant production change. Inspect the failure and confirm it demonstrates the missing or incorrect behavior.
3. Distinguish a behavioral failure from collection, import, syntax, dependency, or environment failures. Fix test setup or report the blocker before treating the run as RED. An expected exception may be the behavior under test; it is not automatically a setup error.

If the test passes immediately, determine whether it covers existing behavior, misses the intended defect, or exposes a mistaken requirement. Do not alter valid behavior merely to manufacture a failure. Record the actual outcome and resolve the test or contract before proceeding.

## GREEN

Return the failing scenario and observed evidence to the active implementation workflow (**sdd-implement** or **sdd-steer**) for the smallest production change that satisfies the accepted contract. Run the focused test again and the relevant regression checks. If the test still fails, return the failure for repair. Do not weaken a valid assertion to make the implementation pass; correct an erroneous expectation only against independent contract evidence.

Report every observed failure and significant warning. Distinguish new failures, established baseline failures, and environment problems where evidence permits; an unexplained failure remains unresolved. A focused green run does not establish that the whole suite passes.

## REFACTOR and repeat

Improve test clarity and remove test duplication while preserving coverage. Return production-refactoring needs to the active implementation workflow within the accepted task scope. Re-run affected checks after changes; refactoring does not introduce new behavior. Repeat the cycle for remaining scenarios.

Return command and outcome evidence to **sdd-verify** and the active implementation workflow for the required boundary verification, including the declared full suite when project policy or the selected boundary requires it. Do not mark task completion from this development cycle alone.

## Interrupted or non-test-first work

Use existing code and Git evidence without discarding pending work. Characterization tests can establish current behavior; they do not prove a past RED run. When useful and safe, demonstrate regression-test sensitivity against a prior implementation in an isolated worktree or controlled fixture. Label that demonstration accurately and keep the working implementation intact. Report missing evidence, blockers, or an authorized exception rather than claiming strict TDD occurred.

## Record exceptions and gaps

Return the concrete limitation, applicable project policy or existing user authorization, observed alternative checks, and remaining coverage or chronology gap to the active implementation/steering owner and **sdd-report**. Persist those facts with existing task/change evidence; when no location is designated, use the owning entry or its existing linked record, or the ordinary report/commit body for taskless maintenance. Undecided exceptions remain blockers. Missing historical RED, characterization, and isolated sensitivity demonstrations stay accurately labeled; no evidence marker proves unobserved execution order. Do not delete code or fabricate a RED run to reconstruct history.
