# Testing strategy

Establish a strategy for the selected task, component, or project from accepted contracts and risks. Use declared test tools and layout rather than introducing another framework or reorganizing tests by default. An existing verification map may help locate checks; it is optional.

## Select scenarios and levels

| Concern | Strategy |
| --- | --- |
| Contract and acceptance | Identify observable outcomes and independently establish expected results. Trace scenarios to the owning requirement or task. |
| Local logic | Use focused unit tests where they expose meaningful behavior without reproducing implementation logic. |
| Component collaboration | Use real cooperating components for contracts that cross ownership or dependency boundaries. |
| User entry points | Exercise public APIs, CLI, installation, or end-to-end paths when those are part of the selected change. |
| Failure and boundary behavior | Cover relevant invalid inputs, limits, exceptions, state transitions, cleanup, and recovery paths. |
| Operational risks | Add relevant scenarios for ordering, concurrency, resource ownership, persistence, portability, security, or performance; these are examples, not a mandatory list. |

Describe scenarios, expected outcomes, test level, fixtures or dependencies, and commands needed. Prefer the smallest set that protects the actual contracts, with integration checks where isolated tests cannot expose the risk. Avoid a test-per-function quota or a coverage percentage used as a substitute for behavioral evidence.

For browser-dependent strategy, derive the required matrix and capabilities from accepted contracts, applicable project policies and the declared framework. Do not impose a framework, additional engines or browser installation on strategy-only work. Return conflicting requirements to the coordinator; test design cannot silently replace them.

For existing behavior, inspect relevant tests before adding duplicates. For a bug, reproduce the reported failure with a regression test and state whether reproduction succeeded. For a refactor, establish behavior-preservation coverage before production edits; a new failing behavior test is unnecessary if the accepted behavior is unchanged and existing checks protect it.

## Strategy boundaries

- Derive expectations from accepted requirements, independently checked fixtures, or established external contracts. Do not choose expected behavior solely because the current code produces it.
- Keep tests deterministic where possible; control time, randomness, external state, and fixture cleanup when they affect the contract.
- Surface unavailable dependencies, unclear contracts, or disputed expected behavior before implementation proceeds on that assumption.
- Return strategy and evidence gaps to the caller. Amendments to accepted requirements or layout need their authorized owning workflow; test design does not silently redefine them.

