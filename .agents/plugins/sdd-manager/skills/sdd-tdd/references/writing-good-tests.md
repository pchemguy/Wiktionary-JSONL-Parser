# Writing good tests

Load this reference whenever writing or changing tests, introducing doubles, or adding test helpers. Each test should protect an observable contract and have a clear explanation of the defect it catches.

## Independent expectations and meaningful failures

- Before writing a test, identify a plausible incorrect branch, argument, result, state transition, or missing effect that it should detect.
- Derive expected values independently: use accepted contracts, literal outcomes, or hand-checked fixtures. Do not call the tested helper to compute both actual and expected values.
- Test outcomes and contract-relevant effects rather than private structure, arbitrary constants, or source-text presence. Exact wording or representation belongs in assertions when the accepted contract requires it.
- Exercise scripts with controlled inputs and inspect outputs, effects, and exit status. Evaluate agent instructions through the consuming agent's behavior; text-presence checks alone cannot demonstrate that a skill works. Structural validators remain useful for format constraints.
- Cover the boundary your code owns. Avoid retesting a dependency's documented internals or trivial forwarding unless your component adds validation, normalization, defaults, lifecycle obligations, or other consequential behavior.

## Real behavior and doubles

Prefer real components and simple controlled fixtures where practical. Use a double when isolation of an external, nondeterministic, costly, or otherwise unsuitable dependency is necessary for the scenario.

| Before introducing a double | Check |
| --- | --- |
| Replacement boundary | Understand the real operation's side effects and preserve those the scenario relies on. Replace the narrow dependency that needs isolation. |
| Returned data | Model realistic contract-compatible structures, including fields relevant to consumers and representative success and failure variants. |
| Assertions | Assert the component's resulting behavior. Argument, order, or call-count checks are appropriate when the interaction itself is part of its contract. |
| Setup complexity | Consider an integration test with real components if the double obscures the behavior or requires extensive imitation of the dependency. |
| Cleanup and helpers | Keep test-only cleanup and helper code in test utilities; do not add production methods solely for tests. Respect actual resource ownership. |

A double's existence or programmed answer is not evidence that the real component works. Ensure that an incorrect production path cannot satisfy the same assertions through a permissive fixture.

## Review sensitivity

Inspect whether plausible faults would fail the tests: for example, a wrong argument, skipped effect, incorrect branch, missing validation, or empty result. If such a fault survives, identify a coverage gap or a test that merely restates the implementation. Use an isolated mutation or controlled faulty fixture when needed to demonstrate sensitivity; do not damage the working code or require mutation tooling by default.

Prefer clear scenario names, narrow assertions, maintainable fixtures, and tests that expose useful failures. Split unrelated behaviors while keeping assertions together when they jointly establish one contract. Re-run changed tests and relevant regressions, and report the evidence and any unresolved gap.

## Examples

These are illustrative Python assertions; replace names and values with the current project's contracts.

```python
# Expected text is independent of the formatter under test.
assert format_record("sample", 3) == "sample:3"

# Reusing the tested formatter on both sides cannot expose its defect.
expected = format_record("sample", 3)
assert format_record("sample", 3) == expected
```

An interaction assertion can be meaningful when the accepted contract specifies it: for example, a component must forward a caller's batch ID unchanged to its sink. Pair that assertion with the relevant real component behavior rather than merely checking that a mock was installed.
